import json
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CORE_DIR = BASE_DIR / "core"
os.makedirs(CORE_DIR, exist_ok=True)

career_db_path = CORE_DIR / "career_database.json"
skills_db_path = CORE_DIR / "skills_database.json"

# Definition of 100+ Careers
careers = [
    # Software Engineering
    {
        "career_name": "Software Engineer",
        "category": "Software Engineering",
        "description": "Develops and maintains software applications using engineering principles.",
        "required_skills": ["Python", "Java", "C++", "C#", "SQL", "Git"],
        "preferred_skills": ["Docker", "Go", "Golang", "Algorithms", "Data Structures", "REST APIs", "CI/CD", "JavaScript", "TypeScript", "React", "Node.js", "FastAPI", "AWS", "Cloud Computing"],
        "required_keywords": ["software engineer", "software developer", "coder", "programmer", "systems developer", "development", "developer", "software", "programming"],
        "related_careers": ["Full Stack Developer", "Backend Developer", "DevOps Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Full Stack Developer",
        "category": "Software Engineering",
        "description": "Designs and builds both frontend and backend components of web applications.",
        "required_skills": ["React", "Node.js", "Express.js", "MongoDB", "SQL", "JavaScript", "TypeScript"],
        "preferred_skills": ["HTML5", "CSS3", "Git", "Redux", "Docker", "REST APIs", "FastAPI", "Next.js", "Tailwind CSS"],
        "required_keywords": ["full stack", "fullstack", "web developer", "front end", "back end", "mern", "javascript", "typescript"],
        "related_careers": ["Frontend Developer", "Backend Developer", "Software Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Frontend Developer",
        "category": "Software Engineering",
        "description": "Specializes in developing the visual and interactive parts of web applications.",
        "required_skills": ["React", "JavaScript", "TypeScript", "HTML5", "CSS3", "Tailwind CSS"],
        "preferred_skills": ["Redux", "Vite", "Webpack", "Angular", "Vue.js", "Svelte", "Bootstrap", "Next.js"],
        "required_keywords": ["frontend", "front-end", "ui developer", "react developer", "web designer", "interface developer"],
        "related_careers": ["Full Stack Developer", "UI Designer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Backend Developer",
        "category": "Software Engineering",
        "description": "Builds and manages server-side logic, databases, APIs, and application performance.",
        "required_skills": ["Node.js", "Express.js", "FastAPI", "Django", "SQL", "Databases"],
        "preferred_skills": ["MongoDB", "PostgreSQL", "Redis", "Docker", "REST APIs", "NestJS", "Spring Boot", "Git"],
        "required_keywords": ["backend", "back-end", "server developer", "api developer", "database developer", "express", "django", "fastapi"],
        "related_careers": ["Full Stack Developer", "Software Engineer", "Database Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Embedded Systems Engineer",
        "category": "Software Engineering",
        "description": "Designs and programs firmware for hardware devices and microcontrollers.",
        "required_skills": ["C", "C++", "Assembly", "Microcontrollers"],
        "preferred_skills": ["FreeRTOS", "Linux", "SPI", "I2C", "ARM Architecture", "RTOS"],
        "related_careers": ["Robotics Engineer", "IoT Engineer"],
        "difficulty_level": "High",
        "growth_level": "Medium",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Graphics Engineer",
        "category": "Software Engineering",
        "description": "Develops rendering systems, shaders, and graphical pipelines for visual apps.",
        "required_skills": ["C++", "OpenGL", "WebGL", "Shader Languages"],
        "preferred_skills": ["DirectX", "Vulkan", "Unity", "Unreal Engine", "Linear Algebra"],
        "related_careers": ["Game Developer", "VR Developer"],
        "difficulty_level": "High",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 75
    },
    {
        "career_name": "Middleware Developer",
        "category": "Software Engineering",
        "description": "Builds and configures services connecting software applications and systems.",
        "required_skills": ["Java", "C++", "Message Queues"],
        "preferred_skills": ["Kafka", "ActiveMQ", "gRPC", "RabbitMQ", "REST APIs"],
        "related_careers": ["Backend Developer", "Platform Engineer"],
        "difficulty_level": "High",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "Desktop Application Developer",
        "category": "Software Engineering",
        "description": "Creates software applications that run locally on computer operating systems.",
        "required_skills": ["C#", "Java", "C++"],
        "preferred_skills": ["Electron", "Qt", "WPF", "Windows Forms", "macOS SDK"],
        "related_careers": ["Software Engineer", "Frontend Developer"],
        "difficulty_level": "Medium",
        "growth_level": "Low",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    
    # Artificial Intelligence
    {
        "career_name": "AI Engineer",
        "category": "Artificial Intelligence",
        "description": "Designs and develops intelligent algorithms and artificial intelligence applications.",
        "required_skills": ["Python", "Machine Learning", "Deep Learning", "LLMs", "NLP", "Generative AI"],
        "preferred_skills": ["FastAPI", "PyTorch", "TensorFlow", "scikit-learn", "Git", "Docker", "AWS", "LangChain", "LlamaIndex"],
        "required_keywords": ["ai", "artificial intelligence", "neural network", "machine learning", "large language model", "gpt", "bert"],
        "related_careers": ["Machine Learning Engineer", "Generative AI Engineer", "NLP Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "AI Architect",
        "category": "Artificial Intelligence",
        "description": "Designs scalable enterprise-wide artificial intelligence architectures and systems.",
        "required_skills": ["AI Architecture", "System Design", "Cloud Architecture"],
        "preferred_skills": ["Python", "Machine Learning", "MLOps", "AWS", "Cloud Computing", "Kubernetes", "Vector Databases"],
        "related_careers": ["Solutions Architect", "AI Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 80
    },
    {
        "career_name": "NLP Engineer",
        "category": "Artificial Intelligence",
        "description": "Builds models and systems capable of understanding and parsing human language.",
        "required_skills": ["NLP", "Transformers", "BERT", "GPT"],
        "preferred_skills": ["Python", "Machine Learning", "Hugging Face", "PyTorch", "TensorFlow", "FastAPI"],
        "related_careers": ["AI Engineer", "Machine Learning Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Computer Vision Engineer",
        "category": "Artificial Intelligence",
        "description": "Develops algorithms to enable computers to extract information from images and videos.",
        "required_skills": ["Python", "OpenCV", "Computer Vision", "Deep Learning"],
        "preferred_skills": ["PyTorch", "TensorFlow", "CUDA", "C++", "Image Processing"],
        "related_careers": ["AI Engineer", "Robotics Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Generative AI Engineer",
        "category": "Artificial Intelligence",
        "description": "Creates applications based on large language models and generative AI networks.",
        "required_skills": ["Python", "Generative AI", "LLMs", "Prompt Engineering"],
        "preferred_skills": ["LangChain", "LlamaIndex", "Vector Databases", "Fine-Tuning", "RAG"],
        "related_careers": ["AI Engineer", "Prompt Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "AI Research Scientist",
        "category": "Artificial Intelligence",
        "description": "Researches and implements cutting-edge algorithms to advance state-of-the-art AI.",
        "required_skills": ["Mathematics", "Statistics", "Research Publications", "Neural Networks"],
        "preferred_skills": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "LaTeX", "TensorFlow"],
        "related_careers": ["Machine Learning Engineer", "AI Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 80
    },
    {
        "career_name": "Prompt Engineer",
        "category": "Artificial Intelligence",
        "description": "Specializes in optimizing input prompts to extract high-quality outputs from AI models.",
        "required_skills": ["Prompt Engineering", "Generative AI", "LLMs"],
        "preferred_skills": ["Python", "LangChain", "GPT", "RAG", "Text Generation"],
        "related_careers": ["Generative AI Engineer", "AI Writer"],
        "difficulty_level": "Low",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 65
    },

    # Machine Learning
    {
        "career_name": "Machine Learning Engineer",
        "category": "Machine Learning",
        "description": "Builds and deploys machine learning models into production systems.",
        "required_skills": ["Python", "Machine Learning", "Deep Learning", "scikit-learn"],
        "preferred_skills": ["SQL", "Docker", "Kubernetes", "AWS", "Git", "Pandas", "NumPy", "Keras", "OpenCV", "PyTorch", "TensorFlow", "MLOps"],
        "required_keywords": ["machine learning", "ml", "neural network", "model training", "predictive model", "scikit", "tensorflow", "pytorch"],
        "related_careers": ["AI Engineer", "Deep Learning Engineer", "Data Scientist"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Deep Learning Engineer",
        "category": "Machine Learning",
        "description": "Specializes in training deep neural networks for complex classification and generation.",
        "required_skills": ["Python", "Deep Learning", "Neural Networks", "PyTorch", "TensorFlow"],
        "preferred_skills": ["CUDA", "Docker", "MLOps", "High Performance Computing", "scikit-learn"],
        "related_careers": ["Machine Learning Engineer", "Computer Vision Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "MLOps Engineer",
        "category": "Machine Learning",
        "description": "Maintains pipeline automation, testing, and deployment systems for ML models.",
        "required_skills": ["Python", "MLOps", "Docker", "Kubernetes", "CI/CD"],
        "preferred_skills": ["MLflow", "Kubeflow", "AWS", "Terraform", "Jenkins", "Git"],
        "related_careers": ["DevOps Engineer", "Machine Learning Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "ML Research Engineer",
        "category": "Machine Learning",
        "description": "Bridges the gap between machine learning research and engineering implementation.",
        "required_skills": ["Mathematics", "Research Publications"],
        "preferred_skills": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "scikit-learn"],
        "related_careers": ["AI Research Scientist", "Machine Learning Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 80
    },
    {
        "career_name": "Reinforcement Learning Engineer",
        "category": "Machine Learning",
        "description": "Develops decision-making agents that learn through reward-based environments.",
        "required_skills": ["Reinforcement Learning", "OpenAI Gym"],
        "preferred_skills": ["Python", "Deep Learning", "PyTorch", "Algorithms"],
        "related_careers": ["Robotics Software Engineer", "AI Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 80
    },

    # Data Science
    {
        "career_name": "Data Scientist",
        "category": "Data Science",
        "description": "Performs statistical analysis, builds predictive models, and uncovers data-driven insights.",
        "required_skills": ["Python", "Statistics", "Machine Learning", "Data Analysis", "SQL"],
        "preferred_skills": ["Pandas", "NumPy", "Tableau", "Power BI", "Spark", "Data Visualization", "R"],
        "required_keywords": ["data science", "data scientist", "model", "analysis", "statistics", "statistical", "prediction"],
        "related_careers": ["Machine Learning Engineer", "Data Analyst", "Data Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Data Analyst",
        "category": "Data Science",
        "description": "Gathers, organizes, and parses data to create dashboards and reports for business stakeholders.",
        "required_skills": ["SQL", "Excel", "Data Analysis", "Tableau", "Statistics"],
        "preferred_skills": ["Python", "Power BI", "R", "Pandas", "Matplotlib", "Jira"],
        "required_keywords": ["data analyst", "reporting", "dashboard", "bi", "tableau", "power bi", "metrics", "analytics"],
        "related_careers": ["Data Scientist", "Business Analyst"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "High",
        "average_match_threshold": 65
    },
    {
        "career_name": "Data Engineer",
        "category": "Data Science",
        "description": "Constructs systems, databases, and pipelines to ingest, store, and process massive datasets.",
        "required_skills": ["SQL", "Python", "ETL", "Data Pipelines"],
        "preferred_skills": ["Apache Spark", "Kafka", "Airflow", "Snowflake", "Databases", "AWS", "BigQuery"],
        "related_careers": ["Database Engineer", "Big Data Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Business Intelligence Developer",
        "category": "Data Science",
        "description": "Designs, implements, and supports BI systems and analytics warehouses.",
        "required_skills": ["SQL", "Tableau", "Power BI", "Data Warehousing"],
        "preferred_skills": ["ETL", "Excel", "Data Modeling", "Databases"],
        "related_careers": ["Data Analyst", "Database Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Data Architect",
        "category": "Data Science",
        "description": "Defines the blueprint for managing data assets and aligning with enterprise goals.",
        "required_skills": ["SQL", "Data Modeling", "Data Architecture"],
        "preferred_skills": ["Snowflake", "BigQuery", "AWS", "Databases", "System Design"],
        "related_careers": ["Database Architect", "Data Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 80
    },
    {
        "career_name": "Big Data Engineer",
        "category": "Data Science",
        "description": "Specializes in processing datasets too large for standard relational database management.",
        "required_skills": ["Hadoop", "Apache Spark", "Java", "Scala", "Python"],
        "preferred_skills": ["Kafka", "Hive", "NoSQL Databases", "Cloud Computing"],
        "related_careers": ["Data Engineer", "Platform Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Quantitative Analyst",
        "category": "Data Science",
        "description": "Applies mathematical models to financial pricing and trading decisions.",
        "required_skills": ["Python", "Mathematics", "Statistics", "Quantitative Finance"],
        "preferred_skills": ["R", "SQL", "C++", "Algorithms"],
        "related_careers": ["Data Scientist", "AI Research Scientist"],
        "difficulty_level": "High",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 80
    },

    # Cloud Computing
    {
        "career_name": "Cloud Engineer",
        "category": "Cloud Computing",
        "description": "Configures, maintains, and supports cloud infrastructure and application environments.",
        "required_skills": ["AWS", "Cloud Computing", "Docker", "Linux"],
        "preferred_skills": ["Terraform", "Kubernetes", "CI/CD", "Python", "Bash"],
        "required_keywords": ["cloud", "aws", "gcp", "azure", "serverless", "infrastructure", "devops", "cloud architect"],
        "related_careers": ["Cloud Architect", "DevOps Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Cloud Architect",
        "category": "Cloud Computing",
        "description": "Designs secure, scalable, and cost-effective cloud architectures for companies.",
        "required_skills": ["AWS", "Cloud Architecture", "Cloud Computing"],
        "preferred_skills": ["Azure", "GCP", "Terraform", "Kubernetes", "System Design"],
        "related_careers": ["Cloud Engineer", "Solutions Architect"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 80
    },
    {
        "career_name": "Cloud Security Engineer",
        "category": "Cloud Computing",
        "description": "Focuses on securing resources and identities inside public cloud infrastructure.",
        "required_skills": ["Cloud Security", "AWS", "Cybersecurity"],
        "preferred_skills": ["Azure", "IAM", "Firewalls", "Network Security", "Docker"],
        "related_careers": ["Security Engineer", "Cloud Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Cloud Migrations Specialist",
        "category": "Cloud Computing",
        "description": "Orchestrates transition of legacy physical servers into virtualized cloud platforms.",
        "required_skills": ["Cloud Computing", "AWS", "Linux"],
        "preferred_skills": ["Database Migration", "DevOps", "Virtualization", "Docker"],
        "related_careers": ["Cloud Engineer", "System Administrator"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "Cloud Infrastructure Engineer",
        "category": "Cloud Computing",
        "description": "Designs infrastructure as code layouts to run system-level services.",
        "required_skills": ["Cloud Computing", "Infrastructure as Code", "AWS"],
        "preferred_skills": ["Terraform", "Docker", "Ansible", "Linux", "Bash"],
        "related_careers": ["Cloud Engineer", "Platform Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },

    # DevOps
    {
        "career_name": "DevOps Engineer",
        "category": "DevOps",
        "description": "Unites software development and operations through pipeline automation and tooling.",
        "required_skills": ["Docker", "Kubernetes", "CI/CD", "Git", "Linux", "Jenkins"],
        "preferred_skills": ["Terraform", "Ansible", "AWS", "Python", "Bash", "Prometheus"],
        "required_keywords": ["devops", "ci/cd", "deployment", "automation", "kubernetes", "docker", "jenkins", "pipelines"],
        "related_careers": ["Site Reliability Engineer", "Platform Engineer", "MLOps Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Build and Release Engineer",
        "category": "DevOps",
        "description": "Manages building, packaging, and testing application builds across testing servers.",
        "required_skills": ["CI/CD", "Git", "Jenkins", "scripting"],
        "preferred_skills": ["Maven", "Gradle", "Docker", "Bash", "GitHub Actions"],
        "related_careers": ["DevOps Engineer", "QA Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "CI/CD Specialist",
        "category": "DevOps",
        "description": "Designs robust pipelines to build, test, and release production workloads automatically.",
        "required_skills": ["CI/CD", "Jenkins", "GitHub Actions", "Git"],
        "preferred_skills": ["GitLab CI", "CircleCI", "Docker", "Ansible", "Linux"],
        "related_careers": ["DevOps Engineer", "Platform Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Platform Automation Engineer",
        "category": "DevOps",
        "description": "Automates operating system configurations, setups, and virtualized workloads.",
        "required_skills": ["scripting", "Ansible", "Terraform", "Docker"],
        "preferred_skills": ["Python", "Bash", "Linux", "Puppet", "Chef"],
        "related_careers": ["Platform Engineer", "DevOps Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "DevSecOps Engineer",
        "category": "DevOps",
        "description": "Integrates scanning tools and security checks directly inside deployment pipelines.",
        "required_skills": ["DevOps", "Cybersecurity", "CI/CD", "Docker"],
        "preferred_skills": ["Security Auditing", "Kubernetes", "Static Analysis", "Vulnerability Scanning"],
        "related_careers": ["Security Engineer", "DevOps Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },

    # Cybersecurity
    {
        "career_name": "Cybersecurity Analyst",
        "category": "Cybersecurity",
        "description": "Monitors endpoints and computer networks to report and block malicious events.",
        "required_skills": ["Network Security", "Information Security", "Firewalls", "Linux"],
        "preferred_skills": ["Python", "Wireshark", "Linux", "SIEM", "Incident Response"],
        "required_keywords": ["cybersecurity", "information security", "security analyst", "soc", "penetration", "threat", "vulnerability"],
        "related_careers": ["SOC Analyst", "Security Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "SOC Analyst",
        "category": "Cybersecurity",
        "description": "Monitors and analyzes logs inside a Security Operations Center environment.",
        "required_skills": ["Security Analytics", "SIEM", "Incident Response"],
        "preferred_skills": ["SOC Operations", "Threat Intelligence", "Wireshark", "Linux"],
        "related_careers": ["Cybersecurity Analyst", "Incident Responder"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 65
    },
    {
        "career_name": "Security Engineer",
        "category": "Cybersecurity",
        "description": "Builds secure networks, authorization pathways, and tests organizational cryptography.",
        "required_skills": ["Cybersecurity", "Cryptography", "Network Security"],
        "preferred_skills": ["Python", "Linux", "Identity Access Management", "Firewalls"],
        "related_careers": ["Cybersecurity Analyst", "Security Architect"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Penetration Tester",
        "category": "Cybersecurity",
        "description": "Finds system flaws by conducting ethical exploits against target corporate devices.",
        "required_skills": ["Penetration Testing", "Ethical Hacking", "Linux", "Kali Linux"],
        "preferred_skills": ["Python", "Metasploit", "Bash", "Web Application Hacking", "OWASP Top 10"],
        "related_careers": ["Security Engineer", "Vulnerability Analyst"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Incident Responder",
        "category": "Cybersecurity",
        "description": "Directs mitigation attempts during or immediately following system security breaches.",
        "required_skills": ["Incident Response", "Digital Forensics", "Cybersecurity"],
        "preferred_skills": ["SIEM", "Reverse Engineering", "Malware Analysis", "Linux"],
        "related_careers": ["SOC Analyst", "Security Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Vulnerability Analyst",
        "category": "Cybersecurity",
        "description": "Conducts regular scans to rank database flaws and network software gaps.",
        "required_skills": ["Vulnerability Assessment", "Cybersecurity"],
        "preferred_skills": ["Nessus", "Qualys", "Penetration Testing", "Risk Assessment"],
        "related_careers": ["Penetration Tester", "SOC Analyst"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Security Architect",
        "category": "Cybersecurity",
        "description": "Builds high-level structures, protocols, and policies governing data flow.",
        "required_skills": ["Security Architecture", "Cybersecurity", "Risk Assessment"],
        "preferred_skills": ["ISO 27001", "Compliance", "Identity Access Management", "Cloud Security"],
        "related_careers": ["Security Engineer", "Solutions Architect"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 80
    },
    {
        "career_name": "Cryptographer",
        "category": "Cybersecurity",
        "description": "Implements and refines algorithms, hash keys, and mathematics securing file storage.",
        "required_skills": ["Cryptography", "Mathematics", "Algorithms"],
        "preferred_skills": ["Python", "Rust", "C++", "Blockchain"],
        "related_careers": ["Security Engineer", "Blockchain Developer"],
        "difficulty_level": "High",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 80
    },

    # Networking
    {
        "career_name": "Network Engineer",
        "category": "Networking",
        "description": "Installs, tests, and configures routers and switches across corporate networks.",
        "required_skills": ["Networking", "Routers", "Switches", "TCP/IP"],
        "preferred_skills": ["Cisco CCNA", "Firewalls", "Network Security", "Linux"],
        "related_careers": ["Network Architect", "System Administrator"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "Network Architect",
        "category": "Networking",
        "description": "Draws blueprints for massive data center LANs and WAN setups.",
        "required_skills": ["Network Architecture", "Networking", "TCP/IP"],
        "preferred_skills": ["SDN", "Cisco CCNP", "Cloud Computing", "System Design"],
        "related_careers": ["Network Engineer", "Solutions Architect"],
        "difficulty_level": "High",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 80
    },
    {
        "career_name": "Network Security Engineer",
        "category": "Networking",
        "description": "Ensures that virtual and physical computer paths are sealed from hacking threats.",
        "required_skills": ["Network Security", "Firewalls", "VPN", "Networking"],
        "preferred_skills": ["IPS/IDS", "Cisco CCNA", "Wireshark", "Cybersecurity"],
        "related_careers": ["Security Engineer", "Network Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Telecommunications Engineer",
        "category": "Networking",
        "description": "Configures systems managing audio, voice, and wireless networks.",
        "required_skills": ["Telecom", "VoIP", "Networking"],
        "preferred_skills": ["SIP", "Wireless Protocols", "Routing Protocols"],
        "related_careers": ["Network Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "Low",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "Network Administrator",
        "category": "Networking",
        "description": "Manages day-to-day office router functions, DHCP IPs, and DNS tables.",
        "required_skills": ["Network Administration", "Networking", "DNS", "DHCP"],
        "preferred_skills": ["Linux", "Windows Server", "Active Directory", "IT Support"],
        "related_careers": ["Network Engineer", "System Administrator"],
        "difficulty_level": "Medium",
        "growth_level": "Low",
        "future_demand": "Medium",
        "average_match_threshold": 65
    },

    # Mobile Development
    {
        "career_name": "Mobile App Developer",
        "category": "Mobile Development",
        "description": "Builds interactive native and web application products for iOS and Android.",
        "required_skills": ["React Native", "Flutter", "Swift", "Kotlin", "Mobile Development"],
        "preferred_skills": ["iOS SDK", "Android SDK", "Git", "REST APIs", "TypeScript", "JavaScript"],
        "required_keywords": ["mobile developer", "app developer", "ios developer", "android developer", "flutter", "react native"],
        "related_careers": ["Android Developer", "iOS Developer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Android Developer",
        "category": "Mobile Development",
        "description": "Specializes in building native Google OS solutions using Kotlin or Java.",
        "required_skills": ["Kotlin", "Java", "Android SDK", "Android Studio"],
        "preferred_skills": ["Git", "REST APIs", "Mobile Development", "Jetpack Compose"],
        "related_careers": ["Mobile App Developer", "React Native Developer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "iOS Developer",
        "category": "Mobile Development",
        "description": "Specializes in native Apple OS applications using Swift or SwiftUI.",
        "required_skills": ["Swift", "iOS SDK", "Xcode", "SwiftUI"],
        "preferred_skills": ["Objective-C", "Git", "Mobile Development", "REST APIs"],
        "related_careers": ["Mobile App Developer", "Flutter Developer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Flutter Developer",
        "category": "Mobile Development",
        "description": "Uses the Dart framework to assemble hybrid compilation packages for mobile systems.",
        "required_skills": ["Flutter", "Dart", "Mobile Development"],
        "preferred_skills": ["Git", "REST APIs", "UI Design", "Firebase"],
        "related_careers": ["Mobile App Developer", "Android Developer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 65
    },
    {
        "career_name": "React Native Developer",
        "category": "Mobile Development",
        "description": "Builds mobile components utilizing React and JavaScript engines.",
        "required_skills": ["React Native"],
        "preferred_skills": ["JavaScript", "TypeScript", "React", "iOS SDK", "Android SDK", "Redux", "Git", "REST APIs"],
        "related_careers": ["Mobile App Developer", "Frontend Developer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 65
    },

    # Game Development
    {
        "career_name": "Game Developer",
        "category": "Game Development",
        "description": "Assembles gameplay, code logic, rendering routines, and physics models.",
        "required_skills": ["C++", "C#", "Unity", "Unreal Engine"],
        "preferred_skills": ["OpenGL", "DirectX", "Linear Algebra", "Physics Simulation", "Git"],
        "related_careers": ["Unity Game Developer", "Unreal Engine Developer"],
        "difficulty_level": "High",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "Unity Game Developer",
        "category": "Game Development",
        "description": "Creates 2D and 3D games within the Unity engine using C# coding patterns.",
        "required_skills": ["C#", "Unity", "3D Mathematics"],
        "preferred_skills": ["Git", "Shader Programming", "Animation Systems", "Mobile Development"],
        "related_careers": ["Game Developer", "AR Developer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "Unreal Engine Developer",
        "category": "Game Development",
        "description": "Builds high-fidelity game packages in Unreal Engine using C++ and Blueprints.",
        "required_skills": ["C++", "Unreal Engine", "Blueprints"],
        "preferred_skills": ["Git", "Physics Programming", "Shader Programming", "3D Mathematics"],
        "related_careers": ["Game Developer", "VR Developer"],
        "difficulty_level": "High",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 75
    },
    {
        "career_name": "Game Physics Programmer",
        "category": "Game Development",
        "description": "Writes code to handle vehicle physics, gravity, collision detection, and ragdolls.",
        "required_skills": ["C++", "Physics Simulation", "Mathematics"],
        "preferred_skills": ["Unreal Engine", "Linear Algebra", "Algorithms"],
        "related_careers": ["Game Developer", "Graphics Engineer"],
        "difficulty_level": "High",
        "growth_level": "Low",
        "future_demand": "Medium",
        "average_match_threshold": 80
    },
    {
        "career_name": "Gameplay Programmer",
        "category": "Game Development",
        "description": "Focuses on NPC behaviors, player controls, camera angles, and item scripts.",
        "required_skills": ["C++", "C#", "Gameplay Logic"],
        "preferred_skills": ["Unity", "Unreal Engine", "Git", "Algorithms"],
        "related_careers": ["Game Developer", "Unity Game Developer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "Game Producer",
        "category": "Game Development",
        "description": "Directs team tasks, calendars, releases, and milestones across game projects.",
        "required_skills": ["Game Production", "Project Management", "Agile"],
        "preferred_skills": ["Jira", "Confluence", "Leadership", "Game Design"],
        "related_careers": ["Project Manager", "Product Manager"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },

    # Blockchain
    {
        "career_name": "Blockchain Developer",
        "category": "Blockchain",
        "description": "Develops cryptography layers, coin databases, and smart contract frameworks.",
        "required_skills": ["Blockchain", "Smart Contracts", "Solidity", "Cryptography"],
        "preferred_skills": ["Ethereum", "Web3.js", "Go", "Rust", "Hyperledger"],
        "related_careers": ["Smart Contract Developer", "Blockchain Architect"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Smart Contract Developer",
        "category": "Blockchain",
        "description": "Writes self-executing automation files deployed to decentralized networks.",
        "required_skills": ["Smart Contracts", "Solidity", "Ethereum"],
        "preferred_skills": ["Rust", "Hardhat", "Truffle", "Web3.js", "Unit Testing"],
        "related_careers": ["Blockchain Developer", "Solidity Developer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Solidity Developer",
        "category": "Blockchain",
        "description": "Writes clean Solidity files to support EVM blockchain token structures.",
        "required_skills": ["Solidity", "Ethereum", "Smart Contracts"],
        "preferred_skills": ["Web3.js", "Truffle", "Hardhat", "JavaScript", "TypeScript"],
        "related_careers": ["Smart Contract Developer", "Blockchain Developer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Blockchain Architect",
        "category": "Blockchain",
        "description": "Designs layout, node infrastructure, consensus engines, and security setups.",
        "required_skills": ["Blockchain Architecture", "Cryptography", "Consensus Protocols"],
        "preferred_skills": ["Solidity", "System Design", "Go", "Rust", "Consensus Algorithms"],
        "related_careers": ["Solutions Architect", "Blockchain Developer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 80
    },
    {
        "career_name": "Cryptographic Protocols Engineer",
        "category": "Blockchain",
        "description": "Constructs zero-knowledge networks, consensus models, and hashing systems.",
        "required_skills": ["Cryptography", "Blockchain", "Mathematics"],
        "preferred_skills": ["Rust", "C++", "Algorithms", "Cryptographic Protocols"],
        "related_careers": ["Cryptographer", "Blockchain Developer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 80
    },

    # AR/VR
    {
        "career_name": "AR Developer",
        "category": "AR/VR",
        "description": "Projects computer-generated elements into actual real-world user feeds.",
        "required_skills": ["AR Development", "Unity", "C#"],
        "preferred_skills": ["ARKit", "ARCore", "Mobile Development", "3D Mathematics"],
        "related_careers": ["Unity AR/VR Developer", "VR Developer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "VR Developer",
        "category": "AR/VR",
        "description": "Assembles simulated 3D environments rendered in head-mounted display visors.",
        "required_skills": ["VR Development", "Unity", "Unreal Engine", "C++"],
        "preferred_skills": ["OpenXR", "WebXR", "OpenGL", "Shader Programming", "3D Mathematics"],
        "related_careers": ["AR Developer", "Unreal Engine Developer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Mixed Reality Engineer",
        "category": "AR/VR",
        "description": "Blends virtual assets and real items inside specialized visor hardware interfaces.",
        "required_skills": ["Unity", "C#", "Mixed Reality"],
        "preferred_skills": ["HoloLens", "ARKit", "3D Modeling", "Spatial Computing"],
        "related_careers": ["AR Developer", "Spatial Computing Developer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Unity AR/VR Developer",
        "category": "AR/VR",
        "description": "Specializes in virtual and augmented reality project layouts compiled using Unity.",
        "required_skills": ["Unity", "C#", "AR/VR"],
        "preferred_skills": ["Git", "Mobile Development", "UX Design", "3D Modeling"],
        "related_careers": ["AR Developer", "Unity Game Developer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Spatial Computing Developer",
        "category": "AR/VR",
        "description": "Programs software that processes depth data to construct physical mapping models.",
        "required_skills": ["Spatial Computing", "C++", "Unity"],
        "preferred_skills": ["Computer Vision", "3D Mathematics", "Sensors", "OpenGL"],
        "related_careers": ["VR Developer", "Computer Vision Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 80
    },

    # IoT
    {
        "career_name": "IoT Engineer",
        "category": "IoT",
        "description": "Connects sensors, gateways, and hardware controllers to the internet.",
        "required_skills": ["IoT", "Embedded Systems", "C", "Microcontrollers", "Python"],
        "preferred_skills": ["MQTT", "Raspberry Pi", "Arduino", "Linux", "Network Protocols"],
        "related_careers": ["Embedded Systems Engineer", "IoT Solutions Architect"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "IoT Solutions Architect",
        "category": "IoT",
        "description": "Draws cloud ingestion routes, data channels, and hardware layouts for massive IoT setups.",
        "required_skills": ["IoT Architecture", "IoT", "Cloud Computing"],
        "preferred_skills": ["AWS IoT", "Azure IoT", "System Design", "Networking", "Embedded Systems"],
        "related_careers": ["Solutions Architect", "IoT Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 80
    },
    {
        "career_name": "Firmware Engineer",
        "category": "IoT",
        "description": "Writes code executed directly on hardware processors and IoT devices.",
        "required_skills": ["Firmware", "C", "C++", "Microcontrollers"],
        "preferred_skills": ["RTOS", "Linux", "SPI", "I2C", "Assembly"],
        "related_careers": ["Embedded Systems Engineer", "Robotics Engineer"],
        "difficulty_level": "High",
        "growth_level": "Medium",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "IoT Security Specialist",
        "category": "IoT",
        "description": "Ensures that smart sensors and gateway nodes are sealed against cyber exploits.",
        "required_skills": ["IoT Security", "Cybersecurity", "Cryptography"],
        "preferred_skills": ["Firmware Analysis", "Network Security", "Penetration Testing"],
        "related_careers": ["Security Engineer", "IoT Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Smart Home Solutions Developer",
        "category": "IoT",
        "description": "Configures smart sensors, automated lines, and control programs.",
        "required_skills": ["IoT", "Smart Home Protocols", "scripting"],
        "preferred_skills": ["Home Assistant", "Raspberry Pi", "Zigbee", "Z-Wave"],
        "related_careers": ["IoT Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 65
    },

    # Robotics
    {
        "career_name": "Robotics Engineer",
        "category": "Robotics",
        "description": "Develops software and hardware loops to manage robotic arms and self-driving vehicles.",
        "required_skills": ["Robotics", "ROS", "C++", "Python", "Control Systems"],
        "preferred_skills": ["Kinematics", "Simulation", "Computer Vision", "SLAM", "Sensors"],
        "related_careers": ["Robotics Software Engineer", "Embedded Systems Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Robotics Software Engineer",
        "category": "Robotics",
        "description": "Writes control logic, pathing software, and ROS scripts.",
        "required_skills": ["ROS", "C++", "Python", "Linux"],
        "preferred_skills": ["Computer Vision", "SLAM", "LIDAR", "Simulation", "Algorithms"],
        "related_careers": ["Robotics Engineer", "Software Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Control Systems Engineer",
        "category": "Robotics",
        "description": "Develops PID loops and stability math models governing engine speeds.",
        "required_skills": ["Control Systems", "MATLAB", "Simulink"],
        "preferred_skills": ["Python", "PID Controllers", "Control Theory", "Microcontrollers"],
        "related_careers": ["Robotics Engineer", "Embedded Systems Engineer"],
        "difficulty_level": "High",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 75
    },
    {
        "career_name": "Automation Engineer",
        "category": "Robotics",
        "description": "Configures factory assembly lines, sensor clusters, and PLC controls.",
        "required_skills": ["PLC Programming", "SCADA", "Automation"],
        "preferred_skills": ["HMI", "Modbus", "Industrial Networks", "Troubleshooting"],
        "related_careers": ["Control Systems Engineer", "Systems Administrator"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "Perception Engineer",
        "category": "Robotics",
        "description": "Programs visual models, LIDAR feeds, and distance sensors to navigate surroundings.",
        "required_skills": ["Computer Vision", "Deep Learning", "LIDAR", "ROS"],
        "preferred_skills": ["C++", "Python", "PyTorch", "TensorFlow", "Image Processing"],
        "related_careers": ["Computer Vision Engineer", "Robotics Software Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 80
    },

    # Database Engineering
    {
        "career_name": "Database Engineer",
        "category": "Database Engineering",
        "description": "Designs, builds, and maintains data storage structures and query patterns.",
        "required_skills": ["SQL", "Database Design", "PostgreSQL", "MySQL"],
        "preferred_skills": ["NoSQL Databases", "Performance Tuning", "Redis", "MongoDB", "Data Modeling"],
        "related_careers": ["Database Administrator", "Data Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Database Administrator",
        "category": "Database Engineering",
        "description": "Monitors table status, indexes, configurations, backups, and restores.",
        "required_skills": ["SQL", "Database Administration", "Backup & Recovery"],
        "preferred_skills": ["Oracle", "MSSQL", "PostgreSQL", "Linux", "Performance Tuning"],
        "related_careers": ["Database Engineer", "Systems Administrator"],
        "difficulty_level": "Medium",
        "growth_level": "Low",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "SQL Developer",
        "category": "Database Engineering",
        "description": "Writes stored procedures, views, and complex queries for software platforms.",
        "required_skills": ["SQL", "Stored Procedures", "Query Optimization"],
        "preferred_skills": ["T-SQL", "PL/SQL", "PostgreSQL", "Database Design"],
        "related_careers": ["Database Engineer", "Backend Developer"],
        "difficulty_level": "Medium",
        "growth_level": "Low",
        "future_demand": "Medium",
        "average_match_threshold": 65
    },
    {
        "career_name": "Database Architect",
        "category": "Database Engineering",
        "description": "Draws data flow schemas, indexing strategies, and multi-tenant databases.",
        "required_skills": ["Database Architecture", "SQL", "Data Modeling"],
        "preferred_skills": ["NoSQL Databases", "Snowflake", "System Design", "AWS", "BigQuery"],
        "related_careers": ["Data Architect", "Database Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 80
    },
    {
        "career_name": "Data Warehouse Engineer",
        "category": "Database Engineering",
        "description": "Constructs massive analysis databases consolidating records from separate software setups.",
        "required_skills": ["SQL", "ETL", "Data Warehousing"],
        "preferred_skills": ["Snowflake", "Redshift", "BigQuery", "Data Pipelines", "SQL Server"],
        "related_careers": ["Data Engineer", "Business Intelligence Developer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },

    # Quality Assurance
    {
        "career_name": "QA Engineer",
        "category": "Quality Assurance",
        "description": "Tests software applications to report bugs and verify release quality.",
        "required_skills": ["QA Methodologies", "Manual Testing", "Bug Tracking"],
        "preferred_skills": ["Automation Testing", "Selenium", "Jest", "Jira", "SQL"],
        "related_careers": ["Automation Test Engineer", "Manual QA Specialist"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 65
    },
    {
        "career_name": "Automation Test Engineer",
        "category": "Quality Assurance",
        "description": "Writes automation scripts using selenium and test runners.",
        "required_skills": ["Selenium", "Cypress", "Test Automation", "Python", "Java"],
        "preferred_skills": ["CI/CD", "Git", "Jest", "Postman", "Jenkins"],
        "related_careers": ["QA Engineer", "Performance Test Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Performance Test Engineer",
        "category": "Quality Assurance",
        "description": "Simulates virtual user loads to record latency spikes and database lags.",
        "required_skills": ["JMeter", "Load Testing", "Performance Testing"],
        "preferred_skills": ["LoadRunner", "Grafana", "SQL", "APM Tools"],
        "related_careers": ["Automation Test Engineer", "Site Reliability Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "Manual QA Specialist",
        "category": "Quality Assurance",
        "description": "Reviews layout flows, UI alignments, and reports bugs in tracking portals.",
        "required_skills": ["Manual Testing", "Test Case Design", "QA Methodologies"],
        "preferred_skills": ["Jira", "Agile", "Excel", "Mobile Testing"],
        "related_careers": ["QA Engineer", "QA Analyst"],
        "difficulty_level": "Low",
        "growth_level": "Low",
        "future_demand": "Medium",
        "average_match_threshold": 60
    },
    {
        "career_name": "QA Analyst",
        "category": "Quality Assurance",
        "description": "Drafts test plans and schedules release validation milestones.",
        "required_skills": ["QA Methodologies", "Agile", "Test Execution"],
        "preferred_skills": ["SQL", "Jira", "Confluence", "Excel"],
        "related_careers": ["QA Engineer", "Manual QA Specialist"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 65
    },

    # UI/UX Design
    {
        "career_name": "UI Designer",
        "category": "UI/UX Design",
        "description": "Builds high-fidelity layouts, buttons, typography systems, and color schemes.",
        "required_skills": ["UI Design", "Figma", "Visual Design", "Typography"],
        "preferred_skills": ["Adobe Illustrator", "Prototyping", "Design Systems", "HTML5", "CSS3"],
        "related_careers": ["UX Designer", "Product Designer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "UX Designer",
        "category": "UI/UX Design",
        "description": "Draws low-fidelity mockups, customer paths, and reviews user feedback.",
        "required_skills": ["UX Design", "Figma", "Wireframing", "Prototyping", "User Research"],
        "preferred_skills": ["UX Writing", "Usability Testing", "Interaction Design", "Jira"],
        "related_careers": ["UI Designer", "UX Researcher"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Product Designer",
        "category": "UI/UX Design",
        "description": "Harmonizes both business strategies and UX layouts to deliver cohesive designs.",
        "required_skills": ["Product Design", "UI/UX", "Figma", "Prototyping"],
        "preferred_skills": ["Design Systems", "User Research", "Interaction Design", "Agile"],
        "related_careers": ["UI Designer", "UX Designer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Interaction Designer",
        "category": "UI/UX Design",
        "description": "Applies screen animations, transition effects, and micro-interactions.",
        "required_skills": ["Interaction Design", "Prototyping", "Figma"],
        "preferred_skills": ["Adobe After Effects", "CSS3", "JavaScript", "HTML5"],
        "related_careers": ["UI Designer", "UX Designer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "Visual Designer",
        "category": "UI/UX Design",
        "description": "Composes layout vector arts, graphics, banner panels, and icons.",
        "required_skills": ["Visual Design", "Graphic Design", "Figma"],
        "preferred_skills": ["Photoshop", "Illustrator", "Typography", "Branding"],
        "related_careers": ["UI Designer", "Product Designer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "UX Researcher",
        "category": "UI/UX Design",
        "description": "Performs A/B tests, interviews users, and reports layout statistics.",
        "required_skills": ["User Research", "Usability Testing", "UX Design"],
        "preferred_skills": ["Statistics", "A/B Testing", "Data Analysis", "Figma"],
        "related_careers": ["UX Designer", "Product Designer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },

    # Product Management
    {
        "career_name": "Product Manager",
        "category": "Product Management",
        "description": "Drives the strategy, roadmap, and feature definitions of software products.",
        "required_skills": ["Product Management", "Product Strategy", "Agile"],
        "preferred_skills": ["Jira", "Confluence", "Leadership", "Market Analysis", "Data Analysis"],
        "related_careers": ["Technical Product Manager", "Product Owner"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Technical Product Manager",
        "category": "Product Management",
        "description": "Directs deep technical features, system APIs, and platform backend structures.",
        "required_skills": ["Product Management", "Technical Strategy", "Software Engineering"],
        "preferred_skills": ["APIs", "Agile", "System Design", "Jira", "Confluence"],
        "related_careers": ["Product Manager", "Solutions Architect"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Product Owner",
        "category": "Product Management",
        "description": "Maintains user stories, prioritizes the engineering backlog, and accepts builds.",
        "required_skills": ["Agile", "Scrum", "Product Backlog", "User Stories"],
        "preferred_skills": ["Jira", "Confluence", "Agile Methodologies", "Communication"],
        "related_careers": ["Product Manager", "Scrum Master"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "High",
        "average_match_threshold": 65
    },
    {
        "career_name": "Associate Product Manager",
        "category": "Product Management",
        "description": "Assists senior product managers in draft sheets, charts, and metrics.",
        "required_skills": ["Product Management", "Data Analysis", "Agile"],
        "preferred_skills": ["Jira", "Excel", "Market Research", "Confluence"],
        "related_careers": ["Product Manager", "Product Owner"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "High",
        "average_match_threshold": 65
    },
    {
        "career_name": "Growth Product Manager",
        "category": "Product Management",
        "description": "Applies SEO tactics, A/B experiments, and sales strategies to expand registrations.",
        "required_skills": ["Product Management", "growth hacking", "SEO", "Data Analytics"],
        "preferred_skills": ["A/B Testing", "Google Analytics", "Marketing", "SQL"],
        "related_careers": ["Product Manager", "Digital Marketing Specialist"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },

    # Project Management
    {
        "career_name": "Project Manager",
        "category": "Project Management",
        "description": "Guides software timelines, budget boundaries, risks, and client stakeholders.",
        "required_skills": ["Project Management", "Agile", "Waterfall", "Budgeting"],
        "preferred_skills": ["MS Project", "Jira", "Risk Management", "Confluence", "Leadership"],
        "related_careers": ["Program Manager", "Scrum Master"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "Scrum Master",
        "category": "Project Management",
        "description": "Hosts standup meetings, removes delivery blocks, and protects sprint structures.",
        "required_skills": ["Scrum", "Agile", "Kanban", "Facilitation"],
        "preferred_skills": ["Jira", "Confluence", "Agile Coaching", "Communication"],
        "related_careers": ["Agile Coach", "Project Manager"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "High",
        "average_match_threshold": 65
    },
    {
        "career_name": "Agile Coach",
        "category": "Project Management",
        "description": "Trains software organizations in scaled Agile framework layouts.",
        "required_skills": ["Agile Coaching", "Scrum", "Kanban", "Scale Agile"],
        "preferred_skills": ["Leadership", "Organizational Change", "Communication", "Jira"],
        "related_careers": ["Scrum Master", "Project Manager"],
        "difficulty_level": "High",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 75
    },
    {
        "career_name": "Delivery Manager",
        "category": "Project Management",
        "description": "Maintains day-to-day software pipelines and clears release milestones.",
        "required_skills": ["Delivery Management", "Agile", "Software Development Life Cycle"],
        "preferred_skills": ["Jira", "Confluence", "Risk Management", "Sprint Planning"],
        "related_careers": ["Project Manager", "Scrum Master"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "Program Manager",
        "category": "Project Management",
        "description": "Coordinates several interconnected projects to achieve high-level business goals.",
        "required_skills": ["Program Management", "Stakeholder Management", "Agile", "Budgeting"],
        "preferred_skills": ["Risk Management", "Strategy", "MS Project", "Leadership"],
        "related_careers": ["Project Manager", "Product Manager"],
        "difficulty_level": "High",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 75
    },

    # Business Analysis
    {
        "career_name": "Business Analyst",
        "category": "Business Analysis",
        "description": "Bridges corporate needs and engineering designs by translating requirements.",
        "required_skills": ["Business Analysis", "Requirements Gathering", "SQL", "Excel"],
        "preferred_skills": ["Agile", "Jira", "Data Analysis", "Confluence", "User Stories"],
        "related_careers": ["Systems Analyst", "Data Analyst"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "High",
        "average_match_threshold": 65
    },
    {
        "career_name": "Technical Analyst",
        "category": "Business Analysis",
        "description": "Reviews API integrations and databases to write exact technical blueprints.",
        "required_skills": ["Technical Writing", "Systems Analysis", "SQL", "UML"],
        "preferred_skills": ["APIs", "Database Design", "Jira", "XML", "JSON"],
        "related_careers": ["Business Analyst", "Technical Writer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "Systems Analyst",
        "category": "Business Analysis",
        "description": "Examines business workflows and databases to design hardware architectures.",
        "required_skills": ["Systems Analysis", "SQL", "Data Flow Diagrams"],
        "preferred_skills": ["Database Design", "System Design", "UML", "Agile"],
        "related_careers": ["Business Analyst", "Database Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "Business Systems Analyst",
        "category": "Business Analysis",
        "description": "Configures and coordinates enterprise ERP databases and dashboards.",
        "required_skills": ["Business Analysis", "Systems Analysis", "SQL"],
        "preferred_skills": ["ERP Systems", "Salesforce", "Excel", "Data Analytics"],
        "related_careers": ["Business Analyst", "Systems Analyst"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },

    # Digital Marketing
    {
        "career_name": "Digital Marketing Specialist",
        "category": "Digital Marketing",
        "description": "Runs online user advertising, SEM promotions, and email outreach lists.",
        "required_skills": ["Digital Marketing", "SEO", "SEM", "Analytics"],
        "preferred_skills": ["Google Ads", "Facebook Ads", "Email Marketing", "Social Media"],
        "related_careers": ["SEO Specialist", "Growth Hacker"],
        "difficulty_level": "Low",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 60
    },
    {
        "career_name": "SEO Specialist",
        "category": "Digital Marketing",
        "description": "Optimizes website structure and tags to rank in search results.",
        "required_skills": ["SEO", "Content Strategy", "Google Analytics"],
        "preferred_skills": ["HTML", "CSS", "WordPress", "Keyword Research"],
        "related_careers": ["Digital Marketing Specialist", "Content Developer"],
        "difficulty_level": "Low",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 60
    },
    {
        "career_name": "Growth Hacker",
        "category": "Digital Marketing",
        "description": "Utilizes rapid experiments, SEO scripts, and page tests to expand signups.",
        "required_skills": ["Growth Marketing", "Data Analytics", "SEO"],
        "preferred_skills": ["A/B Testing", "Google Analytics", "SQL", "HTML5", "CSS3"],
        "related_careers": ["Digital Marketing Specialist", "Growth Product Manager"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Marketing Analyst",
        "category": "Digital Marketing",
        "description": "Calculates user acquisition costs, returns on marketing investments, and sales metrics.",
        "required_skills": ["Data Analysis", "Marketing Metrics", "SQL", "Tableau"],
        "preferred_skills": ["Python", "Power BI", "Excel", "A/B Testing"],
        "related_careers": ["Data Analyst", "Digital Marketing Specialist"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },

    # Technical Writing
    {
        "career_name": "Technical Writer",
        "category": "Technical Writing",
        "description": "Composes user manuals, deployment tutorials, and platform documentations.",
        "required_skills": ["Technical Writing", "Markdown", "Git", "Documentation"],
        "preferred_skills": ["API Documentation", "Confluence", "HTML", "CSS", "Jira"],
        "related_careers": ["Documentation Specialist", "API Writer"],
        "difficulty_level": "Low",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 60
    },
    {
        "career_name": "Documentation Specialist",
        "category": "Technical Writing",
        "description": "Edits, formats, and archives internal technical files and release reports.",
        "required_skills": ["Documentation", "Technical Writing", "Microsoft Word"],
        "preferred_skills": ["Confluence", "SharePoint", "Excel", "Adobe Acrobat"],
        "related_careers": ["Technical Writer"],
        "difficulty_level": "Low",
        "growth_level": "Low",
        "future_demand": "Medium",
        "average_match_threshold": 60
    },
    {
        "career_name": "API Writer",
        "category": "Technical Writing",
        "description": "Builds developer reference guidelines and details API parameters.",
        "required_skills": ["API Documentation", "OpenAPI", "Swagger", "Markdown"],
        "preferred_skills": ["JSON", "Postman", "Git", "REST APIs", "YAML"],
        "related_careers": ["Technical Writer", "Technical Analyst"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Content Developer",
        "category": "Technical Writing",
        "description": "Writes blog posts, tutorial releases, and informational contents.",
        "required_skills": ["Content Strategy", "Writing", "SEO"],
        "preferred_skills": ["HTML", "CSS", "WordPress", "Social Media"],
        "related_careers": ["Technical Writer", "SEO Specialist"],
        "difficulty_level": "Low",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 60
    },

    # Sales Engineering
    {
        "career_name": "Sales Engineer",
        "category": "Sales Engineering",
        "description": "Bridges sales transactions and engineering teams by explaining product features.",
        "required_skills": ["Sales Engineering", "Solutions Architecture", "Technical Sales"],
        "preferred_skills": ["Presentation Skills", "Communication", "Cloud Computing", "APIs"],
        "related_careers": ["Solutions Architect", "Technical Sales Consultant"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Solutions Architect",
        "category": "Sales Engineering",
        "description": "Designs large cloud layouts and database architectures matching client needs.",
        "required_skills": ["Solutions Architecture", "Cloud Computing", "AWS", "Systems Design"],
        "preferred_skills": ["Client Relations", "Security", "Terraform", "Kubernetes", "Azure"],
        "related_careers": ["Cloud Architect", "Sales Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 80
    },
    {
        "career_name": "Technical Sales Consultant",
        "category": "Sales Engineering",
        "description": "Conducts deep product reviews and designs hardware solutions for clients.",
        "required_skills": ["Technical Consulting", "Pre-Sales", "Solutions Architecture"],
        "preferred_skills": ["Presentation", "Client Relations", "Enterprise Software", "Cloud Computing"],
        "related_careers": ["Sales Engineer", "Pre-Sales Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },
    {
        "career_name": "Pre-Sales Engineer",
        "category": "Sales Engineering",
        "description": "Runs initial technical assessments and constructs mock software demonstrations.",
        "required_skills": ["Pre-Sales", "Technical Sales", "Solutions Architecture"],
        "preferred_skills": ["Demos", "Presentation", "REST APIs", "Cloud Computing"],
        "related_careers": ["Sales Engineer", "Technical Sales Consultant"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    },

    # System Administration
    {
        "career_name": "Systems Administrator",
        "category": "System Administration",
        "description": "Coordinates user setups, installs software updates, and monitors office machines.",
        "required_skills": ["System Administration", "Linux", "Windows Server", "Active Directory"],
        "preferred_skills": ["Bash", "PowerShell", "Networking", "Virtualization", "IT Support"],
        "related_careers": ["Linux Administrator", "Network Administrator"],
        "difficulty_level": "Medium",
        "growth_level": "Low",
        "future_demand": "Medium",
        "average_match_threshold": 65
    },
    {
        "career_name": "Linux Administrator",
        "category": "System Administration",
        "description": "Maintains RedHat, Ubuntu, or CentOS operating servers in virtualized clouds.",
        "required_skills": ["Linux", "System Administration", "Bash", "SSH"],
        "preferred_skills": ["RedHat", "Ansible", "Docker", "Python", "Networking"],
        "related_careers": ["Systems Administrator", "Cloud Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Windows Administrator",
        "category": "System Administration",
        "description": "Coordinates Active Directory nodes and configures server clusters.",
        "required_skills": ["Windows Server", "Active Directory", "PowerShell"],
        "preferred_skills": ["Hyper-V", "Azure", "System Administration", "IT Support"],
        "related_careers": ["Systems Administrator", "Network Administrator"],
        "difficulty_level": "Medium",
        "growth_level": "Low",
        "future_demand": "Medium",
        "average_match_threshold": 65
    },
    {
        "career_name": "IT Support Engineer",
        "category": "System Administration",
        "description": "Helps staff members resolve computer problems, network drops, and password errors.",
        "required_skills": ["IT Support", "Troubleshooting", "Operating Systems"],
        "preferred_skills": ["Networking", "Active Directory", "Customer Service", "Hardware Support"],
        "related_careers": ["Systems Administrator"],
        "difficulty_level": "Low",
        "growth_level": "Low",
        "future_demand": "Medium",
        "average_match_threshold": 55
    },

    # Platform Engineering
    {
        "career_name": "Platform Engineer",
        "category": "Platform Engineering",
        "description": "Constructs internal builder tools, deployment pipelines, and cluster setups.",
        "required_skills": ["Platform Engineering", "Kubernetes", "Docker", "Terraform", "Cloud Computing"],
        "preferred_skills": ["CI/CD", "Go", "Golang", "Python", "Bash", "System Design", "Developer Experience"],
        "related_careers": ["DevOps Engineer", "Site Reliability Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "Platform Architect",
        "category": "Platform Engineering",
        "description": "Designs large-scale cluster layouts, container blueprints, and system limits.",
        "required_skills": ["Platform Architecture", "Platform Engineering", "Kubernetes"],
        "preferred_skills": ["Cloud Architecture", "System Design", "Terraform", "Security", "Go"],
        "related_careers": ["Solutions Architect", "Platform Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 80
    },
    {
        "career_name": "Infrastructure Engineer",
        "category": "Platform Engineering",
        "description": "Constructs configuration playbooks and maintains cloud resources.",
        "required_skills": ["Infrastructure as Code", "Terraform", "Cloud Computing", "Ansible"],
        "preferred_skills": ["Linux", "Python", "Bash", "Docker", "Kubernetes"],
        "related_careers": ["Platform Engineer", "Cloud Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },
    {
        "career_name": "Developer Experience Engineer",
        "category": "Platform Engineering",
        "description": "Builds CLI scripts, documentation websites, and testing templates.",
        "required_skills": ["Developer Experience", "DevOps", "CI/CD"],
        "preferred_skills": ["Platform Engineering", "Python", "Bash", "Git", "Docker"],
        "related_careers": ["Platform Engineer", "Software Engineer"],
        "difficulty_level": "Medium",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 70
    },

    # Site Reliability Engineering
    {
        "career_name": "Site Reliability Engineer",
        "category": "Site Reliability Engineering",
        "description": "Applies engineering solutions to operations problems to scale service systems.",
        "required_skills": ["Site Reliability Engineering", "Kubernetes", "Docker", "Linux", "Prometheus", "Grafana"],
        "preferred_skills": ["Python", "Go", "Golang", "Terraform", "CI/CD", "AWS", "Incident Response"],
        "related_careers": ["DevOps Engineer", "Platform Engineer", "SRE Architect"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 75
    },
    {
        "career_name": "SRE Architect",
        "category": "Site Reliability Engineering",
        "description": "Designs large-scale disaster failovers, system redundancy paths, and monitoring grids.",
        "required_skills": ["Site Reliability Engineering", "Systems Architecture", "Cloud Computing"],
        "preferred_skills": ["Kubernetes", "System Design", "Prometheus", "Grafana", "Go"],
        "related_careers": ["Solutions Architect", "Site Reliability Engineer"],
        "difficulty_level": "High",
        "growth_level": "High",
        "future_demand": "High",
        "average_match_threshold": 80
    },
    {
        "career_name": "Infrastructure Operations Engineer",
        "category": "Site Reliability Engineering",
        "description": "Performs system checks, handles physical cluster replacements, and tracks server logs.",
        "required_skills": ["Infrastructure Operations", "Linux", "Network Operations"],
        "preferred_skills": ["Docker", "Virtualization", "Troubleshooting", "Active Directory"],
        "related_careers": ["Site Reliability Engineer", "Systems Administrator"],
        "difficulty_level": "Medium",
        "growth_level": "Medium",
        "future_demand": "Medium",
        "average_match_threshold": 70
    }
]

# Definition of 500+ Skills grouped into the exact dictionary structure expected by SkillIntelligenceService
skill_categories = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript", "Go", "Golang", "Rust", "Kotlin", "Swift", "C++", 
        "C#", "C", "Ruby", "PHP", "Scala", "R", "Perl", "Haskell", "Julia", "Shell Scripting", 
        "Bash", "PowerShell", "Dart", "Objective-C", "MATLAB", "Fortran", "Assembly", "Solidity", 
        "SQL", "HTML5", "CSS3", "Sass", "GraphQL", "Cobol", "Groovy", "Clojure", "Elixir", 
        "Erlang", "F#"
    ],
    "Frontend Frameworks": [
        "React", "React.js", "Next.js", "Angular", "Vue.js", "Svelte", "Redux", "Vite", "Webpack", "Tailwind CSS", 
        "Bootstrap", "Flexbox", "CSS Grid", "Material UI", "Chakra UI", "LESS", "Web Components", "Nuxt.js", 
        "Gatsby", "Ember.js", "Backbone.js", "JQuery", "Responsive Design", "DOM Manipulation", "Babel", 
        "Esbuild", "PostCSS", "Framer Motion", "Three.js", "D3.js", "Chart.js", "Semantic HTML", 
        "SEO Optimization", "PWA"
    ],
    "Backend Frameworks": [
        "Node.js", "Express.js", "NestJS", "FastAPI", "Flask", "Django", "Spring Boot", "Laravel", 
        "ASP.NET", "Ruby on Rails", "Spring", "Fiber", "Gin", "Actix Web", "Tornado", "Fastify", 
        "Koa", "Rocket", "Django REST Framework", "Microservices", "REST APIs", "gRPC", "SOAP", 
        "WebSockets", "Serverless Functions", "Auth0", "JWT", "OAuth", "Passport.js", 
        "Uvicorn", "Gunicorn", "Celery", "Session Management", "API Gateway", "CORS"
    ],
    "Databases": [
        "MongoDB", "MySQL", "PostgreSQL", "Redis", "Firebase", "Oracle", "MSSQL", "SQL Server", 
        "SQLite", "Cassandra", "DynamoDB", "MariaDB", "Elasticsearch", "Neo4j", "ArangoDB", "InfluxDB", 
        "CouchDB", "Database Administration", "Database Design", "SQL Server Integration Services (SSIS)", 
        "Stored Procedures", "Query Optimization", "Database Replication", "Database Migration", 
        "JSON", "XML", "PL/SQL", "T-SQL", "NoSQL Databases", "Graph Databases", "Time Series Databases", 
        "Data Modeling", "Databases", "Sharding", "Clustering", "ACID Transactions"
    ],
    "Cloud Computing": [
        "AWS", "Azure", "Google Cloud", "GCP", "Cloud Computing", "AWS EC2", "AWS S3", 
        "AWS Lambda", "AWS RDS", "AWS IAM", "Azure Functions", "Azure Blob Storage", "GCP Compute Engine", 
        "GCP Cloud Functions", "BigQuery", "Snowflake", "Redshift", "Virtual Private Cloud (VPC)", 
        "Load Balancers", "Serverless", "Infrastructure as Code", "Cloud Migrations", 
        "SaaS", "PaaS", "IaaS", "Multi-Cloud"
    ],
    "DevOps": [
        "Docker", "Kubernetes", "Jenkins", "GitHub Actions", "Git", "GitLab CI", 
        "CircleCI", "Ansible", "Puppet", "Chef", "CI/CD", "Linux", "Prometheus", "Grafana", 
        "Elastic Stack", "Logstash", "Kibana", "Helm Charts", "Istio", "Service Mesh", "Virtualization", 
        "Vagrant", "Nginx", "Apache HTTP Server", "Build Automation", "Maven", "Gradle", "NPM", 
        "Yarn", "Pipelines", "Release Management", "SRE", "Linux Administration"
    ],
    "Artificial Intelligence": [
        "Machine Learning", "AI Engineer", "AI Architecture", "NLP", "Natural Language Processing", "Computer Vision", 
        "Generative AI", "LLMs", "Large Language Models", "Prompt Engineering", "LangChain", 
        "LlamaIndex", "Vector Databases", "Prompt Tuning", "Semantic Search", "Expert Systems", 
        "AI Safety", "Ethics in AI", "Robotics", "Reinforcement Learning", "Neural Networks", 
        "Speech Recognition", "Machine Translation", "Knowledge Graphs", "Information Retrieval", 
        "Ontologies", "Chatbots", "Cognitive Computing"
    ],
    "Machine Learning": [
        "scikit-learn", "Supervised Learning", "Unsupervised Learning", "Classification", "Regression", "Clustering", 
        "Dimensionality Reduction", "Feature Engineering", "Model Evaluation", "Hyperparameter Tuning", 
        "Gradient Boosting", "XGBoost", "LightGBM", "Random Forest", "Support Vector Machines (SVM)", 
        "Decision Trees", "K-Means", "PCA", "MLflow", "Kubeflow", "SageMaker", "Model Deployment", 
        "Model Training", "Data Labeling", "Active Learning"
    ],
    "Deep Learning": [
        "Deep Learning", "Convolutional Neural Networks (CNN)", "Recurrent Neural Networks (RNN)", 
        "Transformers", "PyTorch", "TensorFlow", "Keras", "CUDA", "GPU Computing", "Autoencoders", 
        "Generative Adversarial Networks (GAN)", "LSTM", "Optimization Algorithms", "Backpropagation", 
        "Deep Q-Networks", "Object Detection", "Image Segmentation", "Transfer Learning", "Fine-Tuning"
    ],
    "Generative AI": [
        "Retrieval-Augmented Generation", "ChromaDB", "Pinecone", "Milvus", "Weaviate", 
        "GPT", "BERT", "Claude", "Llama", "Stable Diffusion", "Midjourney", "OpenAI API", 
        "Hugging Face", "Parameter-Efficient Fine-Tuning (PEFT)", "LoRA"
    ],
    "Data Science": [
        "Data Science", "Data Analysis", "Statistics", "Mathematics", "Pandas", "NumPy", 
        "Matplotlib", "Seaborn", "Tableau", "Power BI", "RStudio", "Jupyter Notebooks", 
        "Exploratory Data Analysis (EDA)", "Statistical Modeling", "A/B Testing", "Hypothesis Testing", 
        "Predictive Modeling", "Quantitative Finance", "Quantitative Analysis", "Linear Algebra", 
        "Probability Theory", "Calculus", "Data Visualization", "Data Wrangling", "Data Cleansing"
    ],
    "Data Engineering": [
        "Data Pipelines", "ETL", "Apache Spark", "Kafka", "Airflow", "Hadoop", "Hive", "Scala", 
        "Data Warehousing", "Data Architectures", "DBT (Data Build Tool)", 
        "AWS Redshift", "Google BigQuery", "Azure Synapse", "Data Lake", "Data Streaming", "Spark Streaming", 
        "Flink", "PySpark", "Data Catalog", "Data Governance", "Schema Registry", "Parquet", "Avro"
    ],
    "Cybersecurity": [
        "Cybersecurity", "Network Security", "Information Security", "Firewalls", "VPN", 
        "Ethical Hacking", "Penetration Testing", "Vulnerability Assessment", "SIEM", "Incident Response", 
        "Digital Forensics", "Cryptography", "Security Architecture", "ISO 27001", "OWASP Top 10", 
        "Kali Linux", "Metasploit", "Wireshark", "Nmap", "Nessus", "Qualys", "SOC Operations", 
        "Threat Intelligence", "Malware Analysis", "Reverse Engineering", "IAM", "Identity Access Management", 
        "Zero Trust", "Security Auditing", "Compliance"
    ],
    "Networking": [
        "Networking", "Network Architecture", "Network Administration", "TCP/IP", "DNS", "DHCP", 
        "Routers", "Switches", "SDN", "Software-Defined Networking", "Cisco CCNA", "Cisco CCNP", 
        "VoIP", "Telecom", "SIP", "IP Routing", "BGP", "OSPF", "LAN", "WAN", 
        "VLAN", "Subnetting", "Wireless Protocols", "Network Operations", "Load Balancing"
    ],
    "Testing": [
        "Selenium", "Cypress", "Test Automation", "QA Methodologies", "Manual Testing", "Bug Tracking", 
        "JMeter", "Load Testing", "Performance Testing", "Jest", "JUnit", "Mocha", "Chai", "PyTest", 
        "Test Case Design", "Test Execution", "Postman", "API Testing", "Integration Testing", 
        "Unit Testing", "System Testing", "Regression Testing", "UAT", "LoadRunner", "Playwright"
    ],
    "Mobile Development": [
        "Mobile Development", "Android SDK", "iOS SDK", "Xcode", "Android Studio", "React Native", 
        "Flutter", "Swift", "Kotlin", "SwiftUI", "Dart", "Mobile Testing", 
        "Jetpack Compose", "App Store Guidelines", "Google Play Console", "Cocoapods", 
        "Mobile UI Design", "SQLite", "CoreData"
    ],
    "Blockchain": [
        "Blockchain", "Blockchain Architecture", "Smart Contracts", "Solidity", "Ethereum", 
        "Web3.js", "Truffle", "Hardhat", "Consensus Protocols", "Ethereum Virtual Machine (EVM)", 
        "Hyperledger", "Cryptographic Protocols", "Solana", "DApps", 
        "DeFi", "NFTs", "IPFS", "Consensus Algorithms", "Proof of Work", "Proof of Stake", "Zk-Snarks"
    ],
    "AR/VR": [
        "AR Development", "VR Development", "Mixed Reality", "Unity", "Unreal Engine", 
        "ARKit", "ARCore", "OpenXR", "WebXR", "HoloLens", "Spatial Computing", 
        "3D Modeling", "Oculus SDK", "Vuforia", "Three.js"
    ],
    "IoT": [
        "IoT", "Embedded Systems", "MQTT", "Raspberry Pi", 
        "Arduino", "Firmware", "Sensors", "IoT Security", "Smart Home Protocols", "Zigbee", 
        "Z-Wave", "IoT Architecture", "AWS IoT", "Azure IoT", "GPIO"
    ],
    "Robotics": [
        "Robotics", "Robotics Software", "ROS", "Robot Operating System", 
        "Control Systems", "Simulink", "Kinematics", "SLAM", "LIDAR", "Simulation", 
        "Automation", "PLC Programming", "SCADA", "PID Controllers", "Control Theory", 
        "Robotic Arms", "Autonomous Vehicles"
    ],
    "UI/UX": [
        "UI Design", "UX Design", "Product Design", "Figma", "Adobe XD", "Wireframing", 
        "Prototyping", "User Research", "Interaction Design", "Visual Design", "Typography", 
        "UX Researcher", "Usability Testing", "Design Systems", "Figma Components", "Graphic Design", 
        "Adobe Illustrator", "Photoshop", "Information Architecture", "UX Writing", "Color Theory"
    ],
    "Business Analysis": [
        "Business Analysis", "Requirements Gathering", "Systems Analysis", 
        "UML", "Data Flow Diagrams", "Business Systems Analysis", "ERP Systems", "Salesforce", 
        "Data Analytics", "Use Case Diagrams", "User Stories"
    ],
    "Product Management": [
        "Product Management", "Product Strategy", "Technical Strategy", 
        "Product Backlog", "Product Roadmap", "Competitive Analysis", "KPIs", "APM"
    ],
    "Project Management": [
        "Project Management", "Scrum", "Kanban", "Agile Coaching", "Waterfall", 
        "MS Project", "Risk Management", "Stakeholder Management", 
        "Sprint Planning", "Agile Methodologies", "Scale Agile", "Delivery Management", 
        "Program Manager", "Milestones", "Gantt Charts"
    ],
    "Soft Skills": [
        "Communication", "Leadership", "Teamwork", "Problem Solving", "Critical Thinking", 
        "Presentation Skills", "Client Relations", "Time Management", "Adaptability", "Collaboration", 
        "Mentoring", "Conflict Resolution", "Negotiation", "Empathy", "Creativity", "Decision Making"
    ],
    "Tools & Technologies": [
        "GitHub", "GitLab", "Confluence", "Swagger", "OpenAPI", 
        "LaTeX", "WordPress", "Google Ads", "Facebook Ads", "Email Marketing", "Social Media", 
        "Microsoft Word", "SharePoint", "Adobe Acrobat"
    ]
}

total_skill_count = sum(len(skills) for skills in skill_categories.values())
print(f"Total Careers defined: {len(careers)}")
print(f"Total Skills defined: {total_skill_count}")

# Save career database
with open(career_db_path, "w", encoding="utf-8") as f:
    json.dump(careers, f, indent=2)
print(f"Saved career database to: {career_db_path}")

# Save skills database
with open(skills_db_path, "w", encoding="utf-8") as f:
    json.dump(skill_categories, f, indent=2)
print(f"Saved skills database to: {skills_db_path}")
