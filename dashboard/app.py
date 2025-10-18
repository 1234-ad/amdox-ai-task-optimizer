"""
Dashboard Application
Web interface for analytics and insights
"""

from flask import render_template_string, jsonify
from . import dashboard_bp
import logging

logger = logging.getLogger(__name__)

# Simple HTML dashboard template
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Amdox AI Task Optimizer Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 50px rgba(0,0,0,0.3);
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 32px;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .metric-label {
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 10px;
        }
        .metric-value {
            font-size: 36px;
            font-weight: bold;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .section h2 {
            color: #333;
            margin-bottom: 15px;
            font-size: 24px;
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .feature-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .feature-card h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        .feature-card p {
            color: #666;
            line-height: 1.6;
        }
        .api-endpoint {
            background: #2d3748;
            color: #68d391;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
            overflow-x: auto;
        }
        .status {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
        }
        .status.active {
            background: #48bb78;
            color: white;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 5px;
            transition: background 0.3s;
        }
        .btn:hover {
            background: #764ba2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Amdox AI-Powered Task Optimizer</h1>
        <p class="subtitle">Intelligent employee wellbeing and task management system</p>
        <span class="status active">System Active</span>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-label">System Status</div>
                <div class="metric-value">✓ Online</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Active Modules</div>
                <div class="metric-value">7</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">API Endpoints</div>
                <div class="metric-value">15+</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Analysis Types</div>
                <div class="metric-value">3</div>
            </div>
        </div>
        
        <div class="section">
            <h2>🎯 Core Features</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <h3>📊 Multi-Modal Emotion Analysis</h3>
                    <p>Analyze emotions from text, facial expressions, and speech with AI-powered fusion for comprehensive insights.</p>
                </div>
                <div class="feature-card">
                    <h3>🎯 Intelligent Task Matching</h3>
                    <p>AI recommends optimal tasks based on current emotional state, skills, and workload capacity.</p>
                </div>
                <div class="feature-card">
                    <h3>🚨 Stress & Burnout Detection</h3>
                    <p>Early warning system identifies stress patterns and burnout risks before they escalate.</p>
                </div>
                <div class="feature-card">
                    <h3>📧 Automated HR Alerts</h3>
                    <p>Real-time notifications to HR and managers when intervention is needed.</p>
                </div>
                <div class="feature-card">
                    <h3>👥 Team Optimization</h3>
                    <p>Compose optimal teams based on skills, emotional fitness, and task requirements.</p>
                </div>
                <div class="feature-card">
                    <h3>📈 Analytics Dashboard</h3>
                    <p>Comprehensive insights into employee wellbeing trends and productivity patterns.</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔌 API Endpoints</h2>
            <p style="margin-bottom: 15px;">Access these endpoints to integrate with the system:</p>
            
            <div class="api-endpoint">POST /api/analyze/text - Analyze emotion from text</div>
            <div class="api-endpoint">POST /api/analyze/facial - Analyze facial expressions</div>
            <div class="api-endpoint">POST /api/analyze/speech - Analyze speech emotions</div>
            <div class="api-endpoint">POST /api/analyze/multimodal - Multi-modal emotion fusion</div>
            <div class="api-endpoint">POST /api/tasks/recommend - Get task recommendations</div>
            <div class="api-endpoint">POST /api/tasks/match - Match tasks to employees</div>
            <div class="api-endpoint">GET /api/alerts - Get active alerts</div>
            <div class="api-endpoint">POST /api/teams/optimize - Optimize team composition</div>
            
            <p style="margin-top: 15px;">
                <a href="/api" class="btn">View API Documentation</a>
                <a href="/health" class="btn">System Health Check</a>
            </p>
        </div>
        
        <div class="section">
            <h2>📖 Quick Start</h2>
            <ol style="line-height: 2; color: #666;">
                <li>Send employee text/data to <code>/api/analyze/multimodal</code></li>
                <li>Receive emotional state analysis with stress indicators</li>
                <li>Get task recommendations via <code>/api/tasks/recommend</code></li>
                <li>Monitor alerts through <code>/api/alerts</code></li>
                <li>Review dashboard analytics for trends</li>
            </ol>
        </div>
        
        <footer style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #999;">
            <p>Amdox AI Task Optimizer v1.0.0 | Built with Python, Flask, TensorFlow & PyTorch</p>
            <p style="margin-top: 10px;">Privacy-First • Ethical AI • Employee Wellbeing</p>
        </footer>
    </div>
</body>
</html>
"""

@dashboard_bp.route('/')
def index():
    """Dashboard home page"""
    return render_template_string(DASHBOARD_TEMPLATE)

@dashboard_bp.route('/analytics')
def analytics():
    """Analytics page placeholder"""
    return jsonify({
        'message': 'Analytics dashboard',
        'note': 'Full analytics UI would be implemented here with charting libraries'
    })

@dashboard_bp.route('/employees')
def employees():
    """Employee management page placeholder"""
    return jsonify({
        'message': 'Employee management',
        'note': 'Employee list and details would be displayed here'
    })

@dashboard_bp.route('/tasks')
def tasks():
    """Task management page placeholder"""
    return jsonify({
        'message': 'Task management',
        'note': 'Task list and assignment interface would be here'
    })
