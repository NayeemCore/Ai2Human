"""
Analytics Routes
Provides endpoints for text analysis, comparison, and batch processing.
"""
from flask import Blueprint, request, jsonify
import time
from ..services.text_analytics_service import TextAnalyticsService
from ..services.text_comparison_service import TextComparisonService
from ..services.batch_processing_service import BatchProcessingService

analytics_bp = Blueprint('analytics', __name__)

# Initialize services
text_analytics = TextAnalyticsService()
text_comparison = TextComparisonService()
batch_processor = BatchProcessingService()

@analytics_bp.route('/api/analyze', methods=['POST'])
def analyze_text():
    """
    Analyze text for various metrics including readability, complexity, and AI indicators.
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400
        
        text = data['text']
        
        if not text.strip():
            return jsonify({"error": "Empty text provided"}), 400
        
        # Record processing start time
        start_time = time.time()
        
        # Analyze the text
        analysis_result = text_analytics.analyze_text(text)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        if analysis_result['success']:
            response = {
                "success": True,
                "text_length": len(text),
                "processing_time_ms": round(processing_time, 1),
                "analysis": analysis_result
            }
        else:
            response = {
                "success": False,
                "error": analysis_result.get('error', 'Analysis failed'),
                "processing_time_ms": round(processing_time, 1)
            }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

@analytics_bp.route('/api/compare', methods=['POST'])
def compare_texts():
    """
    Compare original and humanized texts with detailed analysis.
    """
    try:
        data = request.get_json()
        
        if not data or 'original' not in data or 'humanized' not in data:
            return jsonify({"error": "Both original and humanized texts are required"}), 400
        
        original = data['original']
        humanized = data['humanized']
        
        if not original.strip() or not humanized.strip():
            return jsonify({"error": "Both texts must be non-empty"}), 400
        
        # Record processing start time
        start_time = time.time()
        
        # Compare the texts
        comparison_result = text_comparison.compare_texts(original, humanized)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        if comparison_result['success']:
            response = {
                "success": True,
                "original_length": len(original),
                "humanized_length": len(humanized),
                "processing_time_ms": round(processing_time, 1),
                "comparison": comparison_result
            }
        else:
            response = {
                "success": False,
                "error": comparison_result.get('error', 'Comparison failed'),
                "processing_time_ms": round(processing_time, 1)
            }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": f"Comparison failed: {str(e)}"}), 500

@analytics_bp.route('/api/batch', methods=['POST'])
def process_batch():
    """
    Process multiple texts in batch with progress tracking.
    """
    try:
        data = request.get_json()
        
        if not data or 'texts' not in data:
            return jsonify({"error": "No texts provided"}), 400
        
        texts = data['texts']
        mode = data.get('mode', 'balanced').lower()
        batch_id = data.get('batch_id')
        
        if not isinstance(texts, list):
            return jsonify({"error": "Texts must be provided as a list"}), 400
        
        if not texts:
            return jsonify({"error": "Empty text list provided"}), 400
        
        # Validate mode
        if mode not in ['fast', 'balanced', 'aggressive']:
            return jsonify({"error": "Invalid mode. Must be 'fast', 'balanced', or 'aggressive'"}), 400
        
        # Process the batch
        batch_result = batch_processor.process_batch(texts, mode, batch_id)
        
        return jsonify(batch_result)
        
    except Exception as e:
        return jsonify({"error": f"Batch processing failed: {str(e)}"}), 500

@analytics_bp.route('/api/batch/status/<batch_id>', methods=['GET'])
def get_batch_status(batch_id):
    """
    Get the status of a batch processing job.
    """
    try:
        status_result = batch_processor.get_batch_status(batch_id)
        return jsonify(status_result)
        
    except Exception as e:
        return jsonify({"error": f"Status check failed: {str(e)}"}), 500

@analytics_bp.route('/api/batch/active', methods=['GET'])
def get_active_batches():
    """
    Get information about all active batch processing jobs.
    """
    try:
        active_batches = batch_processor.get_active_batches()
        return jsonify({
            "success": True,
            "active_batches": active_batches
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to get active batches: {str(e)}"}), 500

@analytics_bp.route('/api/batch/cleanup', methods=['POST'])
def cleanup_old_batches():
    """
    Clean up old batch processing records.
    """
    try:
        data = request.get_json() or {}
        max_age_hours = data.get('max_age_hours', 24)
        
        # Validate max_age_hours
        if not isinstance(max_age_hours, (int, float)) or max_age_hours <= 0:
            return jsonify({"error": "max_age_hours must be a positive number"}), 400
        
        batch_processor.cleanup_old_batches(max_age_hours)
        
        return jsonify({
            "success": True,
            "message": f"Cleaned up batches older than {max_age_hours} hours"
        })
        
    except Exception as e:
        return jsonify({"error": f"Cleanup failed: {str(e)}"}), 500

@analytics_bp.route('/api/analytics/health', methods=['GET'])
def analytics_health_check():
    """
    Health check for analytics services.
    """
    try:
        # Test each service
        services_status = {}
        
        # Test text analytics
        try:
            test_result = text_analytics.analyze_text("This is a test sentence.")
            services_status['text_analytics'] = 'healthy' if test_result['success'] else 'error'
        except Exception as e:
            services_status['text_analytics'] = f'error: {str(e)}'
        
        # Test text comparison
        try:
            test_result = text_comparison.compare_texts("Original text.", "Modified text.")
            services_status['text_comparison'] = 'healthy' if test_result['success'] else 'error'
        except Exception as e:
            services_status['text_comparison'] = f'error: {str(e)}'
        
        # Test batch processor
        try:
            active_batches = batch_processor.get_active_batches()
            services_status['batch_processing'] = 'healthy'
        except Exception as e:
            services_status['batch_processing'] = f'error: {str(e)}'
        
        overall_status = 'healthy' if all(
            status == 'healthy' for status in services_status.values()
        ) else 'degraded'
        
        return jsonify({
            "status": overall_status,
            "service": "AI Humanizer Analytics",
            "services": services_status,
            "timestamp": time.time()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "service": "AI Humanizer Analytics",
            "error": str(e),
            "timestamp": time.time()
        }), 500

@analytics_bp.route('/api/analytics/stats', methods=['GET'])
def get_analytics_stats():
    """
    Get overall analytics and usage statistics.
    """
    try:
        active_batches = batch_processor.get_active_batches()
        
        stats = {
            "active_batch_count": active_batches['active_batch_count'],
            "total_batches_tracked": len(batch_processor.active_batches),
            "services_available": {
                "text_analytics": True,
                "text_comparison": True,
                "batch_processing": True
            },
            "batch_processor_config": {
                "max_workers": batch_processor.max_workers,
                "max_batch_size": 50
            }
        }
        
        return jsonify({
            "success": True,
            "stats": stats,
            "timestamp": time.time()
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to get stats: {str(e)}"}), 500

