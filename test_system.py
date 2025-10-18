"""
Test Suite for Amdox AI Task Optimizer
Run with: pytest test_system.py
"""

import pytest
from emotion_analyzer.text_analyzer import TextEmotionAnalyzer
from emotion_analyzer.emotion_fusion import EmotionFusion
from task_optimizer.recommendation_engine import TaskRecommendationEngine
from task_optimizer.task_matcher import TaskMatcher
from alert_system.monitor import AlertMonitor

class TestTextEmotionAnalyzer:
    """Test text emotion analysis"""
    
    def setup_method(self):
        self.analyzer = TextEmotionAnalyzer()
    
    def test_happy_emotion(self):
        result = self.analyzer.analyze_emotion("I am so happy and excited!")
        assert result['primary_emotion'] in ['happiness', 'joy', 'happy']
        assert result['emotion_confidence'] > 0.3
    
    def test_stressed_emotion(self):
        result = self.analyzer.analyze_emotion("I am overwhelmed and stressed with deadlines")
        assert result['stress_indicators']['overall_stress_score'] > 0.3
        assert result['stress_indicators']['stress_level'] in ['moderate', 'high']
    
    def test_empty_text(self):
        result = self.analyzer.analyze_emotion("")
        assert result['primary_emotion'] == 'neutral'

class TestEmotionFusion:
    """Test emotion fusion"""
    
    def setup_method(self):
        self.fusion = EmotionFusion()
    
    def test_text_only_fusion(self):
        text_result = {
            'primary_emotion': 'happiness',
            'emotion_confidence': 0.8,
            'stress_indicators': {'overall_stress_score': 0.2}
        }
        result = self.fusion.fuse_emotions(text_result=text_result)
        assert 'dominant_emotion' in result
        assert 'stress_assessment' in result
        assert result['modality_count'] == 1
    
    def test_burnout_risk_detection(self):
        text_result = {
            'primary_emotion': 'sadness',
            'emotion_confidence': 0.9,
            'stress_indicators': {'overall_stress_score': 0.85, 'high_stress': 5}
        }
        result = self.fusion.fuse_emotions(text_result=text_result)
        assert result['stress_assessment']['burnout_risk']['risk_level'] in ['high', 'critical']
        assert result['stress_assessment']['intervention_needed'] == True

class TestTaskRecommendationEngine:
    """Test task recommendation"""
    
    def setup_method(self):
        self.engine = TaskRecommendationEngine()
    
    def test_recommend_for_happy_state(self):
        employee_state = {
            'dominant_emotion': 'happiness',
            'stress_assessment': {
                'overall_stress_score': 0.2,
                'burnout_risk': {'risk_level': 'minimal'}
            }
        }
        tasks = [
            {'task_id': '1', 'name': 'Creative Design', 'category': 'creative', 
             'priority': 'high', 'complexity': 'medium', 'estimated_hours': 4},
            {'task_id': '2', 'name': 'Data Entry', 'category': 'routine',
             'priority': 'low', 'complexity': 'low', 'estimated_hours': 2}
        ]
        
        recommendations = self.engine.recommend_tasks(employee_state, tasks, limit=2)
        assert len(recommendations) > 0
        assert recommendations[0]['match_score'] > 0.3
    
    def test_recommend_for_stressed_state(self):
        employee_state = {
            'dominant_emotion': 'sadness',
            'stress_assessment': {
                'overall_stress_score': 0.8,
                'burnout_risk': {'risk_level': 'high'}
            }
        }
        tasks = [
            {'task_id': '1', 'name': 'Complex Analysis', 'category': 'analytical',
             'priority': 'high', 'complexity': 'high', 'estimated_hours': 8},
            {'task_id': '2', 'name': 'Simple Admin', 'category': 'administrative',
             'priority': 'low', 'complexity': 'low', 'estimated_hours': 1}
        ]
        
        recommendations = self.engine.recommend_tasks(employee_state, tasks, limit=2)
        # Should recommend simpler tasks during high stress
        assert any(r['task']['category'] in ['routine', 'administrative'] 
                  for r in recommendations)

class TestTaskMatcher:
    """Test task-employee matching"""
    
    def setup_method(self):
        self.matcher = TaskMatcher()
    
    def test_skill_matching(self):
        task = {
            'name': 'Python Development',
            'category': 'analytical',
            'required_skills': ['Python', 'Flask'],
            'complexity': 'medium'
        }
        employees = [
            {
                'employee_id': 'E1',
                'name': 'John',
                'skills': ['Python', 'Flask', 'React'],
                'experience_years': 5,
                'performance_rating': 0.9,
                'available': True,
                'current_emotional_state': {
                    'dominant_emotion': 'neutral',
                    'stress_assessment': {'overall_stress_score': 0.3,
                                        'burnout_risk': {'risk_level': 'minimal'}}
                }
            }
        ]
        
        matches = self.matcher.match_task_to_employees(task, employees, limit=1)
        assert len(matches) > 0
        assert matches[0]['match_score'] > 0.5

class TestAlertMonitor:
    """Test alert monitoring"""
    
    def setup_method(self):
        self.monitor = AlertMonitor()
    
    def test_critical_stress_alert(self):
        emotional_state = {
            'dominant_emotion': 'anger',
            'stress_assessment': {
                'overall_stress_score': 0.9,
                'burnout_risk': {
                    'risk_level': 'critical',
                    'risk_score': 0.85,
                    'recommendation': 'Immediate intervention'
                }
            }
        }
        
        alert = self.monitor.monitor_employee('EMP001', emotional_state)
        assert alert is not None
        assert alert['severity'] in ['critical', 'high']
        assert alert['employee_id'] == 'EMP001'
    
    def test_no_alert_for_healthy_state(self):
        emotional_state = {
            'dominant_emotion': 'happiness',
            'stress_assessment': {
                'overall_stress_score': 0.2,
                'burnout_risk': {'risk_level': 'minimal'}
            }
        }
        
        alert = self.monitor.monitor_employee('EMP002', emotional_state)
        assert alert is None

def test_integration_flow():
    """Test complete integration flow"""
    # Analyze text
    analyzer = TextEmotionAnalyzer()
    text_result = analyzer.analyze_emotion("I'm feeling stressed about the deadline")
    
    # Fuse emotions
    fusion = EmotionFusion()
    fused_result = fusion.fuse_emotions(text_result=text_result)
    
    # Check for alerts
    monitor = AlertMonitor()
    alert = monitor.monitor_employee('EMP_TEST', fused_result)
    
    # Get task recommendations
    recommender = TaskRecommendationEngine()
    tasks = [
        {'task_id': 'T1', 'name': 'Easy Task', 'category': 'routine',
         'priority': 'low', 'complexity': 'low', 'estimated_hours': 1}
    ]
    recommendations = recommender.recommend_tasks(fused_result, tasks)
    
    # Verify flow completed
    assert fused_result is not None
    assert recommendations is not None

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
