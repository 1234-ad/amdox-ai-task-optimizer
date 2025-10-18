"""
Notification Service
Sends notifications to HR and managers
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
import os

logger = logging.getLogger(__name__)

class NotificationService:
    """Handles sending notifications via various channels"""
    
    def __init__(self):
        self.email_config = {
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', 587)),
            'sender_email': os.getenv('SENDER_EMAIL', 'noreply@amdox.com'),
            'sender_password': os.getenv('SENDER_PASSWORD', '')
        }
        logger.info("Notification service initialized")
    
    def send_alert_notification(self, alert: Dict, recipients: List[str]) -> bool:
        """
        Send alert notification to specified recipients
        
        Args:
            alert: Alert dictionary
            recipients: List of recipient email addresses
        
        Returns:
            True if notification sent successfully, False otherwise
        """
        
        subject = f"[{alert['severity'].upper()}] Employee Wellbeing Alert: {alert['title']}"
        
        body = self._format_alert_email(alert)
        
        return self.send_email(recipients, subject, body)
    
    def send_email(self, recipients: List[str], subject: str, body: str) -> bool:
        """Send email notification"""
        
        try:
            # Create message
            message = MIMEMultipart()
            message['From'] = self.email_config['sender_email']
            message['To'] = ', '.join(recipients)
            message['Subject'] = subject
            
            message.attach(MIMEText(body, 'html'))
            
            # Send email
            if self.email_config['sender_password']:  # Only send if configured
                with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                    server.starttls()
                    server.login(self.email_config['sender_email'], self.email_config['sender_password'])
                    server.send_message(message)
                
                logger.info(f"Email sent to {', '.join(recipients)}")
                return True
            else:
                logger.warning("Email not configured - notification logged only")
                logger.info(f"Would send to {', '.join(recipients)}: {subject}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def _format_alert_email(self, alert: Dict) -> str:
        """Format alert as HTML email"""
        
        severity_colors = {
            'critical': '#dc3545',
            'high': '#fd7e14',
            'medium': '#ffc107',
            'low': '#28a745',
            'info': '#17a2b8'
        }
        
        color = severity_colors.get(alert['severity'], '#6c757d')
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .alert-box {{ 
                    border-left: 4px solid {color};
                    padding: 15px;
                    margin: 20px 0;
                    background-color: #f8f9fa;
                }}
                .severity {{ 
                    color: {color};
                    font-weight: bold;
                    font-size: 18px;
                }}
                .section {{ margin: 15px 0; }}
                .label {{ font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="alert-box">
                <p class="severity">SEVERITY: {alert['severity'].upper()}</p>
                
                <div class="section">
                    <p class="label">Employee ID:</p>
                    <p>{alert['employee_id']}</p>
                </div>
                
                <div class="section">
                    <p class="label">Alert:</p>
                    <p>{alert['title']}</p>
                </div>
                
                <div class="section">
                    <p class="label">Description:</p>
                    <p>{alert['description']}</p>
                </div>
                
                <div class="section">
                    <p class="label">Recommendation:</p>
                    <p>{alert['recommendation']}</p>
                </div>
                
                <div class="section">
                    <p class="label">Timestamp:</p>
                    <p>{alert['timestamp']}</p>
                </div>
                
                <hr>
                
                <p><em>This is an automated alert from the Amdox AI Task Optimizer system. 
                Please take appropriate action based on the severity and recommendation provided.</em></p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_daily_summary(self, summary: Dict, recipients: List[str]) -> bool:
        """Send daily wellbeing summary report"""
        
        subject = f"Daily Employee Wellbeing Summary - {summary.get('date', 'Today')}"
        body = self._format_summary_email(summary)
        
        return self.send_email(recipients, subject, body)
    
    def _format_summary_email(self, summary: Dict) -> str:
        """Format summary as HTML email"""
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .summary-box {{ padding: 20px; background-color: #f8f9fa; }}
                .metric {{ 
                    display: inline-block;
                    padding: 10px 15px;
                    margin: 10px;
                    background-color: white;
                    border-radius: 5px;
                }}
                .metric-value {{ 
                    font-size: 24px;
                    font-weight: bold;
                    color: #007bff;
                }}
                table {{ 
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{ 
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{ background-color: #007bff; color: white; }}
            </style>
        </head>
        <body>
            <div class="summary-box">
                <h2>Daily Employee Wellbeing Summary</h2>
                <p>Date: {summary.get('date', 'Today')}</p>
                
                <div>
                    <div class="metric">
                        <p>Total Employees Monitored</p>
                        <p class="metric-value">{summary.get('total_employees', 0)}</p>
                    </div>
                    
                    <div class="metric">
                        <p>Average Stress Level</p>
                        <p class="metric-value">{summary.get('average_stress', 0):.2f}</p>
                    </div>
                    
                    <div class="metric">
                        <p>Active Alerts</p>
                        <p class="metric-value">{summary.get('active_alerts', 0)}</p>
                    </div>
                </div>
                
                <h3>Alert Breakdown</h3>
                <table>
                    <tr>
                        <th>Severity</th>
                        <th>Count</th>
                    </tr>
                    {self._format_alert_rows(summary.get('alerts_by_severity', {}))}
                </table>
                
                <p><em>For detailed information, please access the dashboard.</em></p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _format_alert_rows(self, alerts_by_severity: Dict) -> str:
        """Format alert severity rows for table"""
        rows = ""
        for severity, count in alerts_by_severity.items():
            rows += f"<tr><td>{severity.title()}</td><td>{count}</td></tr>"
        return rows if rows else "<tr><td colspan='2'>No alerts</td></tr>"
    
    def send_slack_notification(self, alert: Dict, webhook_url: str) -> bool:
        """Send notification to Slack (placeholder for future implementation)"""
        logger.info(f"Slack notification would be sent for alert: {alert['title']}")
        # Implement Slack webhook integration here
        return True
    
    def send_teams_notification(self, alert: Dict, webhook_url: str) -> bool:
        """Send notification to Microsoft Teams (placeholder for future implementation)"""
        logger.info(f"Teams notification would be sent for alert: {alert['title']}")
        # Implement Teams webhook integration here
        return True
