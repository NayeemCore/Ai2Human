import requests
import json
import time
from typing import Dict, List, Optional

class ProWritingAidService:
    """Service for integrating with ProWritingAid API for advanced grammar and style checking"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.prowritingaid.com"
        self.session = requests.Session()
        
        # Set up authentication headers if API key is provided
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
    
    def check_text_async(self, text: str, reports: List[str] = None) -> Dict:
        """
        Submit text for asynchronous analysis with ProWritingAid
        
        Args:
            text: Text to analyze
            reports: List of report types to generate (e.g., ['grammar', 'style', 'readability'])
            
        Returns:
            Dictionary containing task ID for retrieving results
        """
        if not self.api_key:
            return {
                'error': 'ProWritingAid API key not configured',
                'task_id': None
            }
        
        # Default reports if none specified
        if reports is None:
            reports = ['grammar', 'style', 'overused', 'readability', 'sticky']
        
        try:
            # Prepare request data
            data = {
                'text': text,
                'reports': reports,
                'language': 'en',
                'style': 'General',
                'suggestions': True
            }
            
            # Submit text for analysis
            response = self.session.post(
                f'{self.base_url}/api/async/text',
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'task_id': result.get('taskId'),
                    'status': 'submitted',
                    'error': None
                }
            else:
                return {
                    'error': f'ProWritingAid API error: {response.status_code} - {response.text}',
                    'task_id': None
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'error': f'ProWritingAid request failed: {str(e)}',
                'task_id': None
            }
        except Exception as e:
            return {
                'error': f'ProWritingAid processing error: {str(e)}',
                'task_id': None
            }
    
    def get_analysis_result(self, task_id: str, max_retries: int = 10) -> Dict:
        """
        Retrieve analysis results using task ID
        
        Args:
            task_id: Task ID from async submission
            max_retries: Maximum number of retry attempts
            
        Returns:
            Dictionary containing analysis results
        """
        if not self.api_key or not task_id:
            return {
                'error': 'ProWritingAid API key not configured or invalid task ID',
                'result': None
            }
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(
                    f'{self.base_url}/api/async/text/result/{task_id}',
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Check if processing is complete
                    if result.get('status') == 'Done':
                        return {
                            'result': result.get('result'),
                            'status': 'complete',
                            'error': None
                        }
                    elif result.get('status') in ['Error', 'Failed']:
                        return {
                            'error': f'ProWritingAid analysis failed: {result.get("message", "Unknown error")}',
                            'result': None
                        }
                    else:
                        # Still processing, wait and retry
                        time.sleep(2)
                        continue
                        
                elif response.status_code == 404:
                    return {
                        'error': 'Task not found or expired',
                        'result': None
                    }
                else:
                    return {
                        'error': f'ProWritingAid API error: {response.status_code}',
                        'result': None
                    }
                    
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    return {
                        'error': f'ProWritingAid request failed: {str(e)}',
                        'result': None
                    }
                time.sleep(2)
                continue
        
        return {
            'error': 'ProWritingAid analysis timed out',
            'result': None
        }
    
    def analyze_text_sync(self, text: str, reports: List[str] = None) -> Dict:
        """
        Synchronous text analysis (submit and wait for results)
        
        Args:
            text: Text to analyze
            reports: List of report types to generate
            
        Returns:
            Dictionary containing analysis results
        """
        # Submit for analysis
        submission = self.check_text_async(text, reports)
        
        if submission.get('error'):
            return submission
        
        task_id = submission.get('task_id')
        if not task_id:
            return {
                'error': 'Failed to get task ID from ProWritingAid',
                'result': None
            }
        
        # Wait for and retrieve results
        return self.get_analysis_result(task_id)
    
    def apply_suggestions(self, text: str, suggestions: List[Dict], 
                         apply_grammar: bool = True, apply_style: bool = False) -> str:
        """
        Apply ProWritingAid suggestions to text
        
        Args:
            text: Original text
            suggestions: List of suggestions from ProWritingAid
            apply_grammar: Whether to apply grammar suggestions
            apply_style: Whether to apply style suggestions
            
        Returns:
            Text with applied suggestions
        """
        if not suggestions:
            return text
        
        # Sort suggestions by start position in reverse order
        sorted_suggestions = sorted(
            suggestions, 
            key=lambda x: x.get('startPos', 0), 
            reverse=True
        )
        
        corrected_text = text
        
        for suggestion in sorted_suggestions:
            try:
                start_pos = suggestion.get('startPos', 0)
                end_pos = suggestion.get('endPos', start_pos)
                replacements = suggestion.get('suggestions', [])
                category = suggestion.get('category', '').lower()
                
                # Skip if no replacements
                if not replacements:
                    continue
                
                # Apply based on category and settings
                should_apply = False
                if apply_grammar and category in ['grammar', 'spelling', 'punctuation']:
                    should_apply = True
                elif apply_style and category in ['style', 'readability', 'overused']:
                    should_apply = True
                
                if should_apply and replacements:
                    # Use the first (best) suggestion
                    replacement = replacements[0]
                    corrected_text = (
                        corrected_text[:start_pos] + 
                        replacement + 
                        corrected_text[end_pos:]
                    )
                    
            except (KeyError, IndexError, TypeError):
                # Skip malformed suggestions
                continue
        
        return corrected_text
    
    def get_writing_score(self, analysis_result: Dict) -> Dict:
        """
        Extract writing score and metrics from ProWritingAid analysis
        
        Args:
            analysis_result: Result from ProWritingAid analysis
            
        Returns:
            Dictionary with writing scores and metrics
        """
        if not analysis_result or 'result' not in analysis_result:
            return {
                'overall_score': 0,
                'grammar_score': 0,
                'style_score': 0,
                'readability_score': 0
            }
        
        result = analysis_result['result']
        
        # Extract scores from different reports
        scores = {
            'overall_score': 0,
            'grammar_score': 0,
            'style_score': 0,
            'readability_score': 0,
            'issues_found': 0
        }
        
        # Count issues by category
        tags = result.get('Tags', [])
        grammar_issues = 0
        style_issues = 0
        
        for tag in tags:
            category = tag.get('category', '').lower()
            if category in ['grammar', 'spelling', 'punctuation']:
                grammar_issues += 1
            elif category in ['style', 'readability', 'overused']:
                style_issues += 1
        
        scores['issues_found'] = len(tags)
        
        # Calculate simple scores (higher is better, 0-100 scale)
        text_length = len(result.get('text', ''))
        if text_length > 0:
            # Grammar score: fewer grammar issues = higher score
            scores['grammar_score'] = max(0, 100 - (grammar_issues * 10))
            
            # Style score: fewer style issues = higher score
            scores['style_score'] = max(0, 100 - (style_issues * 5))
            
            # Overall score: average of grammar and style
            scores['overall_score'] = (scores['grammar_score'] + scores['style_score']) / 2
        
        return scores
    
    def enhance_text_quality(self, text: str, apply_corrections: bool = True) -> Dict:
        """
        Comprehensive text quality enhancement using ProWritingAid
        
        Args:
            text: Text to enhance
            apply_corrections: Whether to apply corrections automatically
            
        Returns:
            Dictionary with enhanced text and analysis
        """
        if not self.api_key:
            return {
                'enhanced_text': text,
                'original_text': text,
                'error': 'ProWritingAid API key not configured',
                'scores': {'overall_score': 0}
            }
        
        # Analyze text
        analysis = self.analyze_text_sync(text)
        
        if analysis.get('error'):
            return {
                'enhanced_text': text,
                'original_text': text,
                'error': analysis['error'],
                'scores': {'overall_score': 0}
            }
        
        result = analysis.get('result', {})
        suggestions = result.get('Tags', [])
        
        # Apply corrections if requested
        enhanced_text = text
        if apply_corrections and suggestions:
            enhanced_text = self.apply_suggestions(
                text, suggestions, 
                apply_grammar=True, 
                apply_style=False  # Conservative approach
            )
        
        # Get writing scores
        scores = self.get_writing_score(analysis)
        
        return {
            'enhanced_text': enhanced_text,
            'original_text': text,
            'suggestions': suggestions,
            'scores': scores,
            'analysis': result
        }

