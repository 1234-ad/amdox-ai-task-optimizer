"""
API Routes
REST API endpoints for emotion analysis, task recommendation, and alerts
"""

from flask import request, jsonify
from . import api_bp
import logging

from emotion_analyzer.text_analyzer import TextEmotionAnalyzer
from emotion_analyzer.facial_analyzer import FacialEmotionAnalyzer
from emotion_analyzer.speech_analyzer import SpeechEmotionAnalyzer
from emotion_analyzer.emotion_fusion import EmotionFusion
from task_optimizer.recommendation_engine import TaskRecommendationEngine
from task_optimizer.task_matcher import TaskMatcher
from alert_system.monitor import get_monitor
from alert_system.notifications import NotificationService

logger = logging.getLogger(__name__)

# Initialize analyzers
text_analyzer = TextEmotionAnalyzer()
facial_analyzer = FacialEmotionAnalyzer()
speech_analyzer = SpeechEmotionAnalyzer()
emotion_fusion = EmotionFusion()
task_recommender = TaskRecommendationEngine()
task_matcher = TaskMatcher()
alert_monitor = get_monitor()
notification_service = NotificationService()

@api_bp.route('/analyze/text', methods=['POST'])
def analyze_text():
    """Analyze emotion from text"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        result = text_analyzer.analyze_emotion(text)
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in text analysis: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/analyze/facial', methods=['POST'])
def analyze_facial():
    """Analyze emotion from facial image"""
    try:
        # Handle file upload
        if 'image' not in request.files:
            return jsonify({'error': 'Image file is required'}), 400
        
        image = request.files['image']
        
        # Save temporarily and analyze
        temp_path = f"/tmp/{image.filename}"
        image.save(temp_path)
        
        result = facial_analyzer.analyze_image(temp_path)
        
        # Clean up
        import os
        os.remove(temp_path)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in facial analysis: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/analyze/speech', methods=['POST'])
def analyze_speech():
    """Analyze emotion from speech audio"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'Audio file is required'}), 400
        
        audio = request.files['audio']
        
        # Save temporarily and analyze
        temp_path = f"/tmp/{audio.filename}"
        audio.save(temp_path)
        
        result = speech_analyzer.analyze_audio(temp_path)
        
        # Clean up
        import os
        os.remove(temp_path)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in speech analysis: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/analyze/multimodal', methods=['POST'])
def analyze_multimodal():
    """Analyze emotions using multiple modalities and fuse results"""
    try:
        data = request.get_json()
        
        text_result = None
        facial_result = None
        speech_result = None
        
        # Analyze text if provided
        if 'text' in data and data['text']:
            text_result = text_analyzer.analyze_emotion(data['text'])
        
        # Add support for image and audio URLs/paths in production
        
        # Fuse results
        fused_result = emotion_fusion.fuse_emotions(text_result, facial_result, speech_result)
        
        # Check for alerts if employee_id provided
        if 'employee_id' in data:
            alert = alert_monitor.monitor_employee(data['employee_id'], fused_result)
            fused_result['alert_generated'] = alert is not None
            if alert:
                fused_result['alert'] = alert
        
        return jsonify(fused_result), 200
        
    except Exception as e:
        logger.error(f"Error in multimodal analysis: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tasks/recommend', methods=['POST'])
def recommend_tasks():
    """Get task recommendations based on emotional state"""
    try:
        data = request.get_json()
        
        employee_state = data.get('employee_state', {})
        available_tasks = data.get('available_tasks', [])
        limit = data.get('limit', 5)
        
        if not employee_state:
            return jsonify({'error': 'Employee emotional state is required'}), 400
        
        recommendations = task_recommender.recommend_tasks(
            employee_state,
            available_tasks,
            limit
        )
        
        return jsonify({
            'recommendations': recommendations,
            'count': len(recommendations)
        }), 200
        
    except Exception as e:
        logger.error(f"Error in task recommendation: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tasks/match', methods=['POST'])
def match_tasks():
    """Match tasks to employees"""
    try:
        data = request.get_json()
        
        task = data.get('task', {})
        employees = data.get('employees', [])
        limit = data.get('limit', 3)
        
        if not task or not employees:
            return jsonify({'error': 'Task and employees are required'}), 400
        
        matches = task_matcher.match_task_to_employees(task, employees, limit)
        
        return jsonify({
            'matches': matches,
            'count': len(matches)
        }), 200
        
    except Exception as e:
        logger.error(f"Error in task matching: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tasks/optimize-schedule', methods=['POST'])
def optimize_schedule():
    """Optimize task schedule based on predicted emotional states"""
    try:
        data = request.get_json()
        
        tasks = data.get('tasks', [])
        employee_states = data.get('employee_states', [])
        work_hours = data.get('work_hours', 8)
        
        schedule = task_recommender.optimize_task_schedule(
            tasks,
            employee_states,
            work_hours
        )
        
        return jsonify(schedule), 200
        
    except Exception as e:
        logger.error(f"Error in schedule optimization: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/alerts', methods=['GET'])
def get_alerts():
    """Get active alerts"""
    try:
        severity = request.args.get('severity')
        alerts = alert_monitor.get_active_alerts(severity)
        
        return jsonify({
            'alerts': alerts,
            'count': len(alerts)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/alerts/<alert_id>/acknowledge', methods=['POST'])
def acknowledge_alert(alert_id):
    """Acknowledge an alert"""
    try:
        data = request.get_json()
        acknowledger = data.get('acknowledger', 'Unknown')
        
        success = alert_monitor.acknowledge_alert(alert_id, acknowledger)
        
        if success:
            return jsonify({'message': 'Alert acknowledged', 'alert_id': alert_id}), 200
        else:
            return jsonify({'error': 'Alert not found'}), 404
            
    except Exception as e:
        logger.error(f"Error acknowledging alert: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/alerts/<alert_id>/resolve', methods=['POST'])
def resolve_alert(alert_id):
    """Resolve an alert"""
    try:
        data = request.get_json()
        resolver = data.get('resolver', 'Unknown')
        notes = data.get('resolution_notes', '')
        
        success = alert_monitor.resolve_alert(alert_id, resolver, notes)
        
        if success:
            return jsonify({'message': 'Alert resolved', 'alert_id': alert_id}), 200
        else:
            return jsonify({'error': 'Alert not found'}), 404
            
    except Exception as e:
        logger.error(f"Error resolving alert: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/alerts/statistics', methods=['GET'])
def get_alert_statistics():
    """Get alert statistics"""
    try:
        stats = alert_monitor.get_alert_statistics()
        return jsonify(stats), 200
        
    except Exception as e:
        logger.error(f"Error getting alert statistics: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/employees/<employee_id>/alerts', methods=['GET'])
def get_employee_alerts(employee_id):
    """Get alerts for a specific employee"""
    try:
        days = int(request.args.get('days', 30))
        alerts = alert_monitor.get_employee_alert_history(employee_id, days)
        
        return jsonify({
            'employee_id': employee_id,
            'alerts': alerts,
            'count': len(alerts)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting employee alerts: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/teams/optimize', methods=['POST'])
def optimize_team():
    """Optimize team composition for tasks"""
    try:
        data = request.get_json()
        
        tasks = data.get('tasks', [])
        employees = data.get('employees', [])
        team_size = data.get('team_size', 5)
        
        team_composition = task_matcher.optimize_team_composition(
            tasks,
            employees,
            team_size
        )
        
        return jsonify(team_composition), 200
        
    except Exception as e:
        logger.error(f"Error in team optimization: {e}")
        return jsonify({'error': str(e)}), 500
