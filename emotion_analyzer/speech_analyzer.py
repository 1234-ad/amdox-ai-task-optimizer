"""
Speech Emotion Analyzer
Analyzes emotions from speech/audio using acoustic features
"""

import logging
import numpy as np
import librosa
import soundfile as sf
from typing import Dict, List, Optional
from transformers import pipeline
import warnings

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class SpeechEmotionAnalyzer:
    """Analyzes emotions from speech and audio"""
    
    def __init__(self):
        self.sample_rate = 16000
        self.emotion_labels = ['angry', 'calm', 'fearful', 'happy', 'sad', 'surprised', 'neutral']
        self.load_models()
        logger.info("Speech emotion analyzer initialized")
    
    def load_models(self):
        """Load speech emotion recognition models"""
        try:
            # Load audio classification model
            self.audio_classifier = pipeline(
                "audio-classification",
                model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition",
                device=-1
            )
            logger.info("Speech emotion models loaded successfully")
        except Exception as e:
            logger.error(f"Error loading speech models: {e}")
            self.audio_classifier = None
    
    def analyze_audio(self, audio_path: str) -> Dict:
        """Analyze emotions from an audio file"""
        try:
            # Load audio file
            audio, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Extract acoustic features
            features = self._extract_acoustic_features(audio, sr)
            
            # Analyze emotion using model
            if self.audio_classifier:
                emotion_result = self.audio_classifier(audio_path)
                emotions = {e['label'].lower(): e['score'] for e in emotion_result}
                dominant_emotion = emotion_result[0]['label'].lower()
                confidence = emotion_result[0]['score']
            else:
                emotions = {'neutral': 1.0}
                dominant_emotion = 'neutral'
                confidence = 0.5
            
            # Calculate stress indicators
            stress_score = self._calculate_speech_stress(features, emotions)
            
            result = {
                'dominant_emotion': dominant_emotion,
                'emotions': emotions,
                'confidence': confidence,
                'acoustic_features': features,
                'stress_indicators': {
                    'speech_stress_score': stress_score,
                    'stress_level': self._categorize_stress_level(stress_score),
                    'voice_intensity': features['energy_mean'],
                    'pitch_variation': features['pitch_std']
                },
                'audio_duration': len(audio) / sr
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing audio emotion: {e}")
            return self._default_speech_result()
    
    def _extract_acoustic_features(self, audio: np.ndarray, sr: int) -> Dict:
        """Extract acoustic features from audio signal"""
        features = {}
        
        try:
            # Energy/Intensity
            energy = librosa.feature.rms(y=audio)[0]
            features['energy_mean'] = float(np.mean(energy))
            features['energy_std'] = float(np.std(energy))
            
            # Pitch (F0)
            pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            if pitch_values:
                features['pitch_mean'] = float(np.mean(pitch_values))
                features['pitch_std'] = float(np.std(pitch_values))
            else:
                features['pitch_mean'] = 0.0
                features['pitch_std'] = 0.0
            
            # Zero Crossing Rate
            zcr = librosa.feature.zero_crossing_rate(audio)[0]
            features['zcr_mean'] = float(np.mean(zcr))
            features['zcr_std'] = float(np.std(zcr))
            
            # Spectral features
            spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
            features['spectral_centroid_mean'] = float(np.mean(spectral_centroid))
            
            # MFCCs
            mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
            for i in range(min(5, mfccs.shape[0])):
                features[f'mfcc_{i}_mean'] = float(np.mean(mfccs[i]))
            
            # Tempo
            tempo, _ = librosa.beat.beat_track(y=audio, sr=sr)
            features['tempo'] = float(tempo)
            
        except Exception as e:
            logger.error(f"Error extracting acoustic features: {e}")
        
        return features
    
    def _calculate_speech_stress(self, features: Dict, emotions: Dict) -> float:
        """Calculate stress score from speech characteristics"""
        stress_score = 0.0
        
        # Emotion-based stress
        emotion_weights = {
            'angry': 0.9,
            'fearful': 0.8,
            'sad': 0.6,
            'surprised': 0.4,
            'calm': -0.3,
            'happy': -0.2,
            'neutral': 0.0
        }
        
        for emotion, value in emotions.items():
            if emotion in emotion_weights:
                stress_score += value * emotion_weights[emotion]
        
        # Acoustic feature-based stress
        # High energy can indicate stress
        if 'energy_mean' in features:
            energy_norm = min(features['energy_mean'] / 0.5, 1.0)
            stress_score += energy_norm * 0.2
        
        # High pitch variation can indicate stress
        if 'pitch_std' in features:
            pitch_var_norm = min(features['pitch_std'] / 100.0, 1.0)
            stress_score += pitch_var_norm * 0.15
        
        # Normalize to 0-1 range
        stress_score = max(0.0, min(1.0, stress_score))
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
    
    def _default_speech_result(self) -> Dict:
        """Return default speech analysis result"""
        return {
            'dominant_emotion': 'neutral',
            'emotions': {'neutral': 1.0},
            'confidence': 0.0,
            'acoustic_features': {},
            'stress_indicators': {
                'speech_stress_score': 0.0,
                'stress_level': 'minimal',
                'voice_intensity': 0.0,
                'pitch_variation': 0.0
            },
            'audio_duration': 0.0
        }
    
    def batch_analyze(self, audio_paths: List[str]) -> List[Dict]:
        """Analyze emotions for multiple audio files"""
        return [self.analyze_audio(path) for path in audio_paths]
    
    def analyze_real_time(self, audio_stream: np.ndarray, sr: int) -> Dict:
        """Analyze emotions from real-time audio stream"""
        try:
            features = self._extract_acoustic_features(audio_stream, sr)
            stress_score = self._calculate_speech_stress(features, {'neutral': 1.0})
            
            return {
                'acoustic_features': features,
                'stress_indicators': {
                    'speech_stress_score': stress_score,
                    'stress_level': self._categorize_stress_level(stress_score),
                    'voice_intensity': features.get('energy_mean', 0.0),
                    'pitch_variation': features.get('pitch_std', 0.0)
                }
            }
        except Exception as e:
            logger.error(f"Error in real-time analysis: {e}")
            return self._default_speech_result()
    
    def get_emotion_trends(self, analyses: List[Dict]) -> Dict:
        """Analyze speech emotion trends"""
        if not analyses:
            return {}
        
        emotions = [a['dominant_emotion'] for a in analyses]
        stress_scores = [a['stress_indicators']['speech_stress_score'] for a in analyses]
        
        return {
            'dominant_emotion': max(set(emotions), key=emotions.count),
            'emotion_distribution': {emotion: emotions.count(emotion) / len(emotions) 
                                   for emotion in set(emotions)},
            'average_stress_score': np.mean(stress_scores),
            'max_stress_score': np.max(stress_scores),
            'stress_trend': 'increasing' if len(stress_scores) > 1 and 
                           stress_scores[-1] > stress_scores[0] else 'stable',
            'average_voice_intensity': np.mean([a['stress_indicators']['voice_intensity'] 
                                               for a in analyses]),
            'total_analyses': len(analyses)
        }
