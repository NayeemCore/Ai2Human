"""
HIX Bypass API Service
Provides humanization capabilities using the HIX Bypass API.
"""
import requests
import time
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class HIXBypassService:
    """Service for HIX Bypass API integration."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the HIX Bypass service.
        
        Args:
            api_key: API key for HIX Bypass
        """
        self.base_url = "https://bypass.hix.ai/api"
        self.api_key = api_key
        self.timeout = 30
        self.max_retries = 5
        self.retry_delay = 2  # seconds
        
    def humanize_text(self, text: str, mode: str = "Fast") -> Dict[str, Any]:
        """
        Humanize text using HIX Bypass API.
        
        Args:
            text: Text to humanize
            mode: Humanization mode ("Fast", "Balanced", "Aggressive", "Latest")
            
        Returns:
            Dict containing humanized text and metadata
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "HIX Bypass API key not configured",
                "humanized_text": text,
                "service": "hix_bypass"
            }
        
        # Validate mode
        valid_modes = ["Fast", "Balanced", "Aggressive", "Latest"]
        if mode not in valid_modes:
            mode = "Fast"
        
        try:
            # Step 1: Submit the task
            task_id = self._submit_task(text, mode)
            if not task_id:
                return {
                    "success": False,
                    "error": "Failed to submit task to HIX Bypass",
                    "humanized_text": text,
                    "service": "hix_bypass"
                }
            
            # Step 2: Obtain the result
            result = self._obtain_result(task_id)
            return result
            
        except Exception as e:
            logger.error(f"HIX Bypass unexpected error: {str(e)}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "humanized_text": text,
                "service": "hix_bypass"
            }
    
    def _submit_task(self, text: str, mode: str) -> Optional[str]:
        """
        Submit a humanization task to HIX Bypass.
        
        Args:
            text: Text to humanize
            mode: Humanization mode
            
        Returns:
            Task ID if successful, None otherwise
        """
        try:
            headers = {
                'api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            data = {
                'input': text,
                'mode': mode
            }
            
            response = requests.post(
                f"{self.base_url}/submit",
                json=data,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('err_code') == 0 and 'data' in result:
                    return result['data'].get('task_id')
                else:
                    logger.error(f"HIX Bypass submit error: {result.get('err_msg', 'Unknown error')}")
                    return None
            else:
                logger.error(f"HIX Bypass submit HTTP error: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"HIX Bypass submit request failed: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"HIX Bypass submit unexpected error: {str(e)}")
            return None
    
    def _obtain_result(self, task_id: str) -> Dict[str, Any]:
        """
        Obtain the result of a humanization task from HIX Bypass.
        
        Args:
            task_id: Task ID from submit request
            
        Returns:
            Dict containing humanized text and metadata
        """
        headers = {
            'api-key': self.api_key
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    f"{self.base_url}/obtain",
                    params={'task_id': task_id},
                    headers=headers,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('err_code') == 0 and 'data' in result:
                        data = result['data']
                        
                        # Check if task is completed
                        if data.get('task_status') and data.get('subtask_status') == 'completed':
                            return {
                                "success": True,
                                "humanized_text": data.get('output', data.get('input')),
                                "original_length": data.get('input_words', 0),
                                "humanized_length": data.get('words_used', 0),
                                "detection_result": data.get('detection_result', 'unknown'),
                                "detection_score": data.get('detection_score', 0),
                                "mode": data.get('mode', 'Fast'),
                                "service": "hix_bypass"
                            }
                        elif data.get('subtask_status') in ['processing', 'pending']:
                            # Task still processing, wait and retry
                            logger.info(f"HIX Bypass task {task_id} still processing, attempt {attempt + 1}")
                            time.sleep(self.retry_delay)
                            continue
                        else:
                            # Task failed or unknown status
                            logger.error(f"HIX Bypass task {task_id} failed or unknown status")
                            return {
                                "success": False,
                                "error": f"Task failed with status: {data.get('subtask_status', 'unknown')}",
                                "humanized_text": data.get('input', ''),
                                "service": "hix_bypass"
                            }
                    else:
                        logger.error(f"HIX Bypass obtain error: {result.get('err_msg', 'Unknown error')}")
                        return {
                            "success": False,
                            "error": result.get('err_msg', 'Unknown error'),
                            "humanized_text": '',
                            "service": "hix_bypass"
                        }
                else:
                    logger.error(f"HIX Bypass obtain HTTP error: {response.status_code}")
                    return {
                        "success": False,
                        "error": f"HTTP {response.status_code}: {response.text}",
                        "humanized_text": '',
                        "service": "hix_bypass"
                    }
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"HIX Bypass obtain request failed: {str(e)}")
                if attempt == self.max_retries - 1:
                    return {
                        "success": False,
                        "error": f"Request failed after {self.max_retries} attempts: {str(e)}",
                        "humanized_text": '',
                        "service": "hix_bypass"
                    }
                time.sleep(self.retry_delay)
            except Exception as e:
                logger.error(f"HIX Bypass obtain unexpected error: {str(e)}")
                return {
                    "success": False,
                    "error": f"Unexpected error: {str(e)}",
                    "humanized_text": '',
                    "service": "hix_bypass"
                }
        
        # If we get here, all retries failed
        return {
            "success": False,
            "error": f"Task did not complete after {self.max_retries} attempts",
            "humanized_text": '',
            "service": "hix_bypass"
        }

