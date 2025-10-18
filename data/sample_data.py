"""
Sample Data
Example data structures for testing and development
"""

# Sample Employees
SAMPLE_EMPLOYEES = [
    {
        "employee_id": "EMP001",
        "name": "John Doe",
        "email": "john.doe@company.com",
        "department": "Engineering",
        "position": "Senior Developer",
        "skills": ["Python", "JavaScript", "React", "Docker", "AWS"],
        "experience_years": 8,
        "performance_rating": 0.9,
        "available": True
    },
    {
        "employee_id": "EMP002",
        "name": "Jane Smith",
        "email": "jane.smith@company.com",
        "department": "Design",
        "position": "UI/UX Designer",
        "skills": ["Figma", "Sketch", "User Research", "Prototyping"],
        "experience_years": 5,
        "performance_rating": 0.85,
        "available": True
    },
    {
        "employee_id": "EMP003",
        "name": "Mike Johnson",
        "email": "mike.johnson@company.com",
        "department": "Data Science",
        "position": "Data Analyst",
        "skills": ["Python", "SQL", "Tableau", "Statistics", "Machine Learning"],
        "experience_years": 6,
        "performance_rating": 0.88,
        "available": True
    }
]

# Sample Tasks
SAMPLE_TASKS = [
    {
        "task_id": "TASK001",
        "name": "Design new dashboard UI",
        "description": "Create modern dashboard interface with data visualizations",
        "category": "creative",
        "priority": "high",
        "complexity": "medium",
        "required_skills": ["UI Design", "Figma", "User Research"],
        "estimated_hours": 16,
        "status": "pending"
    },
    {
        "task_id": "TASK002",
        "name": "Implement API endpoints",
        "description": "Build RESTful API for mobile app integration",
        "category": "analytical",
        "priority": "high",
        "complexity": "high",
        "required_skills": ["Python", "Flask", "API Design"],
        "estimated_hours": 24,
        "status": "pending"
    },
    {
        "task_id": "TASK003",
        "name": "Data analysis report",
        "description": "Analyze Q4 sales data and generate insights",
        "category": "analytical",
        "priority": "medium",
        "complexity": "medium",
        "required_skills": ["Python", "SQL", "Data Analysis"],
        "estimated_hours": 12,
        "status": "pending"
    },
    {
        "task_id": "TASK004",
        "name": "Update documentation",
        "description": "Update user manual and API documentation",
        "category": "administrative",
        "priority": "low",
        "complexity": "low",
        "required_skills": ["Technical Writing", "Markdown"],
        "estimated_hours": 6,
        "status": "pending"
    }
]

# Sample Emotional States
SAMPLE_EMOTIONAL_STATES = [
    {
        "dominant_emotion": "happiness",
        "emotion_scores": {
            "happiness": 0.75,
            "neutral": 0.15,
            "surprise": 0.10
        },
        "stress_assessment": {
            "overall_stress_score": 0.2,
            "stress_level": "low",
            "burnout_risk": {
                "risk_level": "minimal",
                "risk_score": 0.1,
                "risk_factors": [],
                "recommendation": "Employee wellbeing appears healthy."
            },
            "intervention_needed": False
        },
        "confidence": 0.85,
        "available_modalities": ["text"],
        "modality_count": 1
    },
    {
        "dominant_emotion": "neutral",
        "emotion_scores": {
            "neutral": 0.65,
            "happiness": 0.20,
            "sadness": 0.15
        },
        "stress_assessment": {
            "overall_stress_score": 0.45,
            "stress_level": "moderate",
            "burnout_risk": {
                "risk_level": "low",
                "risk_score": 0.25,
                "risk_factors": ["Elevated stress levels"],
                "recommendation": "Continue regular check-ins."
            },
            "intervention_needed": False
        },
        "confidence": 0.78,
        "available_modalities": ["text", "facial"],
        "modality_count": 2
    },
    {
        "dominant_emotion": "sadness",
        "emotion_scores": {
            "sadness": 0.60,
            "neutral": 0.25,
            "anger": 0.15
        },
        "stress_assessment": {
            "overall_stress_score": 0.75,
            "stress_level": "high",
            "burnout_risk": {
                "risk_level": "high",
                "risk_score": 0.7,
                "risk_factors": ["High stress levels detected", "Predominant negative emotions"],
                "recommendation": "Schedule check-in with manager and HR."
            },
            "intervention_needed": True
        },
        "confidence": 0.82,
        "available_modalities": ["text", "facial", "speech"],
        "modality_count": 3
    }
]
