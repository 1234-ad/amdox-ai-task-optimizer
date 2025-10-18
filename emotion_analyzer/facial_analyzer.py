"""
Facial Emotion Analyzer
Analyzes emotions from facial expressions using computer vision
"""

import logging
import cv2
import numpy as np
from typing import Dict, List, Optional
import mediapipe as mp
from deepface import DeepFace

logger = logging.getLogger(__name__)

class FacialEmotionAnalyzer:
    """Analyzes emotions from facial expressions"""
    
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            min_detection_confidence=0.5
        )
        self.emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        logger.info("Facial emotion analyzer initialized")
    
    def analyze_image(self, image_path: str) -> Dict:
        """Analyze emotions from a facial image"""
        try:
            # Use DeepFace for emotion analysis
            analysis = DeepFace.analyze(
                img_path=image_path,
                actions=['emotion'],
                enforce_detection=False
            )
            
            if isinstance(analysis, list):
                analysis = analysis[0]
            
            emotions = analysis.get('emotion', {})
            dominant_emotion = analysis.get('dominant_emotion', 'neutral')
            
            # Calculate stress indicators from facial expressions
            stress_score = self._calculate_facial_stress(emotions)
            
            result = {
                'dominant_emotion': dominant_emotion.lower(),
                'emotions': {k.lower(): v for k, v in emotions.items()},
                'confidence': emotions.get(dominant_emotion, 0) / 100.0,
                'stress_indicators': {
                    'facial_stress_score': stress_score,
                    'stress_level': self._categorize_stress_level(stress_score)
                },
                'face_detected': True
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing facial emotion: {e}")
            return self._default_facial_result()
    
    def analyze_frame(self, frame: np.ndarray) -> Dict:
        """Analyze emotions from a video frame"""
        try:
            # Convert frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect face
            results = self.face_mesh.process(rgb_frame)
            
            if not results.multi_face_landmarks:
                return self._default_facial_result()
            
            # Analyze emotion using DeepFace
            analysis = DeepFace.analyze(
                img_path=rgb_frame,
                actions=['emotion'],
                enforce_detection=False
            )
            
            if isinstance(analysis, list):
                analysis = analysis[0]
            
            emotions = analysis.get('emotion', {})
            dominant_emotion = analysis.get('dominant_emotion', 'neutral')
            
            stress_score = self._calculate_facial_stress(emotions)
            
            result = {
                'dominant_emotion': dominant_emotion.lower(),
                'emotions': {k.lower(): v for k, v in emotions.items()},
                'confidence': emotions.get(dominant_emotion, 0) / 100.0,
                'stress_indicators': {
                    'facial_stress_score': stress_score,
                    'stress_level': self._categorize_stress_level(stress_score)
                },
                'face_detected': True
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing frame: {e}")
            return self._default_facial_result()
    
    def _calculate_facial_stress(self, emotions: Dict) -> float:
        """Calculate stress score from facial emotions"""
        stress_weights = {
            'angry': 0.9,
            'fear': 0.8,
            'disgust': 0.7,
            'sad': 0.6,
            'surprise': 0.3,
            'happy': -0.5,
            'neutral': 0.0
        }
        
        total_score = 0.0
        for emotion, value in emotions.items():
            emotion_lower = emotion.lower()
            if emotion_lower in stress_weights:
                total_score += (value / 100.0) * stress_weights[emotion_lower]
        
        # Normalize to 0-1 range
        stress_score = max(0.0, min(1.0, (total_score + 0.5) / 1.5))
        return stress_score
    
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
    
    def _default_facial_result(self) -> Dict:
        """Return default facial analysis result"""
        return {
            'dominant_emotion': 'neutral',
            'emotions': {'neutral': 1.0},
            'confidence': 0.0,
            'stress_indicators': {
                'facial_stress_score': 0.0,
                'stress_level': 'minimal'
            },
            'face_detected': False
        }
    
    def batch_analyze_images(self, image_paths: List[str]) -> List[Dict]:
        """Analyze emotions for multiple images"""
        return [self.analyze_image(path) for path in image_paths]
    
    def analyze_video(self, video_path: str, sample_rate: int = 30) -> List[Dict]:
        """Analyze emotions from a video file"""
        results = []
        
        try:
            cap = cv2.VideoCapture(video_path)
            frame_count = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Analyze every nth frame
                if frame_count % sample_rate == 0:
                    result = self.analyze_frame(frame)
                    result['frame_number'] = frame_count
                    results.append(result)
                
                frame_count += 1
            
            cap.release()
            
        except Exception as e:
            logger.error(f"Error analyzing video: {e}")
        
        return results
    
    def get_emotion_trends(self, analyses: List[Dict]) -> Dict:
        """Analyze facial emotion trends"""
        if not analyses:
            return {}
        
        valid_analyses = [a for a in analyses if a['face_detected']]
        
        if not valid_analyses:
            return {'error': 'No faces detected'}
        
        emotions = [a['dominant_emotion'] for a in valid_analyses]
        stress_scores = [a['stress_indicators']['facial_stress_score'] for a in valid_analyses]
        
        return {
            'dominant_emotion': max(set(emotions), key=emotions.count),
            'emotion_distribution': {emotion: emotions.count(emotion) / len(emotions) 
                                   for emotion in set(emotions)},
            'average_stress_score': np.mean(stress_scores),
            'max_stress_score': np.max(stress_scores),
            'stress_trend': 'increasing' if len(stress_scores) > 1 and 
                           stress_scores[-1] > stress_scores[0] else 'stable',
            'total_analyses': len(valid_analyses),
            'face_detection_rate': len(valid_analyses) / len(analyses)
        }
