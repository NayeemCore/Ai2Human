"""
Text Comparison Service
Provides detailed comparison between original and humanized texts.
"""
import re
import difflib
from typing import Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)

class TextComparisonService:
    """Service for comparing original and humanized texts with detailed analysis."""
    
    def __init__(self):
        pass

    def compare_texts(self, original: str, humanized: str) -> Dict[str, Any]:
        """
        Compare original and humanized texts with detailed analysis.
        
        Args:
            original: Original text
            humanized: Humanized text
            
        Returns:
            Dict containing detailed comparison results
        """
        try:
            # Basic statistics comparison
            basic_comparison = self._compare_basic_stats(original, humanized)
            
            # Word-level changes
            word_changes = self._analyze_word_changes(original, humanized)
            
            # Sentence-level changes
            sentence_changes = self._analyze_sentence_changes(original, humanized)
            
            # Structural changes
            structural_changes = self._analyze_structural_changes(original, humanized)
            
            # Readability comparison
            readability_comparison = self._compare_readability(original, humanized)
            
            # Similarity metrics
            similarity_metrics = self._calculate_similarity_metrics(original, humanized)
            
            # Change summary
            change_summary = self._generate_change_summary(
                word_changes, sentence_changes, structural_changes
            )
            
            return {
                'success': True,
                'basic_comparison': basic_comparison,
                'word_changes': word_changes,
                'sentence_changes': sentence_changes,
                'structural_changes': structural_changes,
                'readability_comparison': readability_comparison,
                'similarity_metrics': similarity_metrics,
                'change_summary': change_summary
            }
            
        except Exception as e:
            logger.error(f"Text comparison error: {str(e)}")
            return {
                'success': False,
                'error': f"Text comparison failed: {str(e)}"
            }

    def _compare_basic_stats(self, original: str, humanized: str) -> Dict[str, Any]:
        """Compare basic statistics between texts."""
        original_stats = self._get_text_stats(original)
        humanized_stats = self._get_text_stats(humanized)
        
        return {
            'original': original_stats,
            'humanized': humanized_stats,
            'changes': {
                'character_change': humanized_stats['characters'] - original_stats['characters'],
                'word_change': humanized_stats['words'] - original_stats['words'],
                'sentence_change': humanized_stats['sentences'] - original_stats['sentences'],
                'character_change_percent': round(
                    ((humanized_stats['characters'] - original_stats['characters']) / original_stats['characters']) * 100, 2
                ) if original_stats['characters'] > 0 else 0,
                'word_change_percent': round(
                    ((humanized_stats['words'] - original_stats['words']) / original_stats['words']) * 100, 2
                ) if original_stats['words'] > 0 else 0
            }
        }

    def _analyze_word_changes(self, original: str, humanized: str) -> Dict[str, Any]:
        """Analyze word-level changes between texts."""
        original_words = re.findall(r'\b\w+\b', original.lower())
        humanized_words = re.findall(r'\b\w+\b', humanized.lower())
        
        # Find added, removed, and changed words
        original_set = set(original_words)
        humanized_set = set(humanized_words)
        
        added_words = list(humanized_set - original_set)
        removed_words = list(original_set - humanized_set)
        common_words = list(original_set & humanized_set)
        
        # Word frequency changes
        original_freq = {}
        humanized_freq = {}
        
        for word in original_words:
            original_freq[word] = original_freq.get(word, 0) + 1
        
        for word in humanized_words:
            humanized_freq[word] = humanized_freq.get(word, 0) + 1
        
        frequency_changes = {}
        for word in common_words:
            orig_count = original_freq.get(word, 0)
            human_count = humanized_freq.get(word, 0)
            if orig_count != human_count:
                frequency_changes[word] = {
                    'original_count': orig_count,
                    'humanized_count': human_count,
                    'change': human_count - orig_count
                }
        
        # Vocabulary complexity changes
        original_complex = [w for w in original_words if len(w) > 6]
        humanized_complex = [w for w in humanized_words if len(w) > 6]
        
        complexity_change = len(humanized_complex) - len(original_complex)
        
        return {
            'added_words': added_words[:20],  # Limit to first 20
            'removed_words': removed_words[:20],
            'added_count': len(added_words),
            'removed_count': len(removed_words),
            'common_words_count': len(common_words),
            'frequency_changes': dict(list(frequency_changes.items())[:10]),  # Top 10 changes
            'vocabulary_complexity': {
                'original_complex_words': len(original_complex),
                'humanized_complex_words': len(humanized_complex),
                'complexity_change': complexity_change
            }
        }

    def _analyze_sentence_changes(self, original: str, humanized: str) -> Dict[str, Any]:
        """Analyze sentence-level changes between texts."""
        original_sentences = re.split(r'[.!?]+', original)
        humanized_sentences = re.split(r'[.!?]+', humanized)
        
        original_sentences = [s.strip() for s in original_sentences if s.strip()]
        humanized_sentences = [s.strip() for s in humanized_sentences if s.strip()]
        
        # Sentence length analysis
        original_lengths = [len(s.split()) for s in original_sentences]
        humanized_lengths = [len(s.split()) for s in humanized_sentences]
        
        avg_original_length = sum(original_lengths) / len(original_lengths) if original_lengths else 0
        avg_humanized_length = sum(humanized_lengths) / len(humanized_lengths) if humanized_lengths else 0
        
        # Sentence structure changes
        original_structures = self._analyze_sentence_structures(original_sentences)
        humanized_structures = self._analyze_sentence_structures(humanized_sentences)
        
        # Find similar sentences using difflib
        sentence_matches = []
        for i, orig_sent in enumerate(original_sentences[:10]):  # Limit to first 10
            best_match = difflib.get_close_matches(orig_sent, humanized_sentences, n=1, cutoff=0.6)
            if best_match:
                similarity = difflib.SequenceMatcher(None, orig_sent, best_match[0]).ratio()
                sentence_matches.append({
                    'original_index': i,
                    'original_sentence': orig_sent,
                    'matched_sentence': best_match[0],
                    'similarity': round(similarity, 3)
                })
        
        return {
            'sentence_count_change': len(humanized_sentences) - len(original_sentences),
            'average_length_change': round(avg_humanized_length - avg_original_length, 2),
            'original_structures': original_structures,
            'humanized_structures': humanized_structures,
            'sentence_matches': sentence_matches,
            'length_distribution': {
                'original': {
                    'min': min(original_lengths) if original_lengths else 0,
                    'max': max(original_lengths) if original_lengths else 0,
                    'avg': round(avg_original_length, 2)
                },
                'humanized': {
                    'min': min(humanized_lengths) if humanized_lengths else 0,
                    'max': max(humanized_lengths) if humanized_lengths else 0,
                    'avg': round(avg_humanized_length, 2)
                }
            }
        }

    def _analyze_structural_changes(self, original: str, humanized: str) -> Dict[str, Any]:
        """Analyze structural changes between texts."""
        # Punctuation analysis
        original_punct = re.findall(r'[.!?;:,\-—()[\]{}"]', original)
        humanized_punct = re.findall(r'[.!?;:,\-—()[\]{}"]', humanized)
        
        punct_changes = {}
        all_punct = set(original_punct + humanized_punct)
        
        for punct in all_punct:
            orig_count = original_punct.count(punct)
            human_count = humanized_punct.count(punct)
            if orig_count != human_count:
                punct_changes[punct] = {
                    'original': orig_count,
                    'humanized': human_count,
                    'change': human_count - orig_count
                }
        
        # Transition word analysis
        transition_words = [
            'however', 'furthermore', 'moreover', 'additionally', 'consequently',
            'therefore', 'subsequently', 'nevertheless', 'nonetheless', 'accordingly',
            'meanwhile', 'finally', 'ultimately', 'specifically', 'particularly'
        ]
        
        original_transitions = []
        humanized_transitions = []
        
        for word in transition_words:
            orig_count = len(re.findall(rf'\b{word}\b', original, re.IGNORECASE))
            human_count = len(re.findall(rf'\b{word}\b', humanized, re.IGNORECASE))
            
            if orig_count > 0 or human_count > 0:
                original_transitions.append((word, orig_count))
                humanized_transitions.append((word, human_count))
        
        # Paragraph structure
        original_paragraphs = len(original.split('\n\n'))
        humanized_paragraphs = len(humanized.split('\n\n'))
        
        return {
            'punctuation_changes': punct_changes,
            'transition_words': {
                'original': dict(original_transitions),
                'humanized': dict(humanized_transitions),
                'total_change': sum(h for _, h in humanized_transitions) - sum(o for _, o in original_transitions)
            },
            'paragraph_structure': {
                'original_paragraphs': original_paragraphs,
                'humanized_paragraphs': humanized_paragraphs,
                'paragraph_change': humanized_paragraphs - original_paragraphs
            }
        }

    def _compare_readability(self, original: str, humanized: str) -> Dict[str, Any]:
        """Compare readability metrics between texts."""
        try:
            # Import text analytics service for readability calculation
            from .text_analytics_service import TextAnalyticsService
            
            analytics = TextAnalyticsService()
            
            original_analysis = analytics.analyze_text(original)
            humanized_analysis = analytics.analyze_text(humanized)
            
            if original_analysis['success'] and humanized_analysis['success']:
                original_readability = original_analysis['readability']
                humanized_readability = humanized_analysis['readability']
                
                return {
                    'original': original_readability,
                    'humanized': humanized_readability,
                    'improvements': {
                        'flesch_ease_change': round(
                            humanized_readability['flesch_reading_ease'] - original_readability['flesch_reading_ease'], 2
                        ),
                        'grade_level_change': round(
                            humanized_readability['average_grade_level'] - original_readability['average_grade_level'], 2
                        ),
                        'readability_improved': (
                            humanized_readability['flesch_reading_ease'] > original_readability['flesch_reading_ease']
                        )
                    }
                }
            else:
                return {'error': 'Could not calculate readability metrics'}
                
        except Exception as e:
            logger.error(f"Readability comparison error: {str(e)}")
            return {'error': f'Readability comparison failed: {str(e)}'}

    def _calculate_similarity_metrics(self, original: str, humanized: str) -> Dict[str, Any]:
        """Calculate various similarity metrics between texts."""
        # Character-level similarity
        char_similarity = difflib.SequenceMatcher(None, original, humanized).ratio()
        
        # Word-level similarity
        original_words = re.findall(r'\b\w+\b', original.lower())
        humanized_words = re.findall(r'\b\w+\b', humanized.lower())
        
        word_similarity = difflib.SequenceMatcher(None, original_words, humanized_words).ratio()
        
        # Sentence-level similarity
        original_sentences = re.split(r'[.!?]+', original)
        humanized_sentences = re.split(r'[.!?]+', humanized)
        
        original_sentences = [s.strip() for s in original_sentences if s.strip()]
        humanized_sentences = [s.strip() for s in humanized_sentences if s.strip()]
        
        sentence_similarity = difflib.SequenceMatcher(None, original_sentences, humanized_sentences).ratio()
        
        # Jaccard similarity (word sets)
        original_set = set(original_words)
        humanized_set = set(humanized_words)
        
        intersection = len(original_set & humanized_set)
        union = len(original_set | humanized_set)
        jaccard_similarity = intersection / union if union > 0 else 0
        
        return {
            'character_similarity': round(char_similarity, 3),
            'word_similarity': round(word_similarity, 3),
            'sentence_similarity': round(sentence_similarity, 3),
            'jaccard_similarity': round(jaccard_similarity, 3),
            'overall_similarity': round((char_similarity + word_similarity + sentence_similarity + jaccard_similarity) / 4, 3)
        }

    def _generate_change_summary(self, word_changes: Dict, sentence_changes: Dict, 
                                structural_changes: Dict) -> Dict[str, Any]:
        """Generate a summary of all changes made."""
        total_word_changes = word_changes['added_count'] + word_changes['removed_count']
        sentence_count_change = abs(sentence_changes['sentence_count_change'])
        punct_changes = len(structural_changes['punctuation_changes'])
        
        # Categorize the level of changes
        if total_word_changes < 5 and sentence_count_change < 2 and punct_changes < 3:
            change_level = 'minimal'
        elif total_word_changes < 15 and sentence_count_change < 5 and punct_changes < 8:
            change_level = 'moderate'
        elif total_word_changes < 30 and sentence_count_change < 10 and punct_changes < 15:
            change_level = 'substantial'
        else:
            change_level = 'extensive'
        
        # Identify main types of changes
        change_types = []
        
        if word_changes['added_count'] > 5:
            change_types.append('vocabulary_expansion')
        if word_changes['removed_count'] > 5:
            change_types.append('vocabulary_simplification')
        if sentence_changes['sentence_count_change'] > 2:
            change_types.append('sentence_restructuring')
        if abs(sentence_changes['average_length_change']) > 2:
            change_types.append('sentence_length_modification')
        if structural_changes['transition_words']['total_change'] > 3:
            change_types.append('transition_enhancement')
        if punct_changes > 5:
            change_types.append('punctuation_modification')
        
        return {
            'change_level': change_level,
            'change_types': change_types,
            'total_word_changes': total_word_changes,
            'sentence_modifications': sentence_count_change,
            'structural_modifications': punct_changes,
            'preservation_score': round(100 - (total_word_changes + sentence_count_change + punct_changes), 2)
        }

    def _get_text_stats(self, text: str) -> Dict[str, int]:
        """Get basic statistics for a text."""
        return {
            'characters': len(text),
            'characters_no_spaces': len(text.replace(' ', '')),
            'words': len(re.findall(r'\b\w+\b', text)),
            'sentences': len(re.split(r'[.!?]+', text)) - 1,  # -1 because split creates empty string at end
            'paragraphs': len(text.split('\n\n'))
        }

    def _analyze_sentence_structures(self, sentences: List[str]) -> Dict[str, int]:
        """Analyze sentence structures in a list of sentences."""
        structures = {
            'simple': 0,
            'compound': 0,
            'complex': 0,
            'compound_complex': 0
        }
        
        for sentence in sentences:
            # Simple heuristics for sentence structure classification
            coord_conjunctions = len(re.findall(r'\b(and|but|or|so|yet)\b', sentence, re.IGNORECASE))
            subord_conjunctions = len(re.findall(r'\b(because|since|although|while|if|when|that|which)\b', sentence, re.IGNORECASE))
            
            if coord_conjunctions > 0 and subord_conjunctions > 0:
                structures['compound_complex'] += 1
            elif coord_conjunctions > 0:
                structures['compound'] += 1
            elif subord_conjunctions > 0:
                structures['complex'] += 1
            else:
                structures['simple'] += 1
        
        return structures

