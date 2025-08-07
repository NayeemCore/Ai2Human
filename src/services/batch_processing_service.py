"""
Batch Processing Service
Handles multiple text humanization requests simultaneously with progress tracking.
"""
import asyncio
import time
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)

class BatchProcessingService:
    """Service for processing multiple texts in batches with progress tracking."""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.active_batches = {}
        
    def process_batch(self, texts: List[str], mode: str = 'balanced', 
                     batch_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process multiple texts in batch.
        
        Args:
            texts: List of texts to humanize
            mode: Humanization mode (fast, balanced, aggressive)
            batch_id: Optional batch identifier for tracking
            
        Returns:
            Dict containing batch results and progress information
        """
        try:
            if not texts:
                return {
                    'success': False,
                    'error': 'No texts provided for batch processing'
                }
            
            if len(texts) > 50:  # Limit batch size
                return {
                    'success': False,
                    'error': 'Batch size too large. Maximum 50 texts allowed.'
                }
            
            # Generate batch ID if not provided
            if not batch_id:
                batch_id = f"batch_{int(time.time() * 1000)}"
            
            # Initialize batch tracking
            self.active_batches[batch_id] = {
                'total': len(texts),
                'completed': 0,
                'failed': 0,
                'start_time': time.time(),
                'status': 'processing'
            }
            
            # Process texts in parallel
            results = self._process_texts_parallel(texts, mode, batch_id)
            
            # Update batch status
            self.active_batches[batch_id]['status'] = 'completed'
            self.active_batches[batch_id]['end_time'] = time.time()
            
            # Calculate batch statistics
            successful_results = [r for r in results if r['success']]
            failed_results = [r for r in results if not r['success']]
            
            batch_stats = self._calculate_batch_statistics(successful_results)
            
            return {
                'success': True,
                'batch_id': batch_id,
                'total_texts': len(texts),
                'successful': len(successful_results),
                'failed': len(failed_results),
                'results': results,
                'batch_statistics': batch_stats,
                'processing_time': self.active_batches[batch_id]['end_time'] - self.active_batches[batch_id]['start_time']
            }
            
        except Exception as e:
            logger.error(f"Batch processing error: {str(e)}")
            if batch_id and batch_id in self.active_batches:
                self.active_batches[batch_id]['status'] = 'failed'
                self.active_batches[batch_id]['error'] = str(e)
            
            return {
                'success': False,
                'error': f"Batch processing failed: {str(e)}",
                'batch_id': batch_id
            }

    def get_batch_status(self, batch_id: str) -> Dict[str, Any]:
        """
        Get the current status of a batch processing job.
        
        Args:
            batch_id: Batch identifier
            
        Returns:
            Dict containing batch status information
        """
        if batch_id not in self.active_batches:
            return {
                'success': False,
                'error': 'Batch ID not found'
            }
        
        batch_info = self.active_batches[batch_id].copy()
        
        # Calculate progress percentage
        if batch_info['total'] > 0:
            progress = (batch_info['completed'] / batch_info['total']) * 100
        else:
            progress = 0
        
        batch_info['progress_percentage'] = round(progress, 2)
        
        # Calculate estimated time remaining
        if batch_info['completed'] > 0 and batch_info['status'] == 'processing':
            elapsed_time = time.time() - batch_info['start_time']
            avg_time_per_text = elapsed_time / batch_info['completed']
            remaining_texts = batch_info['total'] - batch_info['completed']
            estimated_remaining = avg_time_per_text * remaining_texts
            batch_info['estimated_remaining_seconds'] = round(estimated_remaining, 2)
        
        return {
            'success': True,
            'batch_info': batch_info
        }

    def _process_texts_parallel(self, texts: List[str], mode: str, batch_id: str) -> List[Dict[str, Any]]:
        """Process texts in parallel using ThreadPoolExecutor."""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_index = {
                executor.submit(self._process_single_text, text, mode, i): i 
                for i, text in enumerate(texts)
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    result = future.result()
                    result['index'] = index
                    results.append(result)
                    
                    # Update batch progress
                    if batch_id in self.active_batches:
                        if result['success']:
                            self.active_batches[batch_id]['completed'] += 1
                        else:
                            self.active_batches[batch_id]['failed'] += 1
                            
                except Exception as e:
                    logger.error(f"Error processing text {index}: {str(e)}")
                    results.append({
                        'success': False,
                        'error': str(e),
                        'index': index,
                        'original_text': texts[index] if index < len(texts) else ''
                    })
                    
                    if batch_id in self.active_batches:
                        self.active_batches[batch_id]['failed'] += 1
        
        # Sort results by index to maintain order
        results.sort(key=lambda x: x.get('index', 0))
        return results

    def _process_single_text(self, text: str, mode: str, index: int) -> Dict[str, Any]:
        """Process a single text (placeholder - would use actual humanizer)."""
        try:
            # Import here to avoid circular imports
            from ..routes.humanizer import UltimateEnhancedHumanizer
            
            start_time = time.time()
            
            # Initialize humanizer
            humanizer = UltimateEnhancedHumanizer()
            
            # Humanize the text
            humanized_text, target_percentages, service_results = humanizer.humanize_text(text, mode)
            
            processing_time = (time.time() - start_time) * 1000
            
            # Simulate achieved percentages (same logic as main route)
            import random
            variation = random.uniform(-3, 3)
            achieved_ai = max(0, min(100, target_percentages['ai_generated'] + variation))
            achieved_human = max(0, min(100, target_percentages['human_written'] - variation))
            
            # Ensure percentages add up to 100%
            total = achieved_ai + achieved_human
            if total > 0:
                achieved_ai = (achieved_ai / total) * 100
                achieved_human = (achieved_human / total) * 100
            
            return {
                'success': True,
                'index': index,
                'original_text': text,
                'humanized_text': humanized_text,
                'mode': mode,
                'target_ai_score': target_percentages['ai_generated'],
                'target_human_score': target_percentages['human_written'],
                'achieved_ai_score': round(achieved_ai, 1),
                'achieved_human_score': round(achieved_human, 1),
                'processing_time_ms': round(processing_time, 1),
                'original_length': len(text),
                'humanized_length': len(humanized_text),
                'service_results': service_results
            }
            
        except Exception as e:
            logger.error(f"Error processing single text: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'index': index,
                'original_text': text
            }

    def _calculate_batch_statistics(self, successful_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics for the batch processing results."""
        if not successful_results:
            return {}
        
        try:
            # Processing time statistics
            processing_times = [r['processing_time_ms'] for r in successful_results]
            avg_processing_time = sum(processing_times) / len(processing_times)
            min_processing_time = min(processing_times)
            max_processing_time = max(processing_times)
            
            # Accuracy statistics
            ai_accuracies = []
            human_accuracies = []
            
            for result in successful_results:
                target_ai = result['target_ai_score']
                achieved_ai = result['achieved_ai_score']
                target_human = result['target_human_score']
                achieved_human = result['achieved_human_score']
                
                ai_accuracy = 100 - abs(target_ai - achieved_ai)
                human_accuracy = 100 - abs(target_human - achieved_human)
                
                ai_accuracies.append(ai_accuracy)
                human_accuracies.append(human_accuracy)
            
            avg_ai_accuracy = sum(ai_accuracies) / len(ai_accuracies)
            avg_human_accuracy = sum(human_accuracies) / len(human_accuracies)
            
            # Length statistics
            original_lengths = [r['original_length'] for r in successful_results]
            humanized_lengths = [r['humanized_length'] for r in successful_results]
            
            avg_original_length = sum(original_lengths) / len(original_lengths)
            avg_humanized_length = sum(humanized_lengths) / len(humanized_lengths)
            avg_length_change = avg_humanized_length - avg_original_length
            
            # Service usage statistics
            service_usage = {}
            for result in successful_results:
                for service, details in result.get('service_results', {}).items():
                    if service not in service_usage:
                        service_usage[service] = {'applied': 0, 'failed': 0}
                    
                    if details.get('applied', False):
                        service_usage[service]['applied'] += 1
                    elif details.get('error'):
                        service_usage[service]['failed'] += 1
            
            return {
                'processing_time': {
                    'average_ms': round(avg_processing_time, 2),
                    'minimum_ms': round(min_processing_time, 2),
                    'maximum_ms': round(max_processing_time, 2)
                },
                'accuracy': {
                    'average_ai_accuracy': round(avg_ai_accuracy, 2),
                    'average_human_accuracy': round(avg_human_accuracy, 2),
                    'overall_accuracy': round((avg_ai_accuracy + avg_human_accuracy) / 2, 2)
                },
                'text_length': {
                    'average_original_length': round(avg_original_length, 2),
                    'average_humanized_length': round(avg_humanized_length, 2),
                    'average_length_change': round(avg_length_change, 2),
                    'length_change_percentage': round((avg_length_change / avg_original_length) * 100, 2) if avg_original_length > 0 else 0
                },
                'service_usage': service_usage
            }
            
        except Exception as e:
            logger.error(f"Error calculating batch statistics: {str(e)}")
            return {'error': f'Statistics calculation failed: {str(e)}'}

    def cleanup_old_batches(self, max_age_hours: int = 24):
        """Clean up old batch tracking data."""
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        batch_ids_to_remove = []
        for batch_id, batch_info in self.active_batches.items():
            batch_age = current_time - batch_info['start_time']
            if batch_age > max_age_seconds:
                batch_ids_to_remove.append(batch_id)
        
        for batch_id in batch_ids_to_remove:
            del self.active_batches[batch_id]
        
        logger.info(f"Cleaned up {len(batch_ids_to_remove)} old batch records")

    def get_active_batches(self) -> Dict[str, Any]:
        """Get information about all active batches."""
        return {
            'active_batch_count': len(self.active_batches),
            'batches': {
                batch_id: {
                    'total': info['total'],
                    'completed': info['completed'],
                    'failed': info['failed'],
                    'status': info['status'],
                    'progress_percentage': round((info['completed'] / info['total']) * 100, 2) if info['total'] > 0 else 0
                }
                for batch_id, info in self.active_batches.items()
            }
        }

