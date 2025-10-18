"""
Emotion Fusion
Combines multi-modal emotion analysis results for comprehensive assessment
"""

import logging
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class EmotionFusion:
    """Fuses multi-modal emotion analysis results"""
    
    def __init__(self):
        # Weights for different modalities
        self.weights = {
            'text': 0.35,
            'facial': 0.40,
            'speech': 0.25
        }
        
        # Emotion mapping for consistency
        self.emotion_map = {
            'angry': 'anger',
            'fearful': 'fear',
            'calm': 'neutral',
            'sad': 'sadness',
            'happy': 'happiness',
            'surprised': 'surprise',
            'surprise': 'surprise',
            'neutral': 'neutral',
            'disgust': 'disgust',
            'fear': 'fear',
            'joy': 'happiness'
        }
        
        logger.info("Emotion fusion initialized")
    
    def fuse_emotions(self, 
                      text_result: Optional[Dict] = None,
                      facial_result: Optional[Dict] = None,
                      speech_result: Optional[Dict] = None) -> Dict:
        """Fuse emotion results from multiple modalities"""
        
        available_modalities = []
        emotion_scores = {}
        stress_scores = []
        confidences = []
        
        # Process text emotions
        if text_result and text_result.get('primary_emotion'):
            available_modalities.append('text')
            text_emotion = self._normalize_emotion(text_result['primary_emotion'])
            emotion_scores[text_emotion] = emotion_scores.get(text_emotion, 0) + \
                                          self.weights['text'] * text_result.get('emotion_confidence', 0.5)
            stress_scores.append(text_result['stress_indicators']['overall_stress_score'])
            confidences.append(text_result.get('emotion_confidence', 0.5))
        
        # Process facial emotions
        if facial_result and facial_result.get('face_detected'):
            available_modalities.append('facial')
            facial_emotion = self._normalize_emotion(facial_result['dominant_emotion'])
            emotion_scores[facial_emotion] = emotion_scores.get(facial_emotion, 0) + \
                                            self.weights['facial'] * facial_result.get('confidence', 0.5)
            stress_scores.append(facial_result['stress_indicators']['facial_stress_score'])
            confidences.append(facial_result.get('confidence', 0.5))
        
        # Process speech emotions
        if speech_result and speech_result.get('dominant_emotion'):
            available_modalities.append('speech')
            speech_emotion = self._normalize_emotion(speech_result['dominant_emotion'])
            emotion_scores[speech_emotion] = emotion_scores.get(speech_emotion, 0) + \
                                            self.weights['speech'] * speech_result.get('confidence', 0.5)
            stress_scores.append(speech_result['stress_indicators']['speech_stress_score'])
            confidences.append(speech_result.get('confidence', 0.5))
        
        if not emotion_scores:
            return self._default_fusion_result()
        
        # Determine dominant emotion
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        
        # Calculate overall metrics
        overall_stress = np.mean(stress_scores) if stress_scores else 0.0
        overall_confidence = np.mean(confidences) if confidences else 0.0
        
        # Calculate emotion consistency across modalities
        consistency_score = self._calculate_consistency(
            text_result, facial_result, speech_result
        )
        
        # Detect burnout risk
        burnout_risk = self._assess_burnout_risk(
            overall_stress, emotion_scores, text_result
        )
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'dominant_emotion': dominant_emotion,
            'emotion_scores': emotion_scores,
            'confidence': overall_confidence,
            'available_modalities': available_modalities,
            'modality_count': len(available_modalities),
            'stress_assessment': {
                'overall_stress_score': overall_stress,
                'stress_level': self._categorize_stress_level(overall_stress),
                'burnout_risk': burnout_risk,
                'intervention_needed': burnout_risk['risk_level'] in ['high', 'critical']
            },
            'consistency_score': consistency_score,
            'detailed_results': {
                'text': text_result,
                'facial': facial_result,
                'speech': speech_result
            }
        }
        
        return result
    
    def _normalize_emotion(self, emotion: str) -> str:
        """Normalize emotion labels across different modalities"""
        emotion_lower = emotion.lower()
        return self.emotion_map.get(emotion_lower, emotion_lower)
    
    def _calculate_consistency(self, 
                               text_result: Optional[Dict],
                               facial_result: Optional[Dict],
                               speech_result: Optional[Dict]) -> float:
        """Calculate consistency score across modalities"""
        emotions = []
        
        if text_result and text_result.get('primary_emotion'):
            emotions.append(self._normalize_emotion(text_result['primary_emotion']))
        
        if facial_result and facial_result.get('face_detected'):
            emotions.append(self._normalize_emotion(facial_result['dominant_emotion']))
        
        if speech_result and speech_result.get('dominant_emotion'):
            emotions.append(self._normalize_emotion(speech_result['dominant_emotion']))
        
        if len(emotions) < 2:
            return 1.0  # High consistency if only one modality
        
        # Check if all emotions are the same
        if len(set(emotions)) == 1:
            return 1.0
        
        # Calculate agreement ratio
        most_common = max(set(emotions), key=emotions.count)
        agreement_ratio = emotions.count(most_common) / len(emotions)
        
        return agreement_ratio
    
    def _assess_burnout_risk(self, 
                            stress_score: float, 
                            emotions: Dict,
                            text_result: Optional[Dict]) -> Dict:
        """Assess burnout risk based on stress and emotion patterns"""
        
        risk_factors = []
        risk_score = 0.0
        
        # High stress is a major risk factor
        if stress_score >= 0.7:
            risk_factors.append('High stress levels detected')
            risk_score += 0.4
        elif stress_score >= 0.5:
            risk_factors.append('Elevated stress levels')
            risk_score += 0.2
        
        # Negative emotions indicate risk
        negative_emotions = ['anger', 'sadness', 'fear', 'disgust']
        negative_emotion_score = sum(emotions.get(e, 0) for e in negative_emotions)
        
        if negative_emotion_score > 0.5:
            risk_factors.append('Predominant negative emotions')
            risk_score += 0.3
        
        # Check text indicators if available
        if text_result:
            stress_indicators = text_result.get('stress_indicators', {})
            if stress_indicators.get('high_stress', 0) > 2:
                risk_factors.append('Multiple stress keywords detected in communication')
                risk_score += 0.2
        
        # Determine risk level
        if risk_score >= 0.7:
            risk_level = 'critical'
        elif risk_score >= 0.5:
            risk_level = 'high'
        elif risk_score >= 0.3:
            risk_level = 'moderate'
        elif risk_score >= 0.15:
            risk_level = 'low'
        else:
            risk_level = 'minimal'
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'recommendation': self._get_burnout_recommendation(risk_level)
        }
    
    def _get_burnout_recommendation(self, risk_level: str) -> str:
        """Get recommendation based on burnout risk level"""
        recommendations = {
            'critical': 'Immediate HR intervention required. Consider temporary workload reduction and professional support.',
            'high': 'Schedule check-in with manager and HR. Recommend stress management resources.',
            'moderate': 'Monitor closely. Suggest wellness activities and flexible scheduling.',
            'low': 'Continue regular check-ins. Encourage work-life balance.',
            'minimal': 'Employee wellbeing appears healthy. Maintain current support.'
        }
        return recommendations.get(risk_level, 'Monitor employee wellbeing.')
    
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
    
    def _default_fusion_result(self) -> Dict:
        """Return default fusion result"""
        return {
            'timestamp': datetime.now().isoformat(),
            'dominant_emotion': 'neutral',
            'emotion_scores': {'neutral': 1.0},
            'confidence': 0.0,
            'available_modalities': [],
            'modality_count': 0,
            'stress_assessment': {
                'overall_stress_score': 0.0,
                'stress_level': 'minimal',
                'burnout_risk': {
                    'risk_level': 'minimal',
                    'risk_score': 0.0,
                    'risk_factors': [],
                    'recommendation': 'Insufficient data for assessment.'
                },
                'intervention_needed': False
            },
            'consistency_score': 0.0,
            'detailed_results': {
                'text': None,
                'facial': None,
                'speech': None
            }
        }
    
    def batch_fuse(self, results_list: List[Dict]) -> List[Dict]:
        """Fuse multiple sets of emotion results"""
        return [
            self.fuse_emotions(
                r.get('text'),
                r.get('facial'),
                r.get('speech')
            )
            for r in results_list
        ]
    
    def analyze_temporal_patterns(self, fused_results: List[Dict]) -> Dict:
        """Analyze temporal patterns in fused emotion data"""
        if not fused_results:
            return {}
        
        stress_scores = [r['stress_assessment']['overall_stress_score'] for r in fused_results]
        emotions = [r['dominant_emotion'] for r in fused_results]
        burnout_risks = [r['stress_assessment']['burnout_risk']['risk_level'] for r in fused_results]
        
        return {
            'time_period': f"{len(fused_results)} analyses",
            'average_stress': np.mean(stress_scores),
            'stress_trend': self._calculate_trend(stress_scores),
            'dominant_emotion': max(set(emotions), key=emotions.count),
            'emotion_variability': len(set(emotions)) / len(emotions),
            'burnout_risk_history': {
                risk: burnout_risks.count(risk) / len(burnout_risks)
                for risk in set(burnout_risks)
            },
            'intervention_frequency': sum(
                1 for r in fused_results 
                if r['stress_assessment']['intervention_needed']
            ) / len(fused_results)
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction"""
        if len(values) < 2:
            return 'stable'
        
        # Simple linear trend
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.05:
            return 'increasing'
        elif slope < -0.05:
            return 'decreasing'
        else:
            return 'stable'
