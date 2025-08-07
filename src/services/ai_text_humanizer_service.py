"""
AI-Text-Humanizer.com API Service
Provides humanization capabilities using the AI-Text-Humanizer.com API.
"""
import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class AITextHumanizerService:
    """Service for AI-Text-Humanizer.com API integration."""
    
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the AI-Text-Humanizer service.
        
        Args:
            email: Account email for AI-Text-Humanizer.com
            password: Account password for AI-Text-Humanizer.com
        """
        self.base_url = "https://ai-text-humanizer.com/api.php"
        self.email = email
        self.password = password
        self.timeout = 30
        
    def humanize_text(self, text: str) -> Dict[str, Any]:
        """
        Humanize text using AI-Text-Humanizer.com API.
        
        Args:
            text: Text to humanize
            
        Returns:
            Dict containing humanized text and metadata
        """
        if not self.email or not self.password:
            return {
                "success": False,
                "error": "AI-Text-Humanizer credentials not configured",
                "humanized_text": text,
                "service": "ai_text_humanizer"
            }
        
        try:
            data = {
                'email': self.email,
                'pw': self.password,
                'text': text
            }
            
            response = requests.post(
                self.base_url,
                data=data,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                humanized_text = response.text.strip()
                
                # Basic validation - check if response is not an error message
                if humanized_text and not humanized_text.lower().startswith('error'):
                    return {
                        "success": True,
                        "humanized_text": humanized_text,
                        "original_length": len(text),
                        "humanized_length": len(humanized_text),
                        "service": "ai_text_humanizer"
                    }
                else:
                    logger.warning(f"AI-Text-Humanizer returned error: {humanized_text}")
                    return {
                        "success": False,
                        "error": f"API returned error: {humanized_text}",
                        "humanized_text": text,
                        "service": "ai_text_humanizer"
                    }
            else:
                logger.error(f"AI-Text-Humanizer API error: {response.status_code}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "humanized_text": text,
                    "service": "ai_text_humanizer"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"AI-Text-Humanizer request failed: {str(e)}")
            return {
                "success": False,
                "error": f"Request failed: {str(e)}",
                "humanized_text": text,
                "service": "ai_text_humanizer"
            }
        except Exception as e:
            logger.error(f"AI-Text-Humanizer unexpected error: {str(e)}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "humanized_text": text,
                "service": "ai_text_humanizer"
            }

