"""
Text Analytics Service
Provides comprehensive text analysis including readability, sentiment, and complexity metrics.
"""
import re
import math
import statistics
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class TextAnalyticsService:
    """Service for comprehensive text analysis and metrics calculation."""
    
    def __init__(self):
        # Common English words for complexity analysis
        self.common_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
            'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go'
        }
        
        # Sentiment word lists (simplified)
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'outstanding', 'superb', 'brilliant', 'perfect', 'awesome', 'incredible',
            'remarkable', 'exceptional', 'magnificent', 'marvelous', 'splendid',
            'terrific', 'fabulous', 'phenomenal', 'impressive', 'effective',
            'successful', 'beneficial', 'valuable', 'useful', 'helpful', 'positive'
        }
        
        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'dreadful', 'poor', 'worst',
            'disappointing', 'inadequate', 'insufficient', 'problematic', 'difficult',
            'challenging', 'complex', 'complicated', 'confusing', 'unclear',
            'negative', 'harmful', 'dangerous', 'risky', 'ineffective', 'useless'
        }
        
        # Academic/formal words that might indicate AI writing
        self.formal_indicators = {
            'utilize', 'implement', 'facilitate', 'demonstrate', 'comprehensive',
            'significant', 'substantial', 'considerable', 'numerous', 'various',
            'furthermore', 'moreover', 'additionally', 'consequently', 'therefore',
            'subsequently', 'nevertheless', 'however', 'nonetheless', 'accordingly'
        }

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive text analysis.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dict containing various text metrics and analysis results
        """
        try:
            # Basic text statistics
            basic_stats = self._calculate_basic_stats(text)
            
            # Readability metrics
            readability = self._calculate_readability(text)
            
            # Complexity analysis
            complexity = self._analyze_complexity(text)
            
            # Sentiment analysis
            sentiment = self._analyze_sentiment(text)
            
            # AI detection indicators
            ai_indicators = self._analyze_ai_indicators(text)
            
            # Burstiness analysis
            burstiness = self._analyze_burstiness(text)
            
            # Perplexity estimation
            perplexity = self._estimate_perplexity(text)
            
            return {
                'success': True,
                'basic_stats': basic_stats,
                'readability': readability,
                'complexity': complexity,
                'sentiment': sentiment,
                'ai_indicators': ai_indicators,
                'burstiness': burstiness,
                'perplexity': perplexity,
                'overall_score': self._calculate_overall_score(
                    readability, complexity, ai_indicators, burstiness
                )
            }
            
        except Exception as e:
            logger.error(f"Text analysis error: {str(e)}")
            return {
                'success': False,
                'error': f"Text analysis failed: {str(e)}"
            }

    def _calculate_basic_stats(self, text: str) -> Dict[str, Any]:
        """Calculate basic text statistics."""
        sentences = self._split_sentences(text)
        words = self._split_words(text)
        
        # Character counts
        char_count = len(text)
        char_count_no_spaces = len(text.replace(' ', ''))
        
        # Word counts
        word_count = len(words)
        unique_words = len(set(word.lower() for word in words))
        
        # Sentence counts
        sentence_count = len(sentences)
        
        # Average calculations
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        avg_chars_per_word = char_count_no_spaces / word_count if word_count > 0 else 0
        
        # Vocabulary diversity (Type-Token Ratio)
        vocabulary_diversity = unique_words / word_count if word_count > 0 else 0
        
        return {
            'character_count': char_count,
            'character_count_no_spaces': char_count_no_spaces,
            'word_count': word_count,
            'unique_word_count': unique_words,
            'sentence_count': sentence_count,
            'paragraph_count': len(text.split('\n\n')),
            'avg_words_per_sentence': round(avg_words_per_sentence, 2),
            'avg_characters_per_word': round(avg_chars_per_word, 2),
            'vocabulary_diversity': round(vocabulary_diversity, 3)
        }

    def _calculate_readability(self, text: str) -> Dict[str, Any]:
        """Calculate various readability metrics."""
        sentences = self._split_sentences(text)
        words = self._split_words(text)
        syllables = sum(self._count_syllables(word) for word in words)
        
        sentence_count = len(sentences)
        word_count = len(words)
        
        if sentence_count == 0 or word_count == 0:
            return {'error': 'Insufficient text for readability analysis'}
        
        # Flesch Reading Ease
        flesch_ease = 206.835 - (1.015 * (word_count / sentence_count)) - (84.6 * (syllables / word_count))
        flesch_ease = max(0, min(100, flesch_ease))  # Clamp between 0-100
        
        # Flesch-Kincaid Grade Level
        flesch_kincaid = (0.39 * (word_count / sentence_count)) + (11.8 * (syllables / word_count)) - 15.59
        flesch_kincaid = max(0, flesch_kincaid)
        
        # Automated Readability Index (ARI)
        characters = sum(len(word) for word in words)
        ari = (4.71 * (characters / word_count)) + (0.5 * (word_count / sentence_count)) - 21.43
        ari = max(0, ari)
        
        # Coleman-Liau Index
        l = (characters / word_count) * 100
        s = (sentence_count / word_count) * 100
        coleman_liau = (0.0588 * l) - (0.296 * s) - 15.8
        coleman_liau = max(0, coleman_liau)
        
        # Average grade level
        avg_grade = (flesch_kincaid + ari + coleman_liau) / 3
        
        return {
            'flesch_reading_ease': round(flesch_ease, 2),
            'flesch_kincaid_grade': round(flesch_kincaid, 2),
            'automated_readability_index': round(ari, 2),
            'coleman_liau_index': round(coleman_liau, 2),
            'average_grade_level': round(avg_grade, 2),
            'readability_level': self._get_readability_level(flesch_ease)
        }

    def _analyze_complexity(self, text: str) -> Dict[str, Any]:
        """Analyze text complexity."""
        words = self._split_words(text)
        sentences = self._split_sentences(text)
        
        # Lexical complexity
        complex_words = [word for word in words if len(word) > 6]
        complex_word_ratio = len(complex_words) / len(words) if words else 0
        
        # Syntactic complexity
        sentence_lengths = [len(self._split_words(sentence)) for sentence in sentences]
        avg_sentence_length = statistics.mean(sentence_lengths) if sentence_lengths else 0
        sentence_length_variance = statistics.variance(sentence_lengths) if len(sentence_lengths) > 1 else 0
        
        # Formal word usage
        formal_word_count = sum(1 for word in words if word.lower() in self.formal_indicators)
        formal_word_ratio = formal_word_count / len(words) if words else 0
        
        # Punctuation complexity
        punctuation_marks = re.findall(r'[;:,\-—()[\]{}"]', text)
        punctuation_density = len(punctuation_marks) / len(words) if words else 0
        
        return {
            'complex_word_ratio': round(complex_word_ratio, 3),
            'average_sentence_length': round(avg_sentence_length, 2),
            'sentence_length_variance': round(sentence_length_variance, 2),
            'formal_word_ratio': round(formal_word_ratio, 3),
            'punctuation_density': round(punctuation_density, 3),
            'complexity_score': round((complex_word_ratio + formal_word_ratio + punctuation_density) * 100, 2)
        }

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze text sentiment."""
        words = [word.lower() for word in self._split_words(text)]
        
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            sentiment_score = 0
            sentiment_label = 'neutral'
        else:
            sentiment_score = (positive_count - negative_count) / total_sentiment_words
            if sentiment_score > 0.1:
                sentiment_label = 'positive'
            elif sentiment_score < -0.1:
                sentiment_label = 'negative'
            else:
                sentiment_label = 'neutral'
        
        return {
            'positive_word_count': positive_count,
            'negative_word_count': negative_count,
            'sentiment_score': round(sentiment_score, 3),
            'sentiment_label': sentiment_label,
            'sentiment_ratio': round(total_sentiment_words / len(words), 3) if words else 0
        }

    def _analyze_ai_indicators(self, text: str) -> Dict[str, Any]:
        """Analyze indicators that might suggest AI-generated text."""
        words = [word.lower() for word in self._split_words(text)]
        sentences = self._split_sentences(text)
        
        # Formal language indicators
        formal_count = sum(1 for word in words if word in self.formal_indicators)
        formal_ratio = formal_count / len(words) if words else 0
        
        # Repetitive patterns
        word_frequency = {}
        for word in words:
            if word not in self.common_words and len(word) > 3:
                word_frequency[word] = word_frequency.get(word, 0) + 1
        
        repeated_words = sum(1 for count in word_frequency.values() if count > 2)
        repetition_score = repeated_words / len(word_frequency) if word_frequency else 0
        
        # Sentence structure uniformity
        sentence_lengths = [len(self._split_words(sentence)) for sentence in sentences]
        length_variance = statistics.variance(sentence_lengths) if len(sentence_lengths) > 1 else 0
        uniformity_score = 1 / (1 + length_variance) if length_variance > 0 else 1
        
        # Transition word overuse
        transition_words = {
            'however', 'furthermore', 'moreover', 'additionally', 'consequently',
            'therefore', 'subsequently', 'nevertheless', 'nonetheless', 'accordingly'
        }
        transition_count = sum(1 for word in words if word in transition_words)
        transition_ratio = transition_count / len(sentences) if sentences else 0
        
        # Overall AI likelihood score
        ai_score = (formal_ratio * 0.3 + repetition_score * 0.2 + 
                   uniformity_score * 0.3 + min(transition_ratio, 1) * 0.2) * 100
        
        return {
            'formal_language_ratio': round(formal_ratio, 3),
            'repetition_score': round(repetition_score, 3),
            'sentence_uniformity': round(uniformity_score, 3),
            'transition_word_ratio': round(transition_ratio, 3),
            'ai_likelihood_score': round(ai_score, 2),
            'ai_likelihood_level': self._get_ai_likelihood_level(ai_score)
        }

    def _analyze_burstiness(self, text: str) -> Dict[str, Any]:
        """Analyze text burstiness (variation in sentence length and complexity)."""
        sentences = self._split_sentences(text)
        sentence_lengths = [len(self._split_words(sentence)) for sentence in sentences]
        
        if len(sentence_lengths) < 2:
            return {'error': 'Insufficient sentences for burstiness analysis'}
        
        # Length variation
        mean_length = statistics.mean(sentence_lengths)
        length_variance = statistics.variance(sentence_lengths)
        length_std = statistics.stdev(sentence_lengths)
        coefficient_of_variation = length_std / mean_length if mean_length > 0 else 0
        
        # Complexity variation (based on punctuation and word complexity)
        complexity_scores = []
        for sentence in sentences:
            words = self._split_words(sentence)
            complex_words = sum(1 for word in words if len(word) > 6)
            punctuation = len(re.findall(r'[;:,\-—()[\]{}"]', sentence))
            complexity = (complex_words + punctuation) / len(words) if words else 0
            complexity_scores.append(complexity)
        
        complexity_variance = statistics.variance(complexity_scores) if len(complexity_scores) > 1 else 0
        
        # Burstiness score (higher = more human-like variation)
        burstiness_score = (coefficient_of_variation + complexity_variance) * 50
        burstiness_score = min(100, burstiness_score)  # Cap at 100
        
        return {
            'sentence_count': len(sentences),
            'mean_sentence_length': round(mean_length, 2),
            'length_variance': round(length_variance, 2),
            'length_standard_deviation': round(length_std, 2),
            'coefficient_of_variation': round(coefficient_of_variation, 3),
            'complexity_variance': round(complexity_variance, 3),
            'burstiness_score': round(burstiness_score, 2),
            'burstiness_level': self._get_burstiness_level(burstiness_score)
        }

    def _estimate_perplexity(self, text: str) -> Dict[str, Any]:
        """Estimate text perplexity (simplified calculation)."""
        words = [word.lower() for word in self._split_words(text)]
        
        if len(words) < 2:
            return {'error': 'Insufficient text for perplexity estimation'}
        
        # Calculate word frequency
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Calculate probabilities
        total_words = len(words)
        probabilities = [word_freq[word] / total_words for word in words]
        
        # Calculate entropy
        entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
        
        # Perplexity is 2^entropy
        perplexity = 2 ** entropy
        
        # Vocabulary richness
        unique_words = len(set(words))
        vocabulary_richness = unique_words / total_words
        
        return {
            'estimated_perplexity': round(perplexity, 2),
            'entropy': round(entropy, 3),
            'vocabulary_richness': round(vocabulary_richness, 3),
            'unique_word_ratio': round(unique_words / total_words, 3),
            'perplexity_level': self._get_perplexity_level(perplexity)
        }

    def _calculate_overall_score(self, readability: Dict, complexity: Dict, 
                               ai_indicators: Dict, burstiness: Dict) -> Dict[str, Any]:
        """Calculate an overall humanness score."""
        try:
            # Normalize scores to 0-100 scale
            readability_score = min(100, max(0, readability.get('flesch_reading_ease', 50)))
            complexity_score = min(100, complexity.get('complexity_score', 50))
            ai_score = 100 - ai_indicators.get('ai_likelihood_score', 50)  # Invert AI score
            burstiness_score = burstiness.get('burstiness_score', 50)
            
            # Weighted average (adjust weights as needed)
            overall_score = (
                readability_score * 0.25 +
                complexity_score * 0.25 +
                ai_score * 0.3 +
                burstiness_score * 0.2
            )
            
            return {
                'overall_humanness_score': round(overall_score, 2),
                'humanness_level': self._get_humanness_level(overall_score),
                'component_scores': {
                    'readability': round(readability_score, 2),
                    'complexity': round(complexity_score, 2),
                    'anti_ai': round(ai_score, 2),
                    'burstiness': round(burstiness_score, 2)
                }
            }
        except Exception:
            return {
                'overall_humanness_score': 50.0,
                'humanness_level': 'moderate',
                'component_scores': {
                    'readability': 50.0,
                    'complexity': 50.0,
                    'anti_ai': 50.0,
                    'burstiness': 50.0
                }
            }

    # Helper methods
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

    def _split_words(self, text: str) -> List[str]:
        """Split text into words."""
        words = re.findall(r'\b\w+\b', text.lower())
        return words

    def _count_syllables(self, word: str) -> int:
        """Estimate syllable count for a word."""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                syllable_count += 1
            prev_was_vowel = is_vowel
        
        # Handle silent 'e'
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)

    def _get_readability_level(self, flesch_score: float) -> str:
        """Get readability level from Flesch score."""
        if flesch_score >= 90:
            return 'very_easy'
        elif flesch_score >= 80:
            return 'easy'
        elif flesch_score >= 70:
            return 'fairly_easy'
        elif flesch_score >= 60:
            return 'standard'
        elif flesch_score >= 50:
            return 'fairly_difficult'
        elif flesch_score >= 30:
            return 'difficult'
        else:
            return 'very_difficult'

    def _get_ai_likelihood_level(self, ai_score: float) -> str:
        """Get AI likelihood level from score."""
        if ai_score >= 80:
            return 'very_high'
        elif ai_score >= 60:
            return 'high'
        elif ai_score >= 40:
            return 'moderate'
        elif ai_score >= 20:
            return 'low'
        else:
            return 'very_low'

    def _get_burstiness_level(self, burstiness_score: float) -> str:
        """Get burstiness level from score."""
        if burstiness_score >= 80:
            return 'very_high'
        elif burstiness_score >= 60:
            return 'high'
        elif burstiness_score >= 40:
            return 'moderate'
        elif burstiness_score >= 20:
            return 'low'
        else:
            return 'very_low'

    def _get_perplexity_level(self, perplexity: float) -> str:
        """Get perplexity level from score."""
        if perplexity >= 100:
            return 'very_high'
        elif perplexity >= 50:
            return 'high'
        elif perplexity >= 20:
            return 'moderate'
        elif perplexity >= 10:
            return 'low'
        else:
            return 'very_low'

    def _get_humanness_level(self, score: float) -> str:
        """Get humanness level from overall score."""
        if score >= 85:
            return 'very_human'
        elif score >= 70:
            return 'mostly_human'
        elif score >= 55:
            return 'somewhat_human'
        elif score >= 40:
            return 'mixed'
        elif score >= 25:
            return 'somewhat_ai'
        else:
            return 'likely_ai'

