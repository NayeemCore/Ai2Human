import requests
import json
from typing import Dict, List, Optional

class LanguageToolService:
    """Service for integrating with LanguageTool API for grammar and style checking"""
    
    def __init__(self, api_url: str = "https://api.languagetool.org/v2/check"):
        self.api_url = api_url
        self.session = requests.Session()
        
    def check_text(self, text: str, language: str = "en-US", level: str = "default") -> Dict:
        """
        Check text for grammar and style issues using LanguageTool API
        
        Args:
            text: Text to check
            language: Language code (e.g., 'en-US', 'en-GB')
            level: Checking level ('default' or 'picky')
            
        Returns:
            Dictionary containing matches (issues found) and other metadata
        """
        try:
            # Prepare request data
            data = {
                'text': text,
                'language': language,
                'level': level,
                'enabledOnly': 'false'
            }
            
            # Make request to LanguageTool API
            response = self.session.post(
                self.api_url,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    'error': f'LanguageTool API error: {response.status_code}',
                    'matches': []
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'error': f'LanguageTool request failed: {str(e)}',
                'matches': []
            }
        except Exception as e:
            return {
                'error': f'LanguageTool processing error: {str(e)}',
                'matches': []
            }
    
    def apply_corrections(self, text: str, matches: List[Dict], apply_all: bool = False) -> str:
        """
        Apply corrections from LanguageTool matches to the text
        
        Args:
            text: Original text
            matches: List of matches from LanguageTool
            apply_all: If True, apply all suggestions. If False, apply only high-confidence ones
            
        Returns:
            Corrected text
        """
        if not matches:
            return text
            
        # Sort matches by offset in reverse order to avoid position shifts
        sorted_matches = sorted(matches, key=lambda x: x.get('offset', 0), reverse=True)
        
        corrected_text = text
        
        for match in sorted_matches:
            try:
                offset = match.get('offset', 0)
                length = match.get('length', 0)
                replacements = match.get('replacements', [])
                
                # Skip if no replacements available
                if not replacements:
                    continue
                
                # For selective application, only apply high-confidence corrections
                if not apply_all:
                    # Skip corrections for certain rule categories that might change meaning
                    rule_id = match.get('rule', {}).get('id', '')
                    category_id = match.get('rule', {}).get('category', {}).get('id', '')
                    
                    # Skip style suggestions that might change the author's voice
                    skip_categories = ['STYLE', 'REDUNDANCY', 'COLLOQUIALISMS']
                    if category_id in skip_categories:
                        continue
                    
                    # Only apply corrections with high confidence
                    if len(replacements) > 3:  # Too many options, might be uncertain
                        continue
                
                # Apply the first (most likely) replacement
                replacement = replacements[0].get('value', '')
                if replacement:
                    corrected_text = (
                        corrected_text[:offset] + 
                        replacement + 
                        corrected_text[offset + length:]
                    )
                    
            except (KeyError, IndexError, TypeError):
                # Skip malformed matches
                continue
        
        return corrected_text
    
    def get_writing_statistics(self, matches: List[Dict]) -> Dict:
        """
        Extract writing statistics from LanguageTool matches
        
        Args:
            matches: List of matches from LanguageTool
            
        Returns:
            Dictionary with writing statistics
        """
        stats = {
            'total_issues': len(matches),
            'grammar_issues': 0,
            'spelling_issues': 0,
            'style_issues': 0,
            'punctuation_issues': 0,
            'other_issues': 0
        }
        
        for match in matches:
            try:
                category_id = match.get('rule', {}).get('category', {}).get('id', '').upper()
                
                if 'GRAMMAR' in category_id:
                    stats['grammar_issues'] += 1
                elif 'TYPOS' in category_id or 'SPELLING' in category_id:
                    stats['spelling_issues'] += 1
                elif 'STYLE' in category_id:
                    stats['style_issues'] += 1
                elif 'PUNCTUATION' in category_id:
                    stats['punctuation_issues'] += 1
                else:
                    stats['other_issues'] += 1
                    
            except (KeyError, TypeError):
                stats['other_issues'] += 1
        
        return stats
    
    def enhance_text_quality(self, text: str, language: str = "en-US", 
                           apply_corrections: bool = True) -> Dict:
        """
        Comprehensive text quality enhancement using LanguageTool
        
        Args:
            text: Text to enhance
            language: Language code
            apply_corrections: Whether to apply corrections automatically
            
        Returns:
            Dictionary with enhanced text and analysis
        """
        # Check text with LanguageTool
        check_result = self.check_text(text, language, level="picky")
        
        if 'error' in check_result:
            return {
                'enhanced_text': text,
                'original_text': text,
                'error': check_result['error'],
                'statistics': {'total_issues': 0}
            }
        
        matches = check_result.get('matches', [])
        
        # Apply corrections if requested
        enhanced_text = text
        if apply_corrections and matches:
            enhanced_text = self.apply_corrections(text, matches, apply_all=False)
        
        # Get statistics
        statistics = self.get_writing_statistics(matches)
        
        return {
            'enhanced_text': enhanced_text,
            'original_text': text,
            'matches': matches,
            'statistics': statistics,
            'language': check_result.get('language', {}),
            'software': check_result.get('software', {})
        }

