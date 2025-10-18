#!/usr/bin/env python3
"""
Quick Start Script for Amdox AI Task Optimizer
Demonstrates the core functionality of the system
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from emotion_analyzer.text_analyzer import TextEmotionAnalyzer
from emotion_analyzer.emotion_fusion import EmotionFusion
from task_optimizer.recommendation_engine import TaskRecommendationEngine
from task_optimizer.task_matcher import TaskMatcher
from alert_system.monitor import AlertMonitor
from data.sample_data import SAMPLE_EMPLOYEES, SAMPLE_TASKS

def print_separator(title=""):
    print("\n" + "="*70)
    if title:
        print(f" {title}")
        print("="*70)

def demo_text_analysis():
    """Demonstrate text emotion analysis"""
    print_separator("1. TEXT EMOTION ANALYSIS")
    
    analyzer = TextEmotionAnalyzer()
    
    texts = [
        "I'm so excited about this new project! Can't wait to get started!",
        "Feeling overwhelmed with work. Too many deadlines approaching.",
        "Had a productive meeting with the team today."
    ]
    
    for i, text in enumerate(texts, 1):
        print(f"\nText {i}: \"{text}\"")
        result = analyzer.analyze_emotion(text)
        print(f"  Emotion: {result['primary_emotion'].title()}")
        print(f"  Confidence: {result['emotion_confidence']:.2%}")
        print(f"  Stress Level: {result['stress_indicators']['stress_level'].title()}")
        print(f"  Stress Score: {result['stress_indicators']['overall_stress_score']:.2f}")

def demo_emotion_fusion():
    """Demonstrate emotion fusion and burnout detection"""
    print_separator("2. EMOTION FUSION & BURNOUT DETECTION")
    
    analyzer = TextEmotionAnalyzer()
    fusion = EmotionFusion()
    
    stressed_text = "I'm exhausted and overwhelmed. Can't handle more work right now."
    text_result = analyzer.analyze_emotion(stressed_text)
    
    print(f"\nAnalyzing: \"{stressed_text}\"")
    fused_result = fusion.fuse_emotions(text_result=text_result)
    
    print(f"\nFused Results:")
    print(f"  Dominant Emotion: {fused_result['dominant_emotion'].title()}")
    print(f"  Overall Stress: {fused_result['stress_assessment']['overall_stress_score']:.2f}")
    
    burnout = fused_result['stress_assessment']['burnout_risk']
    print(f"\nBurnout Assessment:")
    print(f"  Risk Level: {burnout['risk_level'].upper()}")
    print(f"  Risk Score: {burnout['risk_score']:.2f}")
    print(f"  Recommendation: {burnout['recommendation']}")
    print(f"  Intervention Needed: {'YES' if fused_result['stress_assessment']['intervention_needed'] else 'NO'}")

def demo_task_recommendations():
    """Demonstrate task recommendation"""
    print_separator("3. INTELLIGENT TASK RECOMMENDATIONS")
    
    analyzer = TextEmotionAnalyzer()
    fusion = EmotionFusion()
    recommender = TaskRecommendationEngine()
    
    # Happy employee state
    text = "Great day! Feeling energized and creative!"
    text_result = analyzer.analyze_emotion(text)
    employee_state = fusion.fuse_emotions(text_result=text_result)
    
    print(f"\nEmployee State: {employee_state['dominant_emotion'].title()}")
    print(f"Stress Level: {employee_state['stress_assessment']['stress_level'].title()}")
    
    print(f"\nAvailable Tasks:")
    for task in SAMPLE_TASKS[:3]:
        print(f"  - {task['name']} ({task['category']}, {task['priority']} priority)")
    
    recommendations = recommender.recommend_tasks(employee_state, SAMPLE_TASKS, limit=3)
    
    print(f"\nTop 3 Recommended Tasks:")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n  {i}. {rec['task']['name']}")
        print(f"     Match Score: {rec['match_score']:.2%}")
        print(f"     Reason: {rec['reason']}")
        print(f"     Estimated Time: {rec['estimated_completion_time']}")

def demo_task_matching():
    """Demonstrate employee-task matching"""
    print_separator("4. EMPLOYEE-TASK MATCHING")
    
    analyzer = TextEmotionAnalyzer()
    fusion = EmotionFusion()
    matcher = TaskMatcher()
    
    # Add emotional states to employees
    for emp in SAMPLE_EMPLOYEES:
        text = "Feeling good and ready to work"
        text_result = analyzer.analyze_emotion(text)
        emp['current_emotional_state'] = fusion.fuse_emotions(text_result=text_result)
    
    task = SAMPLE_TASKS[1]  # API implementation task
    print(f"\nTask: {task['name']}")
    print(f"Category: {task['category']}")
    print(f"Required Skills: {', '.join(task['required_skills'])}")
    print(f"Complexity: {task['complexity']}")
    
    matches = matcher.match_task_to_employees(task, SAMPLE_EMPLOYEES, limit=3)
    
    print(f"\nTop Matches:")
    for i, match in enumerate(matches, 1):
        emp = match['employee']
        print(f"\n  {i}. {emp['name']} ({emp['position']})")
        print(f"     Match Score: {match['match_score']:.2%}")
        print(f"     Strengths: {', '.join(match['strengths'][:2]) if match['strengths'] else 'None'}")
        print(f"     Recommendation: {match['recommendation']}")

def demo_alert_system():
    """Demonstrate alert monitoring"""
    print_separator("5. ALERT SYSTEM & HR NOTIFICATIONS")
    
    analyzer = TextEmotionAnalyzer()
    fusion = EmotionFusion()
    monitor = AlertMonitor()
    
    # Simulate stressed employee
    stressed_texts = [
        "Feeling really stressed today. Too much pressure.",
        "Overwhelmed with work. Can't keep up with deadlines.",
        "Exhausted and burned out. Need a break."
    ]
    
    print("\nMonitoring Employee EMP001 over 3 days:\n")
    
    for day, text in enumerate(stressed_texts, 1):
        print(f"Day {day}: \"{text}\"")
        text_result = analyzer.analyze_emotion(text)
        emotional_state = fusion.fuse_emotions(text_result=text_result)
        
        alert = monitor.monitor_employee('EMP001', emotional_state)
        
        if alert:
            print(f"  ⚠️  ALERT GENERATED!")
            print(f"     Severity: {alert['severity'].upper()}")
            print(f"     Title: {alert['title']}")
            print(f"     Recommendation: {alert['recommendation']}")
        else:
            print(f"  ✓ No alert - stress within normal range")
        print()
    
    # Show alert statistics
    stats = monitor.get_alert_statistics()
    print(f"Alert Statistics:")
    print(f"  Total Alerts: {stats['total_alerts']}")
    print(f"  Critical: {stats.get('critical_count', 0)}")
    print(f"  Open Alerts: {stats.get('open_count', 0)}")

def main():
    """Run all demonstrations"""
    print("\n" + "="*70)
    print(" AMDOX AI-POWERED TASK OPTIMIZER - QUICK START DEMO")
    print("="*70)
    print("\nThis demo showcases the core functionality of the system.")
    print("Loading ML models (this may take a moment)...")
    
    try:
        demo_text_analysis()
        demo_emotion_fusion()
        demo_task_recommendations()
        demo_task_matching()
        demo_alert_system()
        
        print_separator("DEMO COMPLETE")
        print("\n✅ All systems operational!")
        print("\nNext Steps:")
        print("  1. Start the web server: python app.py")
        print("  2. Access dashboard: http://localhost:5000/dashboard")
        print("  3. Test the API: See EXAMPLES.md for usage examples")
        print("  4. Read documentation: See SETUP.md for full guide")
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        print("\nNote: Some ML models need to be downloaded on first run.")
        print("This is normal and will only happen once.")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
