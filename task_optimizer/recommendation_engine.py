"""
Task Recommendation Engine
AI-powered task matching based on emotional state and skills
"""

import logging
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class TaskRecommendationEngine:
    """Recommends optimal tasks based on employee state"""
    
    def __init__(self):
        # Task categories and their emotional requirements
        self.task_profiles = {
            'creative': {
                'optimal_emotions': ['happiness', 'surprise', 'neutral'],
                'avoid_emotions': ['sadness', 'anger', 'fear'],
                'optimal_stress': (0.0, 0.3),
                'energy_required': 'high',
                'cognitive_load': 'high'
            },
            'analytical': {
                'optimal_emotions': ['neutral', 'happiness'],
                'avoid_emotions': ['anger', 'fear'],
                'optimal_stress': (0.0, 0.4),
                'energy_required': 'medium',
                'cognitive_load': 'high'
            },
            'routine': {
                'optimal_emotions': ['neutral', 'happiness', 'sadness'],
                'avoid_emotions': ['anger'],
                'optimal_stress': (0.0, 0.6),
                'energy_required': 'low',
                'cognitive_load': 'low'
            },
            'collaborative': {
                'optimal_emotions': ['happiness', 'neutral'],
                'avoid_emotions': ['anger', 'sadness', 'fear'],
                'optimal_stress': (0.0, 0.5),
                'energy_required': 'medium',
                'cognitive_load': 'medium'
            },
            'problem_solving': {
                'optimal_emotions': ['happiness', 'neutral', 'surprise'],
                'avoid_emotions': ['sadness', 'fear'],
                'optimal_stress': (0.0, 0.4),
                'energy_required': 'high',
                'cognitive_load': 'high'
            },
            'administrative': {
                'optimal_emotions': ['neutral', 'happiness'],
                'avoid_emotions': ['anger'],
                'optimal_stress': (0.0, 0.7),
                'energy_required': 'low',
                'cognitive_load': 'low'
            }
        }
        
        logger.info("Task recommendation engine initialized")
    
    def recommend_tasks(self, 
                       employee_state: Dict,
                       available_tasks: List[Dict],
                       limit: int = 5) -> List[Dict]:
        """
        Recommend optimal tasks based on employee's current emotional state
        
        Args:
            employee_state: Emotional state from emotion fusion
            available_tasks: List of available tasks with metadata
            limit: Maximum number of recommendations
        
        Returns:
            List of recommended tasks with match scores
        """
        
        if not available_tasks:
            return []
        
        dominant_emotion = employee_state.get('dominant_emotion', 'neutral')
        stress_level = employee_state.get('stress_assessment', {}).get('overall_stress_score', 0.0)
        burnout_risk = employee_state.get('stress_assessment', {}).get('burnout_risk', {}).get('risk_level', 'minimal')
        
        recommendations = []
        
        for task in available_tasks:
            match_score = self._calculate_task_match(
                task,
                dominant_emotion,
                stress_level,
                burnout_risk
            )
            
            if match_score > 0.3:  # Minimum threshold
                recommendations.append({
                    'task': task,
                    'match_score': match_score,
                    'reason': self._generate_recommendation_reason(
                        task, dominant_emotion, stress_level, match_score
                    ),
                    'estimated_completion_time': self._estimate_completion_time(
                        task, employee_state
                    ),
                    'priority_adjustment': self._calculate_priority_adjustment(
                        task, stress_level, burnout_risk
                    )
                })
        
        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        return recommendations[:limit]
    
    def _calculate_task_match(self,
                             task: Dict,
                             emotion: str,
                             stress: float,
                             burnout_risk: str) -> float:
        """Calculate how well a task matches current employee state"""
        
        task_category = task.get('category', 'routine')
        task_priority = task.get('priority', 'medium')
        task_complexity = task.get('complexity', 'medium')
        
        if task_category not in self.task_profiles:
            task_category = 'routine'
        
        profile = self.task_profiles[task_category]
        match_score = 0.5  # Base score
        
        # Emotion matching (40% weight)
        if emotion in profile['optimal_emotions']:
            match_score += 0.4
        elif emotion in profile['avoid_emotions']:
            match_score -= 0.3
        
        # Stress matching (30% weight)
        optimal_stress_min, optimal_stress_max = profile['optimal_stress']
        if optimal_stress_min <= stress <= optimal_stress_max:
            match_score += 0.3
        elif stress > optimal_stress_max:
            # Penalize based on how far outside range
            excess = stress - optimal_stress_max
            match_score -= 0.2 * (excess / 0.5)
        
        # Burnout risk adjustment (20% weight)
        if burnout_risk in ['high', 'critical']:
            if profile['cognitive_load'] == 'low':
                match_score += 0.2
            elif profile['cognitive_load'] == 'high':
                match_score -= 0.3
        
        # Task priority consideration (10% weight)
        if task_priority == 'high' and stress < 0.5:
            match_score += 0.1
        elif task_priority == 'high' and stress >= 0.7:
            match_score -= 0.1
        
        # Normalize to 0-1 range
        match_score = max(0.0, min(1.0, match_score))
        
        return match_score
    
    def _generate_recommendation_reason(self,
                                       task: Dict,
                                       emotion: str,
                                       stress: float,
                                       match_score: float) -> str:
        """Generate human-readable reason for recommendation"""
        
        task_category = task.get('category', 'routine')
        task_name = task.get('name', 'Task')
        
        if match_score >= 0.8:
            reason = f"Excellent match: Your current {emotion} state is ideal for {task_category} tasks. "
        elif match_score >= 0.6:
            reason = f"Good match: {task_name} aligns well with your current emotional state. "
        else:
            reason = f"Suitable: {task_name} can be completed effectively right now. "
        
        if stress < 0.3:
            reason += "Low stress levels support focused work."
        elif stress < 0.6:
            reason += "Moderate stress is manageable for this task."
        else:
            reason += "Task complexity adjusted for current stress level."
        
        return reason
    
    def _estimate_completion_time(self, task: Dict, employee_state: Dict) -> str:
        """Estimate task completion time based on employee state"""
        
        base_time = task.get('estimated_hours', 2.0)
        stress = employee_state.get('stress_assessment', {}).get('overall_stress_score', 0.0)
        
        # Adjust for stress level
        if stress >= 0.7:
            adjusted_time = base_time * 1.5
        elif stress >= 0.5:
            adjusted_time = base_time * 1.2
        else:
            adjusted_time = base_time
        
        hours = int(adjusted_time)
        minutes = int((adjusted_time - hours) * 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def _calculate_priority_adjustment(self,
                                      task: Dict,
                                      stress: float,
                                      burnout_risk: str) -> str:
        """Calculate if task priority should be adjusted"""
        
        original_priority = task.get('priority', 'medium')
        
        if burnout_risk in ['high', 'critical']:
            if original_priority == 'high':
                return 'Consider delegating or postponing'
            return 'Maintain current priority'
        
        if stress >= 0.7:
            if original_priority == 'high':
                return 'Keep high priority but consider support'
            return 'Can be postponed if needed'
        
        return 'No adjustment needed'
    
    def optimize_task_schedule(self,
                              tasks: List[Dict],
                              employee_states: List[Dict],
                              work_hours: int = 8) -> Dict:
        """
        Optimize task schedule based on predicted emotional states throughout the day
        
        Args:
            tasks: Available tasks to schedule
            employee_states: Predicted emotional states at different times
            work_hours: Available work hours
        
        Returns:
            Optimized schedule with tasks assigned to optimal time slots
        """
        
        schedule = {
            'morning': [],
            'midday': [],
            'afternoon': [],
            'total_tasks': 0,
            'estimated_completion': 0.0
        }
        
        # Divide day into time blocks
        time_blocks = ['morning', 'midday', 'afternoon']
        
        remaining_tasks = tasks.copy()
        total_hours = 0
        
        for i, block in enumerate(time_blocks):
            if i < len(employee_states):
                state = employee_states[i]
            else:
                state = employee_states[-1] if employee_states else {}
            
            # Get recommendations for this time block
            block_recommendations = self.recommend_tasks(
                state,
                remaining_tasks,
                limit=3
            )
            
            block_hours = 0
            for rec in block_recommendations:
                task = rec['task']
                task_hours = task.get('estimated_hours', 1.0)
                
                if total_hours + task_hours <= work_hours:
                    schedule[block].append({
                        'task': task,
                        'match_score': rec['match_score'],
                        'reason': rec['reason']
                    })
                    total_hours += task_hours
                    block_hours += task_hours
                    remaining_tasks.remove(task)
            
            schedule[f'{block}_hours'] = block_hours
        
        schedule['total_tasks'] = len(tasks) - len(remaining_tasks)
        schedule['estimated_completion'] = total_hours
        schedule['unscheduled_tasks'] = len(remaining_tasks)
        
        return schedule
    
    def get_task_category_recommendations(self, emotion: str, stress: float) -> List[str]:
        """Get recommended task categories for given emotional state"""
        
        recommendations = []
        
        for category, profile in self.task_profiles.items():
            if emotion in profile['optimal_emotions']:
                stress_min, stress_max = profile['optimal_stress']
                if stress_min <= stress <= stress_max:
                    recommendations.append(category)
        
        return recommendations if recommendations else ['routine', 'administrative']
    
    def analyze_task_completion_patterns(self,
                                        completed_tasks: List[Dict],
                                        employee_states: List[Dict]) -> Dict:
        """Analyze patterns in task completion based on emotional states"""
        
        if not completed_tasks or not employee_states:
            return {}
        
        patterns = {
            'best_emotion_for_completion': {},
            'best_stress_level': None,
            'optimal_task_categories': [],
            'completion_rate_by_emotion': {}
        }
        
        # Analyze completion by emotion
        emotion_completions = {}
        for task, state in zip(completed_tasks, employee_states):
            emotion = state.get('dominant_emotion', 'neutral')
            emotion_completions[emotion] = emotion_completions.get(emotion, 0) + 1
        
        if emotion_completions:
            patterns['best_emotion_for_completion'] = max(
                emotion_completions.items(),
                key=lambda x: x[1]
            )[0]
        
        # Analyze optimal stress levels
        completed_stress_levels = [
            state.get('stress_assessment', {}).get('overall_stress_score', 0.0)
            for state in employee_states
        ]
        
        if completed_stress_levels:
            patterns['best_stress_level'] = np.mean(completed_stress_levels)
        
        return patterns
