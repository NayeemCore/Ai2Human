"""
Advanced Humanization Service
Provides additional sophisticated humanization algorithms and techniques.
"""
import random
import re
from typing import Dict, List, Tuple, Any
import logging

logger = logging.getLogger(__name__)

class AdvancedHumanizationService:
    """Service for advanced humanization techniques beyond basic vocabulary replacement."""
    
    def __init__(self):
        # Advanced linguistic patterns for more sophisticated humanization
        self.discourse_markers = {
            'addition': ['furthermore', 'moreover', 'additionally', 'in addition', 'also', 'besides'],
            'contrast': ['however', 'nevertheless', 'on the other hand', 'conversely', 'in contrast', 'yet'],
            'cause_effect': ['therefore', 'consequently', 'as a result', 'thus', 'hence', 'accordingly'],
            'example': ['for instance', 'for example', 'such as', 'namely', 'specifically', 'in particular'],
            'emphasis': ['indeed', 'certainly', 'undoubtedly', 'clearly', 'obviously', 'definitely'],
            'sequence': ['first', 'second', 'next', 'then', 'finally', 'subsequently']
        }
        
        # Hedging expressions to add uncertainty and human-like hesitation
        self.hedging_expressions = [
            'it seems that', 'it appears that', 'perhaps', 'possibly', 'likely',
            'it could be argued that', 'one might say', 'to some extent',
            'in many cases', 'generally speaking', 'broadly speaking',
            'it is possible that', 'there is a chance that', 'it may be that'
        ]
        
        # Intensifiers and downtoners for more nuanced expression
        self.intensifiers = ['extremely', 'highly', 'remarkably', 'exceptionally', 'particularly', 'especially']
        self.downtoners = ['somewhat', 'rather', 'quite', 'fairly', 'relatively', 'moderately']
        
        # Colloquial expressions for more natural language
        self.colloquial_replacements = {
            'very good': ['excellent', 'outstanding', 'superb', 'fantastic', 'great'],
            'very bad': ['terrible', 'awful', 'horrible', 'dreadful', 'poor'],
            'very big': ['huge', 'enormous', 'massive', 'gigantic', 'vast'],
            'very small': ['tiny', 'minuscule', 'microscopic', 'minute', 'petite'],
            'very fast': ['rapid', 'swift', 'speedy', 'quick', 'brisk'],
            'very slow': ['sluggish', 'gradual', 'leisurely', 'unhurried', 'deliberate']
        }
        
        # Sentence complexity patterns
        self.complexity_patterns = {
            'simple_to_complex': [
                lambda s: self._add_relative_clause(s),
                lambda s: self._add_participial_phrase(s),
                lambda s: self._add_appositive(s)
            ],
            'complex_to_simple': [
                lambda s: self._split_compound_sentence(s),
                lambda s: self._simplify_relative_clause(s),
                lambda s: self._convert_passive_to_active(s)
            ]
        }
        
        # Emotional and subjective language markers
        self.subjective_markers = [
            'I believe', 'in my opinion', 'from my perspective', 'personally',
            'it strikes me that', 'I feel that', 'my impression is',
            'as I see it', 'to my mind', 'I would argue that'
        ]
        
        # Rhetorical devices for more engaging text
        self.rhetorical_devices = {
            'metaphor': ['like a', 'as if', 'resembles', 'mirrors', 'echoes'],
            'alliteration': self._generate_alliterative_phrases,
            'repetition': self._add_strategic_repetition,
            'parallelism': self._create_parallel_structure
        }

    def apply_advanced_humanization(self, text: str, intensity: float, mode: str) -> Dict[str, Any]:
        """
        Apply advanced humanization techniques to text.
        
        Args:
            text: Input text to humanize
            intensity: Humanization intensity (0.0 to 1.0)
            mode: Humanization mode (fast, balanced, aggressive)
            
        Returns:
            Dict containing humanized text and applied techniques
        """
        try:
            humanized_text = text
            applied_techniques = []
            
            # Apply techniques based on mode and intensity
            if mode == 'fast':
                humanized_text = self._apply_light_humanization(humanized_text, intensity)
                applied_techniques.extend(['discourse_markers', 'hedging'])
            elif mode == 'balanced':
                humanized_text = self._apply_moderate_humanization(humanized_text, intensity)
                applied_techniques.extend(['discourse_markers', 'hedging', 'complexity_variation', 'subjective_markers'])
            elif mode == 'aggressive':
                humanized_text = self._apply_intensive_humanization(humanized_text, intensity)
                applied_techniques.extend(['all_techniques'])
            
            return {
                'success': True,
                'humanized_text': humanized_text,
                'applied_techniques': applied_techniques,
                'original_length': len(text),
                'humanized_length': len(humanized_text),
                'service': 'advanced_humanization'
            }
            
        except Exception as e:
            logger.error(f"Advanced humanization error: {str(e)}")
            return {
                'success': False,
                'error': f"Advanced humanization failed: {str(e)}",
                'humanized_text': text,
                'service': 'advanced_humanization'
            }

    def _apply_light_humanization(self, text: str, intensity: float) -> str:
        """Apply light humanization for fast mode."""
        # Add discourse markers
        text = self._add_discourse_markers(text, intensity * 0.3)
        
        # Add hedging expressions
        text = self._add_hedging_expressions(text, intensity * 0.2)
        
        # Light colloquial replacements
        text = self._apply_colloquial_replacements(text, intensity * 0.2)
        
        return text

    def _apply_moderate_humanization(self, text: str, intensity: float) -> str:
        """Apply moderate humanization for balanced mode."""
        # All light techniques with higher intensity
        text = self._apply_light_humanization(text, intensity)
        
        # Add sentence complexity variation
        text = self._vary_sentence_complexity(text, intensity * 0.4)
        
        # Add subjective markers
        text = self._add_subjective_markers(text, intensity * 0.3)
        
        # Add intensifiers and downtoners
        text = self._add_intensifiers_downtoners(text, intensity * 0.3)
        
        return text

    def _apply_intensive_humanization(self, text: str, intensity: float) -> str:
        """Apply intensive humanization for aggressive mode."""
        # All moderate techniques with maximum intensity
        text = self._apply_moderate_humanization(text, intensity)
        
        # Add rhetorical devices
        text = self._add_rhetorical_devices(text, intensity * 0.5)
        
        # Advanced sentence restructuring
        text = self._advanced_sentence_restructuring(text, intensity * 0.6)
        
        # Add emotional language
        text = self._add_emotional_language(text, intensity * 0.4)
        
        return text

    def _add_discourse_markers(self, text: str, intensity: float) -> str:
        """Add discourse markers to improve text flow."""
        sentences = re.split(r'[.!?]+', text)
        modified_sentences = []
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
                
            if random.random() < intensity and i > 0:
                # Choose appropriate discourse marker based on context
                if 'result' in sentence.lower() or 'effect' in sentence.lower():
                    marker = random.choice(self.discourse_markers['cause_effect'])
                elif 'example' in sentence.lower() or 'instance' in sentence.lower():
                    marker = random.choice(self.discourse_markers['example'])
                elif 'but' in sentence.lower() or 'however' in sentence.lower():
                    marker = random.choice(self.discourse_markers['contrast'])
                else:
                    category = random.choice(list(self.discourse_markers.keys()))
                    marker = random.choice(self.discourse_markers[category])
                
                sentence = f"{marker.capitalize()}, {sentence.lower()}"
            
            modified_sentences.append(sentence)
        
        return '. '.join(modified_sentences) + '.'

    def _add_hedging_expressions(self, text: str, intensity: float) -> str:
        """Add hedging expressions to make text less definitive."""
        sentences = text.split('. ')
        modified_sentences = []
        
        for sentence in sentences:
            if random.random() < intensity:
                # Look for definitive statements to hedge
                if any(word in sentence.lower() for word in ['is', 'are', 'will', 'must', 'always', 'never']):
                    hedge = random.choice(self.hedging_expressions)
                    
                    # Insert hedge appropriately
                    if sentence.lower().startswith(('this', 'that', 'these', 'those', 'the')):
                        sentence = f"{hedge.capitalize()}, {sentence.lower()}"
                    else:
                        words = sentence.split()
                        if len(words) > 3:
                            insert_pos = random.randint(1, min(3, len(words) - 1))
                            words.insert(insert_pos, hedge)
                            sentence = ' '.join(words)
            
            modified_sentences.append(sentence)
        
        return '. '.join(modified_sentences)

    def _apply_colloquial_replacements(self, text: str, intensity: float) -> str:
        """Replace formal expressions with more colloquial ones."""
        for formal, colloquial_list in self.colloquial_replacements.items():
            if formal in text.lower() and random.random() < intensity:
                replacement = random.choice(colloquial_list)
                text = re.sub(re.escape(formal), replacement, text, flags=re.IGNORECASE)
        
        return text

    def _vary_sentence_complexity(self, text: str, intensity: float) -> str:
        """Vary sentence complexity to increase burstiness."""
        sentences = re.split(r'[.!?]+', text)
        modified_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            word_count = len(sentence.split())
            
            if random.random() < intensity:
                if word_count < 8:  # Simple sentence - make more complex
                    if random.random() < 0.5:
                        sentence = self._add_relative_clause(sentence)
                    else:
                        sentence = self._add_participial_phrase(sentence)
                elif word_count > 20:  # Complex sentence - simplify
                    sentence = self._split_compound_sentence(sentence)
            
            modified_sentences.append(sentence)
        
        return '. '.join([s for s in modified_sentences if s]) + '.'

    def _add_subjective_markers(self, text: str, intensity: float) -> str:
        """Add subjective markers to make text more personal."""
        sentences = text.split('. ')
        modified_sentences = []
        
        for i, sentence in enumerate(sentences):
            if random.random() < intensity and i > 0:
                marker = random.choice(self.subjective_markers)
                sentence = f"{marker}, {sentence.lower()}"
            
            modified_sentences.append(sentence)
        
        return '. '.join(modified_sentences)

    def _add_intensifiers_downtoners(self, text: str, intensity: float) -> str:
        """Add intensifiers and downtoners for more nuanced expression."""
        words = text.split()
        modified_words = []
        
        for i, word in enumerate(words):
            if word.lower() in ['good', 'bad', 'big', 'small', 'fast', 'slow', 'important', 'significant']:
                if random.random() < intensity:
                    if random.random() < 0.5:
                        modifier = random.choice(self.intensifiers)
                    else:
                        modifier = random.choice(self.downtoners)
                    modified_words.extend([modifier, word])
                else:
                    modified_words.append(word)
            else:
                modified_words.append(word)
        
        return ' '.join(modified_words)

    def _add_rhetorical_devices(self, text: str, intensity: float) -> str:
        """Add rhetorical devices for more engaging text."""
        if random.random() < intensity * 0.3:
            # Add metaphorical language
            text = self._add_metaphorical_language(text)
        
        if random.random() < intensity * 0.2:
            # Add strategic repetition
            text = self._add_strategic_repetition(text)
        
        return text

    def _advanced_sentence_restructuring(self, text: str, intensity: float) -> str:
        """Apply advanced sentence restructuring techniques."""
        sentences = re.split(r'[.!?]+', text)
        modified_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if random.random() < intensity:
                # Apply various restructuring techniques
                if random.random() < 0.3:
                    sentence = self._fronting_technique(sentence)
                elif random.random() < 0.3:
                    sentence = self._clefting_technique(sentence)
                elif random.random() < 0.3:
                    sentence = self._inversion_technique(sentence)
            
            modified_sentences.append(sentence)
        
        return '. '.join([s for s in modified_sentences if s]) + '.'

    def _add_emotional_language(self, text: str, intensity: float) -> str:
        """Add emotional language to make text more engaging."""
        emotional_adjectives = ['fascinating', 'intriguing', 'remarkable', 'surprising', 'compelling', 'striking']
        
        sentences = text.split('. ')
        modified_sentences = []
        
        for sentence in sentences:
            if random.random() < intensity * 0.3:
                # Add emotional adjectives
                words = sentence.split()
                if len(words) > 3:
                    adj = random.choice(emotional_adjectives)
                    insert_pos = random.randint(1, min(3, len(words) - 1))
                    words.insert(insert_pos, adj)
                    sentence = ' '.join(words)
            
            modified_sentences.append(sentence)
        
        return '. '.join(modified_sentences)

    # Helper methods for specific transformations
    def _add_relative_clause(self, sentence: str) -> str:
        """Add a relative clause to make sentence more complex."""
        words = sentence.split()
        if len(words) > 4:
            # Find a noun to attach relative clause to
            for i, word in enumerate(words):
                if word.lower() in ['system', 'method', 'process', 'technology', 'approach']:
                    relative_clauses = [
                        'which is essential',
                        'that proves effective',
                        'which demonstrates value',
                        'that shows promise'
                    ]
                    clause = random.choice(relative_clauses)
                    words.insert(i + 1, f", {clause},")
                    break
        
        return ' '.join(words)

    def _add_participial_phrase(self, sentence: str) -> str:
        """Add a participial phrase to increase complexity."""
        participial_phrases = [
            'Building on this foundation',
            'Considering these factors',
            'Taking this into account',
            'Recognizing the importance'
        ]
        
        if random.random() < 0.5:
            phrase = random.choice(participial_phrases)
            return f"{phrase}, {sentence.lower()}"
        
        return sentence

    def _add_appositive(self, sentence: str) -> str:
        """Add an appositive for additional information."""
        words = sentence.split()
        if len(words) > 5:
            appositives = [
                'a crucial element',
                'an important factor',
                'a key component',
                'a vital aspect'
            ]
            
            for i, word in enumerate(words):
                if word.lower() in ['technology', 'system', 'method', 'approach']:
                    appositive = random.choice(appositives)
                    words.insert(i + 1, f", {appositive},")
                    break
        
        return ' '.join(words)

    def _split_compound_sentence(self, sentence: str) -> str:
        """Split compound sentences into simpler ones."""
        # Look for coordinating conjunctions
        conjunctions = ['and', 'but', 'or', 'so', 'yet']
        
        for conj in conjunctions:
            if f' {conj} ' in sentence:
                parts = sentence.split(f' {conj} ', 1)
                if len(parts) == 2:
                    return f"{parts[0].strip()}. {parts[1].strip().capitalize()}"
        
        return sentence

    def _fronting_technique(self, sentence: str) -> str:
        """Apply fronting for emphasis."""
        words = sentence.split()
        if len(words) > 6:
            # Look for prepositional phrases to front
            for i, word in enumerate(words):
                if word.lower() in ['in', 'on', 'at', 'by', 'with', 'through']:
                    if i + 2 < len(words):
                        fronted = ' '.join(words[i:i+3])
                        remaining = ' '.join(words[:i] + words[i+3:])
                        return f"{fronted.capitalize()}, {remaining.lower()}"
        
        return sentence

    def _clefting_technique(self, sentence: str) -> str:
        """Apply clefting for emphasis."""
        if sentence.lower().startswith('the'):
            words = sentence.split()
            if len(words) > 4:
                return f"What {' '.join(words[1:]).lower()} is {words[0].lower()}"
        
        return sentence

    def _inversion_technique(self, sentence: str) -> str:
        """Apply inversion for stylistic effect."""
        if 'never' in sentence.lower() or 'rarely' in sentence.lower():
            words = sentence.split()
            for i, word in enumerate(words):
                if word.lower() in ['never', 'rarely', 'seldom']:
                    if i + 2 < len(words):
                        # Simple inversion
                        inverted = f"{word.capitalize()} {words[i+2]} {words[i+1]} {' '.join(words[i+3:])}"
                        return inverted
        
        return sentence

    def _add_metaphorical_language(self, text: str) -> str:
        """Add metaphorical expressions."""
        metaphors = {
            'process': 'journey',
            'system': 'ecosystem',
            'method': 'pathway',
            'approach': 'strategy',
            'solution': 'key'
        }
        
        for literal, metaphor in metaphors.items():
            if literal in text.lower() and random.random() < 0.3:
                text = re.sub(rf'\b{literal}\b', metaphor, text, flags=re.IGNORECASE)
        
        return text

    def _add_strategic_repetition(self, text: str) -> str:
        """Add strategic repetition for emphasis."""
        sentences = text.split('. ')
        if len(sentences) > 2:
            # Find key terms to repeat
            key_terms = ['important', 'essential', 'crucial', 'significant', 'vital']
            
            for term in key_terms:
                if term in text.lower():
                    # Add emphasis through repetition
                    text = text.replace(term, f"{term}, truly {term}")
                    break
        
        return text

    def _generate_alliterative_phrases(self, text: str) -> str:
        """Generate alliterative phrases where appropriate."""
        alliterative_pairs = {
            'significant': 'substantial',
            'important': 'imperative',
            'effective': 'efficient',
            'comprehensive': 'complete',
            'fundamental': 'foundational'
        }
        
        for word, alliterative in alliterative_pairs.items():
            if word in text.lower() and random.random() < 0.2:
                text = re.sub(rf'\b{word}\b', f"{word} and {alliterative}", text, flags=re.IGNORECASE)
        
        return text

    def _create_parallel_structure(self, text: str) -> str:
        """Create parallel structures for better flow."""
        # Look for lists or series
        if ' and ' in text:
            # Simple parallelism enhancement
            text = re.sub(r'(\w+), (\w+), and (\w+)', r'\1, \2, and \3', text)
        
        return text

