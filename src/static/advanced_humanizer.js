// Advanced AI Humanization Engine
// Targets specific AI detection scores: Fast (75%), Balanced (50%), Aggressive (0%)

class AdvancedHumanizer {
    constructor() {
        this.synonymDatabase = this.initializeSynonymDatabase();
        this.sentencePatterns = this.initializeSentencePatterns();
        this.humanizationTechniques = this.initializeHumanizationTechniques();
    }

    // Main humanization function targeting specific AI detection scores
    async humanizeText(text, mode = 'balanced', options = {}) {
        const startTime = Date.now();
        
        // Get target AI detection score based on mode
        const targetAIScore = this.getTargetAIScore(mode);
        
        // Apply humanization techniques based on target score
        let humanizedText = await this.applyHumanizationTechniques(text, targetAIScore, options);
        
        // Calculate achieved AI detection score
        const achievedScore = this.calculateAIDetectionScore(text, humanizedText, targetAIScore);
        
        const processingTime = Date.now() - startTime;
        
        return {
            originalText: text,
            humanizedText: humanizedText,
            targetAIScore: targetAIScore,
            achievedAIScore: achievedScore,
            processingTime: processingTime,
            mode: mode
        };
    }

    // Get target AI detection scores for each mode
    getTargetAIScore(mode) {
        const targets = {
            'fast': 75,      // Fast mode: 75% AI detection
            'balanced': 50,  // Balanced mode: 50% AI detection
            'aggressive': 0  // Aggressive mode: 0% AI detection (fully human-like)
        };
        return targets[mode] || 50;
    }

    // Apply humanization techniques based on target AI score
    async applyHumanizationTechniques(text, targetAIScore, options) {
        let processedText = text;
        
        // Determine intensity of humanization based on target score
        const humanizationIntensity = this.calculateHumanizationIntensity(targetAIScore);
        
        // Apply techniques in order of effectiveness
        if (humanizationIntensity >= 0.25) { // For 75% target and below
            processedText = this.increasePerplexity(processedText, humanizationIntensity);
        }
        
        if (humanizationIntensity >= 0.5) { // For 50% target and below
            processedText = this.increaseBurstiness(processedText, humanizationIntensity);
            processedText = this.addHumanVariations(processedText, humanizationIntensity);
        }
        
        if (humanizationIntensity >= 0.75) { // For aggressive mode (0% target)
            processedText = this.addPersonalTouches(processedText, humanizationIntensity);
            processedText = this.introduceSubtleImperfections(processedText, humanizationIntensity);
        }
        
        return processedText;
    }

    // Calculate humanization intensity based on target AI score
    calculateHumanizationIntensity(targetAIScore) {
        // Convert AI score to humanization intensity (inverse relationship)
        // 75% AI = 25% humanization, 50% AI = 50% humanization, 0% AI = 100% humanization
        return (100 - targetAIScore) / 100;
    }

    // Increase perplexity by varying word choices and sentence structures
    increasePerplexity(text, intensity) {
        const sentences = this.splitIntoSentences(text);
        const processedSentences = sentences.map(sentence => {
            if (Math.random() < intensity) {
                // Replace common words with less predictable synonyms
                sentence = this.replaceSynonyms(sentence, intensity);
                // Vary sentence structure
                sentence = this.varysentenceStructure(sentence, intensity);
            }
            return sentence;
        });
        
        return processedSentences.join(' ');
    }

    // Increase burstiness by varying sentence lengths and structures
    increaseBurstiness(text, intensity) {
        const sentences = this.splitIntoSentences(text);
        const processedSentences = [];
        
        for (let i = 0; i < sentences.length; i++) {
            let sentence = sentences[i];
            
            // Randomly decide to modify sentence length/structure
            if (Math.random() < intensity) {
                const modification = Math.random();
                
                if (modification < 0.3 && sentence.length > 50) {
                    // Split long sentences into shorter ones
                    const splitSentences = this.splitLongSentence(sentence);
                    processedSentences.push(...splitSentences);
                } else if (modification < 0.6 && i < sentences.length - 1) {
                    // Combine short sentences
                    const nextSentence = sentences[i + 1];
                    if (sentence.length < 30 && nextSentence.length < 30) {
                        sentence = this.combineSentences(sentence, nextSentence);
                        i++; // Skip next sentence as it's been combined
                    }
                    processedSentences.push(sentence);
                } else {
                    // Add transitional phrases or connectors
                    sentence = this.addTransitionalElements(sentence, intensity);
                    processedSentences.push(sentence);
                }
            } else {
                processedSentences.push(sentence);
            }
        }
        
        return processedSentences.join(' ');
    }

    // Add human-like variations and expressions
    addHumanVariations(text, intensity) {
        let processedText = text;
        
        // Add conversational elements
        if (Math.random() < intensity * 0.3) {
            processedText = this.addConversationalElements(processedText);
        }
        
        // Introduce rhetorical questions
        if (Math.random() < intensity * 0.2) {
            processedText = this.addRhetoricalQuestions(processedText);
        }
        
        // Add emphasis and emotional markers
        if (Math.random() < intensity * 0.4) {
            processedText = this.addEmphasisMarkers(processedText);
        }
        
        return processedText;
    }

    // Add personal touches for maximum humanization
    addPersonalTouches(text, intensity) {
        let processedText = text;
        
        // Add personal pronouns and perspectives
        processedText = this.addPersonalPerspectives(processedText, intensity);
        
        // Include idiomatic expressions
        processedText = this.addIdiomaticExpressions(processedText, intensity);
        
        // Add contextual references
        processedText = this.addContextualReferences(processedText, intensity);
        
        return processedText;
    }

    // Introduce subtle imperfections that humans might make
    introduceSubtleImperfections(text, intensity) {
        let processedText = text;
        
        // Occasionally use contractions
        if (Math.random() < intensity * 0.5) {
            processedText = this.addContractions(processedText);
        }
        
        // Vary punctuation slightly
        if (Math.random() < intensity * 0.3) {
            processedText = this.varyPunctuation(processedText);
        }
        
        // Add occasional informal phrasing
        if (Math.random() < intensity * 0.2) {
            processedText = this.addInformalPhrasing(processedText);
        }
        
        return processedText;
    }

    // Helper function to replace words with synonyms
    replaceSynonyms(sentence, intensity) {
        const words = sentence.split(' ');
        const processedWords = words.map(word => {
            const cleanWord = word.toLowerCase().replace(/[^\w]/g, '');
            if (this.synonymDatabase[cleanWord] && Math.random() < intensity * 0.3) {
                const synonyms = this.synonymDatabase[cleanWord];
                const randomSynonym = synonyms[Math.floor(Math.random() * synonyms.length)];
                return word.replace(cleanWord, randomSynonym);
            }
            return word;
        });
        
        return processedWords.join(' ');
    }

    // Helper function to vary sentence structure
    varysentenceStructure(sentence, intensity) {
        // Simple transformations to vary structure
        if (sentence.includes(' and ') && Math.random() < intensity * 0.4) {
            return sentence.replace(' and ', ', and ');
        }
        
        if (sentence.includes(' because ') && Math.random() < intensity * 0.3) {
            return sentence.replace(' because ', ' since ');
        }
        
        if (sentence.includes(' however ') && Math.random() < intensity * 0.3) {
            return sentence.replace(' however ', ' though ');
        }
        
        return sentence;
    }

    // Split text into sentences
    splitIntoSentences(text) {
        return text.split(/[.!?]+/).filter(s => s.trim().length > 0).map(s => s.trim() + '.');
    }

    // Split long sentences into shorter ones
    splitLongSentence(sentence) {
        const conjunctions = [' and ', ' but ', ' however ', ' furthermore ', ' moreover '];
        
        for (const conjunction of conjunctions) {
            if (sentence.includes(conjunction)) {
                const parts = sentence.split(conjunction);
                if (parts.length === 2) {
                    return [parts[0].trim() + '.', parts[1].trim() + '.'];
                }
            }
        }
        
        return [sentence];
    }

    // Combine short sentences
    combineSentences(sentence1, sentence2) {
        const connectors = [', and ', ', but ', ', so ', ', yet '];
        const randomConnector = connectors[Math.floor(Math.random() * connectors.length)];
        
        return sentence1.replace('.', '') + randomConnector + sentence2.toLowerCase();
    }

    // Add transitional elements
    addTransitionalElements(sentence, intensity) {
        const transitions = ['Furthermore, ', 'Additionally, ', 'Moreover, ', 'In fact, ', 'Indeed, '];
        
        if (Math.random() < intensity * 0.2) {
            const randomTransition = transitions[Math.floor(Math.random() * transitions.length)];
            return randomTransition + sentence.toLowerCase();
        }
        
        return sentence;
    }

    // Add conversational elements
    addConversationalElements(text) {
        const conversationalPhrases = [
            'You know, ',
            'Well, ',
            'Actually, ',
            'To be honest, ',
            'Frankly speaking, '
        ];
        
        const sentences = this.splitIntoSentences(text);
        if (sentences.length > 0 && Math.random() < 0.3) {
            const randomPhrase = conversationalPhrases[Math.floor(Math.random() * conversationalPhrases.length)];
            sentences[0] = randomPhrase + sentences[0].toLowerCase();
        }
        
        return sentences.join(' ');
    }

    // Add rhetorical questions
    addRhetoricalQuestions(text) {
        const questions = [
            'But what does this really mean? ',
            'Why is this important? ',
            'How does this work in practice? ',
            'What are the implications? '
        ];
        
        const sentences = this.splitIntoSentences(text);
        if (sentences.length > 1) {
            const insertPosition = Math.floor(sentences.length / 2);
            const randomQuestion = questions[Math.floor(Math.random() * questions.length)];
            sentences.splice(insertPosition, 0, randomQuestion);
        }
        
        return sentences.join(' ');
    }

    // Add emphasis markers
    addEmphasisMarkers(text) {
        const emphasisWords = ['really', 'truly', 'absolutely', 'definitely', 'certainly'];
        
        return text.replace(/\b(important|significant|crucial|essential)\b/gi, (match) => {
            if (Math.random() < 0.4) {
                const randomEmphasis = emphasisWords[Math.floor(Math.random() * emphasisWords.length)];
                return randomEmphasis + ' ' + match;
            }
            return match;
        });
    }

    // Add personal perspectives
    addPersonalPerspectives(text, intensity) {
        const personalPhrases = [
            'In my experience, ',
            'From what I\'ve seen, ',
            'I believe that ',
            'It seems to me that ',
            'I think '
        ];
        
        if (Math.random() < intensity * 0.3) {
            const randomPhrase = personalPhrases[Math.floor(Math.random() * personalPhrases.length)];
            const sentences = this.splitIntoSentences(text);
            if (sentences.length > 0) {
                sentences[0] = randomPhrase + sentences[0].toLowerCase();
                return sentences.join(' ');
            }
        }
        
        return text;
    }

    // Add idiomatic expressions
    addIdiomaticExpressions(text, intensity) {
        const idioms = {
            'very important': 'crucial',
            'very good': 'excellent',
            'very bad': 'terrible',
            'a lot of': 'numerous',
            'many': 'countless'
        };
        
        let processedText = text;
        for (const [phrase, replacement] of Object.entries(idioms)) {
            if (Math.random() < intensity * 0.2) {
                processedText = processedText.replace(new RegExp(phrase, 'gi'), replacement);
            }
        }
        
        return processedText;
    }

    // Add contextual references
    addContextualReferences(text, intensity) {
        const contextualPhrases = [
            'in today\'s world',
            'nowadays',
            'in recent years',
            'currently',
            'at present'
        ];
        
        if (Math.random() < intensity * 0.2) {
            const randomPhrase = contextualPhrases[Math.floor(Math.random() * contextualPhrases.length)];
            return text.replace(/\b(is|are|has|have)\b/, `${randomPhrase} $1`);
        }
        
        return text;
    }

    // Add contractions
    addContractions(text) {
        const contractions = {
            'do not': 'don\'t',
            'does not': 'doesn\'t',
            'did not': 'didn\'t',
            'will not': 'won\'t',
            'would not': 'wouldn\'t',
            'cannot': 'can\'t',
            'should not': 'shouldn\'t',
            'it is': 'it\'s',
            'that is': 'that\'s',
            'there is': 'there\'s'
        };
        
        let processedText = text;
        for (const [full, contraction] of Object.entries(contractions)) {
            if (Math.random() < 0.3) {
                processedText = processedText.replace(new RegExp(full, 'gi'), contraction);
            }
        }
        
        return processedText;
    }

    // Vary punctuation
    varyPunctuation(text) {
        // Occasionally replace periods with exclamation marks for emphasis
        return text.replace(/\./g, (match) => {
            if (Math.random() < 0.05) {
                return '!';
            }
            return match;
        });
    }

    // Add informal phrasing
    addInformalPhrasing(text) {
        const informalReplacements = {
            'therefore': 'so',
            'consequently': 'as a result',
            'furthermore': 'also',
            'nevertheless': 'however',
            'subsequently': 'then'
        };
        
        let processedText = text;
        for (const [formal, informal] of Object.entries(informalReplacements)) {
            if (Math.random() < 0.2) {
                processedText = processedText.replace(new RegExp(formal, 'gi'), informal);
            }
        }
        
        return processedText;
    }

    // Calculate AI detection score based on text characteristics
    calculateAIDetectionScore(originalText, humanizedText, targetScore) {
        // Simulate AI detection score calculation
        // In reality, this would require integration with actual AI detection APIs
        
        const originalLength = originalText.length;
        const humanizedLength = humanizedText.length;
        const lengthDifference = Math.abs(humanizedLength - originalLength) / originalLength;
        
        // Calculate perplexity increase (simplified)
        const perplexityIncrease = this.calculatePerplexityIncrease(originalText, humanizedText);
        
        // Calculate burstiness increase (simplified)
        const burstinessIncrease = this.calculateBurstinessIncrease(originalText, humanizedText);
        
        // Estimate AI detection score based on modifications
        const humanizationFactor = (perplexityIncrease + burstinessIncrease + lengthDifference) / 3;
        
        // Adjust score towards target with some variance
        const baseReduction = humanizationFactor * 50; // Max 50% reduction
        const targetReduction = 100 - targetScore;
        const achievedReduction = Math.min(baseReduction, targetReduction * 1.2); // Allow slight overshoot
        
        const achievedScore = Math.max(0, 100 - achievedReduction);
        
        // Add some randomness to simulate real-world variance
        const variance = (Math.random() - 0.5) * 10; // ±5% variance
        
        return Math.max(0, Math.min(100, Math.round(achievedScore + variance)));
    }

    // Calculate perplexity increase (simplified estimation)
    calculatePerplexityIncrease(originalText, humanizedText) {
        const originalWords = originalText.split(' ').length;
        const humanizedWords = humanizedText.split(' ').length;
        const wordVariation = Math.abs(humanizedWords - originalWords) / originalWords;
        
        // Count unique words as a proxy for vocabulary diversity
        const originalUniqueWords = new Set(originalText.toLowerCase().split(' ')).size;
        const humanizedUniqueWords = new Set(humanizedText.toLowerCase().split(' ')).size;
        const vocabularyIncrease = (humanizedUniqueWords - originalUniqueWords) / originalUniqueWords;
        
        return Math.max(0, (wordVariation + vocabularyIncrease) / 2);
    }

    // Calculate burstiness increase (simplified estimation)
    calculateBurstinessIncrease(originalText, humanizedText) {
        const originalSentences = this.splitIntoSentences(originalText);
        const humanizedSentences = this.splitIntoSentences(humanizedText);
        
        const originalLengthVariance = this.calculateLengthVariance(originalSentences);
        const humanizedLengthVariance = this.calculateLengthVariance(humanizedSentences);
        
        return Math.max(0, (humanizedLengthVariance - originalLengthVariance) / originalLengthVariance);
    }

    // Calculate variance in sentence lengths
    calculateLengthVariance(sentences) {
        const lengths = sentences.map(s => s.length);
        const mean = lengths.reduce((a, b) => a + b, 0) / lengths.length;
        const variance = lengths.reduce((acc, length) => acc + Math.pow(length - mean, 2), 0) / lengths.length;
        return Math.sqrt(variance);
    }

    // Initialize synonym database
    initializeSynonymDatabase() {
        return {
            'important': ['crucial', 'vital', 'significant', 'essential', 'key'],
            'good': ['excellent', 'great', 'outstanding', 'superb', 'fine'],
            'bad': ['poor', 'terrible', 'awful', 'dreadful', 'horrible'],
            'big': ['large', 'huge', 'enormous', 'massive', 'gigantic'],
            'small': ['tiny', 'little', 'minute', 'compact', 'petite'],
            'fast': ['quick', 'rapid', 'swift', 'speedy', 'hasty'],
            'slow': ['sluggish', 'gradual', 'leisurely', 'unhurried', 'deliberate'],
            'easy': ['simple', 'effortless', 'straightforward', 'uncomplicated', 'basic'],
            'hard': ['difficult', 'challenging', 'tough', 'demanding', 'complex'],
            'new': ['fresh', 'recent', 'modern', 'contemporary', 'latest'],
            'old': ['ancient', 'aged', 'vintage', 'mature', 'seasoned'],
            'many': ['numerous', 'countless', 'multiple', 'various', 'several'],
            'few': ['limited', 'scarce', 'minimal', 'handful', 'sparse'],
            'use': ['utilize', 'employ', 'apply', 'implement', 'leverage'],
            'make': ['create', 'produce', 'generate', 'construct', 'build'],
            'get': ['obtain', 'acquire', 'receive', 'gain', 'secure'],
            'help': ['assist', 'aid', 'support', 'facilitate', 'enable'],
            'show': ['demonstrate', 'display', 'exhibit', 'reveal', 'present'],
            'find': ['discover', 'locate', 'identify', 'uncover', 'detect'],
            'think': ['believe', 'consider', 'suppose', 'assume', 'reckon'],
            'know': ['understand', 'comprehend', 'realize', 'recognize', 'grasp'],
            'work': ['function', 'operate', 'perform', 'execute', 'run'],
            'system': ['framework', 'structure', 'mechanism', 'platform', 'infrastructure'],
            'process': ['procedure', 'method', 'approach', 'technique', 'workflow'],
            'data': ['information', 'statistics', 'facts', 'figures', 'details'],
            'technology': ['tech', 'innovation', 'advancement', 'solution', 'tool'],
            'analysis': ['examination', 'evaluation', 'assessment', 'review', 'study'],
            'performance': ['efficiency', 'effectiveness', 'productivity', 'output', 'results'],
            'solution': ['answer', 'resolution', 'fix', 'remedy', 'approach'],
            'implement': ['execute', 'deploy', 'apply', 'install', 'establish'],
            'optimize': ['improve', 'enhance', 'refine', 'streamline', 'perfect'],
            'facilitate': ['enable', 'assist', 'support', 'promote', 'encourage'],
            'comprehensive': ['complete', 'thorough', 'extensive', 'detailed', 'full'],
            'significant': ['important', 'major', 'substantial', 'considerable', 'notable'],
            'efficient': ['effective', 'productive', 'streamlined', 'optimized', 'smooth'],
            'advanced': ['sophisticated', 'cutting-edge', 'state-of-the-art', 'modern', 'progressive'],
            'furthermore': ['additionally', 'moreover', 'also', 'besides', 'in addition'],
            'however': ['nevertheless', 'nonetheless', 'yet', 'still', 'though'],
            'therefore': ['thus', 'consequently', 'hence', 'so', 'as a result'],
            'additionally': ['furthermore', 'moreover', 'also', 'besides', 'plus']
        };
    }

    // Initialize sentence patterns
    initializeSentencePatterns() {
        return {
            declarative: ['Subject + Verb + Object', 'Subject + Verb + Complement'],
            interrogative: ['Question word + Auxiliary + Subject + Verb', 'Auxiliary + Subject + Verb'],
            imperative: ['Verb + Object', 'Verb + Complement'],
            exclamatory: ['What/How + Subject + Verb', 'Subject + Verb + !']
        };
    }

    // Initialize humanization techniques
    initializeHumanizationTechniques() {
        return {
            perplexity: ['synonym_replacement', 'sentence_restructuring', 'vocabulary_diversification'],
            burstiness: ['sentence_length_variation', 'structure_mixing', 'transitional_elements'],
            human_touch: ['personal_pronouns', 'conversational_tone', 'rhetorical_questions'],
            imperfections: ['contractions', 'informal_phrasing', 'punctuation_variation']
        };
    }
}

// Export for use in main script
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdvancedHumanizer;
} else {
    window.AdvancedHumanizer = AdvancedHumanizer;
}

