"""
Alert Monitor
Monitors employee wellbeing and triggers HR alerts
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)

class AlertMonitor:
    """Monitors employee wellbeing metrics and triggers alerts"""
    
    def __init__(self):
        self.alert_thresholds = {
            'stress_high': 0.7,
            'stress_critical': 0.85,
            'burnout_risk_high': 'high',
            'burnout_risk_critical': 'critical',
            'consecutive_high_stress_days': 3,
            'negative_emotion_threshold': 0.6
        }
        
        self.employee_history = defaultdict(list)
        self.active_alerts = {}
        
        logger.info("Alert monitor initialized")
    
    def monitor_employee(self, employee_id: str, emotional_state: Dict) -> Optional[Dict]:
        """
        Monitor an employee's emotional state and generate alerts if needed
        
        Args:
            employee_id: Unique employee identifier
            emotional_state: Current emotional state from emotion fusion
        
        Returns:
            Alert dict if intervention needed, None otherwise
        """
        
        # Store history
        self.employee_history[employee_id].append({
            'timestamp': datetime.now(),
            'state': emotional_state
        })
        
        # Keep only last 30 days
        cutoff_date = datetime.now() - timedelta(days=30)
        self.employee_history[employee_id] = [
            entry for entry in self.employee_history[employee_id]
            if entry['timestamp'] > cutoff_date
        ]
        
        # Check for alert conditions
        alert = self._evaluate_alert_conditions(employee_id, emotional_state)
        
        if alert:
            alert_id = f"{employee_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            self.active_alerts[alert_id] = alert
            logger.warning(f"Alert generated for employee {employee_id}: {alert['severity']}")
        
        return alert
    
    def _evaluate_alert_conditions(self, employee_id: str, emotional_state: Dict) -> Optional[Dict]:
        """Evaluate if alert conditions are met"""
        
        stress_score = emotional_state.get('stress_assessment', {}).get('overall_stress_score', 0.0)
        burnout_risk = emotional_state.get('stress_assessment', {}).get('burnout_risk', {})
        dominant_emotion = emotional_state.get('dominant_emotion', 'neutral')
        
        # Critical burnout risk
        if burnout_risk.get('risk_level') == 'critical':
            return self._create_alert(
                employee_id,
                'critical',
                'Critical burnout risk detected',
                'Immediate HR intervention required',
                burnout_risk.get('recommendation', 'Contact employee immediately'),
                emotional_state
            )
        
        # High stress level
        if stress_score >= self.alert_thresholds['stress_critical']:
            return self._create_alert(
                employee_id,
                'critical',
                'Critical stress level detected',
                'Employee showing signs of extreme stress',
                'Schedule urgent check-in and consider workload adjustment',
                emotional_state
            )
        
        # High burnout risk
        if burnout_risk.get('risk_level') == 'high':
            return self._create_alert(
                employee_id,
                'high',
                'High burnout risk detected',
                'Employee at risk of burnout',
                burnout_risk.get('recommendation', 'Schedule check-in with manager'),
                emotional_state
            )
        
        # Prolonged high stress
        if self._check_prolonged_high_stress(employee_id):
            return self._create_alert(
                employee_id,
                'high',
                'Prolonged high stress detected',
                f'Employee has been under high stress for {self.alert_thresholds["consecutive_high_stress_days"]} consecutive days',
                'Urgent manager review and workload assessment needed',
                emotional_state
            )
        
        # Persistent negative emotions
        if self._check_persistent_negative_emotions(employee_id):
            return self._create_alert(
                employee_id,
                'medium',
                'Persistent negative emotions detected',
                'Employee showing consistent negative emotional patterns',
                'Recommend wellness check-in and support resources',
                emotional_state
            )
        
        return None
    
    def _create_alert(self, 
                     employee_id: str,
                     severity: str,
                     title: str,
                     description: str,
                     recommendation: str,
                     emotional_state: Dict) -> Dict:
        """Create alert dictionary"""
        
        return {
            'employee_id': employee_id,
            'severity': severity,
            'title': title,
            'description': description,
            'recommendation': recommendation,
            'timestamp': datetime.now().isoformat(),
            'emotional_state': emotional_state,
            'status': 'open',
            'priority': self._calculate_priority(severity, emotional_state)
        }
    
    def _calculate_priority(self, severity: str, emotional_state: Dict) -> int:
        """Calculate numeric priority (1-5, 5 being highest)"""
        
        base_priority = {
            'critical': 5,
            'high': 4,
            'medium': 3,
            'low': 2,
            'info': 1
        }
        
        return base_priority.get(severity, 3)
    
    def _check_prolonged_high_stress(self, employee_id: str) -> bool:
        """Check if employee has had high stress for consecutive days"""
        
        history = self.employee_history.get(employee_id, [])
        
        if len(history) < self.alert_thresholds['consecutive_high_stress_days']:
            return False
        
        # Check last N days
        recent = history[-self.alert_thresholds['consecutive_high_stress_days']:]
        
        high_stress_count = sum(
            1 for entry in recent
            if entry['state'].get('stress_assessment', {}).get('overall_stress_score', 0) >= 0.7
        )
        
        return high_stress_count >= self.alert_thresholds['consecutive_high_stress_days']
    
    def _check_persistent_negative_emotions(self, employee_id: str) -> bool:
        """Check if employee has persistent negative emotions"""
        
        history = self.employee_history.get(employee_id, [])
        
        if len(history) < 5:  # Need at least 5 data points
            return False
        
        recent = history[-7:]  # Last week
        
        negative_emotions = ['anger', 'sadness', 'fear', 'disgust']
        negative_count = sum(
            1 for entry in recent
            if entry['state'].get('dominant_emotion') in negative_emotions
        )
        
        negative_ratio = negative_count / len(recent)
        
        return negative_ratio >= self.alert_thresholds['negative_emotion_threshold']
    
    def get_active_alerts(self, severity: Optional[str] = None) -> List[Dict]:
        """Get all active alerts, optionally filtered by severity"""
        
        alerts = list(self.active_alerts.values())
        
        if severity:
            alerts = [a for a in alerts if a['severity'] == severity]
        
        # Sort by priority
        alerts.sort(key=lambda x: x['priority'], reverse=True)
        
        return alerts
    
    def acknowledge_alert(self, alert_id: str, acknowledger: str) -> bool:
        """Mark alert as acknowledged"""
        
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id]['status'] = 'acknowledged'
            self.active_alerts[alert_id]['acknowledged_by'] = acknowledger
            self.active_alerts[alert_id]['acknowledged_at'] = datetime.now().isoformat()
            logger.info(f"Alert {alert_id} acknowledged by {acknowledger}")
            return True
        
        return False
    
    def resolve_alert(self, alert_id: str, resolver: str, resolution_notes: str = "") -> bool:
        """Mark alert as resolved"""
        
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id]['status'] = 'resolved'
            self.active_alerts[alert_id]['resolved_by'] = resolver
            self.active_alerts[alert_id]['resolved_at'] = datetime.now().isoformat()
            self.active_alerts[alert_id]['resolution_notes'] = resolution_notes
            logger.info(f"Alert {alert_id} resolved by {resolver}")
            return True
        
        return False
    
    def get_employee_alert_history(self, employee_id: str, days: int = 30) -> List[Dict]:
        """Get alert history for an employee"""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        return [
            alert for alert in self.active_alerts.values()
            if alert['employee_id'] == employee_id and
            datetime.fromisoformat(alert['timestamp']) > cutoff_date
        ]
    
    def get_alert_statistics(self) -> Dict:
        """Get statistics about alerts"""
        
        total_alerts = len(self.active_alerts)
        
        if total_alerts == 0:
            return {
                'total_alerts': 0,
                'by_severity': {},
                'by_status': {},
                'average_resolution_time': None
            }
        
        by_severity = defaultdict(int)
        by_status = defaultdict(int)
        
        for alert in self.active_alerts.values():
            by_severity[alert['severity']] += 1
            by_status[alert['status']] += 1
        
        return {
            'total_alerts': total_alerts,
            'by_severity': dict(by_severity),
            'by_status': dict(by_status),
            'critical_count': by_severity['critical'],
            'open_count': by_status['open']
        }


# Global monitor instance
_monitor = None

def get_monitor() -> AlertMonitor:
    """Get or create global monitor instance"""
    global _monitor
    if _monitor is None:
        _monitor = AlertMonitor()
    return _monitor

def start_alert_monitor():
    """Start the global alert monitor"""
    monitor = get_monitor()
    logger.info("Alert monitor started and ready")
    return monitor
