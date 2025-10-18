"""
Text Emotion Analyzer
Analyzes emotions from text inputs using NLP techniques
"""

import logging
import numpy as np
from typing import Dict, List, Tuple
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

logger = logging.getLogger(__name__)

class TextEmotionAnalyzer:
    """Analyzes emotions from text using multiple NLP models"""
    
    def __init__(self):
        self.setup_nltk()
        self.load_models()
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
    def setup_nltk(self):
        """Download required NLTK data"""
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('vader_lexicon', quiet=True)
        except Exception as e:
            logger.warning(f"NLTK setup warning: {e}")
    
    def load_models(self):
        """Load pre-trained emotion analysis models"""
        try:
            # Load emotion classification model
            self.emotion_classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                device=-1  # Use CPU
            )
            
            # Load stress detection model
            self.stress_classifier = pipeline(
                "text-classification",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=-1
            )
            
            logger.info("Text emotion models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self.emotion_classifier = None
            self.stress_classifier = None
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        if not text:
            return ""
        
        # Remove URLs, mentions, hashtags
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'@\w+|#\w+', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def analyze_emotion(self, text: str) -> Dict:
        """Analyze emotions in text"""
        if not text or not self.emotion_classifier:
            return self._default_emotion_result()
        
        try:
            preprocessed_text = self.preprocess_text(text)
            
            # Get emotion predictions
            emotions = self.emotion_classifier(preprocessed_text)
            
            # Get sentiment using VADER
            vader_scores = self.vader_analyzer.polarity_scores(preprocessed_text)
            
            # Get sentiment using TextBlob
            blob = TextBlob(preprocessed_text)
            textblob_sentiment = blob.sentiment
            
            # Combine results
            result = {
                'primary_emotion': emotions[0]['label'].lower(),
                'emotion_confidence': emotions[0]['score'],
                'all_emotions': {e['label'].lower(): e['score'] for e in emotions},
                'sentiment': {
                    'vader': vader_scores,
                    'textblob': {
                        'polarity': textblob_sentiment.polarity,
                        'subjectivity': textblob_sentiment.subjectivity
                    }
                },
                'stress_indicators': self._detect_stress_indicators(preprocessed_text),
                'text_length': len(preprocessed_text),
                'word_count': len(preprocessed_text.split())
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing emotion: {e}")
            return self._default_emotion_result()
    
    def _detect_stress_indicators(self, text: str) -> Dict:
        """Detect stress and burnout indicators in text"""
        stress_keywords = {
            'high_stress': ['overwhelmed', 'stressed', 'exhausted', 'burnout', 'pressure', 'deadline'],
            'moderate_stress': ['tired', 'busy', 'hectic', 'rush', 'urgent', 'demanding'],
            'negative_emotions': ['frustrated', 'angry', 'upset', 'disappointed', 'worried', 'anxious']
        }
        
        text_lower = text.lower()
        indicators = {}
        
        for category, keywords in stress_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            indicators[category] = count
        
        # Calculate overall stress score
        total_indicators = sum(indicators.values())
        stress_score = min(total_indicators / 10.0, 1.0)  # Normalize to 0-1
        
        indicators['overall_stress_score'] = stress_score
        indicators['stress_level'] = self._categorize_stress_level(stress_score)
        
        return indicators
    
    def _categorize_stress_level(self, score: float) -> str:
        """Categorize stress level based on score"""
        if score >= 0.7:
            return 'high'
        elif score >= 0.4:
            return 'moderate'
        elif score >= 0.2:
            return 'low'
        else:
            return 'minimal'
    
    def _default_emotion_result(self) -> Dict:
        """Return default emotion analysis result"""
        return {
            'primary_emotion': 'neutral',
            'emotion_confidence': 0.5,
            'all_emotions': {'neutral': 0.5},
            'sentiment': {
                'vader': {'compound': 0.0, 'pos': 0.0, 'neu': 1.0, 'neg': 0.0},
                'textblob': {'polarity': 0.0, 'subjectivity': 0.0}
            },
            'stress_indicators': {
                'high_stress': 0,
                'moderate_stress': 0,
                'negative_emotions': 0,
                'overall_stress_score': 0.0,
                'stress_level': 'minimal'
            },
            'text_length': 0,
            'word_count': 0
        }
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Analyze emotions for multiple texts"""
        return [self.analyze_emotion(text) for text in texts]
    
    def get_emotion_trends(self, analyses: List[Dict]) -> Dict:
        """Analyze emotion trends over time"""
        if not analyses:
            return {}
        
        emotions = [a['primary_emotion'] for a in analyses]
        stress_scores = [a['stress_indicators']['overall_stress_score'] for a in analyses]
        
        return {
            'dominant_emotion': max(set(emotions), key=emotions.count),
            'emotion_distribution': {emotion: emotions.count(emotion) / len(emotions) 
                                   for emotion in set(emotions)},
            'average_stress_score': np.mean(stress_scores),
            'stress_trend': 'increasing' if len(stress_scores) > 1 and 
                           stress_scores[-1] > stress_scores[0] else 'stable',
            'total_analyses': len(analyses)
        }