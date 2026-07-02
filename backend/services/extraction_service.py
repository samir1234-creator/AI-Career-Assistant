import re
import logging
from typing import List, Optional, Dict, Any
from domain.schemas.extraction import ResumeExtractionData

logger = logging.getLogger(__name__)

class ExtractionService:
    @staticmethod
    def extract_information(text_content: str) -> ResumeExtractionData:
        """
        Extracts structured information from raw resume text using heuristics and regular expressions.
        """
        logger.info("Starting information extraction from resume text")
        
        if not text_content or not text_content.strip():
            logger.warning("Empty resume text provided for extraction")
            return ResumeExtractionData()

        # Step 1: Pre-process text (clean markdown links of format [text](url) to just text)
        cleaned_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', text_content)
        
        # Step 2: Extract Contact Details and Links
        email = ExtractionService._extract_email(cleaned_text)
        phone = ExtractionService._extract_phone(cleaned_text)
        linkedin = ExtractionService._extract_linkedin(cleaned_text)
        links = ExtractionService._extract_all_links(cleaned_text)
        
        # Step 3: Split text into lines for Name and Section parsing
        lines = [line.strip() for line in cleaned_text.split('\n')]
        
        # Step 4: Extract Name
        name = ExtractionService._extract_name(lines)
        
        # Step 5: Segment text into sections
        sections_content = ExtractionService._segment_sections(lines)
        
        # Step 6: Process section contents
        skills = ExtractionService._parse_skills(sections_content.get("skills", []))
        education = ExtractionService._parse_list_section(sections_content.get("education", []))
        projects = ExtractionService._parse_list_section(sections_content.get("projects", []))
        certifications = ExtractionService._parse_list_section(sections_content.get("certifications", []))
        
        logger.info(f"Extraction complete. Found name: {name}, email: {email}, skills count: {len(skills)}")
        
        return ResumeExtractionData(
            name=name,
            email=email,
            phone=phone,
            linkedin=linkedin,
            links=links,
            skills=skills,
            education=education,
            projects=projects,
            certifications=certifications
        )

    @staticmethod
    def _extract_email(text: str) -> Optional[str]:
        """Extracts and validates the first email address found in the text."""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, text)
        if match:
            email = match.group(0).strip()
            # Basic normalization (remove mailto: if somehow still present)
            if email.lower().startswith("mailto:"):
                email = email[7:]
            return email
        return None

    @staticmethod
    def _extract_phone(text: str) -> Optional[str]:
        """Extracts the first phone number pattern found in the text."""
        # Pattern to match standard formats like +91 9123456789, +1 (555) 555-5555, 9123456789, etc.
        phone_pattern = r'(?:\+?\d{1,4}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\+?\d{1,4}[-.\s]?\d{10}'
        match = re.search(phone_pattern, text)
        if match:
            return match.group(0).strip()
        return None

    @staticmethod
    def _extract_linkedin(text: str) -> Optional[str]:
        """Extracts the first LinkedIn URL/profile string found in the text."""
        linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+/?'
        match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
        return None

    @staticmethod
    def _extract_all_links(text: str) -> List[str]:
        """Extracts all URLs found in the text."""
        url_pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
        matches = re.findall(url_pattern, text)
        
        # Also look for domain-style links without http:// like github.com/user
        domain_pattern = r'(?:github\.com|linkedin\.com|instagram\.com|x\.com|twitter\.com|discord\.com|discord\.gg)/[a-zA-Z0-9_-]+/?'
        domain_matches = re.findall(domain_pattern, text, re.IGNORECASE)
        
        all_links = list(set(matches + domain_matches))
        return [link for link in all_links if link]

    @staticmethod
    def _extract_name(lines: List[str]) -> Optional[str]:
        """Heuristic-based name extraction from the first few lines of the resume."""
        # Keywords that indicate contact info or section headers, which are not names.
        exclude_keywords = {
            "email", "phone", "tel", "mobile", "contact", "linkedin", "github", 
            "address", "resume", "cv", "curriculum", "summary", "objective", 
            "skills", "education", "experience", "projects", "certifications",
            "google", "www.", "http", "@", "mailto"
        }
        
        candidate_lines = []
        for line in lines[:12]:  # Check first 12 lines
            line_str = line.strip()
            if not line_str:
                continue
            
            # Skip if it is a list item or separator
            if line_str.startswith(("-", "*", "•", "+", "|", "_", "=")) or re.match(r'^\d+\.', line_str):
                continue
                
            line_lower = line_str.lower()
            
            # Check if any exclude keyword is in the line
            has_exclude_keyword = False
            for kw in exclude_keywords:
                if kw in line_lower:
                    has_exclude_keyword = True
                    break
                    
            if has_exclude_keyword:
                continue
                
            # Verify it contains letters and is not too long or too short
            cleaned_letters = re.sub(r'[^a-zA-Z\s]', '', line_str).strip()
            if 3 <= len(cleaned_letters) <= 50:
                # Keep the original formatting (e.g. Rahul Sharma)
                return line_str
                
        return None

    @staticmethod
    def _segment_sections(lines: List[str]) -> Dict[str, List[str]]:
        """Segments the resume lines into lists of lines grouped under known headers."""
        section_aliases = {
            "skills": [
                "skills", "technical skills", "key skills", "core skills", "expertise", 
                "technologies", "tools", "languages", "tools & technologies", 
                "languages & technologies", "technical expertise", "skills & tools"
            ],
            "education": [
                "education", "academic background", "academic profile", "academic qualifications", 
                "qualifications", "academic history", "education background", "academic record"
            ],
            "projects": [
                "projects", "key projects", "academic projects", "personal projects", 
                "selected projects", "relevant projects"
            ],
            "certifications": [
                "certifications", "licenses & certifications", "courses", "certifications & courses", 
                "credentials", "professional certifications"
            ]
        }
        
        sections_content = {
            "skills": [],
            "education": [],
            "projects": [],
            "certifications": []
        }
        
        current_section = None
        
        for line in lines:
            line_strip = line.strip()
            if not line_strip:
                continue
                
            # Normalize line for header matching: lowercase, strip trailing colon/punctuation
            normalized = line_strip.rstrip(':-=').strip().lower()
            
            # Check if line matches a section header alias
            section_matched = False
            for sec_key, aliases in section_aliases.items():
                if normalized in aliases:
                    current_section = sec_key
                    section_matched = True
                    break
            
            if section_matched:
                continue
                
            if current_section is not None:
                sections_content[current_section].append(line_strip)
                
        return sections_content

    @staticmethod
    def _parse_skills(lines: List[str]) -> List[str]:
        """Parses and cleans individual skills from raw skills section lines."""
        skills_set = []
        
        # Protection rules for known multi-word skills to prevent split by delimiters
        protection_rules = [
            (r'\bData\s+Structures\s+and\s+Algorithms\b', "__DATA_STRUCTURES_AND_ALGORITHMS__", "Data Structures and Algorithms"),
            (r'\bNatural\s+Language\s+Processing\b', "__NATURAL_LANGUAGE_PROCESSING__", "Natural Language Processing"),
            (r'\bMachine\s+Learning\b', "__MACHINE_LEARNING__", "Machine Learning"),
            (r'\bDeep\s+Learning\b', "__DEEP_LEARNING__", "Deep Learning"),
            (r'\bComputer\s+Vision\b', "__COMPUTER_VISION__", "Computer Vision"),
            (r'\bSpring\s+Boot\b', "__SPRING_BOOT__", "Spring Boot"),
            (r'\bREST\s+APIs\b', "__REST_APIS__", "REST APIs"),
            (r'\bREST\s+API\b', "__REST_API__", "REST API"),
        ]
        
        for line in lines:
            # Skip if empty or just formatting symbols
            if not line or line.strip() in ["-", "*", "•", "+"]:
                continue
                
            # Strip sub-headings like "Programming Languages:", "Web Technologies:"
            if ":" in line:
                parts = line.split(":", 1)
                # If the prefix looks like a category, we take the right hand side
                if len(parts[0].split()) <= 4:
                    line = parts[1]
            
            # Temporary replacement for multi-word skills
            line_placeholder = line
            for pattern, placeholder, _ in protection_rules:
                line_placeholder = re.sub(pattern, placeholder, line_placeholder, flags=re.IGNORECASE)
            
            # Split by common delimiters
            delimiters = r'[,;|•]|\band\b'
            raw_skills = re.split(delimiters, line_placeholder, flags=re.IGNORECASE)
            
            for s in raw_skills:
                cleaned = s.strip()
                for _, placeholder, canonical in protection_rules:
                    if placeholder in cleaned:
                        cleaned = cleaned.replace(placeholder, canonical)
                    
                # Remove leading list bullets if present after split
                cleaned = re.sub(r'^[-*•+]\s*', '', cleaned).strip()
                
                # We skip skills that are empty, too long (not a skill, probably a sentence), or contain numbers/symbols only
                if cleaned and len(cleaned) <= 40 and not re.match(r'^\d+$', cleaned):
                    # Do not deduplicate here, keep duplicates for merging pass
                    skills_set.append(cleaned)
                        
        # Merging pass for known multi-word skills
        known_merges = [
            ("Spring", "Boot", "Spring Boot"),
            ("Machine", "Learning", "Machine Learning"),
            ("Deep", "Learning", "Deep Learning"),
            ("Computer", "Vision", "Computer Vision"),
            ("Natural", "Language", "Processing", "Natural Language Processing"),
            ("Data", "Structures", "and", "Algorithms", "Data Structures and Algorithms"),
            ("Data", "Structures", "Algorithms", "Data Structures and Algorithms"),
            ("Data Structures", "Algorithms", "Data Structures and Algorithms"),
            ("REST", "APIs", "REST APIs"),
            ("REST", "API", "REST API")
        ]
        
        i = 0
        merged_skills = []
        while i < len(skills_set):
            merged = False
            for merge_rule in known_merges:
                n = len(merge_rule) - 1 # number of parts to match
                parts = merge_rule[:n]
                target = merge_rule[n]
                
                if i + n <= len(skills_set):
                    match = True
                    for k in range(n):
                        if skills_set[i + k].strip().lower() != parts[k].lower():
                            match = False
                            break
                    if match:
                        merged_skills.append(target)
                        i += n
                        merged = True
                        break
            if not merged:
                merged_skills.append(skills_set[i])
                i += 1
                
        # Finally, deduplicate the merged list while preserving order
        final_skills = []
        for skill in merged_skills:
            if skill not in final_skills:
                final_skills.append(skill)
                
        return final_skills


    @staticmethod
    def _parse_list_section(lines: List[str]) -> List[str]:
        """Cleans and extracts list-like records under education, projects, or certifications."""
        parsed_items = []
        for line in lines:
            cleaned = line.strip()
            if not cleaned:
                continue
                
            # Strip bullet chars from the start
            cleaned = re.sub(r'^[-*•+]\s*', '', cleaned)
            # Remove markdown bolding formatting
            cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)
            cleaned = cleaned.strip()
            
            if cleaned and cleaned not in parsed_items:
                parsed_items.append(cleaned)
                
        return parsed_items
