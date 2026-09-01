# ============================================================
# skills.py
# Central Skill Dictionary for ATS Resume Screening System
#
# SINGLE SOURCE OF TRUTH
#
# Contains:
#   1. Canonical skills
#   2. Skill aliases
#   3. Related skills
#   4. ATS keyword weights
#
# Designed to work with:
#   - skill_extractor.py
#   - keyword_extractor.py
#   - ranker.py
# ============================================================


# ============================================================
# CANONICAL SKILLS
# ============================================================

SKILLS = [

    # ========================================================
    # PROGRAMMING LANGUAGES
    # ========================================================

    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "php",
    "ruby",
    "go",
    "kotlin",
    "swift",
    "r",
    "scala",

    # ========================================================
    # WEB DEVELOPMENT
    # ========================================================

    "html",
    "css",
    "bootstrap",
    "tailwind css",

    "react",
    "angular",
    "vue",
    "next.js",
    "node.js",
    "express.js",

    "django",
    "flask",
    "fastapi",

    "rest api",
    "graphql",

    # ========================================================
    # DATABASES
    # ========================================================

    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",
    "sqlite",
    "redis",

    "database",
    "database management",

    # ========================================================
    # DATA
    # ========================================================

    "data analysis",
    "data analytics",
    "data cleaning",
    "data preprocessing",
    "data validation",
    "data visualization",
    "data reporting",
    "data quality",
    "data management",
    "data collection",
    "data interpretation",
    "data entry",
    "data extraction",

    "dataset",
    "dataset quality",

    # ========================================================
    # ARTIFICIAL INTELLIGENCE / MACHINE LEARNING
    # ========================================================

    "artificial intelligence",
    "machine learning",
    "deep learning",
    "data science",

    "natural language processing",
    "computer vision",
    "generative ai",

    "predictive modeling",
    "model training",
    "model evaluation",

    # ========================================================
    # PYTHON / DATA SCIENCE
    # ========================================================

    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "matplotlib",
    "seaborn",

    "statistics",

    # ========================================================
    # DATA ANNOTATION / AI OPERATIONS
    # ========================================================

    "data annotation",
    "data labeling",
    "image annotation",
    "text annotation",
    "video annotation",
    "audio annotation",
    "lidar annotation",

    "annotation tools",

    "bounding box annotation",
    "polygon annotation",
    "semantic segmentation",
    "instance segmentation",
    "image classification",
    "object detection",

    # ========================================================
    # QUALITY
    # ========================================================

    "quality assurance",
    "quality control",
    "quality checking",
    "quality inspection",

    # ========================================================
    # CLOUD
    # ========================================================

    "aws",
    "azure",
    "google cloud",

    # ========================================================
    # DEVOPS
    # ========================================================

    "docker",
    "kubernetes",
    "git",
    "github",
    "gitlab",
    "jenkins",
    "linux",

    "ci/cd",
    "continuous integration",
    "continuous deployment",

    # ========================================================
    # OFFICE / PRODUCTIVITY
    # ========================================================

    "excel",
    "word",
    "powerpoint",
    "outlook",

    # ========================================================
    # BUSINESS INTELLIGENCE
    # ========================================================

    "power bi",
    "tableau",
    "looker",

    "business intelligence",
    "business analysis",

    # ========================================================
    # ACCOUNTING / FINANCE
    # ========================================================

    "tally",
    "accounting",
    "bookkeeping",
    "financial analysis",
    "financial reporting",

    # ========================================================
    # MARKETING
    # ========================================================

    "digital marketing",
    "seo",
    "sem",
    "social media marketing",
    "content marketing",
    "google ads",
    "email marketing",

    # ========================================================
    # HUMAN RESOURCES
    # ========================================================

    "recruitment",
    "talent acquisition",
    "human resources",
    "payroll",
    "employee relations",
    "hr operations",

    # ========================================================
    # PROJECT / OPERATIONS
    # ========================================================

    "project management",
    "project coordination",
    "process improvement",
    "process management",
    "workflow management",
    "risk management",

    # ========================================================
    # PROFESSIONAL SKILLS
    # ========================================================

    "communication",
    "leadership",
    "teamwork",
    "problem solving",
    "time management",

    "public speaking",
    "team building",

    "attention to detail",
    "critical thinking",
    "analytical thinking",
    "decision making",

    "adaptability",
    "multitasking",
    "organization",
    "organizational skills",

    "customer service",
    "customer support",

    "stakeholder management",

    "documentation",
    "reporting",
    "research",
    "training",
    "mentoring",

    # ========================================================
    # GENERAL WORK SKILLS
    # ========================================================

    "accuracy",
    "productivity",
    "deadline management",
    "confidentiality",
]


# ============================================================
# SKILL ALIASES
#
# Alias -> canonical skill
#
# IMPORTANT:
# Aliases should only represent genuine equivalent forms.
# Do NOT map vague words to unrelated skills.
# ============================================================

SKILL_ALIASES = {

    # ========================================================
    # EXCEL
    # ========================================================

    "excel": "excel",
    "ms excel": "excel",
    "microsoft excel": "excel",
    "microsoft office excel": "excel",
    "ms office excel": "excel",

    # ========================================================
    # WORD
    # ========================================================

    "word": "word",
    "ms word": "word",
    "microsoft word": "word",
    "microsoft office word": "word",

    # ========================================================
    # POWERPOINT
    # ========================================================

    "powerpoint": "powerpoint",
    "power point": "powerpoint",
    "ms powerpoint": "powerpoint",
    "microsoft powerpoint": "powerpoint",
    "microsoft office powerpoint": "powerpoint",

    # ========================================================
    # OUTLOOK
    # ========================================================

    "outlook": "outlook",
    "ms outlook": "outlook",
    "microsoft outlook": "outlook",

    # ========================================================
    # POWER BI
    # ========================================================

    "power bi": "power bi",
    "power-bi": "power bi",
    "powerbi": "power bi",
    "microsoft power bi": "power bi",

    # ========================================================
    # TABLEAU
    # ========================================================

    "tableau": "tableau",

    # ========================================================
    # LOOKER
    # ========================================================

    "looker": "looker",
    "looker studio": "looker",

    # ========================================================
    # ARTIFICIAL INTELLIGENCE
    # ========================================================

    "ai": "artificial intelligence",
    "a i": "artificial intelligence",
    "a.i": "artificial intelligence",
    "a.i.": "artificial intelligence",
    "artificial intelligence": "artificial intelligence",

    # ========================================================
    # MACHINE LEARNING
    # ========================================================

    "ml": "machine learning",
    "m l": "machine learning",
    "m.l": "machine learning",
    "m.l.": "machine learning",
    "machine learning": "machine learning",

    # ========================================================
    # DEEP LEARNING
    # ========================================================

    "deep learning": "deep learning",
    "deep-learning": "deep learning",

    # ========================================================
    # GENERATIVE AI
    # ========================================================

    "gen ai": "generative ai",
    "genai": "generative ai",
    "generative ai": "generative ai",
    "generative artificial intelligence": "generative ai",

    # ========================================================
    # PYTHON
    # ========================================================

    "python": "python",
    "python programming": "python",
    "python language": "python",
    "python programming language": "python",

    # ========================================================
    # JAVA
    # ========================================================

    "java": "java",
    "java programming": "java",

    # ========================================================
    # JAVASCRIPT
    # ========================================================

    "js": "javascript",
    "javascript": "javascript",
    "javascript programming": "javascript",

    # ========================================================
    # TYPESCRIPT
    # ========================================================

    "ts": "typescript",
    "typescript": "typescript",

    # ========================================================
    # C++
    # ========================================================

    "cpp": "c++",
    "c plus plus": "c++",
    "c++": "c++",

    # ========================================================
    # C#
    # ========================================================

    "c sharp": "c#",
    "c-sharp": "c#",
    "c#": "c#",

    # ========================================================
    # NODE.JS
    # ========================================================

    "node.js": "node.js",
    "nodejs": "node.js",
    "node js": "node.js",

    # ========================================================
    # EXPRESS.JS
    # ========================================================

    "express": "express.js",
    "expressjs": "express.js",
    "express js": "express.js",
    "express.js": "express.js",

    # ========================================================
    # NEXT.JS
    # ========================================================

    "next.js": "next.js",
    "nextjs": "next.js",
    "next js": "next.js",

    # ========================================================
    # REST API
    # ========================================================

    "rest api": "rest api",
    "rest apis": "rest api",
    "restful api": "rest api",
    "restful apis": "rest api",
    "rest-api": "rest api",

    # ========================================================
    # GRAPHQL
    # ========================================================

    "graphql": "graphql",
    "graph ql": "graphql",

    # ========================================================
    # SQL
    # ========================================================

    "sql": "sql",
    "sql query": "sql",
    "sql queries": "sql",
    "structured query language": "sql",

    # ========================================================
    # MYSQL
    # ========================================================

    "mysql": "mysql",
    "mysql database": "mysql",
    "my sql": "mysql",

    # ========================================================
    # POSTGRESQL
    # ========================================================

    "postgres": "postgresql",
    "postgresql": "postgresql",
    "postgre sql": "postgresql",
    "postgres database": "postgresql",

    # ========================================================
    # MONGODB
    # ========================================================

    "mongo": "mongodb",
    "mongo db": "mongodb",
    "mongodb": "mongodb",
    "mongodb database": "mongodb",

    # ========================================================
    # SQLITE
    # ========================================================

    "sqlite": "sqlite",
    "sqlite3": "sqlite",

    # ========================================================
    # DATABASE
    # ========================================================

    "database": "database",
    "databases": "database",
    "db": "database",
    "dbms": "database",
    "database management": "database management",

    # ========================================================
    # SCIKIT-LEARN
    # ========================================================

    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "scikit-learn": "scikit-learn",

    # ========================================================
    # PANDAS
    # ========================================================

    "pandas": "pandas",

    # ========================================================
    # NUMPY
    # ========================================================

    "numpy": "numpy",

    # ========================================================
    # TENSORFLOW
    # ========================================================

    "tensorflow": "tensorflow",
    "tensor flow": "tensorflow",

    # ========================================================
    # PYTORCH
    # ========================================================

    "pytorch": "pytorch",
    "py torch": "pytorch",

    # ========================================================
    # DATA ANALYSIS
    # ========================================================

    "data analysis": "data analysis",
    "data-analysis": "data analysis",
    "data analyses": "data analysis",
    "data analyst": "data analysis",
    "data analysts": "data analysis",

    # ========================================================
    # DATA ANALYTICS
    # ========================================================

    "data analytics": "data analytics",
    "data-analytics": "data analytics",
    "data analystics": "data analytics",

    # ========================================================
    # DATA CLEANING
    # ========================================================

    "data cleaning": "data cleaning",
    "data-cleaning": "data cleaning",
    "data cleansing": "data cleaning",

    # ========================================================
    # DATA PREPROCESSING
    # ========================================================

    "data preprocessing": "data preprocessing",
    "data-preprocessing": "data preprocessing",
    "data pre processing": "data preprocessing",
    "data pre-processing": "data preprocessing",

    # ========================================================
    # DATA VALIDATION
    # ========================================================

    "data validation": "data validation",
    "data-validation": "data validation",
    "data checks": "data validation",
    "data checking": "data validation",
    "data verification": "data validation",

    # ========================================================
    # DATA VISUALIZATION
    # ========================================================

    "data visualization": "data visualization",
    "data-visualization": "data visualization",
    "data visualisation": "data visualization",
    "data-visualisation": "data visualization",

    # ========================================================
    # DATA REPORTING
    # ========================================================

    "data reporting": "data reporting",
    "data-reporting": "data reporting",

    # ========================================================
    # DATA QUALITY
    # ========================================================

    "data quality": "data quality",
    "data-quality": "data quality",
    "data quality check": "data quality",
    "data quality checks": "data quality",
    "data quality checking": "data quality",

    # ========================================================
    # DATA MANAGEMENT
    # ========================================================

    "data management": "data management",
    "data-management": "data management",

    # ========================================================
    # DATA COLLECTION
    # ========================================================

    "data collection": "data collection",
    "data-collection": "data collection",

    # ========================================================
    # DATA ENTRY
    # ========================================================

    "data entry": "data entry",
    "data-entry": "data entry",

    # ========================================================
    # DATA EXTRACTION
    # ========================================================

    "data extraction": "data extraction",
    "data-extraction": "data extraction",

    # ========================================================
    # DATA ANNOTATION
    # ========================================================

    "data annotation": "data annotation",
    "data-annotation": "data annotation",
    "data labeling": "data labeling",
    "data labelling": "data labeling",
    "data-labeling": "data labeling",
    "data-labelling": "data labeling",

    # ========================================================
    # IMAGE ANNOTATION
    # ========================================================

    "image annotation": "image annotation",
    "image-annotation": "image annotation",
    "image labeling": "image annotation",
    "image labelling": "image annotation",
    "image-labeling": "image annotation",
    "image-labelling": "image annotation",

    # ========================================================
    # TEXT ANNOTATION
    # ========================================================

    "text annotation": "text annotation",
    "text-annotation": "text annotation",
    "text labeling": "text annotation",
    "text labelling": "text annotation",
    "text-labeling": "text annotation",
    "text-labelling": "text annotation",

    # ========================================================
    # VIDEO ANNOTATION
    # ========================================================

    "video annotation": "video annotation",
    "video-annotation": "video annotation",
    "video labeling": "video annotation",
    "video labelling": "video annotation",

    # ========================================================
    # AUDIO ANNOTATION
    # ========================================================

    "audio annotation": "audio annotation",
    "audio-annotation": "audio annotation",

    # ========================================================
    # LIDAR ANNOTATION
    # ========================================================

    "lidar annotation": "lidar annotation",
    "lidar-annotation": "lidar annotation",
    "lidar data annotation": "lidar annotation",
    "lidar labeling": "lidar annotation",

    # ========================================================
    # ANNOTATION TOOLS
    # ========================================================

    "annotation tool": "annotation tools",
    "annotation tools": "annotation tools",
    "annotation software": "annotation tools",

    # ========================================================
    # DATASET
    # ========================================================

    "dataset": "dataset",
    "datasets": "dataset",
    "data set": "dataset",
    "data sets": "dataset",

    # ========================================================
    # DATASET QUALITY
    # ========================================================

    "dataset quality": "dataset quality",
    "dataset-quality": "dataset quality",

    # ========================================================
    # BOUNDING BOX
    # ========================================================

    "bounding box annotation": "bounding box annotation",
    "bounding-box annotation": "bounding box annotation",
    "bounding boxes": "bounding box annotation",

    # ========================================================
    # POLYGON
    # ========================================================

    "polygon annotation": "polygon annotation",
    "polygon-annotation": "polygon annotation",

    # ========================================================
    # SEMANTIC SEGMENTATION
    # ========================================================

    "semantic segmentation": "semantic segmentation",
    "semantic-segmentation": "semantic segmentation",

    # ========================================================
    # INSTANCE SEGMENTATION
    # ========================================================

    "instance segmentation": "instance segmentation",
    "instance-segmentation": "instance segmentation",

    # ========================================================
    # IMAGE CLASSIFICATION
    # ========================================================

    "image classification": "image classification",
    "image-classification": "image classification",

    # ========================================================
    # OBJECT DETECTION
    # ========================================================

    "object detection": "object detection",
    "object-detection": "object detection",

    # ========================================================
    # QUALITY ASSURANCE
    # ========================================================

    "qa": "quality assurance",
    "q a": "quality assurance",
    "quality assurance": "quality assurance",
    "quality checking": "quality assurance",
    "quality check": "quality assurance",
    "quality checks": "quality assurance",

    # ========================================================
    # QUALITY CONTROL
    # ========================================================

    "qc": "quality control",
    "q c": "quality control",
    "quality control": "quality control",

    # ========================================================
    # COMMUNICATION
    # ========================================================

    "communication": "communication",
    "communication skills": "communication",
    "communication skill": "communication",

    # ========================================================
    # TEAMWORK
    # ========================================================

    "teamwork": "teamwork",
    "team work": "teamwork",
    "team-work": "teamwork",
    "team player": "teamwork",
    "team players": "teamwork",

    # ========================================================
    # PROBLEM SOLVING
    # ========================================================

    "problem solving": "problem solving",
    "problem-solving": "problem solving",
    "problem solving skills": "problem solving",
    "problem-solving skills": "problem solving",

    # ========================================================
    # TIME MANAGEMENT
    # ========================================================

    "time management": "time management",
    "time-management": "time management",

    # ========================================================
    # PROJECT MANAGEMENT
    # ========================================================

    "project management": "project management",
    "project-management": "project management",

    # ========================================================
    # PROJECT COORDINATION
    # ========================================================

    "project coordination": "project coordination",
    "project-coordination": "project coordination",

    # ========================================================
    # CRITICAL THINKING
    # ========================================================

    "critical thinking": "critical thinking",
    "critical-thinking": "critical thinking",

    # ========================================================
    # ANALYTICAL THINKING
    # ========================================================

    "analytical thinking": "analytical thinking",
    "analytical-thinking": "analytical thinking",

    # ========================================================
    # ATTENTION TO DETAIL
    # ========================================================

    "attention to detail": "attention to detail",
    "attention-to-detail": "attention to detail",
    "attention to details": "attention to detail",

    # ========================================================
    # PROCESS IMPROVEMENT
    # ========================================================

    "process improvement": "process improvement",
    "process-improvement": "process improvement",
    "process improvements": "process improvement",

    # ========================================================
    # PROCESS MANAGEMENT
    # ========================================================

    "process management": "process management",
    "process-management": "process management",

    # ========================================================
    # STATISTICS
    # ========================================================

    "statistics": "statistics",
    "statistical analysis": "statistics",
    "statistical analytics": "statistics",

    # ========================================================
    # REPORTING
    # ========================================================

    "reporting": "reporting",
    "report preparation": "reporting",
    "report generation": "reporting",

    # ========================================================
    # DOCUMENTATION
    # ========================================================

    "documentation": "documentation",
    "documenting": "documentation",
    "documented": "documentation",

    # ========================================================
    # BUSINESS INTELLIGENCE
    # ========================================================

    "business intelligence": "business intelligence",
    "business-intelligence": "business intelligence",
    "bi": "business intelligence",

    # ========================================================
    # BUSINESS ANALYSIS
    # ========================================================

    "business analysis": "business analysis",
    "business-analysis": "business analysis",

    # ========================================================
    # CUSTOMER SERVICE
    # ========================================================

    "customer service": "customer service",
    "customer-service": "customer service",

    # ========================================================
    # CUSTOMER SUPPORT
    # ========================================================

    "customer support": "customer support",
    "customer-support": "customer support",

    # ========================================================
    # RECRUITMENT
    # ========================================================

    "recruitment": "recruitment",
    "recruiting": "recruitment",
    "talent recruitment": "recruitment",

    # ========================================================
    # TALENT ACQUISITION
    # ========================================================

    "talent acquisition": "talent acquisition",
    "talent-acquisition": "talent acquisition",

    # ========================================================
    # HUMAN RESOURCES
    # ========================================================

    "human resources": "human resources",
    "human resource": "human resources",
    "hr": "human resources",

    # ========================================================
    # SEO
    # ========================================================

    "seo": "seo",
    "search engine optimization": "seo",

    # ========================================================
    # SEM
    # ========================================================

    "sem": "sem",
    "search engine marketing": "sem",

    # ========================================================
    # AWS
    # ========================================================

    "aws": "aws",
    "amazon web services": "aws",

    # ========================================================
    # AZURE
    # ========================================================

    "azure": "azure",
    "microsoft azure": "azure",

    # ========================================================
    # GOOGLE CLOUD
    # ========================================================

    "google cloud": "google cloud",
    "gcp": "google cloud",
    "google cloud platform": "google cloud",

    # ========================================================
    # DOCKER
    # ========================================================

    "docker": "docker",
    "docker containers": "docker",

    # ========================================================
    # KUBERNETES
    # ========================================================

    "kubernetes": "kubernetes",
    "k8s": "kubernetes",

    # ========================================================
    # GIT
    # ========================================================

    "git": "git",

    # ========================================================
    # GITHUB
    # ========================================================

    "github": "github",
    "git hub": "github",

    # ========================================================
    # GITLAB
    # ========================================================

    "gitlab": "gitlab",
    "git lab": "gitlab",

    # ========================================================
    # LINUX
    # ========================================================

    "linux": "linux",

    # ========================================================
    # CI/CD
    # ========================================================

    "ci/cd": "ci/cd",
    "ci cd": "ci/cd",
    "cicd": "ci/cd",
    "continuous integration": "continuous integration",
    "continuous deployment": "continuous deployment",

    # ========================================================
    # ACCOUNTING
    # ========================================================

    "accounting": "accounting",
    "accountancy": "accounting",

    # ========================================================
    # BOOKKEEPING
    # ========================================================

    "bookkeeping": "bookkeeping",
    "book keeping": "bookkeeping",

    # ========================================================
    # FINANCIAL ANALYSIS
    # ========================================================

    "financial analysis": "financial analysis",
    "financial-analysis": "financial analysis",

    # ========================================================
    # FINANCIAL REPORTING
    # ========================================================

    "financial reporting": "financial reporting",
    "financial-reporting": "financial reporting",

    # ========================================================
    # TALLY
    # ========================================================

    "tally": "tally",
    "tally erp": "tally",
    "tally erp 9": "tally",
    "tally prime": "tally",
}


# ============================================================
# RELATED SKILLS
#
# These are partial relationships.
#
# They MUST NOT be treated as exact matches.
#
# Example:
#
# MySQL -> SQL = 0.95
#
# This means MySQL provides strong evidence for SQL,
# but MySQL is still kept as its own skill.
# ============================================================

RELATED_SKILLS = {

    # ========================================================
    # DATABASES
    # ========================================================

    "mysql": {
        "sql": 0.95,
        "database": 0.80,
    },

    "postgresql": {
        "sql": 0.95,
        "database": 0.80,
    },

    "oracle": {
        "sql": 0.90,
        "database": 0.80,
    },

    "sqlite": {
        "sql": 0.90,
        "database": 0.80,
    },

    "mongodb": {
        "database": 0.90,
    },

    "redis": {
        "database": 0.70,
    },

    # ========================================================
    # QUALITY
    # ========================================================

    "quality assurance": {
        "data validation": 0.45,
        "data quality": 0.65,
        "quality control": 0.75,
    },

    "quality control": {
        "data validation": 0.50,
        "data quality": 0.70,
        "quality assurance": 0.75,
    },

    "quality checking": {
        "quality assurance": 0.80,
        "quality control": 0.75,
        "data quality": 0.65,
    },

    # ========================================================
    # ANNOTATION
    # ========================================================

    "data annotation": {
        "data quality": 0.65,
        "data validation": 0.35,
        "dataset quality": 0.60,
    },

    "data labeling": {
        "data annotation": 0.95,
        "data quality": 0.55,
        "dataset quality": 0.60,
    },

    "image annotation": {
        "data annotation": 0.85,
        "data quality": 0.55,
        "computer vision": 0.25,
    },

    "text annotation": {
        "data annotation": 0.85,
        "data quality": 0.55,
        "natural language processing": 0.25,
    },

    "video annotation": {
        "data annotation": 0.85,
        "data quality": 0.55,
    },

    "audio annotation": {
        "data annotation": 0.85,
    },

    "lidar annotation": {
        "data annotation": 0.85,
        "data quality": 0.55,
        "computer vision": 0.25,
    },

    "bounding box annotation": {
        "image annotation": 0.90,
        "object detection": 0.65,
        "data annotation": 0.85,
    },

    "polygon annotation": {
        "image annotation": 0.90,
        "semantic segmentation": 0.70,
        "data annotation": 0.85,
    },

    "semantic segmentation": {
        "image annotation": 0.70,
        "computer vision": 0.75,
        "object detection": 0.35,
    },

    "instance segmentation": {
        "image annotation": 0.70,
        "computer vision": 0.75,
        "object detection": 0.50,
    },

    "image classification": {
        "image annotation": 0.60,
        "computer vision": 0.70,
    },

    "object detection": {
        "computer vision": 0.75,
        "image annotation": 0.55,
    },

    # ========================================================
    # DATA ANALYSIS
    # ========================================================

    "data analysis": {
        "data analytics": 0.90,
        "business analysis": 0.65,
        "data interpretation": 0.60,
        "statistics": 0.45,
    },

    "data analytics": {
        "data analysis": 0.90,
        "business analysis": 0.60,
        "statistics": 0.45,
    },

    "data visualization": {
        "power bi": 0.75,
        "tableau": 0.75,
        "data analysis": 0.55,
        "reporting": 0.45,
    },

    "data reporting": {
        "reporting": 0.90,
        "data analysis": 0.25,
    },

    "data validation": {
        "data quality": 0.75,
        "quality assurance": 0.45,
        "quality control": 0.50,
    },

    "data quality": {
        "data validation": 0.75,
        "dataset quality": 0.80,
        "quality assurance": 0.65,
        "quality control": 0.70,
    },

    "dataset quality": {
        "data quality": 0.80,
        "data annotation": 0.60,
        "data validation": 0.50,
    },

    # ========================================================
    # EXCEL
    # ========================================================

    "excel": {
        "data analysis": 0.25,
        "reporting": 0.30,
        "data reporting": 0.30,
        "data entry": 0.40,
    },

    # ========================================================
    # PANDAS
    # ========================================================

    "pandas": {
        "data analysis": 0.60,
        "data cleaning": 0.55,
        "data preprocessing": 0.55,
        "python": 0.75,
    },

    # ========================================================
    # NUMPY
    # ========================================================

    "numpy": {
        "python": 0.75,
        "data science": 0.50,
        "data analysis": 0.40,
    },

    # ========================================================
    # POWER BI
    # ========================================================

    "power bi": {
        "data visualization": 0.90,
        "reporting": 0.65,
        "business intelligence": 0.80,
    },

    # ========================================================
    # TABLEAU
    # ========================================================

    "tableau": {
        "data visualization": 0.90,
        "reporting": 0.60,
        "business intelligence": 0.75,
    },

    # ========================================================
    # PYTHON
    # ========================================================

    "python": {
        "data analysis": 0.25,
        "data science": 0.40,
        "machine learning": 0.30,
    },

    # ========================================================
    # MACHINE LEARNING
    # ========================================================

    "machine learning": {
        "artificial intelligence": 0.90,
        "data science": 0.45,
        "deep learning": 0.65,
    },

    # ========================================================
    # ARTIFICIAL INTELLIGENCE
    # ========================================================

    "artificial intelligence": {
        "machine learning": 0.90,
        "computer vision": 0.45,
        "natural language processing": 0.45,
    },

    # ========================================================
    # COMPUTER VISION
    # ========================================================

    "computer vision": {
        "artificial intelligence": 0.65,
        "machine learning": 0.55,
        "image annotation": 0.30,
        "object detection": 0.60,
    },

    # ========================================================
    # NLP
    # ========================================================

    "natural language processing": {
        "artificial intelligence": 0.65,
        "machine learning": 0.55,
        "text annotation": 0.30,
    },

    # ========================================================
    # PROFESSIONAL SKILLS
    # ========================================================

    "analytical thinking": {
        "data analysis": 0.30,
        "critical thinking": 0.65,
    },

    "problem solving": {
        "analytical thinking": 0.40,
        "critical thinking": 0.45,
    },

    "attention to detail": {
        "quality assurance": 0.35,
        "quality control": 0.35,
        "data quality": 0.30,
    },

    "process improvement": {
        "process management": 0.65,
        "project management": 0.25,
    },

    "project coordination": {
        "project management": 0.75,
        "process management": 0.35,
    },

    # ========================================================
    # BUSINESS
    # ========================================================

    "business intelligence": {
        "business analysis": 0.70,
        "data analysis": 0.45,
        "data visualization": 0.50,
    },

}


# ============================================================
# ATS KEYWORD WEIGHTS
#
# Higher weight = more important keyword.
#
# 5.0 = very important
# 4.0-4.5 = highly important
# 3.0-3.5 = medium importance
# 2.0-2.5 = lower importance
# ============================================================

ATS_KEYWORDS = {

    # ========================================================
    # DATA
    # ========================================================

    "data analysis": 5.0,
    "data analytics": 5.0,
    "data cleaning": 5.0,
    "data preprocessing": 4.5,
    "data validation": 5.0,
    "data visualization": 5.0,
    "data reporting": 4.5,
    "data quality": 4.5,
    "data management": 4.0,
    "data collection": 3.5,
    "data interpretation": 4.0,
    "data entry": 2.5,
    "data extraction": 3.5,

    "dataset": 2.5,
    "dataset quality": 4.5,

    # ========================================================
    # PROGRAMMING
    # ========================================================

    "python": 5.0,
    "java": 4.5,
    "c": 3.5,
    "javascript": 4.5,
    "typescript": 4.0,
    "c++": 4.0,
    "c#": 4.0,
    "php": 3.5,
    "ruby": 3.5,
    "go": 3.5,
    "kotlin": 3.5,
    "swift": 3.5,
    "r": 3.5,
    "scala": 3.5,

    # ========================================================
    # WEB
    # ========================================================

    "html": 3.0,
    "css": 3.0,
    "bootstrap": 3.0,
    "tailwind css": 3.0,
    "react": 4.0,
    "angular": 4.0,
    "vue": 4.0,
    "next.js": 4.0,
    "node.js": 4.0,
    "express.js": 4.0,
    "django": 4.0,
    "flask": 4.0,
    "fastapi": 4.0,
    "rest api": 4.0,
    "graphql": 4.0,

    # ========================================================
    # DATABASES
    # ========================================================

    "sql": 5.0,
    "mysql": 4.5,
    "postgresql": 4.5,
    "mongodb": 4.0,
    "oracle": 4.0,
    "sqlite": 3.5,
    "redis": 3.5,
    "database": 2.5,
    "database management": 3.5,

    # ========================================================
    # AI / ML
    # ========================================================

    "machine learning": 5.0,
    "artificial intelligence": 5.0,
    "deep learning": 4.5,
    "data science": 4.5,
    "computer vision": 4.5,
    "natural language processing": 4.5,
    "generative ai": 4.5,

    "predictive modeling": 4.0,
    "model training": 4.0,
    "model evaluation": 4.0,

    # ========================================================
    # PYTHON ECOSYSTEM
    # ========================================================

    "pandas": 4.5,
    "numpy": 4.0,
    "scikit-learn": 4.5,
    "tensorflow": 4.0,
    "pytorch": 4.0,
    "matplotlib": 3.5,
    "seaborn": 3.5,
    "statistics": 4.0,

    # ========================================================
    # ANNOTATION
    # ========================================================

    "data annotation": 5.0,
    "data labeling": 5.0,
    "image annotation": 5.0,
    "text annotation": 5.0,
    "video annotation": 5.0,
    "audio annotation": 4.5,
    "lidar annotation": 5.0,

    "annotation tools": 4.0,
    "bounding box annotation": 4.5,
    "polygon annotation": 4.5,
    "semantic segmentation": 4.5,
    "instance segmentation": 4.5,
    "image classification": 4.0,
    "object detection": 4.5,

    # ========================================================
    # QUALITY
    # ========================================================

    "quality assurance": 4.5,
    "quality control": 4.5,
    "quality checking": 4.0,
    "quality inspection": 3.5,

    # ========================================================
    # CLOUD / DEVOPS
    # ========================================================

    "aws": 4.0,
    "azure": 4.0,
    "google cloud": 4.0,

    "docker": 4.0,
    "kubernetes": 4.0,

    "git": 3.5,
    "github": 3.0,
    "gitlab": 3.0,
    "jenkins": 3.5,
    "linux": 3.5,

    "ci/cd": 4.0,
    "continuous integration": 3.5,
    "continuous deployment": 3.5,

    # ========================================================
    # OFFICE / BI
    # ========================================================

    "excel": 4.0,
    "power bi": 4.5,
    "tableau": 4.5,
    "looker": 4.0,

    "word": 2.0,
    "powerpoint": 2.5,
    "outlook": 2.0,

    "business intelligence": 4.0,
    "business analysis": 4.0,

    # ========================================================
    # ACCOUNTING / FINANCE
    # ========================================================

    "accounting": 4.0,
    "bookkeeping": 4.0,
    "financial analysis": 4.5,
    "financial reporting": 4.0,
    "tally": 4.0,

    # ========================================================
    # MARKETING
    # ========================================================

    "digital marketing": 4.0,
    "seo": 4.0,
    "sem": 4.0,
    "social media marketing": 3.5,
    "content marketing": 3.5,
    "google ads": 4.0,
    "email marketing": 3.5,

    # ========================================================
    # HR
    # ========================================================

    "recruitment": 4.0,
    "talent acquisition": 4.5,
    "human resources": 4.0,
    "payroll": 4.0,
    "employee relations": 3.5,
    "hr operations": 3.5,

    # ========================================================
    # PROJECT / OPERATIONS
    # ========================================================

    "project management": 3.5,
    "project coordination": 3.0,
    "process improvement": 3.5,
    "process management": 3.0,
    "workflow management": 3.0,
    "risk management": 3.0,

    # ========================================================
    # PROFESSIONAL
    # ========================================================

    "communication": 3.0,
    "leadership": 3.0,
    "teamwork": 3.0,
    "problem solving": 3.0,
    "time management": 2.0,

    "public speaking": 2.5,
    "team building": 2.5,

    "attention to detail": 4.0,
    "critical thinking": 3.0,
    "analytical thinking": 4.0,
    "decision making": 3.0,

    "adaptability": 2.5,
    "multitasking": 2.0,
    "organization": 2.5,
    "organizational skills": 2.5,

    "customer service": 3.5,
    "customer support": 3.5,

    "stakeholder management": 3.5,

    "documentation": 2.5,
    "reporting": 3.5,
    "research": 2.5,
    "training": 2.5,
    "mentoring": 2.5,

    # ========================================================
    # GENERAL
    # ========================================================

    "accuracy": 3.0,
    "productivity": 2.0,
    "deadline management": 2.5,
    "confidentiality": 2.5,
}


# ============================================================
# VALIDATION
# ============================================================

def validate_skill_dictionary():
    """
    Validate the complete skills dictionary.

    Returns:
        list[str]: validation errors
    """

    errors = []

    # --------------------------------------------------------
    # Canonical skill normalization
    # --------------------------------------------------------

    canonical_skills = {
        str(skill).strip().lower()
        for skill in SKILLS
        if str(skill).strip()
    }

    # --------------------------------------------------------
    # Duplicate canonical skills
    # --------------------------------------------------------

    normalized_skills = [
        str(skill).strip().lower()
        for skill in SKILLS
        if str(skill).strip()
    ]

    seen = set()
    duplicates = set()

    for skill in normalized_skills:

        if skill in seen:
            duplicates.add(skill)

        seen.add(skill)

    for skill in sorted(duplicates):

        errors.append(
            f"Duplicate canonical skill: '{skill}'"
        )

    # --------------------------------------------------------
    # Alias validation
    # --------------------------------------------------------

    for alias, canonical in SKILL_ALIASES.items():

        alias_clean = str(alias).strip().lower()
        canonical_clean = str(canonical).strip().lower()

        if not alias_clean:

            errors.append(
                "Empty skill alias found."
            )

            continue

        if not canonical_clean:

            errors.append(
                f"Empty canonical skill for alias: '{alias}'"
            )

            continue

        if canonical_clean not in canonical_skills:

            errors.append(
                f"Alias '{alias}' points to unknown "
                f"canonical skill '{canonical_clean}'"
            )

    # --------------------------------------------------------
    # Related skills validation
    # --------------------------------------------------------

    for source, related in RELATED_SKILLS.items():

        source_clean = str(source).strip().lower()

        if source_clean not in canonical_skills:

            errors.append(
                f"Related skill source '{source}' "
                f"is not in SKILLS"
            )

        if not isinstance(related, dict):

            errors.append(
                f"Related skills for '{source}' "
                f"must be a dictionary."
            )

            continue

        for target, score in related.items():

            target_clean = str(target).strip().lower()

            if target_clean not in canonical_skills:

                errors.append(
                    f"Related skill target '{target}' "
                    f"is not in SKILLS"
                )

            try:

                numeric_score = float(score)

                if not 0.0 <= numeric_score <= 1.0:

                    errors.append(
                        f"Invalid related score: "
                        f"{source} -> {target} = "
                        f"{numeric_score}"
                    )

            except (TypeError, ValueError):

                errors.append(
                    f"Invalid related score: "
                    f"{source} -> {target} = {score}"
                )

    # --------------------------------------------------------
    # ATS keyword validation
    # --------------------------------------------------------

    for keyword, weight in ATS_KEYWORDS.items():

        keyword_clean = str(keyword).strip().lower()

        if not keyword_clean:

            errors.append(
                "Empty ATS keyword found."
            )

            continue

        try:

            numeric_weight = float(weight)

            if numeric_weight <= 0:

                errors.append(
                    f"Invalid ATS weight: "
                    f"{keyword} = {numeric_weight}"
                )

        except (TypeError, ValueError):

            errors.append(
                f"Invalid ATS weight: "
                f"{keyword} = {weight}"
            )

    return errors


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    errors = validate_skill_dictionary()

    print()
    print("=" * 60)
    print("ATS SKILLS DICTIONARY TEST")
    print("=" * 60)

    print(
        "Canonical skills:",
        len(SKILLS)
    )

    print(
        "Aliases:",
        len(SKILL_ALIASES)
    )

    print(
        "Related skill groups:",
        len(RELATED_SKILLS)
    )

    print(
        "ATS keywords:",
        len(ATS_KEYWORDS)
    )

    print()

    if errors:

        print("ERRORS FOUND:")

        for error in errors:

            print("✗", error)

    else:

        print(
            "✓ Skill dictionary is valid."
        )

        print(
            "✓ No duplicate canonical skills."
        )

        print(
            "✓ No broken aliases."
        )

        print(
            "✓ No invalid related-skill scores."
        )

        print(
            "✓ No invalid ATS weights."
        )

    print("=" * 60)