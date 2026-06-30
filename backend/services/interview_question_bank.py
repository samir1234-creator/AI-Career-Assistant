"""
Interview Question Bank
=======================
A comprehensive, organized collection of interview questions for all roles,
types, difficulties, companies, and topics. Designed for dynamic retrieval
and context injection with resume data.
"""

import random
from typing import List, Dict, Any, Optional

# ─────────────────────────────────────────────────────────────
# ROLE-BASED QUESTIONS (Mock Interview)
# ─────────────────────────────────────────────────────────────

ROLE_QUESTIONS: Dict[str, Dict[str, List[Dict]]] = {
    "AI Engineer": {
        "Beginner": [
            {"q": "What is the difference between supervised and unsupervised learning?", "hint": "Think about labeled vs unlabeled data."},
            {"q": "Explain what a neural network is in simple terms.", "hint": "Layers, neurons, activation functions."},
            {"q": "What is overfitting and how do you prevent it?", "hint": "Regularization, dropout, cross-validation."},
            {"q": "What are the most common Python libraries used in AI?", "hint": "NumPy, Pandas, TensorFlow, PyTorch, Scikit-learn."},
            {"q": "What is the purpose of a loss function?", "hint": "Measures the gap between predicted and actual values."},
            {"q": "Explain the concept of a training set, validation set, and test set.", "hint": "Model training, tuning, and evaluation."},
        ],
        "Intermediate": [
            {"q": "Explain the transformer architecture and its advantages over RNNs.", "hint": "Attention mechanism, parallelism, long-range dependencies."},
            {"q": "How does backpropagation work in a neural network?", "hint": "Chain rule, gradient descent, weight updates."},
            {"q": "What is the difference between batch normalization and layer normalization?", "hint": "Batch vs sequence dimension normalization."},
            {"q": "Describe the architecture of a typical RAG (Retrieval-Augmented Generation) system.", "hint": "Vector DB, embeddings, retrieval, generation pipeline."},
            {"q": "How do you handle class imbalance in a classification problem?", "hint": "SMOTE, class weights, oversampling, undersampling."},
            {"q": "Explain attention mechanisms and self-attention.", "hint": "Query, Key, Value matrices, softmax scaling."},
        ],
        "Advanced": [
            {"q": "Design a production-grade LLM inference pipeline with low latency.", "hint": "Batching, quantization, caching, model serving."},
            {"q": "How would you implement efficient fine-tuning of a large language model with limited GPU memory?", "hint": "LoRA, QLoRA, gradient checkpointing, mixed precision."},
            {"q": "Explain the tradeoffs between different vector similarity search algorithms.", "hint": "FAISS, HNSW, Annoy, IVF — accuracy vs speed vs memory."},
            {"q": "How do you evaluate and mitigate hallucinations in LLM applications?", "hint": "RAGAS, faithfulness metrics, grounding, guardrails."},
            {"q": "Design a multi-agent AI system for automated code review.", "hint": "Agent orchestration, tool use, memory, coordination."},
        ],
        "Expert": [
            {"q": "How would you architect a distributed training system for a 70B parameter model?", "hint": "Data parallelism, model parallelism, ZeRO optimization, DeepSpeed."},
            {"q": "Design a real-time AI system that processes 1M events per second with sub-100ms latency.", "hint": "Streaming, Kafka, Flink, model optimization, edge deployment."},
            {"q": "Explain the theoretical foundations of RLHF and its practical implementation challenges.", "hint": "Reward model, PPO, KL divergence, reward hacking."},
        ],
    },
    "Machine Learning Engineer": {
        "Beginner": [
            {"q": "What is the difference between classification and regression?", "hint": "Discrete vs continuous output."},
            {"q": "Explain the bias-variance tradeoff.", "hint": "Model complexity, underfitting, overfitting."},
            {"q": "What is cross-validation and why is it important?", "hint": "K-fold, stratified, preventing data leakage."},
            {"q": "What is feature engineering?", "hint": "Creating new features from raw data to improve model performance."},
            {"q": "What are precision, recall, and F1 score?", "hint": "TP, FP, FN metrics for classification evaluation."},
        ],
        "Intermediate": [
            {"q": "Explain gradient boosting and how it differs from random forests.", "hint": "Sequential vs parallel ensemble, boosting vs bagging."},
            {"q": "How do you productionize a machine learning model?", "hint": "MLflow, Docker, REST API, monitoring, CI/CD."},
            {"q": "What is feature importance and how do you calculate it?", "hint": "Permutation importance, SHAP values, tree-based feature importance."},
            {"q": "Explain the concept of model drift and how you monitor for it.", "hint": "Data drift, concept drift, PSI, monitoring systems."},
            {"q": "How would you design a recommendation system?", "hint": "Collaborative filtering, content-based, matrix factorization."},
        ],
        "Advanced": [
            {"q": "Design a scalable ML pipeline for training models on petabyte-scale data.", "hint": "Spark, distributed training, data sharding, feature stores."},
            {"q": "How do you implement A/B testing for ML models in production?", "hint": "Traffic splitting, statistical significance, guardrail metrics."},
            {"q": "Explain Bayesian optimization for hyperparameter tuning.", "hint": "Surrogate model, acquisition function, Gaussian processes."},
        ],
        "Expert": [
            {"q": "Design a real-time fraud detection system handling 10K transactions per second.", "hint": "Graph neural networks, streaming ML, feature engineering, latency."},
            {"q": "How would you build a federated learning system for healthcare data?", "hint": "Privacy-preserving ML, differential privacy, secure aggregation."},
        ],
    },
    "Software Engineer": {
        "Beginner": [
            {"q": "What is the difference between a stack and a queue?", "hint": "LIFO vs FIFO data structures."},
            {"q": "Explain object-oriented programming principles.", "hint": "Encapsulation, inheritance, polymorphism, abstraction."},
            {"q": "What is version control and why is Git important?", "hint": "Tracking changes, collaboration, branching, merging."},
            {"q": "What is the difference between compiled and interpreted languages?", "hint": "C vs Python — compilation stages."},
            {"q": "Explain what REST APIs are.", "hint": "HTTP verbs, statelessness, JSON, endpoints."},
        ],
        "Intermediate": [
            {"q": "Explain SOLID principles with examples.", "hint": "Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion."},
            {"q": "What design patterns have you used and when?", "hint": "Factory, Singleton, Observer, Strategy, Decorator."},
            {"q": "How do you ensure code quality in a team?", "hint": "Code reviews, testing, linting, CI/CD, documentation."},
            {"q": "Explain the CAP theorem.", "hint": "Consistency, Availability, Partition tolerance — pick two."},
            {"q": "How would you debug a performance issue in production?", "hint": "Profiling, logging, APM tools, bottleneck identification."},
        ],
        "Advanced": [
            {"q": "Design a URL shortening service like bit.ly.", "hint": "Hashing, collision handling, redirection, analytics, caching."},
            {"q": "How do you design for high availability and fault tolerance?", "hint": "Redundancy, load balancing, circuit breakers, graceful degradation."},
            {"q": "Explain event-driven architecture and when to use it.", "hint": "Message queues, pub/sub, decoupling, eventual consistency."},
        ],
        "Expert": [
            {"q": "Design a distributed locking mechanism for a microservices architecture.", "hint": "Redis SETNX, ZooKeeper, etcd, lease renewal."},
            {"q": "How would you architect a system to handle 1 billion users?", "hint": "Horizontal scaling, CDN, DB sharding, caching layers, global distribution."},
        ],
    },
    "Frontend Developer": {
        "Beginner": [
            {"q": "Explain the difference between HTML, CSS, and JavaScript.", "hint": "Structure, styling, behavior."},
            {"q": "What is the DOM and how do you manipulate it?", "hint": "Document Object Model, querySelector, event listeners."},
            {"q": "What is responsive design?", "hint": "Media queries, flexbox, grid, viewport units."},
            {"q": "What are CSS flexbox and grid, and when do you use each?", "hint": "1D vs 2D layout."},
            {"q": "What is the event loop in JavaScript?", "hint": "Call stack, callback queue, microtasks."},
        ],
        "Intermediate": [
            {"q": "Explain React hooks and their rules.", "hint": "useState, useEffect, useContext — no hooks in conditionals."},
            {"q": "What is virtual DOM and how does React's reconciliation work?", "hint": "Diffing algorithm, fiber, reconciler."},
            {"q": "How do you optimize React application performance?", "hint": "Memoization, lazy loading, code splitting, React.memo."},
            {"q": "Explain state management in React applications.", "hint": "Context, Redux, Zustand, Jotai — when to use what."},
            {"q": "What is TypeScript and what are its benefits?", "hint": "Static typing, interfaces, type safety, better DX."},
        ],
        "Advanced": [
            {"q": "How would you implement a micro-frontend architecture?", "hint": "Module federation, independent deployments, shared dependencies."},
            {"q": "Explain Web Workers and when to use them.", "hint": "Offload heavy computation from main thread."},
            {"q": "Design a scalable design system for a large organization.", "hint": "Component library, tokens, theming, documentation, versioning."},
        ],
        "Expert": [
            {"q": "How would you build a collaborative real-time editor like Google Docs?", "hint": "CRDTs, operational transforms, WebSocket, conflict resolution."},
            {"q": "Design a browser-based video editing application.", "hint": "WebAssembly, Canvas API, Media APIs, memory management."},
        ],
    },
    "Backend Developer": {
        "Beginner": [
            {"q": "What is the difference between SQL and NoSQL databases?", "hint": "Relational vs document/key-value — structure, scalability."},
            {"q": "Explain REST vs GraphQL.", "hint": "Multiple endpoints vs single endpoint, over-fetching, under-fetching."},
            {"q": "What is middleware in a backend framework?", "hint": "Request/response pipeline, authentication, logging."},
            {"q": "What are HTTP status codes?", "hint": "2xx success, 4xx client errors, 5xx server errors."},
            {"q": "Explain the concept of a database transaction.", "hint": "ACID properties."},
        ],
        "Intermediate": [
            {"q": "How do you implement JWT authentication?", "hint": "Header, payload, signature — access/refresh token pattern."},
            {"q": "Explain database indexing and when to use it.", "hint": "B-tree, hash indexes — read performance vs write overhead."},
            {"q": "How do you handle rate limiting in APIs?", "hint": "Token bucket, sliding window, Redis-based rate limiters."},
            {"q": "What are database connection pools and why are they important?", "hint": "Reuse connections, prevent exhaustion, performance."},
            {"q": "How do you design a RESTful API with proper versioning?", "hint": "URL path, header, query param versioning — backward compatibility."},
        ],
        "Advanced": [
            {"q": "Design a caching strategy for a high-traffic API.", "hint": "Redis, cache invalidation, TTL, cache-aside vs write-through."},
            {"q": "Explain database sharding vs replication.", "hint": "Horizontal partitioning vs copies — read scaling vs write scaling."},
            {"q": "How do you implement distributed transactions?", "hint": "Saga pattern, two-phase commit, eventual consistency."},
        ],
        "Expert": [
            {"q": "Design a job queue system that can process 10M tasks per day reliably.", "hint": "Message brokers, worker pools, dead letter queues, retry logic."},
            {"q": "How would you architect a multi-tenant SaaS backend?", "hint": "Data isolation strategies, schema-per-tenant vs row-level security."},
        ],
    },
    "Full Stack Developer": {
        "Beginner": [
            {"q": "Explain the full stack of a typical web application.", "hint": "Frontend, backend, database, infrastructure."},
            {"q": "What is the purpose of an API in a full stack application?", "hint": "Decoupling frontend and backend, data exchange."},
            {"q": "How does authentication work in a full stack app?", "hint": "JWT, sessions, cookies, OAuth flow."},
            {"q": "What is CORS and why does it matter?", "hint": "Cross-origin requests, browser security, preflight."},
        ],
        "Intermediate": [
            {"q": "How do you structure a full stack project for scalability?", "hint": "Monorepo vs separate repos, code organization, shared types."},
            {"q": "Explain how you would implement real-time features.", "hint": "WebSockets, Server-Sent Events, polling — tradeoffs."},
            {"q": "How do you handle file uploads in a full stack app?", "hint": "Multipart, streaming, S3, presigned URLs."},
            {"q": "Describe your deployment process for a full stack app.", "hint": "Docker, CI/CD, environment variables, health checks."},
        ],
        "Advanced": [
            {"q": "Design a full stack app that scales to 1M concurrent users.", "hint": "CDN, load balancer, horizontal scaling, database replicas."},
            {"q": "How do you implement end-to-end testing for a full stack application?", "hint": "Cypress, Playwright, test pyramid, mocking strategies."},
        ],
        "Expert": [
            {"q": "Design and implement a zero-downtime deployment strategy.", "hint": "Blue-green, canary, feature flags, database migrations."},
        ],
    },
    "Data Scientist": {
        "Beginner": [
            {"q": "What is the data science lifecycle?", "hint": "Problem definition → data collection → EDA → modeling → evaluation → deployment."},
            {"q": "Explain the difference between correlation and causation.", "hint": "Statistical relationship vs cause-effect — confounders."},
            {"q": "What is exploratory data analysis?", "hint": "Descriptive stats, visualizations, finding patterns and anomalies."},
            {"q": "What is a p-value and what does it represent?", "hint": "Probability of observing results given null hypothesis is true."},
        ],
        "Intermediate": [
            {"q": "Explain principal component analysis (PCA).", "hint": "Dimensionality reduction, eigenvectors, explained variance."},
            {"q": "How do you handle missing data?", "hint": "Imputation, deletion, KNN imputer — MCAR vs MAR vs MNAR."},
            {"q": "What is A/B testing and how do you design one?", "hint": "Control vs treatment, sample size, statistical power, significance."},
            {"q": "Explain the differences between parametric and non-parametric tests.", "hint": "Assumptions about distribution — t-test vs Mann-Whitney."},
        ],
        "Advanced": [
            {"q": "How would you build a causal inference model?", "hint": "Propensity scoring, diff-in-diff, instrumental variables."},
            {"q": "Design a data science platform for an enterprise.", "hint": "Feature store, model registry, experiment tracking, serving."},
        ],
        "Expert": [
            {"q": "How would you apply reinforcement learning to optimize a supply chain?", "hint": "State space, action space, reward design, policy learning."},
        ],
    },
    "Data Analyst": {
        "Beginner": [
            {"q": "What is the difference between data analytics and data science?", "hint": "Descriptive vs predictive — SQL heavy vs model heavy."},
            {"q": "How do you create effective data visualizations?", "hint": "Choosing the right chart, clarity, color, storytelling."},
            {"q": "What SQL commands do you use most frequently?", "hint": "SELECT, WHERE, GROUP BY, JOIN, HAVING, ORDER BY."},
            {"q": "What is a KPI and how do you define one?", "hint": "Key Performance Indicator — measurable, actionable, aligned."},
        ],
        "Intermediate": [
            {"q": "Explain the difference between inner join, left join, right join, and full outer join.", "hint": "Venn diagrams — which rows are included."},
            {"q": "How do you identify and handle outliers in data?", "hint": "IQR method, Z-score, visualization, domain knowledge."},
            {"q": "What is a pivot table and how do you use it?", "hint": "Aggregating data across multiple dimensions."},
            {"q": "How do you tell a story with data?", "hint": "Narrative structure, audience, actionable insights, visualization choice."},
        ],
        "Advanced": [
            {"q": "Design a dashboard for a C-suite executive.", "hint": "High-level KPIs, drill-down capability, real-time vs batch."},
            {"q": "How would you set up a data pipeline from multiple sources?", "hint": "ETL vs ELT, Airflow, data quality, schema evolution."},
        ],
        "Expert": [
            {"q": "How do you build a self-service analytics platform?", "hint": "Data democratization, governance, semantic layer, access control."},
        ],
    },
    "DevOps Engineer": {
        "Beginner": [
            {"q": "What is DevOps and why is it important?", "hint": "Culture of collaboration between Dev and Ops — faster delivery."},
            {"q": "Explain CI/CD pipeline.", "hint": "Continuous Integration, Continuous Delivery/Deployment — automation."},
            {"q": "What is Docker and why do we use containers?", "hint": "Isolation, portability, reproducibility."},
            {"q": "What is the difference between monolithic and microservices architectures?", "hint": "Single deploy vs independent services — tradeoffs."},
        ],
        "Intermediate": [
            {"q": "How do you implement monitoring and alerting in production?", "hint": "Prometheus, Grafana, PagerDuty — SLAs, SLOs, SLIs."},
            {"q": "Explain Kubernetes and its key components.", "hint": "Pods, deployments, services, ingress, namespaces."},
            {"q": "How do you implement Infrastructure as Code?", "hint": "Terraform, CloudFormation — declarative, version-controlled infra."},
            {"q": "What is blue-green deployment?", "hint": "Two identical environments — switch traffic for zero-downtime."},
        ],
        "Advanced": [
            {"q": "Design a disaster recovery strategy for a critical application.", "hint": "RTO, RPO, backup strategies, failover, chaos engineering."},
            {"q": "How do you secure a Kubernetes cluster?", "hint": "RBAC, network policies, secrets management, image scanning."},
        ],
        "Expert": [
            {"q": "Design a platform engineering team's internal developer platform.", "hint": "Golden paths, self-service, paved roads, Developer Experience."},
        ],
    },
    "Cloud Engineer": {
        "Beginner": [
            {"q": "What are the different cloud service models?", "hint": "IaaS, PaaS, SaaS — responsibility models."},
            {"q": "Explain the concept of cloud regions and availability zones.", "hint": "Geographic distribution, fault isolation, latency."},
            {"q": "What is auto-scaling?", "hint": "Automatically adjusting resources based on load."},
        ],
        "Intermediate": [
            {"q": "How do you design a highly available architecture on AWS?", "hint": "Multi-AZ, load balancers, RDS replicas, S3."},
            {"q": "Explain VPC and its components.", "hint": "Subnets, route tables, security groups, NACLs, IGW."},
            {"q": "What is serverless computing and when should you use it?", "hint": "Lambda, Function-as-a-Service — event-driven, cost model."},
        ],
        "Advanced": [
            {"q": "Design a multi-cloud architecture strategy.", "hint": "Vendor lock-in avoidance, data sovereignty, cost optimization."},
            {"q": "How do you implement FinOps for cloud cost optimization?", "hint": "Reserved instances, right-sizing, spot instances, tagging."},
        ],
        "Expert": [
            {"q": "Design a global content delivery system with sub-50ms latency.", "hint": "Edge computing, CDN, anycast routing, caching hierarchy."},
        ],
    },
    "Cybersecurity Engineer": {
        "Beginner": [
            {"q": "What is the CIA triad?", "hint": "Confidentiality, Integrity, Availability."},
            {"q": "Explain the difference between authentication and authorization.", "hint": "Who you are vs what you can do."},
            {"q": "What is SQL injection and how do you prevent it?", "hint": "Parameterized queries, input validation, ORM."},
            {"q": "What is a firewall and how does it work?", "hint": "Network traffic filtering, rules, stateful vs stateless."},
        ],
        "Intermediate": [
            {"q": "Explain OWASP Top 10 vulnerabilities.", "hint": "Injection, Broken Auth, XSS, IDOR, Security Misconfiguration."},
            {"q": "What is penetration testing and its phases?", "hint": "Reconnaissance, scanning, exploitation, post-exploitation, reporting."},
            {"q": "How does TLS/SSL work?", "hint": "Handshake, certificate exchange, symmetric key establishment."},
        ],
        "Advanced": [
            {"q": "Design a zero-trust security architecture.", "hint": "Never trust, always verify — microsegmentation, identity-centric."},
            {"q": "How would you respond to a ransomware attack?", "hint": "Incident response plan, isolation, forensics, recovery."},
        ],
        "Expert": [
            {"q": "Design a threat modeling framework for a fintech application.", "hint": "STRIDE, attack trees, data flow diagrams, risk scoring."},
        ],
    },
    "Android Developer": {
        "Beginner": [
            {"q": "What is the difference between Activity and Fragment?", "hint": "Activity is a full screen, Fragment is a UI piece within Activity."},
            {"q": "Explain the Android Activity lifecycle.", "hint": "onCreate, onStart, onResume, onPause, onStop, onDestroy."},
            {"q": "What is an Intent in Android?", "hint": "Message to start activities, services, or deliver broadcasts."},
        ],
        "Intermediate": [
            {"q": "Explain the MVVM pattern in Android development.", "hint": "Model, View, ViewModel — separation of concerns, testability."},
            {"q": "What is Jetpack Compose and how does it differ from XML layouts?", "hint": "Declarative UI — composable functions vs XML inflation."},
            {"q": "How do you handle background tasks in Android?", "hint": "Coroutines, WorkManager, Foreground Services."},
        ],
        "Advanced": [
            {"q": "How do you optimize Android app performance?", "hint": "Memory profiling, ANR avoidance, rendering optimization, ProGuard."},
            {"q": "Design an offline-first Android application.", "hint": "Room DB, sync strategies, conflict resolution, network state."},
        ],
        "Expert": [
            {"q": "How would you architect a large-scale Android app with multiple teams?", "hint": "Modularization, feature modules, dynamic delivery, clean architecture."},
        ],
    },
    "Product Manager": {
        "Beginner": [
            {"q": "How do you prioritize features on a product roadmap?", "hint": "RICE, MoSCoW, impact/effort matrix."},
            {"q": "What is a product requirements document (PRD)?", "hint": "Problem statement, user stories, acceptance criteria, success metrics."},
            {"q": "How do you gather user requirements?", "hint": "User interviews, surveys, analytics, usability testing."},
        ],
        "Intermediate": [
            {"q": "How do you define and measure product success?", "hint": "OKRs, KPIs, North Star metric, activation, retention."},
            {"q": "Explain how you would launch a new product feature.", "hint": "Feature flags, phased rollout, A/B testing, monitoring."},
            {"q": "How do you handle competing stakeholder priorities?", "hint": "Alignment workshops, data-driven decisions, transparent roadmaps."},
        ],
        "Advanced": [
            {"q": "Design the product strategy for an AI-powered tool entering a competitive market.", "hint": "Differentiation, TAM/SAM/SOM, go-to-market, pricing."},
        ],
        "Expert": [
            {"q": "How do you build and scale a product team from 3 to 30?", "hint": "Hiring, culture, processes, OKR alignment, autonomy vs alignment."},
        ],
    },
    "UI/UX Designer": {
        "Beginner": [
            {"q": "What is the difference between UI and UX design?", "hint": "Visual interface vs user experience — feel vs look."},
            {"q": "What are the principles of good UX design?", "hint": "Usability, accessibility, consistency, feedback, error prevention."},
            {"q": "What is a wireframe and when do you use it?", "hint": "Low-fidelity layout — before visual design."},
        ],
        "Intermediate": [
            {"q": "Explain your design process from brief to final delivery.", "hint": "Research → Ideate → Prototype → Test → Iterate."},
            {"q": "How do you conduct usability testing?", "hint": "Task-based testing, think-aloud protocol, heuristic evaluation."},
            {"q": "What is a design system and why is it important?", "hint": "Component library, tokens, documentation, consistency at scale."},
        ],
        "Advanced": [
            {"q": "How do you design for accessibility (WCAG)?", "hint": "Color contrast, screen readers, keyboard navigation, ARIA labels."},
            {"q": "Design a mobile onboarding flow for a complex B2B product.", "hint": "Progressive disclosure, cognitive load, value demonstration."},
        ],
        "Expert": [
            {"q": "How would you build a design culture in an engineering-first company?", "hint": "Design champions, design reviews, metrics for design quality."},
        ],
    },
}


# ─────────────────────────────────────────────────────────────
# HR INTERVIEW QUESTIONS
# ─────────────────────────────────────────────────────────────

HR_QUESTIONS = [
    {"q": "Tell me about yourself.", "category": "Introduction", "hint": "Present-Past-Future formula: current role → background → why here."},
    {"q": "Why should we hire you?", "category": "Value Proposition", "hint": "Match your skills to their needs, show enthusiasm and unique value."},
    {"q": "What is your greatest strength?", "category": "Strengths", "hint": "Specific, relevant, backed by an example."},
    {"q": "What is your greatest weakness?", "category": "Weaknesses", "hint": "Real weakness + concrete steps you've taken to improve it."},
    {"q": "Where do you see yourself in 5 years?", "category": "Career Goals", "hint": "Align with company growth, show ambition balanced with realistic planning."},
    {"q": "Why are you leaving your current job?", "category": "Motivation", "hint": "Positive framing — growth, new challenges, alignment with goals."},
    {"q": "Why do you want to work here?", "category": "Company Fit", "hint": "Research the company — values, products, mission, recent news."},
    {"q": "Describe your biggest professional achievement.", "category": "Achievement", "hint": "Quantify impact — numbers, percentages, business outcomes."},
    {"q": "How do you handle stress and pressure?", "category": "Resilience", "hint": "Specific techniques, example of handling a stressful situation well."},
    {"q": "Describe a time you failed and what you learned from it.", "category": "Growth", "hint": "Failure → learning → how you applied that learning."},
    {"q": "How do you prioritize your work when you have multiple deadlines?", "category": "Time Management", "hint": "Prioritization framework, communication, stakeholder management."},
    {"q": "What motivates you?", "category": "Motivation", "hint": "Intrinsic motivators aligned with the role."},
    {"q": "Describe your ideal work environment.", "category": "Culture Fit", "hint": "Research company culture, be honest but tactful."},
    {"q": "How do you handle constructive criticism?", "category": "Feedback", "hint": "Open mindset, specific example of acting on feedback."},
    {"q": "What are your salary expectations?", "category": "Compensation", "hint": "Research market rates, provide a range, be confident."},
    {"q": "Do you prefer working independently or in a team?", "category": "Work Style", "hint": "Show adaptability — both depending on context."},
    {"q": "How do you keep up with industry trends?", "category": "Learning", "hint": "Specific resources, communities, projects."},
    {"q": "Tell me about a time you showed leadership.", "category": "Leadership", "hint": "STAR format — Situation, Task, Action, Result."},
    {"q": "How do you handle conflict with a coworker?", "category": "Conflict Resolution", "hint": "Direct communication, empathy, seeking common ground."},
    {"q": "What are your career goals?", "category": "Career Goals", "hint": "Short-term and long-term, aligned with role growth."},
]

# ─────────────────────────────────────────────────────────────
# BEHAVIORAL QUESTIONS (STAR Format)
# ─────────────────────────────────────────────────────────────

BEHAVIORAL_QUESTIONS = [
    {"q": "Tell me about a time you led a team through a difficult project. What was your approach?", "competency": "Leadership", "format": "STAR"},
    {"q": "Describe a situation where you had to make a critical decision with incomplete information.", "competency": "Decision Making", "format": "STAR"},
    {"q": "Tell me about a time you had to adapt quickly to a major unexpected change.", "competency": "Adaptability", "format": "STAR"},
    {"q": "Describe a time you disagreed with your manager and how you handled it.", "competency": "Communication", "format": "STAR"},
    {"q": "Tell me about a time you solved a problem that others had given up on.", "competency": "Problem Solving", "format": "STAR"},
    {"q": "Describe a situation where you had to work with a difficult team member.", "competency": "Collaboration", "format": "STAR"},
    {"q": "Tell me about a time you took initiative to improve a process without being asked.", "competency": "Initiative", "format": "STAR"},
    {"q": "Describe a time when you had to deliver bad news to a stakeholder.", "competency": "Communication", "format": "STAR"},
    {"q": "Tell me about a time you had competing priorities. How did you manage them?", "competency": "Time Management", "format": "STAR"},
    {"q": "Describe a time you mentored or coached someone successfully.", "competency": "Leadership", "format": "STAR"},
    {"q": "Tell me about a time you failed to meet a deadline. What happened and what did you learn?", "competency": "Accountability", "format": "STAR"},
    {"q": "Describe a time you had to learn a completely new technology quickly for a project.", "competency": "Learning Agility", "format": "STAR"},
    {"q": "Tell me about a time you had to convince others to adopt your idea.", "competency": "Influence", "format": "STAR"},
    {"q": "Describe a situation where you demonstrated critical thinking to solve a complex problem.", "competency": "Critical Thinking", "format": "STAR"},
    {"q": "Tell me about a time you went above and beyond to exceed expectations.", "competency": "Work Ethic", "format": "STAR"},
]

# ─────────────────────────────────────────────────────────────
# TECHNICAL QUESTIONS BY TOPIC
# ─────────────────────────────────────────────────────────────

TECHNICAL_QUESTIONS: Dict[str, List[Dict]] = {
    "Python": [
        {"q": "What is the difference between a list and a tuple in Python?", "difficulty": "Beginner"},
        {"q": "Explain Python's GIL and how it affects multithreading.", "difficulty": "Intermediate"},
        {"q": "What are Python decorators and how do you implement them?", "difficulty": "Intermediate"},
        {"q": "Explain Python's memory management and garbage collection.", "difficulty": "Advanced"},
        {"q": "What is metaclass programming in Python?", "difficulty": "Expert"},
        {"q": "Explain asyncio and how async/await works in Python.", "difficulty": "Advanced"},
        {"q": "What are generators and iterators? When would you use each?", "difficulty": "Intermediate"},
        {"q": "Explain Python's MRO (Method Resolution Order).", "difficulty": "Advanced"},
    ],
    "JavaScript": [
        {"q": "Explain the difference between var, let, and const.", "difficulty": "Beginner"},
        {"q": "What is closure in JavaScript? Give an example.", "difficulty": "Intermediate"},
        {"q": "Explain promises, async/await, and the event loop.", "difficulty": "Intermediate"},
        {"q": "What is prototypal inheritance in JavaScript?", "difficulty": "Advanced"},
        {"q": "Explain the module pattern and ES6 modules.", "difficulty": "Intermediate"},
        {"q": "What are WeakMap and WeakSet? When would you use them?", "difficulty": "Advanced"},
    ],
    "React": [
        {"q": "Explain the difference between controlled and uncontrolled components.", "difficulty": "Beginner"},
        {"q": "What is the purpose of useEffect and what are its dependencies?", "difficulty": "Intermediate"},
        {"q": "How does React's rendering optimization work with useMemo and useCallback?", "difficulty": "Intermediate"},
        {"q": "Explain React's Concurrent Mode and Suspense.", "difficulty": "Advanced"},
        {"q": "How would you implement code splitting in a large React app?", "difficulty": "Advanced"},
        {"q": "Explain the new React Server Components model.", "difficulty": "Expert"},
    ],
    "FastAPI": [
        {"q": "What are the advantages of FastAPI over Flask?", "difficulty": "Beginner"},
        {"q": "How do you implement dependency injection in FastAPI?", "difficulty": "Intermediate"},
        {"q": "Explain how FastAPI handles async request processing.", "difficulty": "Intermediate"},
        {"q": "How do you implement background tasks in FastAPI?", "difficulty": "Advanced"},
        {"q": "What are Pydantic models and how does FastAPI use them for validation?", "difficulty": "Intermediate"},
        {"q": "How do you implement WebSockets in FastAPI?", "difficulty": "Advanced"},
    ],
    "Data Structures": [
        {"q": "Explain the time complexity of common operations on a hash map.", "difficulty": "Beginner"},
        {"q": "When would you use a min-heap vs a max-heap?", "difficulty": "Intermediate"},
        {"q": "Explain the difference between a B-tree and a B+ tree.", "difficulty": "Advanced"},
        {"q": "What is a trie and when is it useful?", "difficulty": "Intermediate"},
        {"q": "Explain skip lists and their advantages over balanced BSTs.", "difficulty": "Advanced"},
    ],
    "Algorithms": [
        {"q": "Explain dynamic programming with an example.", "difficulty": "Intermediate"},
        {"q": "What is the difference between BFS and DFS?", "difficulty": "Beginner"},
        {"q": "Explain the concept of amortized analysis.", "difficulty": "Advanced"},
        {"q": "How does Dijkstra's algorithm work and what are its limitations?", "difficulty": "Intermediate"},
        {"q": "Explain the MapReduce paradigm.", "difficulty": "Advanced"},
    ],
    "System Design": [
        {"q": "Design a parking lot system.", "difficulty": "Beginner"},
        {"q": "Design a rate limiter.", "difficulty": "Intermediate"},
        {"q": "Design Twitter's feed ranking system.", "difficulty": "Advanced"},
        {"q": "Design a distributed cache like Redis.", "difficulty": "Advanced"},
        {"q": "Design a real-time notification system for 500M users.", "difficulty": "Expert"},
        {"q": "Design a video streaming service like YouTube.", "difficulty": "Advanced"},
    ],
    "Machine Learning": [
        {"q": "What is the curse of dimensionality?", "difficulty": "Intermediate"},
        {"q": "Explain the difference between L1 and L2 regularization.", "difficulty": "Intermediate"},
        {"q": "What is vanishing gradient problem and how do you solve it?", "difficulty": "Advanced"},
        {"q": "Explain how BERT works.", "difficulty": "Advanced"},
        {"q": "What is contrastive learning?", "difficulty": "Advanced"},
    ],
    "SQL": [
        {"q": "What is the difference between WHERE and HAVING?", "difficulty": "Beginner"},
        {"q": "Explain window functions in SQL.", "difficulty": "Intermediate"},
        {"q": "What are CTEs and when do you use them?", "difficulty": "Intermediate"},
        {"q": "How do you optimize a slow SQL query?", "difficulty": "Advanced"},
        {"q": "Explain the difference between clustered and non-clustered indexes.", "difficulty": "Intermediate"},
    ],
    "Cloud Computing": [
        {"q": "What is the shared responsibility model in cloud security?", "difficulty": "Beginner"},
        {"q": "Explain the difference between EC2, ECS, and Lambda.", "difficulty": "Intermediate"},
        {"q": "What is eventual consistency and when is it acceptable?", "difficulty": "Advanced"},
        {"q": "How does AWS IAM work?", "difficulty": "Intermediate"},
    ],
    "Deep Learning": [
        {"q": "Explain the transformer architecture.", "difficulty": "Intermediate"},
        {"q": "What is batch normalization and why does it work?", "difficulty": "Intermediate"},
        {"q": "Explain how GANs work.", "difficulty": "Advanced"},
        {"q": "What is the attention mechanism?", "difficulty": "Intermediate"},
        {"q": "Explain knowledge distillation.", "difficulty": "Advanced"},
    ],
    "Generative AI": [
        {"q": "What is a large language model?", "difficulty": "Beginner"},
        {"q": "Explain prompt engineering techniques.", "difficulty": "Intermediate"},
        {"q": "What is retrieval-augmented generation (RAG)?", "difficulty": "Intermediate"},
        {"q": "How does RLHF work?", "difficulty": "Advanced"},
        {"q": "What are the tradeoffs between fine-tuning and RAG?", "difficulty": "Advanced"},
    ],
    "Object-Oriented Programming": [
        {"q": "Explain the four pillars of OOP.", "difficulty": "Beginner"},
        {"q": "What is the difference between abstract class and interface?", "difficulty": "Intermediate"},
        {"q": "Explain design patterns you've used in production.", "difficulty": "Advanced"},
        {"q": "What is the composition over inheritance principle?", "difficulty": "Intermediate"},
    ],
}

# ─────────────────────────────────────────────────────────────
# CODING CHALLENGES
# ─────────────────────────────────────────────────────────────

CODING_CHALLENGES = [
    {
        "title": "Two Sum",
        "topic": "Arrays",
        "difficulty": "Easy",
        "problem": "Given an array of integers `nums` and an integer `target`, return the indices of the two numbers that add up to `target`.\n\nExample:\nInput: nums = [2, 7, 11, 15], target = 9\nOutput: [0, 1]\n\nConstraints: Each input has exactly one solution. Do not use the same element twice.",
        "hints": ["Use a hash map to store seen values.", "One pass O(n) solution is possible."],
        "approach": "Hash map approach: iterate array, for each num check if (target - num) exists in map.",
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    },
    {
        "title": "Reverse a Linked List",
        "topic": "Linked Lists",
        "difficulty": "Easy",
        "problem": "Given the head of a singly linked list, reverse the list and return the reversed list.\n\nExample:\nInput: 1 -> 2 -> 3 -> 4 -> 5\nOutput: 5 -> 4 -> 3 -> 2 -> 1",
        "hints": ["Use three pointers: prev, curr, next.", "Iterative approach is simpler; recursive is elegant."],
        "approach": "Iterate with prev=None, curr=head. For each node: save next, point curr.next to prev, advance.",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    {
        "title": "Valid Parentheses",
        "topic": "Strings",
        "difficulty": "Easy",
        "problem": "Given a string s containing just '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\nA string is valid if open brackets are closed by the same type of brackets and in the correct order.\n\nExample:\nInput: s = \"()[]{}\"\nOutput: true\n\nInput: s = \"(]\"\nOutput: false",
        "hints": ["Use a stack.", "Map closing brackets to opening brackets."],
        "approach": "Stack-based: push open brackets, pop and verify when seeing closing brackets.",
        "time_complexity": "O(n)",
        "space_complexity": "O(n)"
    },
    {
        "title": "Maximum Subarray (Kadane's Algorithm)",
        "topic": "Arrays",
        "difficulty": "Medium",
        "problem": "Given an integer array nums, find the contiguous subarray which has the largest sum and return its sum.\n\nExample:\nInput: nums = [-2,1,-3,4,-1,2,1,-5,4]\nOutput: 6\nExplanation: [4,-1,2,1] has the largest sum = 6.",
        "hints": ["Track current sum and max sum.", "Reset current sum to 0 if it goes negative."],
        "approach": "Kadane's: maintain max_current and max_global. At each step: max_current = max(nums[i], max_current + nums[i]).",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)"
    },
    {
        "title": "Binary Search",
        "topic": "Searching",
        "difficulty": "Easy",
        "problem": "Given a sorted array of integers and a target value, return the index of target if found, else -1.\n\nYou must write an algorithm with O(log n) runtime complexity.\n\nExample:\nInput: nums = [-1,0,3,5,9,12], target = 9\nOutput: 4",
        "hints": ["Classic divide and conquer.", "Be careful with mid calculation to avoid overflow: mid = left + (right - left) // 2."],
        "approach": "Maintain left, right pointers. Check mid element, narrow search space by half each iteration.",
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)"
    },
    {
        "title": "Merge Two Sorted Lists",
        "topic": "Linked Lists",
        "difficulty": "Easy",
        "problem": "Merge two sorted linked lists and return it as a sorted list.\n\nExample:\nInput: l1 = 1->2->4, l2 = 1->3->4\nOutput: 1->1->2->3->4->4",
        "hints": ["Use a dummy head node.", "Compare heads and advance the smaller one."],
        "approach": "Dummy head pointer. At each step, compare l1.val and l2.val, attach smaller, advance that pointer.",
        "time_complexity": "O(m+n)",
        "space_complexity": "O(1)"
    },
    {
        "title": "Climbing Stairs",
        "topic": "Dynamic Programming",
        "difficulty": "Easy",
        "problem": "You are climbing a staircase. It takes n steps to reach the top. Each time you can climb 1 or 2 steps. How many distinct ways can you climb to the top?\n\nExample:\nInput: n = 3\nOutput: 3\nExplanation: 1+1+1, 1+2, 2+1",
        "hints": ["This is essentially Fibonacci.", "dp[i] = dp[i-1] + dp[i-2]"],
        "approach": "DP: dp[0]=1, dp[1]=1. For i from 2 to n: dp[i] = dp[i-1] + dp[i-2].",
        "time_complexity": "O(n)",
        "space_complexity": "O(1) optimized"
    },
    {
        "title": "LRU Cache",
        "topic": "Data Structures",
        "difficulty": "Medium",
        "problem": "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.\n\nImplement: LRUCache(capacity), get(key), put(key, value).\n\nBoth get and put must run in O(1) average time complexity.",
        "hints": ["Combine a HashMap with a Doubly Linked List.", "Use a dummy head and tail for easier manipulation."],
        "approach": "HashMap for O(1) lookup + Doubly Linked List for O(1) insertion/deletion. Move accessed node to front.",
        "time_complexity": "O(1)",
        "space_complexity": "O(capacity)"
    },
    {
        "title": "Number of Islands",
        "topic": "Graphs",
        "difficulty": "Medium",
        "problem": "Given an m x n 2D binary grid which represents a map of '1's (land) and '0's (water), return the number of islands.\n\nExample:\nInput: grid = [['1','1','0'],['1','1','0'],['0','0','1']]\nOutput: 2",
        "hints": ["DFS or BFS from each unvisited '1'.", "Mark visited cells to avoid recounting."],
        "approach": "Iterate grid. When '1' found: increment count, DFS to mark all connected '1's as visited.",
        "time_complexity": "O(m*n)",
        "space_complexity": "O(m*n)"
    },
    {
        "title": "Longest Palindromic Substring",
        "topic": "Dynamic Programming",
        "difficulty": "Medium",
        "problem": "Given a string s, return the longest palindromic substring in s.\n\nExample:\nInput: s = \"babad\"\nOutput: \"bab\" (or \"aba\")",
        "hints": ["Expand around center approach is O(n²) space O(1).", "Two cases: odd length (single center) and even length (two centers)."],
        "approach": "For each character, expand outward for both odd and even length palindromes, track longest found.",
        "time_complexity": "O(n²)",
        "space_complexity": "O(1)"
    },
    {
        "title": "Word Search",
        "topic": "Recursion",
        "difficulty": "Medium",
        "problem": "Given an m x n grid of characters board and a string word, return true if word exists in the grid.\n\nThe word can be constructed from letters of sequentially adjacent cells. Adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.",
        "hints": ["Backtracking DFS.", "Mark cells as visited temporarily during exploration."],
        "approach": "DFS with backtracking. For each cell matching word[0], try all 4 directions. Unmark on backtrack.",
        "time_complexity": "O(M*N*4^L) where L=word length",
        "space_complexity": "O(L)"
    },
    {
        "title": "SQL: Find Employees Earning More Than Their Manager",
        "topic": "SQL",
        "difficulty": "Easy",
        "problem": "Given Employee table with (Id, Name, Salary, ManagerId), write a SQL query to find all employees who earn more than their managers.\n\nEmployee table:\nId | Name  | Salary | ManagerId\n1  | Joe   | 70000  | 3\n2  | Henry | 80000  | 4\n3  | Sam   | 60000  | NULL\n4  | Max   | 90000  | NULL\n\nExpected Output: Joe",
        "hints": ["Self-join the Employee table.", "Join on employee.ManagerId = manager.Id"],
        "approach": "SELECT e1.Name FROM Employee e1 JOIN Employee e2 ON e1.ManagerId = e2.Id WHERE e1.Salary > e2.Salary;",
        "time_complexity": "O(n²) naive, O(n log n) with indexes",
        "space_complexity": "O(n)"
    },
]

# ─────────────────────────────────────────────────────────────
# COMPANY-SPECIFIC INTERVIEW PROFILES
# ─────────────────────────────────────────────────────────────

COMPANY_PROFILES: Dict[str, Dict] = {
    "Google": {
        "style": "Heavy emphasis on algorithms, data structures, and system design. Expect 5 rounds: coding (2), system design (1), behavioral (1), Googleyness (1).",
        "focus_areas": ["Data Structures & Algorithms", "System Design", "Googleyness & Leadership", "Coding Efficiency"],
        "difficulty": "Expert",
        "questions": [
            {"q": "Design Google Search autocomplete feature.", "type": "system_design"},
            {"q": "Given a list of words and a pattern, find all words matching the pattern.", "type": "coding"},
            {"q": "Tell me about a time you worked on an ambiguous problem and how you structured your approach.", "type": "behavioral"},
            {"q": "Design YouTube's video recommendation system.", "type": "system_design"},
            {"q": "Find the kth largest element in an unsorted array in O(n) average time.", "type": "coding"},
            {"q": "How would you improve Google Maps?", "type": "product"},
        ]
    },
    "Microsoft": {
        "style": "Focus on problem-solving, cultural fit, and collaboration. Expect 4-5 rounds with emphasis on growth mindset.",
        "focus_areas": ["Problem Solving", "Collaboration", "Growth Mindset", "System Design"],
        "difficulty": "Advanced",
        "questions": [
            {"q": "Design a collaborative document editing system like Google Docs.", "type": "system_design"},
            {"q": "Describe a time you had to learn from failure and what you changed.", "type": "behavioral"},
            {"q": "How would you design Azure's load balancer?", "type": "system_design"},
            {"q": "Implement a function to serialize and deserialize a binary tree.", "type": "coding"},
            {"q": "Tell me about a time you influenced without authority.", "type": "behavioral"},
        ]
    },
    "Amazon": {
        "style": "Heavily behavioral — every answer must reference Leadership Principles. Expect STAR format for all behavioral questions.",
        "focus_areas": ["Leadership Principles", "Customer Obsession", "System Design at Scale", "Ownership"],
        "difficulty": "Advanced",
        "questions": [
            {"q": "Tell me about a time you took ownership of a project that wasn't your responsibility.", "type": "behavioral", "lp": "Ownership"},
            {"q": "Describe a time you used data to make a decision when others disagreed.", "type": "behavioral", "lp": "Are Right, A Lot"},
            {"q": "Design Amazon's order management system.", "type": "system_design"},
            {"q": "Tell me about a time you invented something — a process, tool, or approach.", "type": "behavioral", "lp": "Invent and Simplify"},
            {"q": "Design a warehouse inventory tracking system.", "type": "system_design"},
            {"q": "Tell me about a time you disagreed with your team and held your position.", "type": "behavioral", "lp": "Have Backbone; Disagree and Commit"},
        ]
    },
    "Meta": {
        "style": "Focus on scalability, product thinking, and behavioral interviews. Strong emphasis on moving fast and impact.",
        "focus_areas": ["Scalability", "Product Sense", "Behavioral (Impact focused)", "Systems"],
        "difficulty": "Expert",
        "questions": [
            {"q": "Design Facebook's News Feed ranking system.", "type": "system_design"},
            {"q": "Tell me about the most impactful project you've worked on. What made it impactful?", "type": "behavioral"},
            {"q": "Design Instagram Stories.", "type": "product"},
            {"q": "How would you detect fake accounts on Meta's platforms?", "type": "system_design"},
            {"q": "Given a social graph, find all mutual friends between two users efficiently.", "type": "coding"},
        ]
    },
    "Apple": {
        "style": "Focus on attention to detail, design thinking, and technical depth. Strong cultural emphasis on excellence.",
        "focus_areas": ["Attention to Detail", "Technical Excellence", "Design Thinking", "Team Collaboration"],
        "difficulty": "Advanced",
        "questions": [
            {"q": "Design the Apple Pay transaction processing system.", "type": "system_design"},
            {"q": "How would you improve the iPhone's battery life through software optimization?", "type": "product"},
            {"q": "Tell me about a time you pushed back on a design decision and why.", "type": "behavioral"},
            {"q": "Implement an autocomplete feature for iOS keyboard.", "type": "coding"},
        ]
    },
    "Netflix": {
        "style": "Strong emphasis on culture fit — high performance, freedom & responsibility. Values independent thinkers.",
        "focus_areas": ["Systems at Scale", "Culture Fit", "Streaming Tech", "Data-driven Decisions"],
        "difficulty": "Expert",
        "questions": [
            {"q": "Design Netflix's video recommendation engine.", "type": "system_design"},
            {"q": "How would you build a content delivery network for streaming?", "type": "system_design"},
            {"q": "Tell me about a time you had radical candor with a colleague.", "type": "behavioral"},
            {"q": "How would you A/B test a new Netflix feature?", "type": "product"},
        ]
    },
    "Adobe": {
        "style": "Balanced technical and creative. Emphasis on problem-solving, collaboration, and building for diverse users.",
        "focus_areas": ["Problem Solving", "User-Centered Design", "Technical Skills", "Collaboration"],
        "difficulty": "Intermediate",
        "questions": [
            {"q": "Design a collaborative design tool like Figma.", "type": "system_design"},
            {"q": "How would you implement image compression algorithm?", "type": "coding"},
            {"q": "Describe a time you made a product more accessible to users.", "type": "behavioral"},
        ]
    },
    "Oracle": {
        "style": "Heavy database and enterprise focus. Expect deep SQL, database internals, and Java/cloud questions.",
        "focus_areas": ["Database Internals", "SQL & PL/SQL", "Java", "Cloud Infrastructure"],
        "difficulty": "Advanced",
        "questions": [
            {"q": "Explain how database transactions and MVCC work internally.", "type": "technical"},
            {"q": "Write a PL/SQL procedure to find duplicate records.", "type": "coding"},
            {"q": "Design a high-availability database clustering solution.", "type": "system_design"},
        ]
    },
    "IBM": {
        "style": "Strong focus on enterprise solutions, AI (Watson), and cloud (IBM Cloud). Behavioral emphasis on innovation.",
        "focus_areas": ["Enterprise Architecture", "AI/ML", "Cloud Solutions", "Problem Solving"],
        "difficulty": "Advanced",
        "questions": [
            {"q": "How would you migrate a legacy on-premise system to the cloud?", "type": "system_design"},
            {"q": "Design an enterprise AI chatbot solution.", "type": "system_design"},
            {"q": "Tell me about a time you innovated in a constrained environment.", "type": "behavioral"},
        ]
    },
    "OpenAI": {
        "style": "Deep AI/ML focus. Emphasis on safety, research, and building responsible AI systems.",
        "focus_areas": ["LLMs & Transformers", "AI Safety", "ML Research", "Systems Programming"],
        "difficulty": "Expert",
        "questions": [
            {"q": "How would you design an AI content moderation system that is fair and effective?", "type": "system_design"},
            {"q": "Explain the challenges of aligning LLMs with human values.", "type": "technical"},
            {"q": "How would you evaluate the factuality of an LLM's outputs at scale?", "type": "technical"},
            {"q": "Design GPT-4's inference infrastructure for millions of concurrent users.", "type": "system_design"},
        ]
    },
    "Infosys": {
        "style": "Focus on fundamentals, process, and client delivery. Behavioral questions focus on teamwork and adaptability.",
        "focus_areas": ["Programming Fundamentals", "Database", "OOP", "Problem Solving"],
        "difficulty": "Beginner",
        "questions": [
            {"q": "Explain the software development lifecycle and which models you've used.", "type": "technical"},
            {"q": "Write a program to find the second largest element in an array.", "type": "coding"},
            {"q": "Tell me about a time you worked with a difficult client requirement.", "type": "behavioral"},
            {"q": "What is normalization in databases? Explain up to 3NF.", "type": "technical"},
        ]
    },
    "TCS": {
        "style": "Strong emphasis on fundamentals, aptitude, and communication. Process-oriented culture.",
        "focus_areas": ["Aptitude", "Programming Basics", "Communication", "Domain Knowledge"],
        "difficulty": "Beginner",
        "questions": [
            {"q": "What are the differences between process and thread?", "type": "technical"},
            {"q": "Write a program to check if a string is a palindrome.", "type": "coding"},
            {"q": "Explain OOPS concepts with real-world examples.", "type": "technical"},
            {"q": "Tell me about yourself and your career goals.", "type": "hr"},
        ]
    },
    "Accenture": {
        "style": "Balanced technical and consulting. Values adaptability, client focus, and innovation.",
        "focus_areas": ["Problem Solving", "Communication", "Technology Consulting", "Agile"],
        "difficulty": "Intermediate",
        "questions": [
            {"q": "How would you advise a traditional retail client on digital transformation?", "type": "consulting"},
            {"q": "Describe your experience with Agile methodology.", "type": "technical"},
            {"q": "Tell me about a time you dealt with an ambiguous requirement from a client.", "type": "behavioral"},
        ]
    },
    "Capgemini": {
        "style": "Focus on technology consulting, digital transformation, and cloud. Values teamwork.",
        "focus_areas": ["Cloud Computing", "Digital Transformation", "Programming", "Teamwork"],
        "difficulty": "Intermediate",
        "questions": [
            {"q": "What cloud certifications do you have and how have you applied cloud skills?", "type": "technical"},
            {"q": "How would you implement DevOps practices in a legacy organization?", "type": "consulting"},
            {"q": "Describe a successful team project you led.", "type": "behavioral"},
        ]
    },
    "Wipro": {
        "style": "Strong fundamentals, process adherence, and client delivery. Values communication.",
        "focus_areas": ["Core Programming", "Testing", "Communication", "Process"],
        "difficulty": "Beginner",
        "questions": [
            {"q": "Explain different types of software testing.", "type": "technical"},
            {"q": "Write SQL to find the 3rd highest salary.", "type": "coding"},
            {"q": "Describe how you handled a challenging project deadline.", "type": "behavioral"},
        ]
    },
}


# ─────────────────────────────────────────────────────────────
# BADGE CATALOG
# ─────────────────────────────────────────────────────────────

INTERVIEW_BADGE_CATALOG = [
    {"id": "interview_beginner",     "name": "Interview Beginner",   "emoji": "🎯", "color": "#60a5fa", "description": "Completed your first interview session",         "condition": "complete_1_session"},
    {"id": "technical_master",       "name": "Technical Master",     "emoji": "⚙️", "color": "#a78bfa", "description": "Scored 85%+ in a Technical interview",          "condition": "technical_score_85"},
    {"id": "hr_expert",              "name": "HR Expert",            "emoji": "🤝", "color": "#34d399", "description": "Scored 85%+ in an HR interview",                "condition": "hr_score_85"},
    {"id": "coding_champion",        "name": "Coding Champion",      "emoji": "💻", "color": "#f59e0b", "description": "Solved 5 coding challenges successfully",       "condition": "coding_5_solved"},
    {"id": "ai_engineer_ready",      "name": "AI Engineer Ready",    "emoji": "🤖", "color": "#f472b6", "description": "Completed AI Engineer mock interview",           "condition": "role_ai_engineer"},
    {"id": "communication_pro",      "name": "Communication Pro",    "emoji": "🗣️", "color": "#38bdf8", "description": "Scored 90%+ on communication in 3 sessions",   "condition": "communication_90_3x"},
    {"id": "hundred_interview_club", "name": "100 Interview Club",   "emoji": "💯", "color": "#ff6b6b", "description": "Completed 100 interview sessions",              "condition": "complete_100_sessions"},
    {"id": "behavioral_star",        "name": "Behavioral STAR",      "emoji": "⭐", "color": "#fbbf24", "description": "Completed 5 behavioral interviews",             "condition": "behavioral_5_sessions"},
    {"id": "consistency_king",       "name": "Consistency King",     "emoji": "🔥", "color": "#f97316", "description": "7-day interview practice streak",               "condition": "7_day_streak"},
    {"id": "perfectionist",          "name": "Perfectionist",        "emoji": "🏆", "color": "#10b981", "description": "Scored 95%+ in any interview",                 "condition": "score_95_any"},
]


# ─────────────────────────────────────────────────────────────
# HELPER FUNCTIONS & RANDOMIZATION ENGINE
# ─────────────────────────────────────────────────────────────

TECH_CONCEPTS = {
    "AI Engineer": [
        "parameter-efficient fine-tuning (PEFT)", "rag orchestration pipelines", 
        "vector embedding strategy", "llm alignment techniques (RLHF/DPO)", 
        "mixture-of-experts (MoE) architectures", "attention mechanism bottlenecks"
    ],
    "Machine Learning Engineer": [
        "data leakage prevention", "feature store architectures", "model drift monitoring",
        "distributed training strategies", "online model evaluation", "quantization and pruning techniques"
    ],
    "Software Engineer": [
        "microservices orchestration", "concurrency and race conditions", "eventual consistency",
        "distributed database sharding", "caching invalidation strategies", "asynchronous event loops"
    ],
    "Frontend Developer": [
        "browser rendering pipelines", "state propagation bottlenecks", "micro-frontends routing",
        "web accessibility (WCAG) audits", "virtual DOM diffing performance", "code splitting & lazy loading patterns"
    ],
    "Backend Developer": [
        "database transaction isolation levels", "distributed locking mechanisms", "rate limiting algorithms",
        "connection pooling exhaustion", "REST vs gRPC trade-offs", "message queue backpressure"
    ],
    "Full Stack Developer": [
        "end-to-end type safety", "state synchronization between client and server", "monorepo build optimization",
        "CORS policy design", "real-time WebSocket updates", "static site generation vs server-side rendering"
    ],
    "Data Scientist": [
        "causal inference & propensity score matching", "exploratory data analysis heuristics",
        "handling non-random missing data (MNAR)", "multi-armed bandit testing vs A/B testing",
        "dimensionality reduction projection loss", "statistical power and sample size calculation"
    ],
    "Data Analyst": [
        "cohort analysis and user retention metrics", "SQL window function performance", "data warehousing star schemas",
        "anomaly detection in metrics", "interactive dashboard design patterns", "automated reporting ETL pipelines"
    ],
    "DevOps Engineer": [
        "blue-green vs canary deployments", "Infrastructure-as-Code state locking", "chaos engineering experiment design",
        "multi-tenant Kubernetes security", "CI/CD pipeline parallelization", "service mesh traffic routing"
    ],
    "Cloud Engineer": [
        "multi-region active-active failover", "cloud cost optimization metrics", "serverless scaling cold starts",
        "virtual private cloud peering topologies", "distributed object storage policies", "cross-region data replication latency"
    ],
    "Cybersecurity Engineer": [
        "zero-trust networking access", "threat modeling STRIDE methodologies", "OWASP Top 10 prevention strategies",
        "securing API authentication handshakes", "incident response containment", "differential privacy algorithms"
    ],
    "Android Developer": [
        "Jetpack Compose recomposition cycles", "offline-first database synchronization", "memory leak profiling in Android",
        "coroutines exception handling", "app bundle modularization", "Android background task constraints"
    ],
    "Product Manager": [
        "RICE prioritization framework", "North Star metric definition", "user retention funnel analysis",
        "go-to-market strategies for SaaS", "managing technical debt trade-offs", "phased feature rollouts"
    ],
    "UI/UX Designer": [
        "design system token structures", "cognitive load reduction strategies", "heuristic evaluation principles",
        "accessible color contrast ratios", "responsive layout grid structures", "interactive prototyping friction points"
    ],
    "Python": ["GIL lock and CPU-bound tasks", "metaclass creation", "asyncio event loop optimization", "memory management and reference counting"],
    "JavaScript": ["event loop phases", "closures and memory leaks", "prototypal inheritance", "asynchronous microtasks vs macrotasks"],
    "React": ["Server Components hydration", "reconciliation diffing algorithm", "useRef vs useState render trigger", "context API performance limits"],
    "FastAPI": ["Pydantic v2 validation changes", "async route concurrent handling", "dependency injection lifespan", "background tasks concurrency"],
    "Data Structures": ["trie prefix trees optimization", "skip list search complexity", "B+ tree leaf traversal", "hash map collision resolution"],
    "Algorithms": ["amortized time complexity", "dynamic programming memoization space", "Dijkstra vs A* heuristics", "sorting stability trade-offs"],
    "System Design": ["consistent hashing", "Saga pattern for distributed transactions", "write-ahead logging", "read/write throughput scaling"],
    "Machine Learning": ["bias-variance trade-offs", "L1 vs L2 regularization gradients", "hyperparameter search validation", "feature selection methods"],
    "SQL": ["query planner indexes scan", "transaction isolation levels", "recursive common table expressions", "sharding vs partition key selection"],
    "Cloud Computing": ["regions vs availability zones", "serverless lambda cold start optimization", "shared responsibility model", "VPC routing configuration"],
    "Deep Learning": ["exploding and vanishing gradients", "attention weight computation", "batch normalization vs layer normalization", "dropout regularization effect"],
    "Generative AI": ["RAG retrieval validation", "context window size performance", "RLHF reward modeling", "quantization precision trade-offs"],
    "Object-Oriented Programming": ["Liskov substitution principle", "dependency inversion", "composition vs inheritance", "factory vs strategy design patterns"]
}

def rephrase_question(q: str) -> str:
    """Wrap a question dynamically in diverse professional contexts to make it feel fresh."""
    q_clean = q.rstrip('?').strip()
    
    # Check if the question is already complex/long to avoid making it overly wordy
    if len(q_clean) > 80:
        return q
        
    wrappers = [
        f"{q_clean}, particularly when designing for high-throughput production environments?",
        f"How would you explain the concept of '{q_clean}' to a junior engineer you are mentoring?",
        f"What are the major engineering trade-offs and scaling limitations associated with: {q_clean}?",
        f"Can you walk through a production incident or system bottleneck you resolved related to: {q_clean}?",
        f"If you were architecting a high-availability system, how would you approach: {q_clean}?",
        f"What are the best practices, security implications, and design patterns when dealing with: {q_clean}?",
    ]
    return random.choice(wrappers)

def generate_random_tech_question(topic: str) -> Dict:
    """Generate a dynamic technical question based on a role or technical topic."""
    concepts = TECH_CONCEPTS.get(topic, ["performance optimization", "architectural scaling", "best practices"])
    concept = random.choice(concepts)
    templates = [
        f"How would you address the challenges of {concept} when developing a high-performance system using {topic}?",
        f"Can you explain the trade-offs and performance implications of {concept} in a {topic} environment?",
        f"What are the best practices for implementing and testing {concept} within a project utilizing {topic}?",
        f"Describe a scenario where {concept} would be critical to resolve a production bottleneck in {topic}.",
        f"How do you evaluate security and reliability when integrating {concept} in a {topic}-based stack?",
    ]
    return {"q": random.choice(templates), "hint": f"Focus on concrete patterns, optimization techniques, and trade-offs related to {concept}."}

def generate_random_behavioral_question() -> Dict:
    """Generate a dynamic behavioral (STAR) question."""
    competencies = ["Leadership", "Conflict Resolution", "Adaptability", "Problem Solving", "Collaboration", "Decision Making", "Time Management"]
    situations = [
        "when a critical system failed in production right before a major client demo",
        "when you had to deliver a complex feature under an extremely tight deadline with resource constraints",
        "when you disagreed with your manager or a technical lead on an architectural decision",
        "when you had to work with a team member who had a very different work style or was uncooperative",
        "when you had to take ownership of a legacy codebase with zero documentation and fix a high-priority bug",
        "when you discovered a major security vulnerability or data leak threat during a routine review",
        "when you had to pivot your technical implementation completely due to changing client requirements"
    ]
    situation = random.choice(situations)
    competency = random.choice(competencies)
    templates = [
        f"Tell me about a time {situation}. What actions did you take, and how did you measure success?",
        f"Describe a situation {situation}. What was the outcome, and what would you do differently next time?",
        f"Give an example of a time {situation}. How did you handle communication and stakeholder expectations?",
        f"Reflecting on a time {situation}, how did this experience shape your approach to {competency}?"
    ]
    return {
        "q": random.choice(templates),
        "competency": competency,
        "format": "STAR"
    }

def generate_random_hr_question() -> Dict:
    """Generate a dynamic HR or culture fit question."""
    categories = ["Culture Fit", "Motivation", "Career Growth", "Time Management", "Collaboration"]
    topics = [
        "balancing short-term project deadlines with long-term technical excellence",
        "fostering an inclusive, collaborative culture within a highly remote team",
        "handling constructive feedback on your work from stakeholders or peers",
        "staying motivated when working on routine maintenance vs new feature development",
        "your ideal team dynamic and how you contribute to team cohesion",
        "navigating career growth while aligning with company objectives"
    ]
    topic = random.choice(topics)
    category = random.choice(categories)
    templates = [
        f"What is your philosophy on {topic}, and how has it evolved throughout your career?",
        f"Can you share your perspective on {topic} and how you would apply it to this role?",
        f"How do you personally handle situations involving {topic} to ensure a positive outcome?",
        f"Why is {topic} important to you, and what kind of environment enables you to succeed in this area?"
    ]
    return {
        "q": random.choice(templates),
        "category": category,
        "hint": "Be authentic, draw from your personal experiences, and show self-awareness."
    }

def randomize_coding_challenge(challenge: dict) -> dict:
    """Inject randomized parameters, target values, constraints, and arrays into coding challenges on the fly."""
    import copy
    c = copy.deepcopy(challenge)
    title = c.get("title", "")
    
    if title == "Two Sum":
        diff = random.randint(3, 10)
        a = random.randint(1, 15)
        b = random.randint(1, 15)
        while a == b:
            b = random.randint(1, 15)
        nums = [a, b]
        for _ in range(2):
            val = random.randint(1, 15)
            while val in nums:
                val = random.randint(1, 15)
            nums.append(val)
        random.shuffle(nums)
        target = a + b
        idx_a = nums.index(a)
        idx_b = nums.index(b)
        c["problem"] = f"Given an array of integers `nums` and an integer `target`, return the indices of the two numbers that add up to `target`.\n\nExample:\nInput: nums = {nums}, target = {target}\nOutput: {sorted([idx_a, idx_b])}\n\nConstraints: Each input has exactly one solution. Do not use the same element twice."
        
    elif title == "Reverse a Linked List":
        length = random.randint(4, 7)
        start = random.randint(1, 10)
        lst = [str(start + i) for i in range(length)]
        input_str = " -> ".join(lst)
        output_str = " -> ".join(reversed(lst))
        c["problem"] = f"Given the head of a singly linked list, reverse the list and return the reversed list.\n\nExample:\nInput: {input_str}\nOutput: {output_str}"
        
    elif title == "Valid Parentheses":
        pairs = {"(": ")", "{": "}", "[": "]"}
        keys = list(pairs.keys())
        ex_true_parts = []
        for _ in range(random.randint(2, 3)):
            k = random.choice(keys)
            ex_true_parts.append(k + pairs[k])
        ex_true = "".join(ex_true_parts)
        
        k1, k2 = random.sample(keys, 2)
        ex_false = k1 + pairs[k2]
        
        c["problem"] = f"Given a string `s` containing just '(', ')', '{{', '}}', '[' and ']', determine if the input string is valid.\n\nA string is valid if open brackets are closed by the same type of brackets and in the correct order.\n\nExample 1:\nInput: s = \"{ex_true}\"\nOutput: true\n\nExample 2:\nInput: s = \"{ex_false}\"\nOutput: false"
        
    elif title == "Maximum Subarray (Kadane's Algorithm)":
        nums = [random.randint(-5, 5) for _ in range(9)]
        max_so_far = nums[0]
        curr_max = nums[0]
        for x in nums[1:]:
            curr_max = max(x, curr_max + x)
            max_so_far = max(max_so_far, curr_max)
        c["problem"] = f"Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.\n\nExample:\nInput: nums = {nums}\nOutput: {max_so_far}\nExplanation: The contiguous subarray with the maximum sum."
        
    elif title == "Binary Search":
        length = random.randint(5, 8)
        nums = sorted(random.sample(range(-10, 20), length))
        if random.choice([True, False]):
            target = random.choice(nums)
            output = nums.index(target)
        else:
            target = random.randint(-15, 25)
            while target in nums:
                target = random.randint(-15, 25)
            output = -1
        c["problem"] = f"Given a sorted array of integers `nums` and a `target` value, return the index of `target` if found, else -1.\n\nYou must write an algorithm with O(log n) runtime complexity.\n\nExample:\nInput: nums = {nums}, target = {target}\nOutput: {output}"
        
    elif title == "Merge Two Sorted Lists":
        length1 = random.randint(2, 4)
        length2 = random.randint(2, 4)
        l1 = sorted(random.sample(range(1, 15), length1))
        l2 = sorted(random.sample(range(1, 15), length2))
        out = sorted(l1 + l2)
        l1_str = "->".join(map(str, l1))
        l2_str = "->".join(map(str, l2))
        out_str = "->".join(map(str, out))
        c["problem"] = f"Merge two sorted linked lists and return it as a sorted list.\n\nExample:\nInput: l1 = {l1_str}, l2 = {l2_str}\nOutput: {out_str}"
        
    elif title == "Climbing Stairs":
        n = random.randint(3, 6)
        a, b = 1, 1
        for _ in range(n - 1):
            a, b = b, a + b
        c["problem"] = f"You are climbing a staircase. It takes n steps to reach the top. Each time you can climb 1 or 2 steps. How many distinct ways can you climb to the top?\n\nExample:\nInput: n = {n}\nOutput: {b}"
        
    elif title == "LRU Cache":
        cap = random.randint(2, 4)
        c["problem"] = f"Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.\n\nImplement: BaseLRUCache(capacity={cap}), get(key), put(key, value).\n\nBoth get and put must run in O(1) average time complexity."
        
    elif title == "Number of Islands":
        rows = random.randint(3, 4)
        cols = random.randint(3, 4)
        grid = [[random.choice(['0', '1']) for _ in range(cols)] for _ in range(rows)]
        island_grid = [row[:] for row in grid]
        islands = 0
        def dfs(r, c):
            if r < 0 or c < 0 or r >= rows or c >= cols or island_grid[r][c] == '0':
                return
            island_grid[r][c] = '0'
            dfs(r+1, c)
            dfs(r-1, c)
            dfs(r, c+1)
            dfs(r, c-1)
        for r in range(rows):
            for c in range(cols):
                if island_grid[r][c] == '1':
                    islands += 1
                    dfs(r, c)
        c["problem"] = f"Given an m x n 2D binary grid which represents a map of '1's (land) and '0's (water), return the number of islands.\n\nExample:\nInput: grid = {grid}\nOutput: {islands}"

    elif title == "Longest Palindromic Substring":
        options = ["babad", "cbbd", "a", "ac", "racecar", "noon", "abacaba"]
        s = random.choice(options)
        def get_longest_palindrome(string):
            if not string: return ""
            start, end = 0, 0
            def expand(left, right):
                while left >= 0 and right < len(string) and string[left] == string[right]:
                    left -= 1
                    right += 1
                return right - left - 1
            for i in range(len(string)):
                len1 = expand(i, i)
                len2 = expand(i, i+1)
                max_len = max(len1, len2)
                if max_len > end - start:
                    start = i - (max_len - 1) // 2
                    end = i + max_len // 2
            return string[start:end+1]
        pal = get_longest_palindrome(s)
        c["problem"] = f"Given a string `s`, return the longest palindromic substring in `s`.\n\nExample:\nInput: s = \"{s}\"\nOutput: \"{pal}\""

    elif title == "Word Search":
        cases = [
            {"board": [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "word": "ABCCED", "output": "true"},
            {"board": [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "word": "SEE", "output": "true"},
            {"board": [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "word": "ABCB", "output": "false"},
            {"board": [["C","A","T"],["B","A","T"],["R","A","T"]], "word": "CAT", "output": "true"},
            {"board": [["C","A","T"],["B","A","T"],["R","A","T"]], "word": "CAB", "output": "false"}
        ]
        case = random.choice(cases)
        c["problem"] = f"Given an m x n grid of characters `board` and a string `word`, return true if `word` exists in the grid.\n\nThe word can be constructed from letters of sequentially adjacent cells. Adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.\n\nExample:\nInput: board = {case['board']}, word = \"{case['word']}\"\nOutput: {case['output']}"

    elif title == "SQL: Find Employees Earning More Than Their Manager":
        salary_joe = random.randint(60, 95) * 1000
        salary_henry = random.randint(60, 95) * 1000
        salary_sam = random.randint(50, 75) * 1000
        salary_max = random.randint(50, 75) * 1000
        expected = []
        if salary_joe > salary_sam:
            expected.append("Joe")
        if salary_henry > salary_max:
            expected.append("Henry")
        output = ", ".join(expected) if expected else "None"
        c["problem"] = f"Given Employee table with (Id, Name, Salary, ManagerId), write a SQL query to find all employees who earn more than their managers.\n\nEmployee table:\nId | Name  | Salary | ManagerId\n1  | Joe   | {salary_joe}  | 3\n2  | Henry | {salary_henry}  | 4\n3  | Sam   | {salary_sam}  | NULL\n4  | Max   | {salary_max}  | NULL\n\nExpected Output: {output}"

    constraints = [
        "Time complexity must be strictly optimal.",
        "Do not allocate extra memory unless necessary.",
        "Handle all edge cases, including null inputs, empty collections, and extreme bounds.",
        "Optimize for readability and structured variable naming."
    ]
    random.shuffle(constraints)
    c["problem"] = c["problem"] + f"\n\nAdditional constraint: {constraints[0]}"
    return c

def get_role_questions(role: str, difficulty: str, count: int = 5) -> List[Dict]:
    """Get questions for a specific role and difficulty, randomized and dynamically rephrased."""
    role_data = ROLE_QUESTIONS.get(role, ROLE_QUESTIONS.get("Software Engineer", {}))
    diff_questions = role_data.get(difficulty, role_data.get("Intermediate", []))
    
    rephrased_bank = []
    for q in diff_questions:
        rephrased_bank.append({
            "q": rephrase_question(q["q"]),
            "hint": q.get("hint", "")
        })
        
    dynamic_qs = []
    for _ in range(count * 2):
        dynamic_qs.append(generate_random_tech_question(role))
        
    combined = rephrased_bank + dynamic_qs
    random.shuffle(combined)
    
    seen = set()
    unique_combined = []
    for item in combined:
        if item["q"] not in seen:
            seen.add(item["q"])
            unique_combined.append(item)
            
    while len(unique_combined) < count:
        q_new = generate_random_tech_question(role)
        if q_new["q"] not in seen:
            seen.add(q_new["q"])
            unique_combined.append(q_new)
            
    return unique_combined[:count]

def get_hr_questions(count: int = 10) -> List[Dict]:
    """Get randomized and dynamically rephrased HR questions."""
    rephrased_bank = []
    for q in HR_QUESTIONS:
        rephrased_bank.append({
            "q": rephrase_question(q["q"]),
            "category": q.get("category", "General"),
            "hint": q.get("hint", "")
        })
        
    dynamic_qs = [generate_random_hr_question() for _ in range(count * 2)]
    combined = rephrased_bank + dynamic_qs
    random.shuffle(combined)
    
    seen = set()
    unique_combined = []
    for item in combined:
        if item["q"] not in seen:
            seen.add(item["q"])
            unique_combined.append(item)
            
    while len(unique_combined) < count:
        q_new = generate_random_hr_question()
        if q_new["q"] not in seen:
            seen.add(q_new["q"])
            unique_combined.append(q_new)
            
    return unique_combined[:count]

def get_behavioral_questions(count: int = 5) -> List[Dict]:
    """Get randomized and dynamically rephrased behavioral questions."""
    rephrased_bank = []
    for q in BEHAVIORAL_QUESTIONS:
        rephrased_bank.append({
            "q": rephrase_question(q["q"]),
            "competency": q.get("competency", "General"),
            "format": "STAR"
        })
        
    dynamic_qs = [generate_random_behavioral_question() for _ in range(count * 2)]
    combined = rephrased_bank + dynamic_qs
    random.shuffle(combined)
    
    seen = set()
    unique_combined = []
    for item in combined:
        if item["q"] not in seen:
            seen.add(item["q"])
            unique_combined.append(item)
            
    while len(unique_combined) < count:
        q_new = generate_random_behavioral_question()
        if q_new["q"] not in seen:
            seen.add(q_new["q"])
            unique_combined.append(q_new)
            
    return unique_combined[:count]

def get_technical_questions(topics: List[str], difficulty: Optional[str], count: int = 10) -> List[Dict]:
    """Get technical questions for specified topics, dynamically rephrased and randomized."""
    selected_bank = []
    for topic in topics:
        topic_qs = TECHNICAL_QUESTIONS.get(topic, [])
        if difficulty:
            topic_qs = [q for q in topic_qs if q.get("difficulty") == difficulty] or topic_qs
        selected_bank.extend(topic_qs)
        
    rephrased_bank = []
    for q in selected_bank:
        rephrased_bank.append({
            "q": rephrase_question(q["q"]),
            "difficulty": q.get("difficulty", difficulty or "Intermediate")
        })
        
    dynamic_qs = []
    for topic in topics:
        for _ in range(max(2, count // len(topics) * 2)):
            dynamic_qs.append(generate_random_tech_question(topic))
            
    combined = rephrased_bank + dynamic_qs
    random.shuffle(combined)
    
    seen = set()
    unique_combined = []
    for item in combined:
        if item["q"] not in seen:
            seen.add(item["q"])
            unique_combined.append(item)
            
    while len(unique_combined) < count:
        random_topic = random.choice(topics) if topics else "System Design"
        q_new = generate_random_tech_question(random_topic)
        if q_new["q"] not in seen:
            seen.add(q_new["q"])
            unique_combined.append(q_new)
            
    return unique_combined[:count]

def get_coding_challenges(topics: List[str], difficulty: Optional[str], count: int = 3) -> List[Dict]:
    """Get coding challenges filtered by topic and difficulty, randomized on the fly."""
    challenges = list(CODING_CHALLENGES)
    
    if topics:
        filtered = [c for c in challenges if c["topic"] in topics]
        if filtered:
            challenges = filtered
            
    if difficulty:
        filtered = [c for c in challenges if c["difficulty"] == difficulty]
        if filtered:
            challenges = filtered
            
    randomized_challenges = [randomize_coding_challenge(c) for c in challenges]
    random.shuffle(randomized_challenges)
    return randomized_challenges[:count]

def get_company_questions(company: str, count: int = 5) -> Dict:
    """Get company profile and randomized/rephrased questions."""
    profile = COMPANY_PROFILES.get(company, {
        "style": "Standard technical interview with behavioral components.",
        "focus_areas": ["Problem Solving", "Communication", "Technical Skills"],
        "difficulty": "Intermediate",
        "questions": []
    })
    
    bank_qs = profile.get("questions", [])
    rephrased_bank = []
    for q in bank_qs:
        q_text = q.get("q", q) if isinstance(q, dict) else str(q)
        q_type = q.get("type", "general") if isinstance(q, dict) else "general"
        rephrased_bank.append({
            "q": rephrase_question(q_text),
            "type": q_type,
            "lp": q.get("lp", "") if isinstance(q, dict) else ""
        })
        
    focus_areas = profile.get("focus_areas", ["Software Engineering"])
    dynamic_qs = []
    for _ in range(count * 2):
        q_style = random.choice(["tech", "behavioral", "hr"])
        if q_style == "tech" and focus_areas:
            topic = random.choice(focus_areas)
            dq = generate_random_tech_question(topic)
            dq["type"] = "technical"
        elif q_style == "behavioral":
            dq = generate_random_behavioral_question()
            dq["type"] = "behavioral"
        else:
            dq = generate_random_hr_question()
            dq["type"] = "hr"
        dynamic_qs.append(dq)
        
    combined = rephrased_bank + dynamic_qs
    random.shuffle(combined)
    
    seen = set()
    unique_combined = []
    for item in combined:
        if item["q"] not in seen:
            seen.add(item["q"])
            unique_combined.append(item)
            
    while len(unique_combined) < count:
        q_style = random.choice(["tech", "behavioral", "hr"])
        if q_style == "tech" and focus_areas:
            topic = random.choice(focus_areas)
            dq = generate_random_tech_question(topic)
            dq["type"] = "technical"
        elif q_style == "behavioral":
            dq = generate_random_behavioral_question()
            dq["type"] = "behavioral"
        else:
            dq = generate_random_hr_question()
            dq["type"] = "hr"
        if dq["q"] not in seen:
            seen.add(dq["q"])
            unique_combined.append(dq)
            
    profile_copy = dict(profile)
    profile_copy["questions"] = unique_combined[:count]
    return profile_copy

def generate_resume_questions_from_data(resume_data: Dict[str, Any], count: int = 8) -> List[Dict]:
    """Generate personalized questions from resume data."""
    questions = []
    
    # Projects-based questions
    projects = resume_data.get("projects", [])
    for proj in projects[:3]:
        proj_name = proj.get("name", "your project") if isinstance(proj, dict) else str(proj)
        proj_tech = proj.get("technologies", []) if isinstance(proj, dict) else []
        tech_str = ", ".join(proj_tech[:3]) if proj_tech else "your tech stack"
        
        questions.extend([
            {"q": f"I see you built '{proj_name}'. Can you walk me through its architecture and the key technical decisions you made?", "source": "project"},
            {"q": f"What was the most challenging problem you solved while working on '{proj_name}'?", "source": "project"},
        ])
        if proj_tech:
            questions.append({"q": f"You used {tech_str} in '{proj_name}'. Why did you choose this stack over alternatives?", "source": "project"})
    
    # Skills-based questions
    skills = resume_data.get("skills", [])
    if isinstance(skills, list) and skills:
        top_skills = skills[:5]
        for skill in top_skills[:2]:
            skill_name = skill if isinstance(skill, str) else skill.get("name", "this skill")
            questions.append({"q": f"How proficient are you in {skill_name} and can you describe a project where you used it extensively?", "source": "skill"})
    
    # Experience-based questions
    experience = resume_data.get("experience", []) or resume_data.get("work_experience", [])
    for exp in experience[:2]:
        if isinstance(exp, dict):
            company = exp.get("company", "your previous company")
            role = exp.get("role", "your role") or exp.get("title", "your role")
            questions.append({"q": f"At {company} as {role}, what was your biggest contribution and how did it impact the team?", "source": "experience"})
    
    # Education/certification questions
    certifications = resume_data.get("certifications", [])
    for cert in certifications[:1]:
        cert_name = cert if isinstance(cert, str) else cert.get("name", "this certification")
        questions.append({"q": f"You have the {cert_name} certification. How have you applied those skills in real projects?", "source": "certification"})
    
    # Generic technical personalization
    questions.extend([
        {"q": "Looking at your resume, you have experience across multiple areas. What is your strongest technical skill and why?", "source": "general"},
        {"q": "Where do you feel you need the most improvement compared to what's on your resume?", "source": "general"},
        {"q": "What project on your resume are you most proud of, and why?", "source": "general"},
    ])
    
    random.shuffle(questions)
    return questions[:count]


def check_badge_eligibility(stats: Dict[str, Any], existing_badge_ids: List[str]) -> List[Dict]:
    """Check which badges the user has newly earned."""
    new_badges = []
    
    conditions = {
        "complete_1_session": stats.get("total_completed", 0) >= 1,
        "technical_score_85": stats.get("best_technical_score", 0) >= 85,
        "hr_score_85": stats.get("best_hr_score", 0) >= 85,
        "coding_5_solved": stats.get("coding_count", 0) >= 5,
        "role_ai_engineer": stats.get("has_ai_engineer_session", False),
        "communication_90_3x": stats.get("high_comm_sessions", 0) >= 3,
        "complete_100_sessions": stats.get("total_completed", 0) >= 100,
        "behavioral_5_sessions": stats.get("behavioral_count", 0) >= 5,
        "7_day_streak": stats.get("streak_days", 0) >= 7,
        "score_95_any": stats.get("best_score", 0) >= 95,
    }
    
    for badge in INTERVIEW_BADGE_CATALOG:
        if badge["id"] not in existing_badge_ids:
            if conditions.get(badge["condition"], False):
                new_badges.append(badge)
    
    return new_badges
