from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
import json
import os
from pathlib import Path

from models import (
    Project,
    ProjectSummary,
    ProjectsResponse,
    ProjectFilter,
    ProjectCategory,
    ProjectStatus,
    ErrorResponse
)

router = APIRouter()

# In a real app, this would be a database
# For now, we'll use a JSON file for persistence
DATA_FILE = Path("projects_data.json")


def load_projects() -> List[Project]:
    """Load projects from JSON file"""
    if not DATA_FILE.exists():
        # Generate and save sample projects on first request
        sample_projects = get_sample_projects()
        save_projects(sample_projects)
        return sample_projects
    
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return [Project(**project) for project in data]
    except Exception as e:
        print(f"Error loading projects: {e}")
        return get_sample_projects()


def save_projects(projects: List[Project]) -> None:
    """Save projects to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump([project.dict() for project in projects], f, indent=2, default=str)
    except Exception as e:
        print(f"Error saving projects: {e}")


def get_sample_projects() -> List[Project]:
    """Generate sample projects for demonstration"""
    from datetime import datetime
    from models import Technology, ProjectLink, ProjectContent
    import random
    
    # Define project templates for different categories
    web_apps = [
        {
            "title": "E-commerce Platform",
            "description": "Full-stack e-commerce solution with payment integration",
            "tech": ["React", "Node.js", "MongoDB", "Stripe API"],
            "tags": ["ecommerce", "fullstack", "payment", "react"]
        },
        {
            "title": "Social Media Dashboard",
            "description": "Analytics dashboard for social media management",
            "tech": ["Vue.js", "Django", "PostgreSQL", "Chart.js"],
            "tags": ["social-media", "analytics", "vue", "dashboard"]
        },
        {
            "title": "Recipe Sharing App",
            "description": "Community platform for sharing and discovering recipes",
            "tech": ["Angular", "Spring Boot", "MySQL", "AWS S3"],
            "tags": ["food", "community", "angular", "spring"]
        },
        {
            "title": "Project Management Tool",
            "description": "Collaborative project management with real-time updates",
            "tech": ["Next.js", "GraphQL", "Prisma", "PostgreSQL"],
            "tags": ["productivity", "collaboration", "nextjs", "graphql"]
        },
        {
            "title": "Learning Management System",
            "description": "Online education platform with video streaming",
            "tech": ["React", "Express.js", "MongoDB", "AWS CloudFront"],
            "tags": ["education", "video", "react", "aws"]
        },
        {
            "title": "Real Estate Platform",
            "description": "Property listing and management system",
            "tech": ["Vue.js", "Laravel", "MySQL", "Google Maps API"],
            "tags": ["real-estate", "maps", "vue", "laravel"]
        },
        {
            "title": "Event Management System",
            "description": "Platform for organizing and managing events",
            "tech": ["React", "FastAPI", "PostgreSQL", "Redis"],
            "tags": ["events", "management", "react", "fastapi"]
        },
        {
            "title": "Fitness Tracking App",
            "description": "Personal fitness and workout tracking application",
            "tech": ["React Native", "Node.js", "MongoDB", "Chart.js"],
            "tags": ["fitness", "mobile", "react-native", "health"]
        },
        {
            "title": "Restaurant Ordering System",
            "description": "Online food ordering with delivery tracking",
            "tech": ["Angular", "NestJS", "TypeORM", "PostgreSQL"],
            "tags": ["food", "delivery", "angular", "nestjs"]
        },
        {
            "title": "Travel Booking Platform",
            "description": "Hotel and flight booking system with reviews",
            "tech": ["React", "Django", "PostgreSQL", "Stripe API"],
            "tags": ["travel", "booking", "react", "django"]
        }
    ]
    
    mobile_apps = [
        {
            "title": "Weather Forecast App",
            "description": "Beautiful weather app with detailed forecasts",
            "tech": ["React Native", "OpenWeather API", "Redux", "SQLite"],
            "tags": ["weather", "mobile", "react-native", "api"]
        },
        {
            "title": "Personal Finance Tracker",
            "description": "Mobile app for tracking expenses and budgets",
            "tech": ["Flutter", "Dart", "Firebase", "Chart.js"],
            "tags": ["finance", "mobile", "flutter", "firebase"]
        },
        {
            "title": "Meditation Timer App",
            "description": "Mindfulness and meditation tracking application",
            "tech": ["React Native", "Expo", "AsyncStorage", "Audio API"],
            "tags": ["meditation", "wellness", "mobile", "audio"]
        },
        {
            "title": "Language Learning App",
            "description": "Interactive language learning with gamification",
            "tech": ["Flutter", "Firebase", "TensorFlow Lite", "SQLite"],
            "tags": ["education", "language", "flutter", "ml"]
        },
        {
            "title": "Habit Tracker",
            "description": "Daily habit tracking with streak counters",
            "tech": ["React Native", "Redux", "SQLite", "Push Notifications"],
            "tags": ["productivity", "habits", "mobile", "notifications"]
        },
        {
            "title": "Photo Editor Mobile",
            "description": "Mobile photo editing with filters and effects",
            "tech": ["Swift", "CoreImage", "CloudKit", "Metal"],
            "tags": ["photo", "mobile", "ios", "image-processing"]
        },
        {
            "title": "Music Streaming App",
            "description": "Mobile music streaming with offline playback",
            "tech": ["Kotlin", "Android SDK", "ExoPlayer", "Room"],
            "tags": ["music", "streaming", "android", "audio"]
        },
        {
            "title": "Food Delivery App",
            "description": "On-demand food delivery with real-time tracking",
            "tech": ["React Native", "Google Maps", "Firebase", "Stripe"],
            "tags": ["food", "delivery", "mobile", "maps"]
        },
        {
            "title": "Fitness Companion",
            "description": "Personal trainer app with workout plans",
            "tech": ["Flutter", "HealthKit", "Firebase", "TensorFlow"],
            "tags": ["fitness", "health", "mobile", "ai"]
        },
        {
            "title": "Social Travel App",
            "description": "Travel planning and sharing with friends",
            "tech": ["React Native", "Maps SDK", "Firebase", "Stripe"],
            "tags": ["travel", "social", "mobile", "maps"]
        }
    ]
    
    ml_projects = [
        {
            "title": "Sentiment Analysis API",
            "description": "NLP model for analyzing text sentiment",
            "tech": ["Python", "Transformers", "FastAPI", "Docker"],
            "tags": ["nlp", "sentiment", "python", "api"]
        },
        {
            "title": "Computer Vision Classifier",
            "description": "Image classification using deep learning",
            "tech": ["Python", "TensorFlow", "OpenCV", "Flask"],
            "tags": ["computer-vision", "deep-learning", "tensorflow", "python"]
        },
        {
            "title": "Recommendation Engine",
            "description": "ML-powered product recommendation system",
            "tech": ["Python", "Scikit-learn", "Pandas", "Redis"],
            "tags": ["recommendation", "ml", "python", "redis"]
        },
        {
            "title": "Fraud Detection Model",
            "description": "Machine learning model for detecting fraudulent transactions",
            "tech": ["Python", "XGBoost", "Pandas", "MLflow"],
            "tags": ["fraud-detection", "ml", "xgboost", "python"]
        },
        {
            "title": "Chatbot NLP Engine",
            "description": "Natural language processing for intelligent chatbots",
            "tech": ["Python", "spaCy", "NLTK", "Rasa"],
            "tags": ["chatbot", "nlp", "python", "rasa"]
        },
        {
            "title": "Time Series Forecasting",
            "description": "Predictive analytics for business metrics",
            "tech": ["Python", "Prophet", "Pandas", "Matplotlib"],
            "tags": ["forecasting", "time-series", "python", "analytics"]
        },
        {
            "title": "Object Detection System",
            "description": "Real-time object detection and tracking",
            "tech": ["Python", "YOLO", "OpenCV", "FastAPI"],
            "tags": ["object-detection", "computer-vision", "yolo", "python"]
        },
        {
            "title": "Speech Recognition Model",
            "description": "Custom speech-to-text conversion system",
            "tech": ["Python", "Whisper", "Librosa", "Torch"],
            "tags": ["speech", "audio", "ml", "python"]
        },
        {
            "title": "Anomaly Detection Engine",
            "description": "Unsupervised learning for anomaly detection",
            "tech": ["Python", "PyTorch", "Scikit-learn", "Redis"],
            "tags": ["anomaly-detection", "unsupervised", "pytorch", "python"]
        }
    ]
    
    desktop_apps = [
        {
            "title": "Code Editor Pro",
            "description": "Advanced code editor with plugin system",
            "tech": ["Electron", "Monaco Editor", "Node.js", "SQLite"],
            "tags": ["editor", "desktop", "electron", "coding"]
        },
        {
            "title": "Photo Studio",
            "description": "Professional photo editing desktop application",
            "tech": ["Qt", "C++", "OpenCV", "SQLite"],
            "tags": ["photo", "desktop", "cpp", "image-processing"]
        },
        {
            "title": "Audio Workstation",
            "description": "Digital audio workstation for music production",
            "tech": ["JUCE", "C++", "Audio APIs", "VST"],
            "tags": ["audio", "music", "desktop", "cpp"]
        },
        {
            "title": "3D Modeling Tool",
            "description": "3D modeling and animation software",
            "tech": ["OpenGL", "C++", "Qt", "Python"],
            "tags": ["3d", "modeling", "desktop", "graphics"]
        },
        {
            "title": "Database Manager",
            "description": "Universal database management tool",
            "tech": ["JavaFX", "Java", "JDBC", "SQLite"],
            "tags": ["database", "desktop", "java", "management"]
        },
        {
            "title": "Video Editor",
            "description": "Professional video editing software",
            "tech": ["C++", "FFmpeg", "Qt", "OpenGL"],
            "tags": ["video", "editing", "desktop", "multimedia"]
        },
        {
            "title": "System Monitor",
            "description": "Advanced system monitoring and diagnostics",
            "tech": ["C#", "WPF", ".NET Core", "WMI"],
            "tags": ["system", "monitoring", "desktop", "diagnostics"]
        }
    ]
    
    data_projects = [
        {
            "title": "Sales Analytics Dashboard",
            "description": "Interactive dashboard for sales data visualization",
            "tech": ["Python", "Streamlit", "Plotly", "Pandas"],
            "tags": ["analytics", "visualization", "python", "streamlit"]
        },
        {
            "title": "Data Pipeline ETL",
            "description": "Automated data extraction and transformation pipeline",
            "tech": ["Python", "Apache Airflow", "PostgreSQL", "Docker"],
            "tags": ["etl", "pipeline", "airflow", "python"]
        },
        {
            "title": "Customer Segmentation Analysis",
            "description": "Machine learning for customer behavior analysis",
            "tech": ["Python", "Scikit-learn", "Jupyter", "Seaborn"],
            "tags": ["segmentation", "ml", "python", "analysis"]
        },
        {
            "title": "Real-time Analytics Engine",
            "description": "Stream processing for real-time data analytics",
            "tech": ["Apache Kafka", "Apache Spark", "Scala", "Redis"],
            "tags": ["streaming", "real-time", "kafka", "spark"]
        },
        {
            "title": "Business Intelligence Platform",
            "description": "Comprehensive BI solution with reporting",
            "tech": ["Python", "Apache Superset", "PostgreSQL", "Redis"],
            "tags": ["bi", "reporting", "python", "superset"]
        },
        {
            "title": "Data Lake Architecture",
            "description": "Scalable data lake for big data processing",
            "tech": ["AWS S3", "Apache Spark", "Python", "Parquet"],
            "tags": ["data-lake", "big-data", "aws", "spark"]
        },
        {
            "title": "Financial Risk Analytics",
            "description": "Risk assessment and financial modeling platform",
            "tech": ["R", "Shiny", "PostgreSQL", "Plotly"],
            "tags": ["finance", "risk", "r", "analytics"]
        }
    ]
    
    iot_projects = [
        {
            "title": "Smart Home Controller",
            "description": "IoT system for home automation and monitoring",
            "tech": ["Raspberry Pi", "Python", "MQTT", "React"],
            "tags": ["iot", "home-automation", "raspberry-pi", "mqtt"]
        },
        {
            "title": "Environmental Monitoring",
            "description": "IoT sensors for environmental data collection",
            "tech": ["Arduino", "C++", "InfluxDB", "Grafana"],
            "tags": ["iot", "sensors", "arduino", "monitoring"]
        },
        {
            "title": "Industrial IoT Platform",
            "description": "Enterprise IoT solution for manufacturing",
            "tech": ["Node.js", "MongoDB", "MQTT", "Docker"],
            "tags": ["iot", "industrial", "nodejs", "manufacturing"]
        },
        {
            "title": "Smart Agriculture System",
            "description": "IoT-based precision farming solution",
            "tech": ["ESP32", "MicroPython", "LoRaWAN", "AWS IoT"],
            "tags": ["iot", "agriculture", "esp32", "lorawan"]
        },
        {
            "title": "Fleet Tracking System",
            "description": "GPS-based vehicle tracking and management",
            "tech": ["GPS Modules", "Node.js", "MongoDB", "React"],
            "tags": ["iot", "tracking", "gps", "fleet"]
        },
        {
            "title": "Smart City Infrastructure",
            "description": "IoT platform for smart city management",
            "tech": ["LoRaWAN", "Python", "TimescaleDB", "Grafana"],
            "tags": ["iot", "smart-city", "lorawan", "infrastructure"]
        }
    ]
    
    game_projects = [
        {
            "title": "2D Platformer Adventure",
            "description": "Retro-style 2D platformer with pixel art",
            "tech": ["Unity", "C#", "Photoshop", "Audio Tools"],
            "tags": ["game", "2d", "unity", "platformer"]
        },
        {
            "title": "Mobile Puzzle Game",
            "description": "Addictive puzzle game for mobile devices",
            "tech": ["Unity", "C#", "Unity Analytics", "AdMob"],
            "tags": ["game", "mobile", "puzzle", "unity"]
        },
        {
            "title": "VR Space Exploration",
            "description": "Virtual reality space exploration experience",
            "tech": ["Unreal Engine", "C++", "Oculus SDK", "3D Modeling"],
            "tags": ["vr", "space", "unreal", "3d"]
        },
        {
            "title": "Multiplayer Racing Game",
            "description": "Online multiplayer racing with custom tracks",
            "tech": ["Unity", "Photon", "C#", "Blender"],
            "tags": ["game", "racing", "multiplayer", "unity"]
        },
        {
            "title": "RPG Game Engine",
            "description": "Custom RPG game engine and editor",
            "tech": ["C++", "OpenGL", "Lua", "ImGui"],
            "tags": ["game", "engine", "rpg", "cpp"]
        },
        {
            "title": "AR Treasure Hunt",
            "description": "Augmented reality location-based game",
            "tech": ["ARKit", "Swift", "CoreLocation", "RealityKit"],
            "tags": ["ar", "mobile", "location", "ios"]
        }
    ]
    
    # Generate projects
    projects = []
    project_counter = 1
    
    categories_mapping = {
        "web_app": (web_apps, ProjectCategory.web_app),
        "mobile_app": (mobile_apps, ProjectCategory.mobile_app),
        "machine_learning": (ml_projects, ProjectCategory.machine_learning),
        "desktop_app": (desktop_apps, ProjectCategory.desktop_app),
        "data_science": (data_projects, ProjectCategory.data_science),
        "iot": (iot_projects, ProjectCategory.iot),
        "game": (game_projects, ProjectCategory.game)
    }
    
    statuses = [ProjectStatus.active, ProjectStatus.completed, ProjectStatus.in_progress, ProjectStatus.on_hold]
    
    # Create multiple projects for each category
    # First, create at least one cycle for each category to ensure representation
    for category_name, (templates, category_enum) in categories_mapping.items():
        for template in templates:
            if len(projects) >= 150:  # Limit to 150 projects
                break
            
            project_id = f"project-{project_counter:03d}"
            title = template['title']
            
            # Create technologies
            technologies = []
            tech_categories_map = {
                "React": "frontend", "Vue.js": "frontend", "Angular": "frontend", "Next.js": "frontend",
                "Node.js": "backend", "Django": "backend", "FastAPI": "backend", "Spring Boot": "backend",
                "Python": "backend", "JavaScript": "frontend", "TypeScript": "frontend", "Java": "backend",
                "MongoDB": "database", "PostgreSQL": "database", "MySQL": "database", "SQLite": "database",
                "Docker": "devops", "AWS": "cloud", "Redis": "cache", "Kubernetes": "devops"
            }
            
            for tech_name in template['tech'][:4]:  # Limit to 4 technologies
                tech_category = tech_categories_map.get(tech_name, "other")
                version = f"{random.randint(1, 5)}.{random.randint(0, 9)}" if random.choice([True, False]) else None
                
                technologies.append(Technology(
                    name=tech_name,
                    version=version,
                    category=tech_category
                ))
            
            # Create links
            links = [ProjectLink(title="GitHub", url=f"https://github.com/username/{project_id}", type="github")]
            if random.choice([True, False]):
                links.append(ProjectLink(title="Live Demo", url=f"https://{project_id}.example.com", type="demo"))
            
            # Create content
            features = [
                "Responsive design and mobile-first approach",
                "Real-time data synchronization", 
                "Advanced search and filtering capabilities",
                "Performance optimization and caching",
                "User authentication and authorization"
            ]
            
            content = ProjectContent(
                overview=f"{template['description']}. This project demonstrates modern development practices and clean architecture principles.",
                features=random.sample(features, 3),
                technical_details=f"Built using {', '.join(template['tech'][:3])}. Follows industry best practices for scalability, security, and maintainability.",
                challenges="Balancing performance with feature richness while maintaining code quality and user experience.",
                learnings=f"Gained expertise in {template['tech'][0]} and modern development workflows.",
                next_steps="Planning to add advanced analytics, improved user interface, and additional integrations."
            )
            
            # Random image from Unsplash
            image_urls = [
                "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=200&fit=crop",
                "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=400&h=200&fit=crop",
                "https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=400&h=200&fit=crop",
                "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=400&h=200&fit=crop",
                "https://images.unsplash.com/photo-1551650975-87deedd944c3?w=400&h=200&fit=crop",
                "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=200&fit=crop",
                "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400&h=200&fit=crop",
                "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=400&h=200&fit=crop",
                "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=400&h=200&fit=crop",
                "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=400&h=200&fit=crop"
            ]
            
            project = Project(
                id=project_id,
                title=title,
                short_description=template['description'],
                category=category_enum,
                status=random.choice(statuses),
                technologies=technologies,
                links=links,
                content=content,
                image_url=random.choice(image_urls),
                tags=template['tags'],
                priority=random.randint(1, 10)
            )
            
            projects.append(project)
            project_counter += 1
    
    # Then create additional cycles for remaining slots
    remaining_slots = 150 - len(projects)
    cycles_needed = remaining_slots // len(categories_mapping)
    
    for cycle in range(1, cycles_needed + 2):
        for category_name, (templates, category_enum) in categories_mapping.items():
            for template in templates:
                if len(projects) >= 150:  # Limit to 150 projects
                    break
                
                project_id = f"project-{project_counter:03d}"
                title = f"{template['title']}" + (f" v{cycle + 1}" if cycle > 0 else "")
                
                # Create technologies
                technologies = []
                for i, tech_name in enumerate(template['tech'][:4]):  # Limit to 4 technologies
                    tech_categories = {
                        "React": "frontend", "Vue.js": "frontend", "Angular": "frontend", "Next.js": "frontend",
                        "Node.js": "backend", "Django": "backend", "FastAPI": "backend", "Spring Boot": "backend",
                        "Python": "backend", "JavaScript": "frontend", "TypeScript": "frontend",
                        "MongoDB": "database", "PostgreSQL": "database", "MySQL": "database", "SQLite": "database",
                        "Docker": "devops", "AWS": "cloud", "Redis": "cache"
                    }
                    
                    tech_category = tech_categories.get(tech_name, "other")
                    version = f"{random.randint(1, 5)}.{random.randint(0, 9)}" if random.choice([True, False]) else None
                    
                    technologies.append(Technology(
                        name=tech_name,
                        version=version,
                        category=tech_category
                    ))
                
                # Create links
                links = [
                    ProjectLink(
                        title="GitHub",
                        url=f"https://github.com/username/{project_id}",
                        type="github"
                    )
                ]
                
                if random.choice([True, False]):
                    links.append(ProjectLink(
                        title="Live Demo",
                        url=f"https://{project_id}.example.com",
                        type="demo"
                    ))
                
                # Create content
                features = [
                    "Responsive design and mobile-first approach",
                    "Real-time data synchronization",
                    "User authentication and authorization",
                    "Advanced search and filtering capabilities",
                    "Performance optimization and caching"
                ]
                
                content = ProjectContent(
                    overview=f"{template['description']}. This project demonstrates modern development practices and clean architecture principles.",
                    features=random.sample(features, 3),
                    technical_details=f"Built using {', '.join(template['tech'][:3])}. Follows industry best practices for scalability, security, and maintainability.",
                    challenges="Balancing performance with feature richness while maintaining code quality and user experience.",
                    learnings=f"Gained expertise in {template['tech'][0]} and modern development workflows.",
                    next_steps="Planning to add advanced analytics, improved user interface, and additional integrations."
                )
                
                # Random image from Unsplash
                image_urls = [
                    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=200&fit=crop",
                    "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=400&h=200&fit=crop",
                    "https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=400&h=200&fit=crop",
                    "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=400&h=200&fit=crop",
                    "https://images.unsplash.com/photo-1551650975-87deedd944c3?w=400&h=200&fit=crop",
                    "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=200&fit=crop",
                    "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400&h=200&fit=crop",
                    "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=400&h=200&fit=crop"
                ]
                
                project = Project(
                    id=project_id,
                    title=title,
                    short_description=template['description'],
                    category=category_enum,
                    status=random.choice(statuses),
                    technologies=technologies,
                    links=links,
                    content=content,
                    image_url=random.choice(image_urls),
                    tags=template['tags'],
                    priority=random.randint(1, 10)
                )
                
                projects.append(project)
                project_counter += 1
                
            if len(projects) >= 150:
                break
    
    return projects


@router.get("/projects", response_model=ProjectsResponse)
async def get_projects(
    category: Optional[ProjectCategory] = Query(None, description="Filter by category"),
    status: Optional[ProjectStatus] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    tags: Optional[str] = Query(None, description="Comma-separated tags to filter by"),
    limit: int = Query(20, ge=1, le=100, description="Number of projects to return"),
    offset: int = Query(0, ge=0, description="Number of projects to skip")
):
    """Get all projects with optional filtering"""
    projects = load_projects()
    
    # Apply filters
    if category:
        projects = [p for p in projects if p.category == category]
    
    if status:
        projects = [p for p in projects if p.status == status]
    
    if search:
        search_lower = search.lower()
        projects = [
            p for p in projects 
            if search_lower in p.title.lower() 
            or search_lower in p.short_description.lower()
        ]
    
    if tags:
        tag_list = [tag.strip().lower() for tag in tags.split(",")]
        projects = [
            p for p in projects 
            if any(tag in [t.lower() for t in p.tags] for tag in tag_list)
        ]
    
    # Sort by priority (highest first) then by title
    projects.sort(key=lambda x: (-x.priority, x.title))
    
    # Calculate category counts
    all_projects = load_projects()
    categories = {}
    for project in all_projects:
        cat = project.category.value
        categories[cat] = categories.get(cat, 0) + 1
    
    # Apply pagination
    total = len(projects)
    projects = projects[offset:offset + limit]
    
    # Convert to summary format
    project_summaries = [
        ProjectSummary(
            id=p.id,
            title=p.title,
            short_description=p.short_description,
            category=p.category,
            status=p.status,
            image_url=p.image_url,
            tags=p.tags,
            priority=p.priority
        )
        for p in projects
    ]
    
    return ProjectsResponse(
        projects=project_summaries,
        total=total,
        categories=categories
    )


@router.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: str):
    """Get a specific project by ID"""
    projects = load_projects()
    
    for project in projects:
        if project.id == project_id:
            return project
    
    raise HTTPException(status_code=404, detail="Project not found")


@router.post("/projects", response_model=Project)
async def create_project(project: Project):
    """Create a new project"""
    projects = load_projects()
    
    # Check if project ID already exists
    if any(p.id == project.id for p in projects):
        raise HTTPException(status_code=400, detail="Project ID already exists")
    
    projects.append(project)
    save_projects(projects)
    
    return project


@router.put("/projects/{project_id}", response_model=Project)
async def update_project(project_id: str, updated_project: Project):
    """Update an existing project"""
    projects = load_projects()
    
    for i, project in enumerate(projects):
        if project.id == project_id:
            updated_project.id = project_id  # Ensure ID doesn't change
            projects[i] = updated_project
            save_projects(projects)
            return updated_project
    
    raise HTTPException(status_code=404, detail="Project not found")


@router.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    """Delete a project"""
    projects = load_projects()
    
    for i, project in enumerate(projects):
        if project.id == project_id:
            del projects[i]
            save_projects(projects)
            return {"message": "Project deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Project not found")


# Initialize sample data if no data file exists
# Commented out to avoid import-time initialization issues
# This will be handled on first request instead
# if not DATA_FILE.exists():
#     save_projects(get_sample_projects()) 