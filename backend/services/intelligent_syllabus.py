import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# Predefined high-quality progressive weekly syllabus content
SYLLABUS_DB: Dict[str, List[Dict[str, Any]]] = {
    "python": [
        {
            "title": "Python Core Syntax & Development Setup",
            "description": "Establish a professional Python local setup and master variables, data types, and basic operator structures.",
            "topics": ["Interpreter Setup (VS Code, Virtual Environments)", "Primitive Data Types (int, float, str, bool)", "Basic Operators (Arithmetic, Comparison, Logical)", "Input/Output Methods & Formatting"],
            "practice_tasks": ["Configure a virtualenv and write a hello_world.py script.", "Build a terminal-based unit converter supporting multiple metrics."],
            "mini_assignments": ["Create a dynamic user profile generator compiling input information into clean, formatted stdout."],
            "quiz": "Python Core Syntax & Operators (10 Questions)",
            "expected_outcome": "Configure isolated development environments and run Python scripts using basic data formats and expressions.",
            "estimated_hours": 8
        },
        {
            "title": "Branching, Iterations, and Functions",
            "description": "Adopt logical branching, list iterations, and modularize code using scoped functions.",
            "topics": ["Conditional Statements (if-elif-else)", "Loops (while, for, break, continue)", "Function Parameters, Returns & Scoping", "Flexible Arguments (*args, **kwargs)"],
            "practice_tasks": ["Write loops filtering prime numbers from arbitrary lists.", "Implement mathematical functions with variable-length inputs."],
            "mini_assignments": ["Design a robust text-based interactive adventure engine with helper utility functions."],
            "quiz": "Branching, Loops & Functional Scopes (10 Questions)",
            "expected_outcome": "Formulate logic using loops and structure applications cleanly into modular reusable functions.",
            "estimated_hours": 10
        },
        {
            "title": "Advanced Collections & Data Persistence",
            "description": "Leverage Python's built-in data collections and interface with local file directories.",
            "topics": ["Collections (Lists, Tuples, Dictionaries, Sets)", "List Comprehensions & Generators", "File I/O (Text, JSON, CSV operations)", "Context Managers (with statement)"],
            "practice_tasks": ["Read and aggregate statistics from a local multi-column CSV file.", "Convert a raw dictionary of records into a structured JSON string and write to disk."],
            "mini_assignments": ["Build a file-based contact journal application with database backup options."],
            "quiz": "Python Collections & File Integration (10 Questions)",
            "expected_outcome": "Efficiently query and mutate built-in data structures and serialize datasets to external system files.",
            "estimated_hours": 10
        },
        {
            "title": "Object-Oriented Programming & Exception Handling",
            "description": "Employ structural OOP patterns to build modular abstractions and handle code errors gracefully.",
            "topics": ["Class Structures & Instantiation", "OOP Pillars (Inheritance, Encapsulation, Polymorphism)", "Error Types & Stack Traces", "Try-Except-Finally Exception Handling"],
            "practice_tasks": ["Design a class hierarchy representing bank accounts with debit/credit restrictions.", "Write custom exceptions handling negative user inputs on calculators."],
            "mini_assignments": ["Develop an Inventory Management CLI using structural class hierarchies and error-handling guardrails."],
            "quiz": "OOP Abstractions & Exception Architecture (10 Questions)",
            "expected_outcome": "Construct clean OOP structures, implement custom class interfaces, and manage application errors programmatically.",
            "estimated_hours": 12
        }
    ],
    "c programming": [
        {
            "title": "Introduction to C, Data Types & Operators",
            "description": "Understand basic memory modeling, compile-build chains, and foundational C operators.",
            "topics": ["C Compilation Model (gcc, clang, makefiles)", "Primitive Types (int, float, double, char)", "Variables, Constants & Scoping rules", "Basic Operators & Formatting (printf, scanf)"],
            "practice_tasks": ["Write, compile, and run a simple CLI calculator.", "Implement a conversion tool tracking memory sizes of different data types."],
            "mini_assignments": ["Create a Celsius-to-Fahrenheit table generator using basic arithmetic operations and formatted columns."],
            "quiz": "C Compilation, Types & Basic Console I/O (10 Questions)",
            "expected_outcome": "Understand compile-time logic and write C files handling basic numbers and format specs.",
            "estimated_hours": 8
        },
        {
            "title": "Conditional Statements, Loops & Functions",
            "description": "Master structured execution in C using branch logic, iterations, and stack-frame functions.",
            "topics": ["Conditional Branches (if-else, switch-case)", "Repetitive Structures (while, for, do-while)", "Function prototypes & header declarations", "Scope, lifetime & storage classes (static, extern)"],
            "practice_tasks": ["Implement a loop that prints Fibonacci sequences up to a user limit.", "Write modular arithmetic helpers separated into header and source files."],
            "mini_assignments": ["Build a text-based console menu system executing custom mathematical operations based on selections."],
            "quiz": "Control Flow, Iterations & Function Architectures (10 Questions)",
            "expected_outcome": "Write logical checks and loops, define modular functions, and use header files for clean project structure.",
            "estimated_hours": 10
        },
        {
            "title": "Arrays, Strings & Pointers",
            "description": "Uncover memory addressing and pointer dereferencing alongside array structures and string buffers.",
            "topics": ["1D & 2D Arrays in memory", "Pointers, Addresses, and Dereferencing (* & &)", "Pointer Arithmetic and Array mapping", "Null-terminated Strings and string.h library"],
            "practice_tasks": ["Reverse an array in-place using two-pointer swapping algorithms.", "Implement custom string copy/concatenation functions using pointers directly."],
            "mini_assignments": ["Write a text manipulation tool that searches and replaces characters in string buffers without high-level abstractions."],
            "quiz": "Pointers, Memory Addressing & String Buffers (10 Questions)",
            "expected_outcome": "Navigate computer memory directly using pointer arithmetic, allocate stack array buffers, and parse strings at the character level.",
            "estimated_hours": 12
        },
        {
            "title": "Structures, File Handling & Mini Project",
            "description": "Build user-defined custom models using structs and persist records directly into binary/text files.",
            "topics": ["Custom Types (structs, unions, enums)", "Dynamic Memory (malloc, calloc, free)", "File Handlers (fopen, fread, fwrite, fclose)", "Pointer to structs & Arrow operator (->)"],
            "practice_tasks": ["Model a Student database record using struct attributes.", "Create, write, and close a local text log file using stdio streams."],
            "mini_assignments": ["Develop a CLI Database Tool allowing users to add, list, search, and save records to a binary file."],
            "quiz": "Structs, Dynamic Allocation & File I/O (10 Questions)",
            "expected_outcome": "Allocate heap memory dynamically, manage complex records using structs, and write robust persistent files in C.",
            "estimated_hours": 12
        }
    ],
    "sql": [
        {
            "title": "SQL Fundamentals & Core Queries",
            "description": "Learn relational database structures and construct basic SELECT queries with filtering criteria.",
            "topics": ["Relational Database Management Systems (RDBMS)", "SELECT statement & Column Aliases", "Filtering rows (WHERE, BETWEEN, LIKE, IN)", "Sorting & Pagination (ORDER BY, LIMIT, OFFSET)"],
            "practice_tasks": ["Install SQLite or PostgreSQL and create sample tables.", "Write queries to fetch and filter records from a sample database."],
            "mini_assignments": ["Query a dummy retail database to extract customer orders above a threshold and sort by date."],
            "quiz": "Relational Basics & Row Filtering (10 Questions)",
            "expected_outcome": "Connect to databases and write clean SELECT queries with specific filters and sorting commands.",
            "estimated_hours": 8
        },
        {
            "title": "Joins & Data Aggregation",
            "description": "Combine multi-table datasets and execute mathematical aggregates to calculate metric results.",
            "topics": ["Inner, Left, Right & Full Outer Joins", "Aggregates (SUM, AVG, MIN, MAX, COUNT)", "Grouping Rows (GROUP BY, HAVING)", "Set Operators (UNION, INTERSECT, EXCEPT)"],
            "practice_tasks": ["Write join queries resolving entity relationships (e.g. Orders to Customers).", "Compute average purchase values grouped by transaction department."],
            "mini_assignments": ["Generate an executive sales report summarizing total revenues, product counts, and customers per region."],
            "quiz": "Multi-Table Joins & Grouping Aggregates (10 Questions)",
            "expected_outcome": "Merge multi-table structures and perform metric aggregations with filter constraints on grouped buckets.",
            "estimated_hours": 10
        },
        {
            "title": "Subqueries, CTEs & Advanced Functions",
            "description": "Structure complex queries utilizing nested queries, Common Table Expressions (CTEs), and built-in transformations.",
            "topics": ["Nested Subqueries (IN, EXISTS, Scalar)", "Common Table Expressions (WITH clauses)", "String, Date & Mathematical Functions", "CASE WHEN Conditional Logic"],
            "practice_tasks": ["Implement subqueries matching records against average tables.", "Refactor long nested subqueries into readable CTE chains."],
            "mini_assignments": ["Build a customer segmentation report classification query ranking accounts by transactional activity tiers using CASE WHEN."],
            "quiz": "Subqueries, CTE Structures & String/Date functions (10 Questions)",
            "expected_outcome": "Formulate highly readable complex query pipelines, manipulate date/string formats, and model conditional evaluations in SQL.",
            "estimated_hours": 10
        }
    ],
    "machine learning": [
        {
            "title": "Data Preprocessing & EDA Fundamentals",
            "description": "Establish baseline data analysis flows by importing, cleaning, and visualizing datasets for training.",
            "topics": ["Data Cleaning (Handling Missing Values, Outliers)", "Feature Encoding (One-Hot, Ordinal, Label Encoding)", "Feature Scaling (Standardization, Normalization)", "Exploratory Data Analysis (EDA) & Correlation Matrices"],
            "practice_tasks": ["Clean a raw tabular dataset in Pandas and generate plots for variables.", "Apply standard scaling to continuous column values and encode categorical arrays."],
            "mini_assignments": ["Preprocess a housing prices dataset, handling missing features, encoding fields, and splitting into train/test sets."],
            "quiz": "Data Preprocessing & Scaling (10 Questions)",
            "expected_outcome": "Clean and transform raw datasets into formats compatible with machine learning models.",
            "estimated_hours": 8
        },
        {
            "title": "Supervised Learning Models (Regression & Classification)",
            "description": "Train, interpret, and validate baseline linear and non-linear classification/regression models.",
            "topics": ["Linear & Logistic Regression", "Decision Trees & Random Forests", "Hyperplanes & Support Vector Machines (SVM)", "Scikit-Learn estimators & predictors API"],
            "practice_tasks": ["Train a Logistic Regression model to predict binary churn indicators.", "Visualize a trained Decision Tree model to audit features of node splits."],
            "mini_assignments": ["Construct a multi-class classifier model on patient diagnostic records, comparing tree-based architectures with linear configurations."],
            "quiz": "Supervised Estimators & Classifiers (10 Questions)",
            "expected_outcome": "Deploy standard linear and tree-based classification/regression models and audit parameters.",
            "estimated_hours": 10
        },
        {
            "title": "Model Evaluation & Hyperparameter Optimization",
            "description": "Evaluate predictive quality using cross-validation and optimize hyperparameters using automated searches.",
            "topics": ["Metrics (Accuracy, Precision, Recall, F1, ROC-AUC)", "Confusion Matrices & Classification Reports", "Cross-Validation Techniques (K-Fold, Stratified)", "Search Optimization (GridSearchCV, RandomizedSearchCV)"],
            "practice_tasks": ["Plot ROC-AUC curves for validation classifiers.", "Execute randomized searches across decision tree configurations to prevent overfitting."],
            "mini_assignments": ["Build an optimized classification pipeline with automated parameter search tuning, reporting validation performance matrices."],
            "quiz": "Evaluation Metrics & Optimization Searches (10 Questions)",
            "expected_outcome": "Choose correct evaluation metrics for models and systematically fine-tune hyperparameters via scikit-learn search features.",
            "estimated_hours": 10
        },
        {
            "title": "Unsupervised Learning & Clustering",
            "description": "Uncover hidden patterns in unlabeled datasets using clustering and dimensionality reduction models.",
            "topics": ["K-Means Clustering & Elbow Method", "Hierarchical Clustering & Dendrograms", "Principal Component Analysis (PCA) for Dimensionality Reduction", "Anomaly Detection basics"],
            "practice_tasks": ["Apply PCA to reduce high-dimensional image arrays into two primary axes.", "Segment customer transactions using K-Means clustering, auditing cluster counts via Silhouette scores."],
            "mini_assignments": ["Segment an unlabelled transactional database into buyer personas, rendering cluster distributions visually."],
            "quiz": "Clustering Models & PCA Transforms (10 Questions)",
            "expected_outcome": "Segment unlabeled datasets and reduce vector features without loss of high-variance details.",
            "estimated_hours": 10
        },
        {
            "title": "Advanced Ensemble Methods & Feature Selection",
            "description": "Boost prediction accuracies by chaining estimators via bagging, boosting, and feature filters.",
            "topics": ["Gradient Boosting Models (XGBoost, LightGBM)", "Adaboost & Voting Classifiers", "Feature Selection (Recursive Feature Elimination, L1 Regularization)", "Feature Importances audit"],
            "practice_tasks": ["Train an XGBoost model on tabular transaction logs.", "Run feature importances logs on random forest classifiers to filter out noisy predictors."],
            "mini_assignments": ["Develop a churn prediction model using LightGBM, applying feature pruning to maximize performance metrics."],
            "quiz": "Ensemble Architectures & Feature Pruning (10 Questions)",
            "expected_outcome": "Implement high-performance boosting algorithms and optimize feature inputs to avoid model bloat.",
            "estimated_hours": 12
        },
        {
            "title": "Machine Learning Portfolio Project",
            "description": "Consolidate all modeling stages into a clean, end-to-end, production-ready machine learning project.",
            "topics": ["Pipeline Integration (ColumnTransformer, Pipeline classes)", "Model Serialization (Joblib, Pickle)", "Project Documentation and Performance summary", "Model inference testing"],
            "practice_tasks": ["Combine preprocessing transforms and estimator training into a single scikit-learn Pipeline class.", "Serialize a trained classifier to a local file and reload it in a test script to confirm matching outputs."],
            "mini_assignments": ["Create and document a GitHub portfolio repository containing a fully runnable machine learning project with raw preprocessing pipeline integrations."],
            "quiz": "End-to-End Pipeline & Serialization (10 Questions)",
            "expected_outcome": "Structure machine learning code into unified pipelines, serialize models, and construct project assets.",
            "estimated_hours": 12
        }
    ]
}

class IntelligentSyllabusGenerator:
    """
    Dynamically generates week-by-week syllabus configurations for any technology skill,
    handling template lookups and dynamic fallbacks.
    """
    
    @staticmethod
    def generate_week(skill: str, week_num: int, total_weeks: int, templates: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        skill_lower = skill.lower().strip()
        
        # 1. Check if we have predefined progressive weeks for this exact skill
        if skill_lower in SYLLABUS_DB:
            template_weeks = SYLLABUS_DB[skill_lower]
            return IntelligentSyllabusGenerator._adapt_template_weeks(template_weeks, week_num, total_weeks, skill)
            
        # 2. Check if we have this skill in raw json templates
        if templates and skill_lower in templates:
            weekly_breakdown = templates[skill_lower].get("weekly_breakdown", [])
            if weekly_breakdown:
                return IntelligentSyllabusGenerator._adapt_json_template_weeks(weekly_breakdown, week_num, total_weeks, skill)
                
        # 3. Dynamic Fallback Generation (keeps weeks distinct, progressive, and highly detailed)
        return IntelligentSyllabusGenerator._generate_fallback_week(skill, week_num, total_weeks)
        
    @staticmethod
    def _adapt_template_weeks(template_weeks: List[Dict[str, Any]], week_num: int, total_weeks: int, skill: str) -> Dict[str, Any]:
        """
        Adapts template weeks to fit the requested timeframe.
        Merges extra topics if shortened, or adds progressive expansions if stretched.
        """
        t_count = len(template_weeks)
        
        # Scenario A: Perfect match or normal index access
        if week_num < total_weeks:
            # For intermediate weeks, we can pull directly from template if available, or interpolate
            t_idx = min(week_num - 1, t_count - 1)
            week_data = template_weeks[t_idx].copy()
            # If we are mapping multiple template weeks to a smaller number of slots, we might adjust
            return week_data
        
        # Scenario B: This is the last week. If the timeline was shortened (total_weeks < t_count),
        # merge all remaining template weeks into this final week's content.
        if total_weeks < t_count:
            last_template_idx = total_weeks - 1
            base_week = template_weeks[last_template_idx].copy()
            
            # Combine remaining topics, practice tasks, assignments from the template
            combined_topics = list(base_week["topics"])
            combined_practice = list(base_week["practice_tasks"])
            combined_assignments = list(base_week["mini_assignments"])
            
            for extra_w in template_weeks[total_weeks:]:
                combined_topics.extend(extra_w["topics"])
                combined_practice.extend(extra_w["practice_tasks"])
                combined_assignments.extend(extra_w["mini_assignments"])
                
            # De-duplicate
            base_week["topics"] = sorted(list(set(combined_topics)))[:5]
            base_week["practice_tasks"] = sorted(list(set(combined_practice)))[:2]
            base_week["mini_assignments"] = sorted(list(set(combined_assignments)))[:2]
            base_week["title"] = f"Advanced {skill} Integration & Project Wrap-Up"
            base_week["description"] = f"Synthesize all {skill} concepts, compile portfolio elements, and finalize mini-applications."
            base_week["expected_outcome"] = f"Achieve core operational competency in all facets of {skill} and demonstrate practical portfolio integrations."
            base_week["estimated_hours"] = 12
            return base_week

        # Scenario C: Stretched timeline (total_weeks > t_count).
        # We index normally for the initial weeks, and append progressive advanced weeks for the remainder.
        if week_num <= t_count:
            return template_weeks[week_num - 1].copy()
            
        # These are stretched/added weeks
        extra_w = week_num - t_count
        if extra_w == 1:
            return {
                "title": f"Advanced {skill} Architecture & Optimization",
                "description": f"Investigate advanced performance bottlenecks, optimizations, and scaling systems in {skill}.",
                "topics": [f"Profiling {skill} code execution", "Performance bottlenecks and tuning", "Best practices and architectural design patterns"],
                "practice_tasks": [f"Benchmark standard functions inside {skill} modules.", "Refactor a core subroutine to reduce CPU/memory profiles."],
                "mini_assignments": [f"Develop an optimized, documented micro-module utilizing advanced {skill} features."],
                "quiz": f"Advanced {skill} Architecture and Optimization (10 Questions)",
                "expected_outcome": f"Debug runtime behaviors, profile memory spaces, and write highly performant scripts in {skill}.",
                "estimated_hours": 12
            }
        else:
            return {
                "title": f"{skill} Integration, Testing & CI/CD Deployment",
                "description": f"Establish automated testing boundaries and package/deploy {skill} modules into production pipelines.",
                "topics": ["Automated Unit & Integration Testing", "CI/CD deployment configurations", "Containerization/Packaging fundamentals", "Code auditing and documentation engines"],
                "practice_tasks": [f"Write a suite of automated unit tests for {skill} routines.", "Configure a CI pipeline linting code commits automatically."],
                "mini_assignments": [f"Build and compile a production-ready package or container image of a {skill} program."],
                "quiz": f"{skill} Testing, QA & Operations Assessment",
                "expected_outcome": f"Prepare, test, package, and deploy {skill} code structures according to enterprise guidelines.",
                "estimated_hours": 12
            }

    @staticmethod
    def _adapt_json_template_weeks(weekly_breakdown: List[Dict[str, Any]], week_num: int, total_weeks: int, skill: str) -> Dict[str, Any]:
        """
        Adapts raw JSON templates and enriches them with high-fidelity description,
        practice tasks, mini assignments, quiz, and outcome fields.
        """
        t_count = len(weekly_breakdown)
        
        # Determine which template week to use
        if week_num < total_weeks:
            t_idx = min(week_num - 1, t_count - 1)
            base_week = weekly_breakdown[t_idx]
            title = base_week.get("title", f"{skill} Foundations - Week {week_num}")
            topics = base_week.get("topics", [f"Core mechanics of {skill}"])
        elif total_weeks < t_count:
            # Shortened timeline, merge remaining weeks
            last_template_idx = total_weeks - 1
            base_week = weekly_breakdown[last_template_idx]
            title = f"Advanced {skill} Integration & Project Wrap-Up"
            
            combined_topics = list(base_week.get("topics", []))
            for extra_w in weekly_breakdown[total_weeks:]:
                combined_topics.extend(extra_w.get("topics", []))
            topics = sorted(list(set(combined_topics)))[:5]
        else:
            # Stretched timeline (total_weeks >= t_count)
            if week_num <= t_count:
                base_week = weekly_breakdown[week_num - 1]
                title = base_week.get("title", f"{skill} Foundations - Week {week_num}")
                topics = base_week.get("topics", [f"Core mechanics of {skill}"])
            else:
                # Extra stretched weeks
                extra_w = week_num - t_count
                if extra_w == 1:
                    title = f"Advanced {skill} Architecture & Optimization"
                    topics = [f"Profiling {skill} code execution", "Performance bottlenecks and tuning", "Best practices and architectural design patterns"]
                else:
                    title = f"{skill} Integration, Testing & CI/CD Deployment"
                    topics = ["Automated Unit & Integration Testing", "CI/CD deployment configurations", "Containerization/Packaging fundamentals", "Code auditing and documentation engines"]

        # Dynamically enrich the template week fields
        desc = f"Deep dive into {title}, focusing on the implementation and execution of {', '.join(topics[:3])}."
        
        practice = [
            f"Write practical scripts to demonstrate and test {topics[0]}.",
            f"Build a simulation code logic modeling {topics[1] if len(topics) > 1 else topics[0]} behaviors."
        ]
        assignment = [f"Implement an end-to-end task integration of {title} incorporating custom parameters."]
        quiz = f"{title} Comprehension Assessment"
        outcome = f"Configure, troubleshoot, and leverage {title} features in code pipelines."
        hours = 12 if week_num == total_weeks else (8 if week_num == 1 else 10)
        
        return {
            "title": title,
            "description": desc,
            "topics": topics,
            "practice_tasks": practice,
            "mini_assignments": assignment,
            "quiz": quiz,
            "expected_outcome": outcome,
            "estimated_hours": hours
        }

    @staticmethod
    def _generate_fallback_week(skill: str, week_num: int, total_weeks: int) -> Dict[str, Any]:
        """
        Dynamically designs progressive week configurations for unknown skills,
        guaranteeing different learning objectives each week.
        """
        # Determine progression stage
        if total_weeks <= 1:
            title = f"{skill} Fundamentals & Environment Setup"
            desc = f"Understand the core mechanics, basic syntaxes, and design setups for {skill} projects."
            topics = [f"Foundational syntax of {skill}", f"Installation & local {skill} environment configs", "Basic command operations"]
            practice = [f"Install standard {skill} toolchains and write baseline routines.", f"Execute simple code lines and test standard inputs."]
            assignment = [f"Build a basic greeting or metrics converter CLI using {skill}."]
            quiz = f"{skill} Foundations Quiz"
            outcome = f"Build, configure, and execute standard programs in {skill}."
            hours = 8
        elif total_weeks == 2:
            if week_num == 1:
                title = f"{skill} Foundations & Basic Syntax"
                desc = f"Master the starting syntax, local compilation or execution processes, and variables in {skill}."
                topics = [f"Introduction to {skill}", "Variables, constants, and data types", "Logical operators and branching statements"]
                practice = [f"Setup local compiler or runtimes for {skill}.", "Construct conditional checks using basic parameters."]
                assignment = [f"Develop an interactive branch-selector script using {skill} conditional logic."]
                quiz = f"{skill} Syntax & Configuration Quiz"
                outcome = f"Setup files, compile scripts, and manipulate variables using {skill}."
                hours = 8
            else:
                title = f"{skill} Intermediate Features & Project Integration"
                desc = f"Introduce multi-file architectures, libraries, error handling, and build a project using {skill}."
                topics = [f"Custom modules and file referencing in {skill}", "Basic collection lists and arrays", "Error boundaries and logs parsing", "Final functional project structure"]
                practice = [f"Parse a basic input array using standard {skill} routines.", "Write exception catch blocks handling conversion errors."]
                assignment = [f"Create an end-to-end persistent {skill} script that handles file data aggregation."]
                quiz = f"Intermediate {skill} Applications Assessment"
                outcome = f"Develop multi-file applications with error handling and local files interfacing in {skill}."
                hours = 12
        elif total_weeks == 3:
            if week_num == 1:
                title = f"{skill} Foundations & Scoping Rules"
                desc = f"Understand installation, environment scopes, standard variables, and arithmetic models in {skill}."
                topics = [f"Introduction to {skill} environment patterns", "Basic syntaxes, data schemas, and typings", "Conditional branches & iterations"]
                practice = [f"Install toolchains and compile Hello World in {skill}.", "Build conditional branches processing command options."]
                assignment = [f"Write a console program mapping currency values using {skill} primitives."]
                quiz = f"{skill} Setup & Basics Quiz"
                outcome = f"Run localized {skill} environments and structure simple branch executions."
                hours = 8
            elif week_num == 2:
                title = f"{skill} Intermediate Workflows & Collections"
                desc = f"Introduce complex collections, structured loops, functional parameter passings, and error diagnostics in {skill}."
                topics = [f"Lists, maps, and advanced arrays in {skill}", "Functional modularity and references", "Error tracking and debug assertions"]
                practice = [f"Write nested loops to filter objects in collections.", f"Write customized modular functions resolving data logic."]
                assignment = [f"Create a database records query manager mimicking static tables in {skill}."]
                quiz = f"Intermediate {skill} Logic & Structures Quiz"
                outcome = f"Utilize standard collections, write functional scripts, and troubleshoot error messages in {skill}."
                hours = 10
            else:
                title = f"{skill} Advanced Optimization & Project Completion"
                desc = f"Implement optimization algorithms, automated testing routines, and create a showcase {skill} project."
                topics = ["Performance optimizations and compiler configurations", "Automated unit tests execution", "Final modular project packaging"]
                practice = [f"Audit and profile a slow execution thread in {skill}.", "Construct test suites covering boundary case inputs."]
                assignment = [f"Build, test, and release a finished command-line app structured as a reusable {skill} portfolio asset."]
                quiz = f"{skill} Advanced Master Quiz"
                outcome = f"Write performance-tuned, unit-tested, and fully organized code in {skill}."
                hours = 12
        else:
            # 4 or more weeks
            pct = week_num / total_weeks
            if pct <= 0.25:
                title = f"{skill} Core Syntax & Environment Setups"
                desc = f"Establish workspace pipelines and digest primitive syntaxes, variables, and formatting rules of {skill}."
                topics = [f"Workspace configuration guides for {skill}", "Variables declaration and data classes", "Basic operator expressions"]
                practice = [f"Set up and test the {skill} interpreter or compiler.", "Create basic calculation expressions and test print commands."]
                assignment = [f"Write a script that processes numeric prompts and outputs styled strings in {skill}."]
                quiz = f"{skill} Core Operations Quiz"
                outcome = f"Build a functioning local work environment and run basic inputs/outputs using {skill}."
                hours = 8
            elif pct <= 0.50:
                title = f"{skill} Control Flows & Modular Function Design"
                desc = f"Adopt standard programming branching, loop constructs, scope boundaries, and functional modularity."
                topics = ["Condition branches and validation structures", "For and While loop indices", "Functions declarations, arguments, and return types"]
                practice = [f"Construct automated loops checking numeric arrays.", "Write functions extracting specific metrics from input params."]
                assignment = [f"Develop a text selection menu routing calculations to modular functions in {skill}."]
                quiz = f"{skill} Control Logic & Scoping Quiz"
                outcome = f"Develop robust structural branches and loops to manage script calculations in {skill}."
                hours = 10
            elif pct <= 0.75:
                title = f"{skill} Advanced Data Collections & Error Diagnostics"
                desc = f"Leverage advanced array/list schemas, file directories connectivity, and establish structural error diagnostics."
                topics = ["Structured memory containers (Lists, Dicts/Maps)", "Input/Output file streams reading & writing", "Exception interception hierarchies"]
                practice = [f"Write records into a local text log file via {skill}.", "Handle program errors dynamically without collapsing operations."]
                assignment = [f"Build a file-based task organizer program keeping entries updated on local disk files in {skill}."]
                quiz = f"{skill} Collections, Files & Exceptions Quiz"
                outcome = f"Manipulate database lists, read/write local files, and secure applications with robust exception catching in {skill}."
                hours = 10
            else:
                title = f"Advanced {skill} Engineering & Deployment Systems"
                desc = f"Apply professional scaling patterns, automated unit testing, compile optimized bundles, and complete final projects."
                topics = ["Performance optimization and memory analysis", "Automated QA and Unit Testing strategies", "Deployment, containerization, or code packaging configs"]
                practice = [f"Construct unit test scripts asserting module results in {skill}.", f"Build automated packaging logs compiling final {skill} programs."]
                assignment = [f"Deliver an optimized, fully unit-tested, and well-documented {skill} repository ready for showcase."]
                quiz = f"{skill} Professional Engineering Assessment"
                outcome = f"Perform profiling, write automated tests, package programs, and deploy final codebases in {skill}."
                hours = 12

        return {
            "title": title,
            "description": desc,
            "topics": topics,
            "practice_tasks": practice,
            "mini_assignments": assignment,
            "quiz": quiz,
            "expected_outcome": outcome,
            "estimated_hours": hours
        }
