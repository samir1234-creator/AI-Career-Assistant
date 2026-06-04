import re
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple
from domain.schemas.ats import ATSScoringRequest, ATSScoringResponse, ScoreBreakdown

class ScoringRule(ABC):
    """
    Abstract Base Class for an ATS scoring rule to adhere to the Open-Closed Principle.
    """
    @abstractmethod
    def evaluate(self, data: ATSScoringRequest) -> Tuple[int, int, List[str], List[str], List[str]]:
        """
        Evaluates the resume data.
        Returns:
            Tuple[score, max_score, strengths, weaknesses, recommendations]
        """
        pass

class SkillsScoringRule(ScoringRule):
    def evaluate(self, data: ATSScoringRequest) -> Tuple[int, int, List[str], List[str], List[str]]:
        skills_count = len(data.skills)
        max_score = 30
        strengths = []
        weaknesses = []
        recommendations = []
        
        if skills_count == 0:
            score = 0
            weaknesses.append("No skills detected in resume")
            recommendations.append("Add technical skills matching target roles")
        elif skills_count <= 3:
            score = 10
            weaknesses.append("Very limited skill list (1-3 skills)")
            recommendations.append("Expand your skills section with relevant tools, frameworks, and programming languages")
        elif skills_count <= 7:
            score = 20
            strengths.append("Good diversity of technical skills")
            recommendations.append("Include more core technical competencies and libraries to stand out")
        else:
            score = 30
            strengths.append("Strong technical skill set")
            
        return score, max_score, strengths, weaknesses, recommendations

class ProjectsScoringRule(ScoringRule):
    def evaluate(self, data: ATSScoringRequest) -> Tuple[int, int, List[str], List[str], List[str]]:
        project_count = len(data.projects)
        max_score = 25
        strengths = []
        weaknesses = []
        recommendations = []
        
        # 1. Quantity score (max 10)
        if project_count == 0:
            qty_score = 0
            weaknesses.append("No projects or work history listed on resume")
            recommendations.append("Include details of key projects and work history")
        elif project_count == 1:
            qty_score = 5
            weaknesses.append("Only one project/experience entry listed")
            recommendations.append("Include additional project/job entries to show practical application of skills")
        else:
            qty_score = 10
            strengths.append("Multiple projects/job roles listed")
            
        # 2. Quality checks (max 15)
        has_metrics = False
        has_internship = False
        has_work_exp = False
        
        metric_pattern = r'\b\d+(?:%|x|\s*k|\s*m|\s*\+)?\b|\b\d+,\d+\b'
        work_keywords = [
            r'\bexperience\b', r'\bjob\b', r'\bwork\b', r'\bemployment\b',
            r'\bdeveloper\b', r'\bengineer\b', r'\banalyst\b', r'\bmanager\b',
            r'\blead\b', r'\barchitect\b', r'\bconsultant\b', r'\bspecialist\b'
        ]
        
        for project in data.projects:
            project_lower = project.lower()
            if re.search(metric_pattern, project):
                has_metrics = True
            if "intern" in project_lower or "internship" in project_lower or "co-op" in project_lower or "trainee" in project_lower:
                has_internship = True
            for kw in work_keywords:
                if re.search(kw, project_lower):
                    has_work_exp = True
                    
        # Apply professional experience check (max 5)
        if has_work_exp:
            work_score = 5
            strengths.append("Professional work experience detected")
        else:
            work_score = 0
            if project_count > 0:
                weaknesses.append("Work experience missing")
                recommendations.append("Add professional work experience or contract roles to demonstrate industry practice")
                
        # Apply internship check (max 5)
        if has_internship:
            intern_score = 5
            strengths.append("Internship experience found")
        else:
            intern_score = 0
            if project_count > 0:
                weaknesses.append("Internship experience missing")
                recommendations.append("Include internship experience or professional entry-level roles")
                
        # Apply metrics check (max 5)
        if has_metrics:
            metrics_score = 5
            strengths.append("Project descriptions highlight measurable impact")
        else:
            metrics_score = 0
            if project_count > 0:
                weaknesses.append("Quantified achievements missing")
                recommendations.append("Add quantified project achievements (e.g. metrics, percentages, speed improvements)")
                
        score = min(qty_score + work_score + intern_score + metrics_score, max_score)
        return score, max_score, strengths, weaknesses, recommendations

class EducationScoringRule(ScoringRule):
    def evaluate(self, data: ATSScoringRequest) -> Tuple[int, int, List[str], List[str], List[str]]:
        edu_count = len(data.education)
        max_score = 15
        strengths = []
        weaknesses = []
        recommendations = []
        
        if edu_count > 0:
            score = 15
            strengths.append("Academic background clearly documented")
        else:
            score = 0
            weaknesses.append("Education details missing")
            recommendations.append("Add your education background (degrees, institutions, graduation dates)")
            
        return score, max_score, strengths, weaknesses, recommendations

class CertificationsScoringRule(ScoringRule):
    def evaluate(self, data: ATSScoringRequest) -> Tuple[int, int, List[str], List[str], List[str]]:
        cert_count = len(data.certifications)
        max_score = 10
        strengths = []
        weaknesses = []
        recommendations = []
        
        if cert_count > 0:
            score = 10
            strengths.append("Relevant certifications found")
        else:
            score = 0
            weaknesses.append("No professional certifications detected")
            recommendations.append("List professional certifications or courses related to your field")
            
        return score, max_score, strengths, weaknesses, recommendations

class AchievementsScoringRule(ScoringRule):
    def evaluate(self, data: ATSScoringRequest) -> Tuple[int, int, List[str], List[str], List[str]]:
        ach_count = len(data.achievements)
        max_score = 10
        strengths = []
        weaknesses = []
        recommendations = []
        
        if ach_count > 0:
            score = 10
            strengths.append("Achievements section detected")
        else:
            score = 0
            weaknesses.append("No achievements section detected")
            recommendations.append("Add an achievements section highlighting awards, leadership, or honors")
            
        return score, max_score, strengths, weaknesses, recommendations

class ContactInfoScoringRule(ScoringRule):
    def evaluate(self, data: ATSScoringRequest) -> Tuple[int, int, List[str], List[str], List[str]]:
        max_score = 10
        score = 0.0
        strengths = []
        weaknesses = []
        recommendations = []
        
        present_fields = []
        if data.name and data.name.strip():
            score += 1.5
            present_fields.append("Name")
        if data.email and data.email.strip():
            score += 1.5
            present_fields.append("Email")
        if data.phone and data.phone.strip():
            score += 1.5
            present_fields.append("Phone")
        if data.linkedin and data.linkedin.strip():
            score += 1.5
            present_fields.append("LinkedIn")
            
        combined_text = (data.linkedin or "") + " " + " ".join(data.projects)
        
        # Check for GitHub profile (max 2 points)
        has_github = False
        if "github" in combined_text.lower():
            has_github = True
            
        # Check for Portfolio link (max 2 points)
        has_portfolio = False
        portfolio_patterns = [r'\bportfolio\b', r'\bpersonal website\b', r'github\.io', r'vercel\.app', r'netlify\.app', r'pages\.dev']
        for pattern in portfolio_patterns:
            if re.search(pattern, combined_text.lower()):
                has_portfolio = True
                break
                
        if score == 6.0:
            strengths.append("Basic contact details available")
        else:
            missing = []
            if "Name" not in present_fields: missing.append("Name")
            if "Email" not in present_fields: missing.append("Email")
            if "Phone" not in present_fields: missing.append("Phone")
            if "LinkedIn" not in present_fields: missing.append("LinkedIn")
            weaknesses.append(f"Missing basic contact details: {', '.join(missing)}")
            recommendations.append(f"Ensure your contact details include your {', '.join(missing)}")
            
        if has_github:
            score += 2.0
            strengths.append("GitHub profile link included")
        else:
            weaknesses.append("GitHub link missing")
            recommendations.append("Add GitHub profile link to showcase your source code")
            
        if has_portfolio:
            score += 2.0
            strengths.append("Portfolio website link included")
        else:
            weaknesses.append("Portfolio website missing")
            recommendations.append("Add a personal portfolio website link to present your projects visually")
            
        return int(score), max_score, strengths, weaknesses, recommendations

class ATSScoringService:
    def __init__(self):
        self.rules: List[ScoringRule] = [
            SkillsScoringRule(),
            ProjectsScoringRule(),
            EducationScoringRule(),
            CertificationsScoringRule(),
            AchievementsScoringRule(),
            ContactInfoScoringRule()
        ]

    def calculate_score(self, data: ATSScoringRequest) -> ATSScoringResponse:
        """
        Executes all scoring rules and aggregates the scores and feedback.
        """
        total_score = 0
        breakdown_data = {}
        all_strengths = []
        all_weaknesses = []
        all_recommendations = []
        
        for rule in self.rules:
            score, _, strengths, weaknesses, recommendations = rule.evaluate(data)
            
            # Map class names to breakdown dictionary keys
            rule_name = rule.__class__.__name__
            if "Skills" in rule_name:
                breakdown_data["skills"] = score
            elif "Projects" in rule_name:
                breakdown_data["projects"] = score
            elif "Education" in rule_name:
                breakdown_data["education"] = score
            elif "Certifications" in rule_name:
                breakdown_data["certifications"] = score
            elif "Achievements" in rule_name:
                breakdown_data["achievements"] = score
            elif "Contact" in rule_name:
                breakdown_data["contact"] = score
                
            total_score += score
            all_strengths.extend(strengths)
            all_weaknesses.extend(weaknesses)
            all_recommendations.extend(recommendations)
            
        # Ensure overall score cap at 100
        overall_score = min(total_score, 100)
        
        return ATSScoringResponse(
            ats_score=overall_score,
            score_breakdown=ScoreBreakdown(**breakdown_data),
            strengths=all_strengths,
            weaknesses=all_weaknesses,
            recommendations=all_recommendations
        )
