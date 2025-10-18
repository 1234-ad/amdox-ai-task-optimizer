"""
Task Matcher
Matches employees to tasks based on skills, emotions, and availability
"""

import logging
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class TaskMatcher:
    """Matches tasks to employees based on multiple factors"""
    
    def __init__(self):
        self.skill_weights = {
            'expertise': 0.35,
            'experience': 0.25,
            'past_performance': 0.20,
            'emotional_state': 0.15,
            'availability': 0.05
        }
        logger.info("Task matcher initialized")
    
    def match_task_to_employees(self,
                                task: Dict,
                                employees: List[Dict],
                                limit: int = 3) -> List[Dict]:
        """
        Find best employee matches for a given task
        
        Args:
            task: Task details including required skills
            employees: List of available employees with their profiles
            limit: Maximum number of matches to return
        
        Returns:
            Sorted list of employee matches with scores
        """
        
        if not employees:
            return []
        
        matches = []
        
        for employee in employees:
            match_score = self._calculate_employee_task_match(employee, task)
            
            if match_score > 0.4:  # Minimum threshold
                matches.append({
                    'employee': employee,
                    'match_score': match_score,
                    'strengths': self._identify_match_strengths(employee, task),
                    'concerns': self._identify_match_concerns(employee, task),
                    'recommendation': self._generate_match_recommendation(
                        employee, task, match_score
                    )
                })
        
        # Sort by match score
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        return matches[:limit]
    
    def _calculate_employee_task_match(self, employee: Dict, task: Dict) -> float:
        """Calculate overall match score between employee and task"""
        
        scores = {}
        
        # Skill/Expertise matching
        scores['expertise'] = self._calculate_skill_match(
            employee.get('skills', []),
            task.get('required_skills', [])
        )
        
        # Experience matching
        scores['experience'] = self._calculate_experience_match(
            employee.get('experience_years', 0),
            task.get('complexity', 'medium')
        )
        
        # Past performance
        scores['past_performance'] = employee.get('performance_rating', 0.7)
        
        # Emotional state matching
        emotional_state = employee.get('current_emotional_state', {})
        scores['emotional_state'] = self._calculate_emotional_fitness(
            emotional_state,
            task.get('category', 'routine')
        )
        
        # Availability
        scores['availability'] = 1.0 if employee.get('available', True) else 0.3
        
        # Calculate weighted total
        total_score = sum(
            scores[factor] * self.skill_weights[factor]
            for factor in self.skill_weights
        )
        
        return min(1.0, max(0.0, total_score))
    
    def _calculate_skill_match(self, employee_skills: List[str], required_skills: List[str]) -> float:
        """Calculate skill match percentage"""
        
        if not required_skills:
            return 0.8  # No specific skills required
        
        if not employee_skills:
            return 0.2  # No skills listed
        
        # Convert to lowercase for comparison
        emp_skills = set(s.lower() for s in employee_skills)
        req_skills = set(s.lower() for s in required_skills)
        
        # Calculate overlap
        matched_skills = emp_skills.intersection(req_skills)
        match_ratio = len(matched_skills) / len(req_skills)
        
        # Bonus for additional relevant skills
        additional_skills = len(emp_skills - req_skills)
        bonus = min(0.2, additional_skills * 0.05)
        
        return min(1.0, match_ratio + bonus)
    
    def _calculate_experience_match(self, experience_years: float, complexity: str) -> float:
        """Calculate if employee experience matches task complexity"""
        
        complexity_requirements = {
            'low': 0,
            'medium': 2,
            'high': 5,
            'expert': 10
        }
        
        required_years = complexity_requirements.get(complexity, 2)
        
        if experience_years >= required_years:
            # Experience meets or exceeds requirement
            return min(1.0, 0.7 + (experience_years - required_years) * 0.05)
        else:
            # Experience below requirement
            ratio = experience_years / required_years if required_years > 0 else 0.5
            return max(0.3, ratio)
    
    def _calculate_emotional_fitness(self, emotional_state: Dict, task_category: str) -> float:
        """Calculate emotional fitness for task category"""
        
        if not emotional_state:
            return 0.5  # Neutral score if no data
        
        stress_level = emotional_state.get('stress_assessment', {}).get('overall_stress_score', 0.0)
        dominant_emotion = emotional_state.get('dominant_emotion', 'neutral')
        burnout_risk = emotional_state.get('stress_assessment', {}).get('burnout_risk', {}).get('risk_level', 'minimal')
        
        # Task category requirements
        optimal_conditions = {
            'creative': {'max_stress': 0.4, 'good_emotions': ['happiness', 'surprise', 'neutral']},
            'analytical': {'max_stress': 0.5, 'good_emotions': ['neutral', 'happiness']},
            'routine': {'max_stress': 0.7, 'good_emotions': ['neutral', 'happiness', 'sadness']},
            'collaborative': {'max_stress': 0.5, 'good_emotions': ['happiness', 'neutral']},
            'problem_solving': {'max_stress': 0.4, 'good_emotions': ['happiness', 'neutral', 'surprise']},
            'administrative': {'max_stress': 0.8, 'good_emotions': ['neutral', 'happiness']}
        }
        
        conditions = optimal_conditions.get(task_category, {'max_stress': 0.6, 'good_emotions': ['neutral']})
        
        fitness_score = 0.5
        
        # Check stress level
        if stress_level <= conditions['max_stress']:
            fitness_score += 0.3
        else:
            excess = stress_level - conditions['max_stress']
            fitness_score -= excess * 0.5
        
        # Check emotion
        if dominant_emotion in conditions['good_emotions']:
            fitness_score += 0.2
        
        # Check burnout risk
        if burnout_risk in ['high', 'critical']:
            fitness_score -= 0.3
        elif burnout_risk == 'minimal':
            fitness_score += 0.1
        
        return max(0.0, min(1.0, fitness_score))
    
    def _identify_match_strengths(self, employee: Dict, task: Dict) -> List[str]:
        """Identify strengths in the employee-task match"""
        
        strengths = []
        
        # Check skills
        emp_skills = set(s.lower() for s in employee.get('skills', []))
        req_skills = set(s.lower() for s in task.get('required_skills', []))
        matched_skills = emp_skills.intersection(req_skills)
        
        if matched_skills:
            strengths.append(f"Has required skills: {', '.join(list(matched_skills)[:3])}")
        
        # Check experience
        experience = employee.get('experience_years', 0)
        if experience >= 5:
            strengths.append(f"Experienced professional ({experience} years)")
        
        # Check performance
        performance = employee.get('performance_rating', 0)
        if performance >= 0.8:
            strengths.append("High performance track record")
        
        # Check emotional state
        emotional_state = employee.get('current_emotional_state', {})
        stress = emotional_state.get('stress_assessment', {}).get('overall_stress_score', 0.5)
        if stress < 0.3:
            strengths.append("Currently low stress - optimal for focused work")
        
        return strengths
    
    def _identify_match_concerns(self, employee: Dict, task: Dict) -> List[str]:
        """Identify potential concerns in the employee-task match"""
        
        concerns = []
        
        # Check emotional state
        emotional_state = employee.get('current_emotional_state', {})
        stress = emotional_state.get('stress_assessment', {}).get('overall_stress_score', 0.0)
        burnout_risk = emotional_state.get('stress_assessment', {}).get('burnout_risk', {}).get('risk_level', 'minimal')
        
        if burnout_risk in ['high', 'critical']:
            concerns.append(f"High burnout risk - recommend workload review")
        elif stress >= 0.7:
            concerns.append("Currently under high stress")
        
        # Check availability
        if not employee.get('available', True):
            concerns.append("Limited availability")
        
        # Check skill gaps
        emp_skills = set(s.lower() for s in employee.get('skills', []))
        req_skills = set(s.lower() for s in task.get('required_skills', []))
        missing_skills = req_skills - emp_skills
        
        if missing_skills and len(missing_skills) > len(req_skills) * 0.5:
            concerns.append(f"May need training in: {', '.join(list(missing_skills)[:2])}")
        
        return concerns
    
    def _generate_match_recommendation(self, employee: Dict, task: Dict, score: float) -> str:
        """Generate recommendation text for the match"""
        
        emp_name = employee.get('name', 'Employee')
        task_name = task.get('name', 'Task')
        
        if score >= 0.8:
            return f"{emp_name} is an excellent match for {task_name}. Assign with confidence."
        elif score >= 0.65:
            return f"{emp_name} is a good match for {task_name}. Consider assigning."
        elif score >= 0.5:
            return f"{emp_name} can handle {task_name} but may need support."
        else:
            return f"{emp_name} is suitable for {task_name} with proper guidance."
    
    def optimize_team_composition(self,
                                  tasks: List[Dict],
                                  employees: List[Dict],
                                  team_size: int = 5) -> Dict:
        """
        Optimize team composition for a set of tasks
        
        Args:
            tasks: List of tasks to be completed
            employees: Available employees
            team_size: Desired team size
        
        Returns:
            Optimized team composition with role assignments
        """
        
        # Collect all required skills
        all_required_skills = set()
        for task in tasks:
            all_required_skills.update(task.get('required_skills', []))
        
        # Score employees based on skill coverage and emotional fitness
        employee_scores = []
        for employee in employees:
            emp_skills = set(s.lower() for s in employee.get('skills', []))
            skill_coverage = len(emp_skills.intersection(all_required_skills)) / len(all_required_skills) if all_required_skills else 0
            
            emotional_state = employee.get('current_emotional_state', {})
            emotional_fitness = self._calculate_average_emotional_fitness(emotional_state, tasks)
            
            overall_score = (skill_coverage * 0.6) + (emotional_fitness * 0.4)
            
            employee_scores.append({
                'employee': employee,
                'score': overall_score,
                'skill_coverage': skill_coverage,
                'emotional_fitness': emotional_fitness
            })
        
        # Sort and select top employees
        employee_scores.sort(key=lambda x: x['score'], reverse=True)
        selected_team = employee_scores[:team_size]
        
        # Assign roles based on strengths
        team_composition = {
            'members': [],
            'skill_coverage': 0.0,
            'average_emotional_fitness': 0.0,
            'estimated_capacity': 0
        }
        
        for member in selected_team:
            team_composition['members'].append({
                'employee': member['employee'],
                'role': self._suggest_role(member['employee'], tasks),
                'score': member['score']
            })
        
        # Calculate team metrics
        if selected_team:
            team_composition['skill_coverage'] = np.mean([m['skill_coverage'] for m in selected_team])
            team_composition['average_emotional_fitness'] = np.mean([m['emotional_fitness'] for m in selected_team])
            team_composition['estimated_capacity'] = len(selected_team) * 8  # hours per day
        
        return team_composition
    
    def _calculate_average_emotional_fitness(self, emotional_state: Dict, tasks: List[Dict]) -> float:
        """Calculate average emotional fitness across multiple tasks"""
        
        if not tasks:
            return 0.5
        
        fitness_scores = []
        for task in tasks:
            category = task.get('category', 'routine')
            score = self._calculate_emotional_fitness(emotional_state, category)
            fitness_scores.append(score)
        
        return np.mean(fitness_scores) if fitness_scores else 0.5
    
    def _suggest_role(self, employee: Dict, tasks: List[Dict]) -> str:
        """Suggest optimal role for employee based on skills and tasks"""
        
        skills = employee.get('skills', [])
        experience = employee.get('experience_years', 0)
        
        # Simple role suggestion logic
        skill_set = set(s.lower() for s in skills)
        
        if experience >= 10:
            return 'Team Lead'
        elif 'management' in skill_set or 'leadership' in skill_set:
            return 'Project Coordinator'
        elif any(s in skill_set for s in ['design', 'creative', 'ui', 'ux']):
            return 'Creative Specialist'
        elif any(s in skill_set for s in ['analysis', 'data', 'research']):
            return 'Analyst'
        elif any(s in skill_set for s in ['development', 'programming', 'coding']):
            return 'Developer'
        else:
            return 'Team Member'
