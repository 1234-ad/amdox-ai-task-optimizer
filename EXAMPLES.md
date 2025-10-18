# API Usage Examples

## Text Emotion Analysis

```python
import requests

response = requests.post('http://localhost:5000/api/analyze/text', json={
    'text': 'I am feeling overwhelmed with work and deadlines are approaching fast.'
})

print(response.json())
```

## Multimodal Analysis with Alert Monitoring

```python
import requests

response = requests.post('http://localhost:5000/api/analyze/multimodal', json={
    'employee_id': 'EMP001',
    'text': 'Feeling stressed and exhausted. Too much work.'
})

result = response.json()
print(f"Dominant Emotion: {result['dominant_emotion']}")
print(f"Stress Level: {result['stress_assessment']['stress_level']}")
print(f"Burnout Risk: {result['stress_assessment']['burnout_risk']['risk_level']}")
print(f"Alert Generated: {result.get('alert_generated', False)}")
```

## Task Recommendations

```python
import requests
from data.sample_data import SAMPLE_EMOTIONAL_STATES, SAMPLE_TASKS

response = requests.post('http://localhost:5000/api/tasks/recommend', json={
    'employee_state': SAMPLE_EMOTIONAL_STATES[0],
    'available_tasks': SAMPLE_TASKS,
    'limit': 3
})

recommendations = response.json()['recommendations']
for rec in recommendations:
    print(f"Task: {rec['task']['name']}")
    print(f"Match Score: {rec['match_score']:.2f}")
    print(f"Reason: {rec['reason']}\n")
```

## Task-Employee Matching

```python
import requests
from data.sample_data import SAMPLE_EMPLOYEES, SAMPLE_TASKS

response = requests.post('http://localhost:5000/api/tasks/match', json={
    'task': SAMPLE_TASKS[0],
    'employees': SAMPLE_EMPLOYEES,
    'limit': 3
})

matches = response.json()['matches']
for match in matches:
    print(f"Employee: {match['employee']['name']}")
    print(f"Match Score: {match['match_score']:.2f}")
    print(f"Strengths: {', '.join(match['strengths'])}")
    print(f"Recommendation: {match['recommendation']}\n")
```

## Get Active Alerts

```python
import requests

# Get all alerts
response = requests.get('http://localhost:5000/api/alerts')
alerts = response.json()['alerts']

# Get only critical alerts
response = requests.get('http://localhost:5000/api/alerts?severity=critical')
critical_alerts = response.json()['alerts']

for alert in critical_alerts:
    print(f"Alert: {alert['title']}")
    print(f"Employee: {alert['employee_id']}")
    print(f"Severity: {alert['severity']}")
    print(f"Recommendation: {alert['recommendation']}\n")
```

## Acknowledge and Resolve Alerts

```python
import requests

alert_id = 'EMP001_20231018120000'

# Acknowledge alert
response = requests.post(f'http://localhost:5000/api/alerts/{alert_id}/acknowledge', json={
    'acknowledger': 'HR Manager'
})

# Resolve alert
response = requests.post(f'http://localhost:5000/api/alerts/{alert_id}/resolve', json={
    'resolver': 'HR Manager',
    'resolution_notes': 'Met with employee. Adjusted workload and scheduled follow-up.'
})
```

## Team Optimization

```python
import requests
from data.sample_data import SAMPLE_EMPLOYEES, SAMPLE_TASKS

response = requests.post('http://localhost:5000/api/teams/optimize', json={
    'tasks': SAMPLE_TASKS,
    'employees': SAMPLE_EMPLOYEES,
    'team_size': 3
})

team = response.json()
print(f"Team Skill Coverage: {team['skill_coverage']:.2%}")
print(f"Average Emotional Fitness: {team['average_emotional_fitness']:.2f}")
print("\nTeam Members:")
for member in team['members']:
    print(f"- {member['employee']['name']} ({member['role']})")
```

## Schedule Optimization

```python
import requests
from data.sample_data import SAMPLE_TASKS, SAMPLE_EMOTIONAL_STATES

# Predict employee states at different times of day
morning_state = SAMPLE_EMOTIONAL_STATES[0]
midday_state = SAMPLE_EMOTIONAL_STATES[1]
afternoon_state = SAMPLE_EMOTIONAL_STATES[1]

response = requests.post('http://localhost:5000/api/tasks/optimize-schedule', json={
    'tasks': SAMPLE_TASKS,
    'employee_states': [morning_state, midday_state, afternoon_state],
    'work_hours': 8
})

schedule = response.json()
print(f"Total Tasks Scheduled: {schedule['total_tasks']}")
print(f"Estimated Completion: {schedule['estimated_completion']} hours")
print(f"\nMorning Tasks: {len(schedule['morning'])}")
print(f"Midday Tasks: {len(schedule['midday'])}")
print(f"Afternoon Tasks: {len(schedule['afternoon'])}")
```

## Python SDK Usage

```python
# Direct usage without API calls
from emotion_analyzer.text_analyzer import TextEmotionAnalyzer
from emotion_analyzer.emotion_fusion import EmotionFusion
from task_optimizer.recommendation_engine import TaskRecommendationEngine

# Initialize
text_analyzer = TextEmotionAnalyzer()
emotion_fusion = EmotionFusion()
task_recommender = TaskRecommendationEngine()

# Analyze
text_result = text_analyzer.analyze_emotion("I'm excited about this new project!")
fused_result = emotion_fusion.fuse_emotions(text_result=text_result)

# Get recommendations
tasks = [...]  # Your tasks
recommendations = task_recommender.recommend_tasks(fused_result, tasks)
```

## Batch Processing

```python
import requests

texts = [
    "Great day at work!",
    "Feeling stressed with deadlines",
    "Team meeting went well",
    "Overwhelmed with tasks"
]

results = []
for text in texts:
    response = requests.post('http://localhost:5000/api/analyze/text', json={'text': text})
    results.append(response.json())

# Analyze trends
from emotion_analyzer.text_analyzer import TextEmotionAnalyzer
analyzer = TextEmotionAnalyzer()
trends = analyzer.get_emotion_trends(results)
print(f"Dominant Emotion: {trends['dominant_emotion']}")
print(f"Average Stress: {trends['average_stress_score']:.2f}")
```
