import { useState, useEffect , useMemo} from "react";
import { ResumeUpload } from '../components/ResumeUpload/ResumeUpload';
import { formatFileSize } from '../utils/formatters';
import { extractResumeInfo, classifySkills, getATSScore, getRecommendations, getSkillGapAnalysis, generateRoadmap } from '../services/api';
import { RoadmapDashboard } from './RoadmapDashboard';
import { useLocation, useNavigate } from 'react-router-dom';

const CATEGORY_DISPLAY_NAMES = {
  'Programming Language': 'Programming Languages',
  'Frontend Framework': 'Frontend Frameworks',
  'Backend Framework': 'Backend Frameworks',
  'Database': 'Databases',
  'Cloud Computing': 'Cloud Computing',
  'DevOps': 'DevOps',
  'Artificial Intelligence': 'Artificial Intelligence',
  'Data Science': 'Data Science',
  'Mobile Development': 'Mobile Development',
  'Tools & Technologies': 'Tools & Technologies',
  'Other': 'Other / Uncategorized'
};

// Clean candidate name
const cleanCandidateName = (name) => {
  if (!name) return 'Anonymous Candidate';
  return name.trim();
};

const splitConcatenatedSkills = (skillStr) => {
  if (!skillStr) return [];
  
  const knownKeywords = [
    "JavaScript", "TypeScript", "Python", "React", "Node.js", "NodeJS", "FastAPI", "MongoDB", "MySQL", 
    "Machine Learning", "Deep Learning", "Docker", "Git", "Java", "HTML", "CSS", "SQL", "PostgreSQL", 
    "AWS", "GCP", "Azure", "Kubernetes", "Linux", "Django", "Flask", "Express", "GraphQL", "REST API",
    "C\\+\\+", "C#", "PHP", "Angular", "Vue", "Svelte", "Redux", "Webpack", "Vite", "NoSQL", "Redis",
    "Spring Boot", "Computer Vision", "Natural Language Processing", "Data Structures and Algorithms", "REST APIs"
  ];
  
  let tempStr = skillStr;
  const foundSkills = [];
  const sortedKeywords = [...knownKeywords].sort((a, b) => b.length - a.length);
  
  let matchFound = true;
  while (matchFound) {
    matchFound = false;
    for (const kw of sortedKeywords) {
      const escapedKw = kw.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&');
      const regex = new RegExp(escapedKw, 'i');
      const match = tempStr.match(regex);
      if (match) {
        foundSkills.push(kw);
        tempStr = tempStr.replace(regex, ' ');
        matchFound = true;
        break;
      }
    }
  }
  
  tempStr.split(/\s+/).forEach(part => {
    const trimmed = part.trim();
    if (trimmed && trimmed.length > 1) {
      foundSkills.push(trimmed);
    }
  });
  
  return foundSkills;
};

// Heuristically parse skills from the array (which might contain comma-separated values or concatenated words)
const getParsedSkills = (skillsList) => {
  if (!skillsList) return [];
  const list = Array.isArray(skillsList) ? skillsList : [skillsList];
  
  const initialSplit = list.flatMap(s => s.split(/[,;|•]|\band\b/i).map(item => item.trim())).filter(Boolean);
  const finalSkills = [];
  
  initialSplit.forEach(skill => {
    const subSkills = splitConcatenatedSkills(skill);
    if (subSkills.length > 0) {
      subSkills.forEach(ss => {
        if (!finalSkills.includes(ss)) {
          finalSkills.push(ss);
        }
      });
    } else {
      if (!finalSkills.includes(skill)) {
        finalSkills.push(skill);
      }
    }
  });
  
  return finalSkills;
};

// Heuristically extract achievements and additional information sections from raw text
const parseAdditionalSections = (textContent) => {
  const sections = {
    achievements: [],
    additionalInfo: []
  };
  
  if (!textContent) return sections;
  
  const lines = textContent.split('\n').map(line => line.trim());
  let currentSection = null;
  
  const achievementHeaders = [
    "achievements", "key achievements", "honors", "awards", "honors & awards", "accomplishments"
  ];
  const additionalHeaders = [
    "additional information", "additional info", "personal details", "hobbies", "interests", "languages", "extra details", "personal information"
  ];
  const otherHeaders = [
    "skills", "technical skills", "key skills", "core skills", "expertise", "technologies", "tools", "languages",
    "education", "academic background", "academic profile", "academic qualifications", "qualifications",
    "projects", "key projects", "academic projects", "personal projects", "selected projects", "relevant projects",
    "certifications", "licenses & certifications", "courses", "credentials", "professional certifications"
  ];
  
  for (let line of lines) {
    if (!line) continue;
    
    // Normalize line for header matching
    const normalized = line.replace(/[:-=]$/, '').trim().toLowerCase();
    
    if (achievementHeaders.includes(normalized)) {
      currentSection = "achievements";
      continue;
    } else if (additionalHeaders.includes(normalized)) {
      currentSection = "additionalInfo";
      continue;
    } else if (otherHeaders.includes(normalized)) {
      currentSection = null;
      continue;
    }
    
    if (currentSection) {
      // Clean bullet points
      const cleanLine = line.replace(/^[-*•+]\s*/, '').trim();
      if (cleanLine) {
        sections[currentSection].push(cleanLine);
      }
    }
  }
  
  return sections;
};

// Clean any lines in sections like certifications that are part of achievements/additional info
const cleanSectionData = (sectionList, itemsToRemove) => {
  if (!sectionList) return [];
  const headerPatterns = [
    /achievements/i,
    /additional\s+information/i,
    /additional\s+info/i,
    /personal\s+details/i,
    /hobbies/i,
    /interests/i,
    /languages/i,
    /extra\s+details/i
  ];
  
  const normalizedToRemove = itemsToRemove.map(item => item.toLowerCase());
  
  return sectionList.filter(item => {
    const trimmed = item.trim();
    // Remove if it matches a header pattern
    if (headerPatterns.some(pat => pat.test(trimmed))) {
      return false;
    }
    // Remove if it matches any of the items we extracted separately
    const cleanItem = trimmed.replace(/^[-*•+]\s*/, '').trim().toLowerCase();
    if (normalizedToRemove.includes(cleanItem)) {
      return false;
    }
    return true;
  });
};

// Convert additional information list into structured key-value pairs
const parseAdditionalInfoToFields = (lines) => {
  const fields = [];
  
  lines.forEach(line => {
    const cleanLine = line.replace(/^[-*•+]\s*/, '').trim();
    if (!cleanLine) return;
    
    // Check if line contains a colon separating key and value
    const colonIndex = cleanLine.indexOf(':');
    if (colonIndex > 0) {
      const key = cleanLine.substring(0, colonIndex).trim();
      const val = cleanLine.substring(colonIndex + 1).trim();
      if (key && val) {
        fields.push({ label: key, value: val });
        return;
      }
    }
    
    // Fallback: Check if line contains a dash separating key and value
    const dashIndex = cleanLine.indexOf(' - ');
    if (dashIndex > 0) {
      const key = cleanLine.substring(0, dashIndex).trim();
      const val = cleanLine.substring(dashIndex + 3).trim();
      if (key && val) {
        fields.push({ label: key, value: val });
        return;
      }
    }
    
    // Otherwise, treat the whole line as a general detail
    fields.push({ label: "Detail", value: cleanLine });
  });
  
  return fields;
};

const isSkillMatched = (skillName, candidateSkills) => {
  if (!skillName || !candidateSkills) return false;
  const s = skillName.trim().toLowerCase();
  return candidateSkills.some(cand => {
    const c = cand.trim().toLowerCase();
    return c === s || c.includes(s) || s.includes(c);
  });
};

const isDevModeEnabled = () => {
  try {
    if (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_DEV_MODE === 'true') {
      return true;
    }
  } catch { /* ignore */ }
  try {
    if (typeof window !== 'undefined') {
      if (window.localStorage && window.localStorage.getItem('dev_mode') === 'true') {
        return true;
      }
      if (window.__DEV_MODE__ === true) {
        return true;
      }
    }
  } catch { /* ignore */ }
  return false;
};

const AnalyzerPage = ({ initialTab }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const restoredAnalysis = location.state?.restoredAnalysis;

  const [parsedData, setParsedData] = useState(null);
  const [extractedData, setExtractedData] = useState(null);
  const [enrichedSkills, setEnrichedSkills] = useState([]);
  const [atsData, setAtsData] = useState(null);
  const [recommendationsData, setRecommendationsData] = useState(null);
  const [isExtracting, setIsExtracting] = useState(false);
  const [extractionError, setExtractionError] = useState(null);
  const [activeTab, setActiveTab] = useState(initialTab || 'profile');

  // Restore analysis details from history if passed
  useEffect(() => {
    if (restoredAnalysis) {
      if (restoredAnalysis.resume) {
        const filename = restoredAnalysis.resume.resume_file_url === 'local_text_only' 
          ? 'Uploaded Resume' 
          : (restoredAnalysis.resume.resume_file_url?.split('/').pop() || 'Resume');
          
        setParsedData({
          filename: filename,
          text_content: restoredAnalysis.resume.resume_text,
          file_size_bytes: 0
        });
        
        if (restoredAnalysis.resume.parsed_data) {
          setExtractedData(restoredAnalysis.resume.parsed_data);
          
          const cleanedSkills = getParsedSkills(restoredAnalysis.resume.parsed_data.skills);
          if (cleanedSkills.length > 0) {
            classifySkills(cleanedSkills).then(classificationResult => {
              setEnrichedSkills(classificationResult.skills || []);
            }).catch(err => {
              console.error("Failed to classify restored skills:", err);
            });
          }
        }
      }
      if (restoredAnalysis.ats) {
        setAtsData(restoredAnalysis.ats.report_data);
      }
      if (restoredAnalysis.recommendations) {
        setRecommendationsData(restoredAnalysis.recommendations.recommendations);
      }
      setActiveTab(initialTab || 'profile');
    } else {
      setParsedData(null);
      setExtractedData(null);
      setEnrichedSkills([]);
      setAtsData(null);
      setRecommendationsData(null);
    }
  }, [restoredAnalysis, initialTab]);

  useEffect(() => {
    if (initialTab) {
      setActiveTab(initialTab);
    }
  }, [initialTab]);

  const [expandedGaps, setExpandedGaps] = useState({});
  const [skillGaps, setSkillGaps] = useState({});
  const [loadingGaps, setLoadingGaps] = useState({});
  const [showJson, setShowJson] = useState({});
  const [gapErrors, setGapErrors] = useState({});
  const [activeRoadmap, setActiveRoadmap] = useState(null);
  const [loadingRoadmap, setLoadingRoadmap] = useState({});
  const [roadmapError, setRoadmapError] = useState({});

  const handleToggleGap = async (roleName, career) => {
    const isExpanded = !expandedGaps[roleName];
    setExpandedGaps(prev => ({
      ...prev,
      [roleName]: isExpanded
    }));

    if (isExpanded && !skillGaps[roleName]) {
      setLoadingGaps(prev => ({
        ...prev,
        [roleName]: true
      }));
      setGapErrors(prev => ({
        ...prev,
        [roleName]: null
      }));

      try {
        // Calculate matched/missing required and preferred skills
        const reqSkillsEnriched = (career?.required_skills || []).map(s => ({
          name: s,
          matched: isSkillMatched(s, processedData?.skills || [])
        }));
        const prefSkillsEnriched = (career?.preferred_skills || []).map(s => ({
          name: s,
          matched: isSkillMatched(s, processedData?.skills || [])
        }));

        const matched_skills = [
          ...reqSkillsEnriched.filter(s => s.matched).map(s => s.name),
          ...prefSkillsEnriched.filter(s => s.matched).map(s => s.name)
        ];
        const missing_skills = [
          ...reqSkillsEnriched.filter(s => !s.matched).map(s => s.name),
          ...prefSkillsEnriched.filter(s => !s.matched).map(s => s.name)
        ];

        const gapData = await getSkillGapAnalysis({
          career: roleName,
          matched_skills,
          missing_skills
        });

        setSkillGaps(prev => ({
          ...prev,
          [roleName]: gapData
        }));
      } catch (err) {
        console.error(`Failed to analyze skill gap for ${roleName}:`, err);
        setGapErrors(prev => ({
          ...prev,
          [roleName]: err.message || err.toString()
        }));
      } finally {
        setLoadingGaps(prev => ({
          ...prev,
          [roleName]: false
        }));
      }
    }
  };

  const handleGenerateRoadmap = async (roleName, career) => {
    setLoadingRoadmap(prev => ({ ...prev, [roleName]: true }));
    setRoadmapError(prev => ({ ...prev, [roleName]: null }));

    try {
      const reqSkillsEnriched = (career?.required_skills || []).map(s => ({
        name: s,
        matched: isSkillMatched(s, processedData?.skills || [])
      }));
      const prefSkillsEnriched = (career?.preferred_skills || []).map(s => ({
        name: s,
        matched: isSkillMatched(s, processedData?.skills || [])
      }));

      const matched_skills = [
        ...reqSkillsEnriched.filter(s => s.matched).map(s => s.name),
        ...prefSkillsEnriched.filter(s => s.matched).map(s => s.name)
      ];
      const missing_skills = [
        ...reqSkillsEnriched.filter(s => !s.matched).map(s => s.name),
        ...prefSkillsEnriched.filter(s => !s.matched).map(s => s.name)
      ];

      const res = await generateRoadmap({
        career: roleName,
        matched_skills,
        missing_skills,
        career_readiness: skillGaps[roleName]?.career_readiness || 50,
        projects: processedData?.projects?.map(p => typeof p === 'object' ? p.title : p) || [],
        certifications: processedData?.certifications?.map(c => typeof c === 'object' ? c.name : c) || [],
        education: processedData?.education?.map(e => typeof e === 'object' ? e.degree || e.school : e) || [],
        ats_score: atsData?.ats_score || 70
      });

      navigate('/roadmap', { state: { roadmapData: res } });
    } catch (err) {
      console.error("Roadmap generation failed:", err);
      setRoadmapError(prev => ({ ...prev, [roleName]: err.message || "Failed to generate roadmap" }));
    } finally {
      setLoadingRoadmap(prev => ({ ...prev, [roleName]: false }));
    }
  };

  const handleUploadSuccess = async (data) => {
    setParsedData(data);
    setIsExtracting(true);
    setExtractionError(null);
    setExtractedData(null);
    setEnrichedSkills([]);
    setAtsData(null);
    setRecommendationsData(null);
    
    try {
      const result = await extractResumeInfo(data.text_content);
      setExtractedData(result);
      
      const cleanedSkills = getParsedSkills(result.skills);
      if (cleanedSkills.length > 0) {
        try {
          const classificationResult = await classifySkills(cleanedSkills);
          setEnrichedSkills(classificationResult.skills || []);
        } catch (classifyErr) {
          console.error("Failed to classify skills:", classifyErr);
        }
      }

      // Request ATS Score using extracted info & parsed achievements
      const extraSections = parseAdditionalSections(data.text_content);
      const atsPayload = {
        name: result.name,
        email: result.email,
        phone: result.phone,
        linkedin: result.linkedin,
        skills: cleanedSkills,
        projects: result.projects || [],
        education: result.education || [],
        certifications: result.certifications || [],
        achievements: extraSections.achievements || []
      };

      let calculatedAtsScore = 70;
      try {
        const atsResult = await getATSScore(atsPayload);
        setAtsData(atsResult);
        calculatedAtsScore = atsResult.ats_score;
      } catch (atsErr) {
        console.error("Failed to calculate ATS score:", atsErr);
      }

      // Request career recommendations using the calculated ATS score
      try {
        const recPayload = {
          skills: cleanedSkills,
          projects: result.projects || [],
          education: result.education || [],
          certifications: result.certifications || [],
          ats_score: calculatedAtsScore
        };
        const recResult = await getRecommendations(recPayload);
        setRecommendationsData(recResult.recommended_careers || []);
      } catch (recErr) {
        console.error("Failed to fetch recommendations:", recErr);
      }

    } catch (err) {
      setExtractionError(err.message || 'Failed to extract structured information.');
    } finally {
      setIsExtracting(false);
    }
  };

  const handleReset = () => {
    setParsedData(null);
    setExtractedData(null);
    setEnrichedSkills([]);
    setAtsData(null);
    setRecommendationsData(null);
    setExpandedGaps({});
    setSkillGaps({});
    setLoadingGaps({});
    setShowJson({});
    setGapErrors({});
    setExtractionError(null);
    setActiveTab('profile');
  };

  const groupedSkills = useMemo(() => {
    if (!enrichedSkills || enrichedSkills.length === 0) return {};
    
    const groups = {};
    enrichedSkills.forEach(skill => {
      const cat = skill.category || 'Other';
      if (!groups[cat]) {
        groups[cat] = [];
      }
      groups[cat].push(skill.name);
    });
    return groups;
  }, [enrichedSkills]);


  const processedData = useMemo(() => {
    if (!extractedData) return null;
    
    const extraSections = parseAdditionalSections(parsedData?.text_content);
    const achievements = extraSections.achievements;
    const additionalInfo = parseAdditionalInfoToFields(extraSections.additionalInfo);
    
    const rawExtraLines = [...extraSections.achievements, ...extraSections.additionalInfo];
    
    const cleanedCertifications = cleanSectionData(extractedData.certifications, rawExtraLines);
    const cleanedProjects = cleanSectionData(extractedData.projects, rawExtraLines);
    const cleanedEducation = cleanSectionData(extractedData.education, rawExtraLines);
    const cleanedSkills = getParsedSkills(extractedData.skills);
    
    return {
      name: cleanCandidateName(extractedData.name),
      email: extractedData.email,
      phone: extractedData.phone,
      linkedin: extractedData.linkedin,
      skills: cleanedSkills,
      education: cleanedEducation,
      projects: cleanedProjects,
      certifications: cleanedCertifications,
      achievements: achievements,
      additionalInfo: additionalInfo
    };
  }, [extractedData, parsedData]);

  return (
    <div className="container">
      <div className="text-center mb-8">
        <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '1rem', color: '#fff' }}>
          Resume Analyzer
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>
          Upload your resume (PDF) to extract and organize its content.
        </p>
      </div>

      {!parsedData ? (
        <ResumeUpload onUploadSuccess={handleUploadSuccess} />
      ) : (
        <div style={{ backgroundColor: 'var(--bg-card)', padding: '2rem', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
            <div>
              <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--text-light)' }}>
                Analysis Results
              </h2>
              <span style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                {parsedData.filename} ({formatFileSize(parsedData.file_size_bytes)})
              </span>
            </div>
            <button 
              onClick={handleReset}
              style={{
                backgroundColor: 'transparent',
                color: 'var(--text-muted)',
                border: '1px solid var(--border-color)',
                padding: '0.5rem 1rem',
                borderRadius: '6px',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
              }}
              onMouseEnter={(e) => {
                e.target.style.borderColor = 'var(--text-light)';
                e.target.style.color = 'var(--text-light)';
              }}
              onMouseLeave={(e) => {
                e.target.style.borderColor = 'var(--border-color)';
                e.target.style.color = 'var(--text-muted)';
              }}
            >
              Upload Another
            </button>
          </div>

          {/* Tab Navigation */}
          <div className="tabs-nav">
            <button 
              className={`tab-button ${activeTab === 'profile' ? 'active' : ''}`}
              onClick={() => setActiveTab('profile')}
            >
              ✨ Structured Profile
            </button>
            <button 
              className={`tab-button ${activeTab === 'ats' ? 'active' : ''}`}
              onClick={() => setActiveTab('ats')}
            >
              🎯 ATS Feedback
            </button>
            <button 
              className={`tab-button ${activeTab === 'recommendations' ? 'active' : ''}`}
              onClick={() => setActiveTab('recommendations')}
            >
              💼 Career Recommendations
            </button>
            <button 
              className={`tab-button ${activeTab === 'raw' ? 'active' : ''}`}
              onClick={() => setActiveTab('raw')}
            >
              📄 Raw Extracted Text
            </button>
          </div>
          
          {/* Tab Content */}
          {activeTab === 'profile' && (
            <div>
              {isExtracting && (
                <div className="loader-container">
                  <div className="spinner"></div>
                  <p style={{ color: 'var(--text-muted)', fontWeight: 500 }}>
                    Extracting structured information from resume...
                  </p>
                </div>
              )}

              {extractionError && (
                <div className="error-container">
                  <p><strong>Error:</strong> {extractionError}</p>
                  <p style={{ fontSize: '0.9rem', marginTop: '0.5rem' }}>
                    You can still view the raw text of your resume in the "Raw Extracted Text" tab.
                  </p>
                </div>
              )}

              {!isExtracting && !extractionError && processedData && (
                <div className="profile-grid">
                  {/* Left Column: Contact Summary Card */}
                  <div className="profile-header-card">
                    <div className="profile-avatar">
                      <span className="profile-avatar-icon">👤</span>
                    </div>
                    <h3 className="profile-name">
                      {processedData.name || 'Anonymous Candidate'}
                    </h3>
                    
                    <div className="contact-info-list">
                      {processedData.email && (
                        <a href={`mailto:${processedData.email}`} className="contact-item-link">
                          <span className="contact-icon">✉️</span>
                          <span>{processedData.email}</span>
                        </a>
                      )}
                      
                      {processedData.phone && (
                        <a href={`tel:${processedData.phone}`} className="contact-item-link">
                          <span className="contact-icon">📞</span>
                          <span>{processedData.phone}</span>
                        </a>
                      )}
                      
                      {processedData.linkedin && (
                        <a 
                          href={processedData.linkedin.startsWith('http') ? processedData.linkedin : `https://${processedData.linkedin}`} 
                          target="_blank" 
                          rel="noopener noreferrer" 
                          className="contact-item-link"
                        >
                          <span className="contact-icon">🔗</span>
                          <span>LinkedIn Profile</span>
                        </a>
                      )}

                      {!processedData.email && !processedData.phone && !processedData.linkedin && (
                        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', fontStyle: 'italic' }}>
                          No contact information identified.
                        </p>
                      )}
                    </div>

                    {atsData && (
                      <div style={{ marginTop: '1.5rem', paddingTop: '1.5rem', borderTop: '1px solid var(--border-color)', textAlign: 'left' }}>
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold', marginBottom: '0.5rem', letterSpacing: '0.05em' }}>
                          ATS Score
                        </div>
                        <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.25rem' }}>
                          <span style={{ 
                            fontSize: '2rem', 
                            fontWeight: 'bold', 
                            color: atsData.ats_score >= 70 ? 'var(--success)' : atsData.ats_score >= 50 ? '#f59e0b' : 'var(--error)' 
                          }}>
                            {atsData.ats_score}
                          </span>
                          <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>/ 100</span>
                        </div>
                        <div style={{ width: '100%', height: '6px', backgroundColor: 'rgba(255,255,255,0.08)', borderRadius: '3px', marginTop: '0.6rem', overflow: 'hidden' }}>
                          <div style={{ 
                            width: `${atsData.ats_score}%`, 
                            height: '100%', 
                            backgroundColor: atsData.ats_score >= 70 ? 'var(--success)' : atsData.ats_score >= 50 ? '#f59e0b' : 'var(--error)',
                            borderRadius: '3px',
                            transition: 'width 0.8s cubic-bezier(0.4, 0, 0.2, 1)'
                          }} />
                        </div>
                        <button 
                          onClick={() => setActiveTab('ats')}
                          style={{
                            marginTop: '1rem',
                            backgroundColor: 'rgba(79, 70, 229, 0.1)',
                            border: '1px solid rgba(79, 70, 229, 0.2)',
                            color: '#a5b4fc',
                            padding: '0.4rem 0.8rem',
                            borderRadius: '6px',
                            cursor: 'pointer',
                            fontSize: '0.85rem',
                            width: '100%',
                            fontWeight: '600',
                            transition: 'all 0.2s ease'
                          }}
                          onMouseEnter={(e) => {
                            e.target.style.backgroundColor = 'var(--primary)';
                            e.target.style.color = 'var(--text-light)';
                            e.target.style.borderColor = 'var(--primary)';
                          }}
                          onMouseLeave={(e) => {
                            e.target.style.backgroundColor = 'rgba(79, 70, 229, 0.1)';
                            e.target.style.color = '#a5b4fc';
                            e.target.style.borderColor = 'rgba(79, 70, 229, 0.2)';
                          }}
                        >
                          View Breakdown &amp; Feedback &rarr;
                        </button>
                        {recommendationsData && (
                          <button 
                            onClick={() => setActiveTab('recommendations')}
                            style={{
                              marginTop: '0.5rem',
                              backgroundColor: 'rgba(16, 185, 129, 0.1)',
                              border: '1px solid rgba(16, 185, 129, 0.2)',
                              color: '#a7f3d0',
                              padding: '0.4rem 0.8rem',
                              borderRadius: '6px',
                              cursor: 'pointer',
                              fontSize: '0.85rem',
                              width: '100%',
                              fontWeight: '600',
                              transition: 'all 0.2s ease'
                            }}
                            onMouseEnter={(e) => {
                              e.target.style.backgroundColor = 'var(--success)';
                              e.target.style.color = 'var(--text-light)';
                              e.target.style.borderColor = 'var(--success)';
                            }}
                            onMouseLeave={(e) => {
                              e.target.style.backgroundColor = 'rgba(16, 185, 129, 0.1)';
                              e.target.style.color = '#a7f3d0';
                              e.target.style.borderColor = 'rgba(16, 185, 129, 0.2)';
                            }}
                          >
                            View Career Path Insights &rarr;
                          </button>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Right Column: Structured Sections */}
                  <div>
                    {/* Skills Section */}
                    <div className="section-card">
                      <h4 className="section-title">
                        <span>🛠️</span> Technical Skills
                      </h4>
                      {Object.keys(groupedSkills).length > 0 ? (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                          {Object.entries(groupedSkills).map(([category, skillsList]) => {
                            const displayName = CATEGORY_DISPLAY_NAMES[category] || category;
                            return (
                              <div key={category} className="skill-category-group">
                                <h5 className="skill-category-title" style={{ 
                                  fontSize: '1rem', 
                                  fontWeight: '600', 
                                  color: 'var(--text-light)', 
                                  marginBottom: '0.6rem',
                                  fontFamily: "'Outfit', sans-serif"
                                }}>
                                  {displayName}
                                </h5>
                                <div className="skills-container">
                                  {skillsList.map((skill, index) => (
                                    <span key={index} className="skill-tag">
                                      {skill}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      ) : (
                        processedData.skills && processedData.skills.length > 0 ? (
                          <div className="skills-container">
                            {processedData.skills.map((skill, index) => (
                              <span key={index} className="skill-tag">
                                {skill}
                              </span>
                            ))}
                          </div>
                        ) : (
                          <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', fontSize: '0.95rem' }}>
                            No technical skills identified in the resume text.
                          </p>
                        )
                      )}
                    </div>

                    {/* Achievements Section */}
                    {processedData.achievements && processedData.achievements.length > 0 && (
                      <div className="section-card">
                        <h4 className="section-title">
                          <span>🏆</span> Achievements
                        </h4>
                        <div className="achievements-list">
                          {processedData.achievements.map((achievement, index) => (
                            <div key={index} className="achievement-item">
                              <span className="achievement-icon">🏆</span>
                              <div className="achievement-text">{achievement}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Projects Section */}
                    <div className="section-card">
                      <h4 className="section-title">
                        <span>🚀</span> Projects & Experience
                      </h4>
                      {processedData.projects && processedData.projects.length > 0 ? (
                        <div className="timeline-list">
                          {processedData.projects.map((project, index) => (
                            <div key={index} className="timeline-item">
                              <div className="timeline-content">
                                {project}
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', fontSize: '0.95rem' }}>
                          No project entries identified.
                        </p>
                      )}
                    </div>

                    {/* Education Section */}
                    <div className="section-card">
                      <h4 className="section-title">
                        <span>🎓</span> Education
                      </h4>
                      {processedData.education && processedData.education.length > 0 ? (
                        <div className="timeline-list">
                          {processedData.education.map((edu, index) => (
                            <div key={index} className="timeline-item">
                              <div className="timeline-content">
                                {edu}
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', fontSize: '0.95rem' }}>
                          No education details identified.
                        </p>
                      )}
                    </div>

                    {/* Certifications Section */}
                    {processedData.certifications && processedData.certifications.length > 0 && (
                      <div className="section-card">
                        <h4 className="section-title">
                          <span>📜</span> Certifications
                        </h4>
                        <div className="timeline-list">
                          {processedData.certifications.map((cert, index) => (
                            <div key={index} className="timeline-item">
                              <div className="timeline-content">
                                {cert}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Additional Information Section */}
                    {processedData.additionalInfo && processedData.additionalInfo.length > 0 && (
                      <div className="section-card">
                        <h4 className="section-title">
                          <span>ℹ️</span> Additional Information
                        </h4>
                        <div className="additional-info-list">
                          {processedData.additionalInfo.map((info, index) => (
                            <div key={index} className="info-item-card">
                              <span className="info-item-label">{info.label}</span>
                              <span className="info-item-value">{info.value}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'ats' && (
            <div>
              {isExtracting && (
                <div className="loader-container">
                  <div className="spinner"></div>
                  <p style={{ color: 'var(--text-muted)', fontWeight: 500 }}>
                    Evaluating ATS Score...
                  </p>
                </div>
              )}

              {!isExtracting && !atsData && (
                <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', padding: '2rem', textAlign: 'center' }}>
                  No ATS details available. Please upload a resume first.
                </p>
              )}

              {!isExtracting && atsData && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                  {/* Top Section: Score Circular Widget and Breakdown */}
                  <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: '1fr', 
                    gap: '2rem',
                    backgroundColor: 'rgba(255, 255, 255, 0.02)',
                    padding: '2rem',
                    borderRadius: '12px',
                    border: '1px solid var(--border-color)'
                  }}>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '2rem', alignItems: 'center', justifyContent: 'space-around' }}>
                      
                      {/* Radial Progress Counter */}
                      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
                        <div style={{ 
                          width: '150px', 
                          height: '150px', 
                          borderRadius: '50%', 
                          background: `conic-gradient(${
                            atsData.ats_score >= 70 ? 'var(--success)' : atsData.ats_score >= 50 ? '#f59e0b' : 'var(--error)'
                          } ${atsData.ats_score * 3.6}deg, rgba(255,255,255,0.06) 0deg)`,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          boxShadow: '0 8px 24px rgba(0,0,0,0.2)'
                        }}>
                          <div style={{ 
                            width: '130px', 
                            height: '130px', 
                            borderRadius: '50%', 
                            backgroundColor: 'var(--bg-card)', 
                            display: 'flex', 
                            flexDirection: 'column', 
                            alignItems: 'center', 
                            justifyContent: 'center' 
                          }}>
                            <span style={{ fontSize: '2.5rem', fontWeight: '800', color: 'var(--text-light)', fontFamily: "'Outfit', sans-serif" }}>
                              {atsData.ats_score}
                            </span>
                            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>
                              Score / 100
                            </span>
                          </div>
                        </div>
                        <h4 style={{ 
                          marginTop: '0.5rem', 
                          fontSize: '1.1rem', 
                          fontWeight: '600', 
                          color: atsData.ats_score >= 70 ? 'var(--success)' : atsData.ats_score >= 50 ? '#f59e0b' : 'var(--error)' 
                        }}>
                          {atsData.ats_score >= 70 ? 'Good Match' : atsData.ats_score >= 50 ? 'Needs Improvement' : 'Low Match'}
                        </h4>
                      </div>

                      {/* Score Breakdown Section */}
                      <div style={{ flex: 1, minWidth: '280px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        <h4 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: 'var(--text-light)', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem', marginBottom: '0.5rem' }}>
                          Score Breakdown
                        </h4>
                        
                        {/* Skills */}
                        <div>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: '0.25rem' }}>
                            <span style={{ fontWeight: '500' }}>Skills</span>
                            <span style={{ color: 'var(--text-muted)' }}>{atsData.score_breakdown.skills} / 30</span>
                          </div>
                          <div style={{ width: '100%', height: '6px', backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                            <div style={{ width: `${(atsData.score_breakdown.skills / 30) * 100}%`, height: '100%', backgroundColor: 'var(--primary)', borderRadius: '3px' }} />
                          </div>
                        </div>

                        {/* Projects */}
                        <div>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: '0.25rem' }}>
                            <span style={{ fontWeight: '500' }}>Projects</span>
                            <span style={{ color: 'var(--text-muted)' }}>{atsData.score_breakdown.projects} / 25</span>
                          </div>
                          <div style={{ width: '100%', height: '6px', backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                            <div style={{ width: `${(atsData.score_breakdown.projects / 25) * 100}%`, height: '100%', backgroundColor: 'var(--success)', borderRadius: '3px' }} />
                          </div>
                        </div>

                        {/* Education */}
                        <div>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: '0.25rem' }}>
                            <span style={{ fontWeight: '500' }}>Education</span>
                            <span style={{ color: 'var(--text-muted)' }}>{atsData.score_breakdown.education} / 15</span>
                          </div>
                          <div style={{ width: '100%', height: '6px', backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                            <div style={{ width: `${(atsData.score_breakdown.education / 15) * 100}%`, height: '100%', backgroundColor: '#60a5fa', borderRadius: '3px' }} />
                          </div>
                        </div>

                        {/* Certifications */}
                        <div>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: '0.25rem' }}>
                            <span style={{ fontWeight: '500' }}>Certifications</span>
                            <span style={{ color: 'var(--text-muted)' }}>{atsData.score_breakdown.certifications} / 10</span>
                          </div>
                          <div style={{ width: '100%', height: '6px', backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                            <div style={{ width: `${(atsData.score_breakdown.certifications / 10) * 100}%`, height: '100%', backgroundColor: '#c084fc', borderRadius: '3px' }} />
                          </div>
                        </div>

                        {/* Achievements */}
                        <div>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: '0.25rem' }}>
                            <span style={{ fontWeight: '500' }}>Achievements</span>
                            <span style={{ color: 'var(--text-muted)' }}>{atsData.score_breakdown.achievements} / 10</span>
                          </div>
                          <div style={{ width: '100%', height: '6px', backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                            <div style={{ width: `${(atsData.score_breakdown.achievements / 10) * 100}%`, height: '100%', backgroundColor: '#fb7185', borderRadius: '3px' }} />
                          </div>
                        </div>

                        {/* Contact details */}
                        <div>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: '0.25rem' }}>
                            <span style={{ fontWeight: '500' }}>Contact Details</span>
                            <span style={{ color: 'var(--text-muted)' }}>{atsData.score_breakdown.contact} / 10</span>
                          </div>
                          <div style={{ width: '100%', height: '6px', backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                            <div style={{ width: `${(atsData.score_breakdown.contact / 10) * 100}%`, height: '100%', backgroundColor: '#2dd4bf', borderRadius: '3px' }} />
                          </div>
                        </div>

                      </div>
                    </div>
                  </div>

                  {/* Recommendations and Feedback Section */}
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '1.5rem' }}>
                    <div className="profile-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
                      
                      {/* Strengths card */}
                      <div className="section-card" style={{ height: 'fit-content' }}>
                        <h4 className="section-title" style={{ color: 'var(--success)', borderBottomColor: 'rgba(16, 185, 129, 0.2)' }}>
                          <span>✓</span> Strengths
                        </h4>
                        <ul style={{ listStyleType: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
                          {atsData.strengths && atsData.strengths.map((str, idx) => (
                            <li key={idx} style={{ display: 'flex', gap: '0.6rem', alignItems: 'flex-start', color: '#e2e8f0', fontSize: '0.95rem' }}>
                              <span style={{ color: 'var(--success)', fontWeight: 'bold' }}>✓</span>
                              <span>{str}</span>
                            </li>
                          ))}
                          {(!atsData.strengths || atsData.strengths.length === 0) && (
                            <li style={{ color: 'var(--text-muted)', fontStyle: 'italic', fontSize: '0.9rem' }}>
                              No significant strengths detected.
                            </li>
                          )}
                        </ul>
                      </div>

                      {/* Areas to Improve card */}
                      <div className="section-card" style={{ height: 'fit-content' }}>
                        <h4 className="section-title" style={{ color: '#f87171', borderBottomColor: 'rgba(239, 68, 68, 0.2)' }}>
                          <span>✗</span> Areas to Improve
                        </h4>
                        <ul style={{ listStyleType: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
                          {atsData.weaknesses && atsData.weaknesses.map((weak, idx) => (
                            <li key={idx} style={{ display: 'flex', gap: '0.6rem', alignItems: 'flex-start', color: '#e2e8f0', fontSize: '0.95rem' }}>
                              <span style={{ color: '#f87171', fontWeight: 'bold' }}>✗</span>
                              <span>{weak}</span>
                            </li>
                          ))}
                          {atsData.recommendations && atsData.recommendations.map((rec, idx) => (
                            <li key={`rec-${idx}`} style={{ display: 'flex', gap: '0.6rem', alignItems: 'flex-start', color: '#cbd5e1', fontSize: '0.92rem', paddingLeft: '1rem', fontStyle: 'italic' }}>
                              <span style={{ color: 'var(--text-muted)' }}>&bull;</span>
                              <span>{rec}</span>
                            </li>
                          ))}
                          {(!atsData.weaknesses || atsData.weaknesses.length === 0) && (!atsData.recommendations || atsData.recommendations.length === 0) && (
                            <li style={{ color: 'var(--text-muted)', fontStyle: 'italic', fontSize: '0.9rem' }}>
                              No improvement areas identified. Excellent resume!
                            </li>
                          )}
                        </ul>
                      </div>

                    </div>
                  </div>

                </div>
              )}
            </div>
          )}

          {activeTab === 'recommendations' && (
            <div>
              {isExtracting && (
                <div className="loader-container">
                  <div className="spinner"></div>
                  <p style={{ color: 'var(--text-muted)', fontWeight: 500 }}>
                    Analyzing profiles for Career Recommendation...
                  </p>
                </div>
              )}

              {!isExtracting && !recommendationsData && (
                <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', padding: '2rem', textAlign: 'center' }}>
                  No recommendations available. Please upload a resume first.
                </p>
              )}

              {!isExtracting && recommendationsData && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                  
                  <div style={{ 
                    backgroundColor: 'rgba(255, 255, 255, 0.01)',
                    padding: '1.5rem',
                    borderRadius: '12px',
                    border: '1px solid var(--border-color)',
                    marginBottom: '1rem'
                  }}>
                    <h3 style={{ fontSize: '1.35rem', fontWeight: 'bold', color: 'var(--text-light)', marginBottom: '0.5rem', fontFamily: "'Outfit', sans-serif" }}>
                      💼 Local Career Intelligence Insights
                    </h3>
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', lineHeight: '1.6' }}>
                      Based on our localized matching rules, we analyzed your <strong>{processedData.skills.length} skills</strong>, <strong>{processedData.projects.length} projects</strong>, and <strong>ATS score ({atsData?.ats_score ?? 70})</strong>. Here are your top 5 matching career paths, complete with skill gap analysis.
                    </p>
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    {recommendationsData.map((career, idx) => {
                      // Perform skill gap classification
                      const reqSkillsEnriched = career.required_skills.map(skill => {
                        const matched = isSkillMatched(skill, processedData.skills);
                        return { name: skill, matched };
                      });

                      const prefSkillsEnriched = career.preferred_skills.map(skill => {
                        const matched = isSkillMatched(skill, processedData.skills);
                        return { name: skill, matched };
                      });

                      return (
                        <div key={idx} className="section-card" style={{ 
                          padding: '2rem',
                          position: 'relative',
                          overflow: 'hidden'
                        }}>
                          {/* Top Rank Badge */}
                          <div style={{
                            position: 'absolute',
                            top: 0,
                            right: 0,
                            backgroundColor: 'rgba(99, 102, 241, 0.1)',
                            borderBottomLeftRadius: '12px',
                            borderLeft: '1px solid var(--border-color)',
                            borderBottom: '1px solid var(--border-color)',
                            padding: '0.5rem 1rem',
                            fontSize: '0.9rem',
                            fontWeight: 'bold',
                            color: '#a5b4fc'
                          }}>
                            Rank #{idx + 1}
                          </div>

                          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1.5rem', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.25rem' }}>
                            <div>
                              <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--text-light)', marginBottom: '0.25rem', fontFamily: "'Outfit', sans-serif" }}>
                                {career.role}
                              </h3>
                              <span style={{ fontSize: '0.85rem', color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: '700' }}>
                                📁 {career.category}
                              </span>
                            </div>

                            {/* Match Meter */}
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                              <div style={{ textAlign: 'right' }}>
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Match Score</div>
                                <div style={{ fontSize: '1.5rem', fontWeight: '800', color: career.match_score >= 70 ? 'var(--success)' : career.match_score >= 50 ? '#f59e0b' : 'var(--error)' }}>
                                  {career.match_score}%
                                </div>
                              </div>
                              <div style={{ 
                                width: '60px', 
                                height: '60px', 
                                borderRadius: '50%', 
                                background: `conic-gradient(${
                                  career.match_score >= 70 ? 'var(--success)' : career.match_score >= 50 ? '#f59e0b' : 'var(--error)'
                                } ${career.match_score * 3.6}deg, rgba(255,255,255,0.06) 0deg)`,
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center'
                              }}>
                                <div style={{ width: '48px', height: '48px', borderRadius: '50%', backgroundColor: 'var(--bg-card)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.8rem', fontWeight: 'bold', color: 'var(--text-light)' }}>
                                  🎯
                                </div>
                              </div>
                            </div>
                          </div>

                          <p style={{ color: '#cbd5e1', fontSize: '0.95rem', lineHeight: '1.6', marginBottom: '1.5rem' }}>
                            {career.description}
                          </p>

                          {/* Metadata Badges */}
                          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem', marginBottom: '1.5rem' }}>
                            <span style={{ 
                              fontSize: '0.75rem', 
                              fontWeight: '600', 
                              backgroundColor: 'rgba(245, 158, 11, 0.08)', 
                              color: '#f59e0b', 
                              border: '1px solid rgba(245, 158, 11, 0.2)',
                              padding: '0.3rem 0.6rem',
                              borderRadius: '4px'
                            }}>
                              ⚡ Difficulty: {career.difficulty_level}
                            </span>
                            <span style={{ 
                              fontSize: '0.75rem', 
                              fontWeight: '600', 
                              backgroundColor: 'rgba(16, 185, 129, 0.08)', 
                              color: 'var(--success)', 
                              border: '1px solid rgba(16, 185, 129, 0.2)',
                              padding: '0.3rem 0.6rem',
                              borderRadius: '4px'
                            }}>
                              📈 Growth: {career.growth_level}
                            </span>
                            <span style={{ 
                              fontSize: '0.75rem', 
                              fontWeight: '600', 
                              backgroundColor: 'rgba(99, 102, 241, 0.08)', 
                              color: '#a5b4fc', 
                              border: '1px solid rgba(99, 102, 241, 0.2)',
                              padding: '0.3rem 0.6rem',
                              borderRadius: '4px'
                            }}>
                              🔥 Future Demand: {career.future_demand}
                            </span>
                          </div>

                          {/* Matching Reasons */}
                          <div style={{ marginBottom: '1.5rem' }}>
                            <h4 style={{ fontSize: '0.95rem', fontWeight: 'bold', color: 'var(--text-light)', marginBottom: '0.5rem' }}>Match Breakdown</h4>
                            <ul style={{ listStyleType: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                              {career.reason.map((r, rIdx) => (
                                <li key={rIdx} style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', fontSize: '0.9rem', color: '#e2e8f0' }}>
                                  <span style={{ color: 'var(--success)', fontWeight: 'bold' }}>✓</span>
                                  <span>{r}</span>
                                </li>
                              ))}
                            </ul>
                          </div>

                          {/* Skill Gap Analysis */}
                          <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '1.5rem', padding: '1.25rem', backgroundColor: 'rgba(255,255,255,0.01)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.04)', marginBottom: '1.5rem' }}>
                            <div>
                              <h4 style={{ fontSize: '0.9rem', fontWeight: 'bold', color: 'var(--text-light)', marginBottom: '0.6rem', display: 'flex', justifyContent: 'space-between' }}>
                                <span>Required Skills Gap Analysis</span>
                                <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>
                                  {reqSkillsEnriched.filter(s => s.matched).length} / {reqSkillsEnriched.length} Matched
                                </span>
                              </h4>
                              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                                {reqSkillsEnriched.map((skill, sIdx) => (
                                  <span key={sIdx} style={{ 
                                    fontSize: '0.8rem', 
                                    padding: '0.3rem 0.6rem', 
                                    borderRadius: '4px',
                                    fontWeight: '500',
                                    display: 'inline-flex',
                                    alignItems: 'center',
                                    gap: '0.25rem',
                                    backgroundColor: skill.matched ? 'rgba(16, 185, 129, 0.08)' : 'rgba(239, 68, 68, 0.05)',
                                    color: skill.matched ? '#34d399' : '#f87171',
                                    border: skill.matched ? '1px solid rgba(16, 185, 129, 0.15)' : '1px solid rgba(239, 68, 68, 0.15)'
                                  }}>
                                    {skill.matched ? '●' : '○'} {skill.name}
                                  </span>
                                ))}
                              </div>
                            </div>

                            {prefSkillsEnriched.length > 0 && (
                              <div>
                                <h4 style={{ fontSize: '0.9rem', fontWeight: 'bold', color: 'var(--text-light)', marginBottom: '0.6rem', display: 'flex', justifyContent: 'space-between' }}>
                                  <span>Preferred Skills Gap Analysis</span>
                                  <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>
                                    {prefSkillsEnriched.filter(s => s.matched).length} / {prefSkillsEnriched.length} Matched
                                  </span>
                                </h4>
                                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                                  {prefSkillsEnriched.map((skill, sIdx) => (
                                    <span key={sIdx} style={{ 
                                      fontSize: '0.8rem', 
                                      padding: '0.3rem 0.6rem', 
                                      borderRadius: '4px',
                                      fontWeight: '500',
                                      display: 'inline-flex',
                                      alignItems: 'center',
                                      gap: '0.25rem',
                                      backgroundColor: skill.matched ? 'rgba(99, 102, 241, 0.08)' : 'rgba(255,255,255,0.02)',
                                      color: skill.matched ? '#a5b4fc' : 'var(--text-muted)',
                                      border: skill.matched ? '1px solid rgba(99, 102, 241, 0.15)' : '1px solid var(--border-color)'
                                    }}>
                                      {skill.matched ? '●' : '○'} {skill.name}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>

                          {/* Collapsible Advanced Skill Gap Intelligence */}
                          <div style={{ marginBottom: '1.5rem' }}>
                            <button
                              onClick={() => handleToggleGap(career.role, career)}
                              style={{
                                backgroundColor: expandedGaps[career.role] ? 'rgba(79, 70, 229, 0.2)' : 'rgba(255, 255, 255, 0.03)',
                                border: expandedGaps[career.role] ? '1px solid var(--primary)' : '1px solid var(--border-color)',
                                color: 'var(--text-light)',
                                padding: '0.65rem 1.25rem',
                                borderRadius: '8px',
                                cursor: 'pointer',
                                width: '100%',
                                fontWeight: '600',
                                display: 'flex',
                                justifyContent: 'center',
                                alignItems: 'center',
                                gap: '0.5rem',
                                transition: 'all 0.2s ease',
                                fontSize: '0.9rem',
                                outline: 'none'
                              }}
                            >
                              <span>📊</span> {expandedGaps[career.role] ? 'Collapse Skill Gap Intelligence' : 'Analyze Skill Gap Intelligence'}
                            </button>

                            {expandedGaps[career.role] && (
                              <div style={{
                                marginTop: '1rem',
                                padding: '1.25rem',
                                backgroundColor: 'rgba(255, 255, 255, 0.015)',
                                borderRadius: '10px',
                                border: '1px solid rgba(255, 255, 255, 0.04)',
                                display: 'flex',
                                flexDirection: 'column',
                                gap: '1.25rem'
                              }}>
                                {loadingGaps[career.role] ? (
                                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '1.5rem 0' }}>
                                    <div className="spinner" style={{ width: '32px', height: '32px', border: '3px solid var(--border-color)', borderTopColor: 'var(--primary)', borderRadius: '50%', marginBottom: '0.75rem' }}></div>
                                    <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Generating skill gap report...</span>
                                  </div>
                                ) : skillGaps[career.role] ? (
                                  <>
                                    {(() => {
                                      const renderEffortBadge = (effort) => {
                                        let color = '#34d399';
                                        let bg = 'rgba(16, 185, 129, 0.08)';
                                        let border = '1px solid rgba(16, 185, 129, 0.15)';
                                        if (effort === 'Very High') {
                                          color = '#f87171';
                                          bg = 'rgba(239, 68, 68, 0.08)';
                                          border = '1px solid rgba(239, 68, 68, 0.15)';
                                        } else if (effort === 'High') {
                                          color = '#fbbf24';
                                          bg = 'rgba(245, 158, 11, 0.08)';
                                          border = '1px solid rgba(245, 158, 11, 0.15)';
                                        } else if (effort === 'Medium') {
                                          color = '#60a5fa';
                                          bg = 'rgba(59, 130, 246, 0.08)';
                                          border = '1px solid rgba(59, 130, 246, 0.15)';
                                        }
                                        return (
                                          <span style={{
                                            fontSize: '0.7rem',
                                            fontWeight: '600',
                                            color: color,
                                            backgroundColor: bg,
                                            border: border,
                                            padding: '0.15rem 0.4rem',
                                            borderRadius: '4px',
                                            textTransform: 'uppercase',
                                            display: 'inline-block'
                                          }}>
                                            {effort}
                                          </span>
                                        );
                                      };

                                      const readiness = skillGaps[career.role].career_readiness;
                                      let readinessColor = 'var(--success)';
                                      if (readiness < 26) readinessColor = 'var(--error)';
                                      else if (readiness < 51) readinessColor = '#f97316';
                                      else if (readiness < 76) readinessColor = '#fbbf24';
                                      else if (readiness < 91) readinessColor = '#818cf8';

                                      const totalSkillsToLearn = skillGaps[career.role].critical_skills.length +
                                                                 skillGaps[career.role].important_skills.length +
                                                                 skillGaps[career.role].optional_skills.length;

                                      return (
                                        <>
                                          {/* Metrics Grid */}
                                          <div style={{
                                            display: 'grid',
                                            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                                            gap: '1rem'
                                          }}>
                                            {/* Readiness Card */}
                                            <div style={{
                                              backgroundColor: 'var(--bg-card)',
                                              border: '1px solid var(--border-color)',
                                              borderRadius: '8px',
                                              padding: '1rem',
                                              display: 'flex',
                                              alignItems: 'center',
                                              gap: '0.85rem'
                                            }}>
                                              <div style={{
                                                width: '52px',
                                                height: '52px',
                                                borderRadius: '50%',
                                                background: `conic-gradient(${readinessColor} ${readiness * 3.6}deg, rgba(255,255,255,0.06) 0deg)`,
                                                display: 'flex',
                                                alignItems: 'center',
                                                justifyContent: 'center',
                                                flexShrink: 0
                                              }}>
                                                <div style={{ width: '40px', height: '40px', borderRadius: '50%', backgroundColor: 'var(--bg-card)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.85rem', fontWeight: 'bold' }}>
                                                  {readiness}%
                                                </div>
                                              </div>
                                              <div>
                                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Career Readiness</div>
                                                <div style={{ 
                                                  fontSize: '1rem', 
                                                  fontWeight: 'bold', 
                                                  color: readinessColor
                                                }}>
                                                  {skillGaps[career.role].career_readiness_level}
                                                </div>
                                              </div>
                                            </div>

                                            {/* Gap Severity Card */}
                                            <div style={{
                                              backgroundColor: 'var(--bg-card)',
                                              border: '1px solid var(--border-color)',
                                              borderRadius: '8px',
                                              padding: '1rem',
                                              display: 'flex',
                                              alignItems: 'center',
                                              gap: '0.85rem'
                                            }}>
                                              <div style={{
                                                width: '40px',
                                                height: '40px',
                                                borderRadius: '6px',
                                                backgroundColor: skillGaps[career.role].gap_severity === 'Low Gap' ? 'rgba(16, 185, 129, 0.1)' :
                                                                 skillGaps[career.role].gap_severity === 'Medium Gap' ? 'rgba(245, 158, 11, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                                                display: 'flex',
                                                alignItems: 'center',
                                                justifyContent: 'center',
                                                fontSize: '1.25rem',
                                                color: skillGaps[career.role].gap_severity === 'Low Gap' ? 'var(--success)' :
                                                       skillGaps[career.role].gap_severity === 'Medium Gap' ? '#fbbf24' : 'var(--error)',
                                                flexShrink: 0
                                              }}>
                                                {skillGaps[career.role].gap_severity === 'Low Gap' ? '🟢' :
                                                 skillGaps[career.role].gap_severity === 'Medium Gap' ? '🟡' : '🔴'}
                                              </div>
                                              <div>
                                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Gap Severity</div>
                                                <div style={{
                                                  fontSize: '1rem',
                                                  fontWeight: 'bold',
                                                  color: skillGaps[career.role].gap_severity === 'Low Gap' ? 'var(--success)' :
                                                         skillGaps[career.role].gap_severity === 'Medium Gap' ? '#fbbf24' : '#f87171'
                                                }}>
                                                  {skillGaps[career.role].gap_severity}
                                                </div>
                                              </div>
                                            </div>

                                            {/* Estimated Time to Job Ready */}
                                            <div style={{
                                              backgroundColor: 'var(--bg-card)',
                                              border: '1px solid var(--border-color)',
                                              borderRadius: '8px',
                                              padding: '1rem',
                                              display: 'flex',
                                              alignItems: 'center',
                                              gap: '0.85rem'
                                            }}>
                                              <div style={{
                                                width: '40px',
                                                height: '40px',
                                                borderRadius: '6px',
                                                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                                                display: 'flex',
                                                alignItems: 'center',
                                                justifyContent: 'center',
                                                fontSize: '1.25rem',
                                                color: '#818cf8',
                                                flexShrink: 0
                                              }}>
                                                ⏱️
                                              </div>
                                              <div>
                                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Time to Job Ready</div>
                                                <div style={{ fontSize: '1rem', fontWeight: 'bold', color: '#a5b4fc' }}>
                                                  {skillGaps[career.role].job_ready_time_months}
                                                </div>
                                                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                                                  or {skillGaps[career.role].job_ready_time_weeks}
                                                </div>
                                              </div>
                                            </div>

                                            {/* Total Gaps Card */}
                                            <div style={{
                                              backgroundColor: 'var(--bg-card)',
                                              border: '1px solid var(--border-color)',
                                              borderRadius: '8px',
                                              padding: '1rem',
                                              display: 'flex',
                                              alignItems: 'center',
                                              gap: '0.85rem'
                                            }}>
                                              <div style={{
                                                width: '40px',
                                                height: '40px',
                                                borderRadius: '6px',
                                                backgroundColor: 'rgba(255, 255, 255, 0.03)',
                                                display: 'flex',
                                                alignItems: 'center',
                                                justifyContent: 'center',
                                                fontSize: '1.25rem',
                                                color: '#cbd5e1',
                                                flexShrink: 0
                                              }}>
                                                📚
                                              </div>
                                              <div>
                                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Missing Skills</div>
                                                <div style={{ fontSize: '1rem', fontWeight: 'bold', color: 'var(--text-light)' }}>
                                                  {totalSkillsToLearn} Skills
                                                </div>
                                                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                                                  to learn in total
                                                </div>
                                              </div>
                                            </div>
                                          </div>

                                          {/* Career Readiness Insights Summary Text */}
                                          <div style={{
                                            backgroundColor: 'rgba(99, 102, 241, 0.04)',
                                            borderLeft: '4px solid #6366f1',
                                            padding: '1.25rem',
                                            borderRadius: '8px',
                                            lineHeight: '1.6',
                                            whiteSpace: 'pre-line',
                                            fontSize: '0.925rem',
                                            color: '#e2e8f0'
                                          }}>
                                            <h4 style={{ fontWeight: '700', color: 'var(--text-light)', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.4rem', fontFamily: "'Outfit', sans-serif" }}>
                                              <span>💡</span> Career Readiness Insights
                                            </h4>
                                            {skillGaps[career.role].insights.summary_text}
                                          </div>

                                          {/* Strong & Weak Areas list */}
                                          <div style={{
                                            backgroundColor: 'rgba(255,255,255,0.01)',
                                            border: '1px solid var(--border-color)',
                                            borderRadius: '8px',
                                            padding: '1.25rem',
                                            display: 'grid',
                                            gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
                                            gap: '1.5rem'
                                          }}>
                                            <div>
                                              <div style={{ fontSize: '0.85rem', color: 'var(--success)', fontWeight: 'bold', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>✓ Strong Areas</div>
                                              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
                                                {skillGaps[career.role].insights.strong_areas.slice(0, 8).map((sa, saIdx) => (
                                                  <div key={saIdx} style={{ fontSize: '0.85rem', color: '#cbd5e1', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                                                    ✓ {sa}
                                                  </div>
                                                ))}
                                                {skillGaps[career.role].insights.strong_areas.length > 8 && (
                                                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', paddingLeft: '0.75rem' }}>+{skillGaps[career.role].insights.strong_areas.length - 8} more</div>
                                                )}
                                                {skillGaps[career.role].insights.strong_areas.length === 0 && (
                                                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>None detected</span>
                                                )}
                                              </div>
                                            </div>
                                            <div>
                                              <div style={{ fontSize: '0.85rem', color: '#fca5a5', fontWeight: 'bold', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>✗ Weak Areas</div>
                                              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
                                                {skillGaps[career.role].insights.weak_areas.slice(0, 8).map((wa, waIdx) => (
                                                  <div key={waIdx} style={{ fontSize: '0.85rem', color: '#cbd5e1', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                                                    ✗ {wa}
                                                  </div>
                                                ))}
                                                {skillGaps[career.role].insights.weak_areas.length > 8 && (
                                                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', paddingLeft: '0.75rem' }}>+{skillGaps[career.role].insights.weak_areas.length - 8} more</div>
                                                )}
                                                {skillGaps[career.role].insights.weak_areas.length === 0 && (
                                                  <span style={{ fontSize: '0.8rem', color: 'var(--success)', fontStyle: 'italic' }}>No major weaknesses</span>
                                                )}
                                              </div>
                                            </div>
                                          </div>

                                          {/* Milestone Career Roadmap */}
                                          {skillGaps[career.role].milestones && skillGaps[career.role].milestones.length > 0 && (
                                            <div style={{
                                              backgroundColor: 'rgba(255, 255, 255, 0.01)',
                                              border: '1px solid var(--border-color)',
                                              borderRadius: '10px',
                                              padding: '1.5rem',
                                            }}>
                                              <h4 style={{ fontSize: '1rem', fontWeight: 'bold', color: 'var(--text-light)', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem', fontFamily: "'Outfit', sans-serif" }}>
                                                <span>🗺️</span> Milestone Career Roadmap
                                              </h4>
                                              <div style={{
                                                display: 'flex',
                                                flexDirection: 'column',
                                                gap: '1.5rem',
                                                position: 'relative',
                                                paddingLeft: '1.25rem',
                                                borderLeft: '2px dashed rgba(99, 102, 241, 0.25)'
                                              }}>
                                                {skillGaps[career.role].milestones.map((milestone, mIdx) => {
                                                  const isLast = mIdx === skillGaps[career.role].milestones.length - 1;
                                                  return (
                                                    <div key={mIdx} style={{
                                                      position: 'relative',
                                                      display: 'flex',
                                                      flexDirection: 'column',
                                                      gap: '0.5rem'
                                                    }}>
                                                      {/* Milestone Step Indicator Badge */}
                                                      <div style={{
                                                        position: 'absolute',
                                                        left: '-2.05rem',
                                                        top: '0.15rem',
                                                        width: '24px',
                                                        height: '24px',
                                                        borderRadius: '50%',
                                                        backgroundColor: isLast ? 'rgba(16, 185, 129, 0.1)' : 'rgba(99, 102, 241, 0.1)',
                                                        border: isLast ? '2px solid var(--success)' : '2px solid var(--primary)',
                                                        color: isLast ? 'var(--success)' : 'var(--text-light)',
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        justifyContent: 'center',
                                                        fontSize: '0.75rem',
                                                        fontWeight: 'bold',
                                                        zIndex: 2,
                                                        boxShadow: '0 0 8px rgba(99, 102, 241, 0.2)'
                                                      }}>
                                                        {isLast ? '✓' : milestone.index}
                                                      </div>
                                                      
                                                      {/* Milestone Content Box */}
                                                      <div style={{
                                                        backgroundColor: isLast ? 'rgba(16, 185, 129, 0.03)' : 'rgba(255, 255, 255, 0.01)',
                                                        border: isLast ? '1px solid rgba(16, 185, 129, 0.15)' : '1px solid var(--border-color)',
                                                        borderRadius: '8px',
                                                        padding: '1rem 1.25rem',
                                                        transition: 'transform 0.2s ease, box-shadow 0.2s ease',
                                                        cursor: 'default'
                                                      }}
                                                      onMouseEnter={(e) => {
                                                        e.currentTarget.style.transform = 'translateX(4px)';
                                                        e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
                                                      }}
                                                      onMouseLeave={(e) => {
                                                        e.currentTarget.style.transform = 'none';
                                                        e.currentTarget.style.boxShadow = 'none';
                                                      }}
                                                      >
                                                        <div style={{
                                                          fontWeight: '700',
                                                          fontSize: '0.95rem',
                                                          color: isLast ? 'var(--success)' : 'var(--text-light)',
                                                          fontFamily: "'Outfit', sans-serif",
                                                          marginBottom: '0.4rem'
                                                        }}>
                                                          {milestone.title}
                                                        </div>
                                                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', marginTop: '0.5rem' }}>
                                                          {milestone.skills.map((skill, sIdx) => (
                                                            <span key={sIdx} style={{
                                                              fontSize: '0.75rem',
                                                              backgroundColor: isLast ? 'rgba(16, 185, 129, 0.08)' : 'rgba(99, 102, 241, 0.05)',
                                                              border: isLast ? '1px solid rgba(16, 185, 129, 0.2)' : '1px solid rgba(99, 102, 241, 0.2)',
                                                              color: isLast ? '#34d399' : '#cbd5e1',
                                                              padding: '0.25rem 0.6rem',
                                                              borderRadius: '4px',
                                                              fontWeight: '600'
                                                            }}>
                                                              {skill}
                                                            </span>
                                                          ))}
                                                        </div>
                                                      </div>
                                                    </div>
                                                  );
                                                })}
                                              </div>
                                            </div>
                                          )}

                                          {/* Recommended Learning Order */}
                                          {skillGaps[career.role].priority_ranking && skillGaps[career.role].priority_ranking.length > 0 && (
                                            <div style={{
                                              backgroundColor: 'rgba(255, 255, 255, 0.01)',
                                              border: '1px solid var(--border-color)',
                                              borderRadius: '10px',
                                              padding: '1.25rem',
                                            }}>
                                              <h4 style={{ fontSize: '1rem', fontWeight: 'bold', color: 'var(--text-light)', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem', fontFamily: "'Outfit', sans-serif" }}>
                                                <span>📈</span> Recommended Learning Order
                                              </h4>
                                              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', paddingLeft: '0.5rem' }}>
                                                {skillGaps[career.role].priority_ranking.map((skillName, rIdx) => {
                                                  const allMissing = [
                                                    ...skillGaps[career.role].critical_skills,
                                                    ...skillGaps[career.role].important_skills,
                                                    ...skillGaps[career.role].optional_skills
                                                  ];
                                                  const skillItem = allMissing.find(item => item.skill.toLowerCase() === skillName.toLowerCase());
                                                  const priority = skillItem ? skillItem.priority : 'Optional';
                                                  const effort = skillItem ? skillItem.effort_score : 'Medium';
                                                  
                                                  const roadmapItem = skillGaps[career.role].roadmap_compatibility.find(item => item.skill.toLowerCase() === skillName.toLowerCase());
                                                  const dependencies = roadmapItem ? roadmapItem.dependencies : [];
                                                  
                                                  let priorityColor = '#c7d2fe';
                                                  let priorityBg = 'rgba(99, 102, 241, 0.08)';
                                                  let priorityBorder = '1px solid rgba(99, 102, 241, 0.15)';
                                                  if (priority === 'Critical') {
                                                    priorityColor = '#fca5a5';
                                                    priorityBg = 'rgba(239, 68, 68, 0.08)';
                                                    priorityBorder = '1px solid rgba(239, 68, 68, 0.15)';
                                                  } else if (priority === 'Important') {
                                                    priorityColor = '#fbcfe8';
                                                    priorityBg = 'rgba(244, 63, 94, 0.06)';
                                                    priorityBorder = '1px solid rgba(244, 63, 94, 0.12)';
                                                  }

                                                  return (
                                                    <div key={rIdx} style={{
                                                      display: 'flex',
                                                      gap: '1rem',
                                                      alignItems: 'flex-start',
                                                      position: 'relative'
                                                    }}>
                                                      <div style={{
                                                        display: 'flex',
                                                        flexDirection: 'column',
                                                        alignItems: 'center',
                                                        flexShrink: 0
                                                      }}>
                                                        <div style={{
                                                          width: '26px',
                                                          height: '26px',
                                                          borderRadius: '50%',
                                                          backgroundColor: 'rgba(79, 70, 229, 0.08)',
                                                          border: '2px solid var(--primary)',
                                                          color: 'var(--text-light)',
                                                          display: 'flex',
                                                          alignItems: 'center',
                                                          justifyContent: 'center',
                                                          fontWeight: 'bold',
                                                          fontSize: '0.8rem',
                                                          zIndex: 1
                                                        }}>
                                                          {rIdx + 1}
                                                        </div>
                                                        {rIdx < skillGaps[career.role].priority_ranking.length - 1 && (
                                                          <div style={{
                                                            width: '2px',
                                                            height: '38px',
                                                            backgroundColor: 'var(--border-color)',
                                                            marginTop: '0.2rem',
                                                            marginBottom: '0.2rem'
                                                          }} />
                                                        )}
                                                      </div>
                                                      <div style={{ flex: 1, paddingTop: '0.1rem' }}>
                                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                                                          <span style={{ fontWeight: '600', color: 'var(--text-light)', fontSize: '0.9rem' }}>{skillName}</span>
                                                          <span style={{
                                                            fontSize: '0.65rem',
                                                            fontWeight: '700',
                                                            color: priorityColor,
                                                            backgroundColor: priorityBg,
                                                            border: priorityBorder,
                                                            padding: '0.1rem 0.35rem',
                                                            borderRadius: '3px',
                                                            textTransform: 'uppercase'
                                                          }}>{priority}</span>
                                                          {renderEffortBadge(effort)}
                                                          {skillItem && (
                                                            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                                                              ⏱️ {skillItem.estimated_learning_time}
                                                            </span>
                                                          )}
                                                        </div>
                                                        {dependencies && dependencies.length > 0 && (
                                                          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.2rem', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                                                            <span style={{ color: '#818cf8', fontWeight: '500' }}>Prerequisites:</span> {dependencies.join(', ')}
                                                          </div>
                                                        )}
                                                      </div>
                                                    </div>
                                                  );
                                                })}
                                              </div>
                                            </div>
                                          )}

                                          {/* Grouped Missing Skills tag cloud */}
                                          {skillGaps[career.role].missing_categories && Object.keys(skillGaps[career.role].missing_categories).length > 0 && (
                                            <div style={{
                                              backgroundColor: 'rgba(255, 255, 255, 0.01)',
                                              border: '1px solid var(--border-color)',
                                              borderRadius: '10px',
                                              padding: '1.25rem',
                                            }}>
                                              <h4 style={{ fontSize: '1rem', fontWeight: 'bold', color: 'var(--text-light)', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem', fontFamily: "'Outfit', sans-serif" }}>
                                                <span>📁</span> Missing Skills by Category
                                              </h4>
                                              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.25rem' }}>
                                                {Object.entries(skillGaps[career.role].missing_categories).map(([catName, skillsList]) => (
                                                  <div key={catName} style={{
                                                    backgroundColor: 'rgba(255, 255, 255, 0.015)',
                                                    border: '1px solid rgba(255, 255, 255, 0.03)',
                                                    borderRadius: '8px',
                                                    padding: '1rem',
                                                  }}>
                                                    <h5 style={{ fontSize: '0.8rem', fontWeight: '800', color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>
                                                      {catName}
                                                    </h5>
                                                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                                                      {skillsList.map((skill, sIdx) => (
                                                        <span key={sIdx} style={{
                                                          fontSize: '0.75rem',
                                                          backgroundColor: 'rgba(79, 70, 229, 0.06)',
                                                          border: '1px solid rgba(79, 70, 229, 0.2)',
                                                          color: '#cbd5e1',
                                                          padding: '0.25rem 0.55rem',
                                                          borderRadius: '4px',
                                                          fontWeight: '500'
                                                        }}>
                                                          {skill}
                                                        </span>
                                                      ))}
                                                    </div>
                                                  </div>
                                                ))}
                                              </div>
                                            </div>
                                          )}

                                          {/* Detailed Lists with Effort Score Badges */}
                                          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                                            {/* Critical Skills */}
                                            {skillGaps[career.role].critical_skills.length > 0 && (
                                              <div>
                                                <div style={{ fontSize: '0.8rem', color: '#fca5a5', fontWeight: 'bold', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                                  🚨 Critical Missing Skills
                                                </div>
                                                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                                                  {skillGaps[career.role].critical_skills.map((item, itemIdx) => (
                                                    <div key={itemIdx} style={{
                                                      backgroundColor: 'rgba(239, 68, 68, 0.02)',
                                                      border: '1px solid rgba(239, 68, 68, 0.1)',
                                                      borderRadius: '6px',
                                                      padding: '0.5rem 0.75rem',
                                                      display: 'flex',
                                                      justifyContent: 'space-between',
                                                      alignItems: 'center',
                                                      gap: '0.5rem',
                                                      flexWrap: 'wrap'
                                                    }}>
                                                      <span style={{ fontWeight: '600', color: 'var(--text-light)', fontSize: '0.85rem' }}>{item.skill}</span>
                                                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                                                        <span style={{ fontSize: '0.75rem', color: '#fca5a5', fontWeight: 'bold' }}>Impact: {item.impact_score}</span>
                                                        {renderEffortBadge(item.effort_score)}
                                                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', backgroundColor: 'rgba(255,255,255,0.03)', padding: '0.15rem 0.4rem', borderRadius: '3px' }}>
                                                          ⏱️ {item.estimated_learning_time}
                                                        </span>
                                                      </div>
                                                    </div>
                                                  ))}
                                                </div>
                                              </div>
                                            )}

                                            {/* Important Skills */}
                                            {skillGaps[career.role].important_skills.length > 0 && (
                                              <div>
                                                <div style={{ fontSize: '0.8rem', color: '#fbcfe8', fontWeight: 'bold', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                                  ⚡ Important Missing Skills
                                                </div>
                                                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                                                  {skillGaps[career.role].important_skills.map((item, itemIdx) => (
                                                    <div key={itemIdx} style={{
                                                      backgroundColor: 'rgba(244, 63, 94, 0.01)',
                                                      border: '1px solid rgba(244, 63, 94, 0.08)',
                                                      borderRadius: '6px',
                                                      padding: '0.5rem 0.75rem',
                                                      display: 'flex',
                                                      justifyContent: 'space-between',
                                                      alignItems: 'center',
                                                      gap: '0.5rem',
                                                      flexWrap: 'wrap'
                                                    }}>
                                                      <span style={{ fontWeight: '600', color: 'var(--text-light)', fontSize: '0.85rem' }}>{item.skill}</span>
                                                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                                                        <span style={{ fontSize: '0.75rem', color: '#fbcfe8', fontWeight: 'bold' }}>Impact: {item.impact_score}</span>
                                                        {renderEffortBadge(item.effort_score)}
                                                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', backgroundColor: 'rgba(255,255,255,0.03)', padding: '0.15rem 0.4rem', borderRadius: '3px' }}>
                                                          ⏱️ {item.estimated_learning_time}
                                                        </span>
                                                      </div>
                                                    </div>
                                                  ))}
                                                </div>
                                              </div>
                                            )}

                                            {/* Optional Skills */}
                                            {skillGaps[career.role].optional_skills.length > 0 && (
                                              <div>
                                                <div style={{ fontSize: '0.8rem', color: '#c7d2fe', fontWeight: 'bold', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                                  💡 Optional Missing Skills
                                                </div>
                                                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                                                  {skillGaps[career.role].optional_skills.map((item, itemIdx) => (
                                                    <div key={itemIdx} style={{
                                                      backgroundColor: 'rgba(99, 102, 241, 0.01)',
                                                      border: '1px solid rgba(99, 102, 241, 0.08)',
                                                      borderRadius: '6px',
                                                      padding: '0.5rem 0.75rem',
                                                      display: 'flex',
                                                      justifyContent: 'space-between',
                                                      alignItems: 'center',
                                                      gap: '0.5rem',
                                                      flexWrap: 'wrap'
                                                    }}>
                                                      <span style={{ fontWeight: '600', color: 'var(--text-light)', fontSize: '0.85rem' }}>{item.skill}</span>
                                                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                                                        <span style={{ fontSize: '0.75rem', color: '#c7d2fe', fontWeight: 'bold' }}>Impact: {item.impact_score}</span>
                                                        {renderEffortBadge(item.effort_score)}
                                                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', backgroundColor: 'rgba(255,255,255,0.03)', padding: '0.15rem 0.4rem', borderRadius: '3px' }}>
                                                          ⏱️ {item.estimated_learning_time}
                                                        </span>
                                                      </div>
                                                    </div>
                                                  ))}
                                                </div>
                                              </div>
                                            )}
                                          </div>

                                          {/* Roadmap Compatibility / Intelligence Summary */}
                                          {isDevModeEnabled() ? (
                                            <div style={{ marginTop: '1rem', borderTop: '1px solid var(--border-color)', paddingTop: '1.25rem' }}>
                                              <button
                                                onClick={() => setShowJson(prev => ({ ...prev, [career.role]: !prev[career.role] }))}
                                                style={{
                                                  backgroundColor: 'transparent',
                                                  border: '1px solid var(--border-color)',
                                                  color: 'var(--text-muted)',
                                                  fontSize: '0.8rem',
                                                  cursor: 'pointer',
                                                  padding: '0.4rem 0.8rem',
                                                  borderRadius: '6px',
                                                  transition: 'all 0.2s ease',
                                                  fontWeight: '600'
                                                }}
                                                onMouseEnter={(e) => { e.target.style.color = 'var(--text-light)'; e.target.style.borderColor = 'var(--text-light)'; }}
                                                onMouseLeave={(e) => { e.target.style.color = 'var(--text-muted)'; e.target.style.borderColor = 'var(--border-color)'; }}
                                              >
                                                {showJson[career.role] ? 'Hide Roadmap Compatibility Data' : 'View Phase 7 Compatibility Layer (JSON)'}
                                              </button>
                                              {showJson[career.role] && (
                                                <div style={{ marginTop: '0.75rem' }}>
                                                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '0.25rem' }}>
                                                    The following JSON structure is designed for direct consumption by Phase 7 Roadmap Generation:
                                                  </span>
                                                  <pre style={{
                                                    backgroundColor: '#0f172a',
                                                    border: '1px solid var(--border-color)',
                                                    borderRadius: '6px',
                                                    padding: '1rem',
                                                    fontSize: '0.75rem',
                                                    color: '#cbd5e1',
                                                    overflowX: 'auto',
                                                    maxHeight: '220px',
                                                    fontFamily: 'monospace',
                                                    whiteSpace: 'pre-wrap',
                                                    wordBreak: 'break-all'
                                                  }}>
                                                            {JSON.stringify(skillGaps[career.role].roadmap_compatibility, null, 2)}
                                                  </pre>
                                                </div>
                                              )}
                                            </div>
                                          ) : (
                                            <div style={{ marginTop: '1.5rem', borderTop: '1px solid var(--border-color)', paddingTop: '1.25rem' }}>
                                              <h4 style={{ fontSize: '1rem', fontWeight: 'bold', color: 'var(--text-light)', marginBottom: '1rem', fontFamily: "'Outfit', sans-serif", display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                                                <span>🧠</span> Roadmap Intelligence Summary
                                              </h4>
                                              <div style={{
                                                backgroundColor: 'rgba(99, 102, 241, 0.02)',
                                                border: '1px solid rgba(99, 102, 241, 0.1)',
                                                borderRadius: '8px',
                                                padding: '1.25rem',
                                                display: 'flex',
                                                flexDirection: 'column',
                                                gap: '0.75rem'
                                              }}>
                                                <div style={{ fontSize: '0.925rem', color: '#cbd5e1', lineHeight: '1.6' }}>
                                                  For your transition into the <strong>{career.role}</strong> role, we calculated an estimated study timeline of <strong>{skillGaps[career.role].job_ready_time_months}</strong> (approx. {skillGaps[career.role].job_ready_time_weeks}). 
                                                  Your initial readiness level is classified as <strong>{skillGaps[career.role].career_readiness_level}</strong> ({skillGaps[career.role].career_readiness}% match).
                                                </div>
                                                <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', borderTop: '1px dashed var(--border-color)', paddingTop: '0.75rem' }}>
                                                  💡 <strong>Key Recommendation:</strong> Focus on resolving the {skillGaps[career.role].critical_skills?.length || 0} critical skill gaps to jumpstart your career readiness level.
                                                </div>
                                                <div style={{ marginTop: '0.5rem', borderTop: '1px solid rgba(255,255,255,0.05)', paddingTop: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                                  <button
                                                    onClick={() => handleGenerateRoadmap(career.role, career)}
                                                    disabled={loadingRoadmap[career.role]}
                                                    style={{
                                                      backgroundColor: '#6366f1',
                                                      border: 'none',
                                                      color: '#fff',
                                                      fontSize: '0.85rem',
                                                      cursor: 'pointer',
                                                      padding: '0.6rem 1.2rem',
                                                      borderRadius: '6px',
                                                      transition: 'all 0.2s ease',
                                                      fontWeight: '700',
                                                      display: 'inline-flex',
                                                      alignItems: 'center',
                                                      justifyContent: 'center',
                                                      gap: '0.5rem',
                                                      boxShadow: '0 4px 12px rgba(99, 102, 241, 0.25)',
                                                      outline: 'none',
                                                      width: 'fit-content'
                                                    }}
                                                    onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = '#4f46e5'; e.currentTarget.style.transform = 'translateY(-1px)'; }}
                                                    onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = '#6366f1'; e.currentTarget.style.transform = 'none'; }}
                                                  >
                                                    {loadingRoadmap[career.role] ? (
                                                      <>
                                                        <div className="spinner" style={{ width: '14px', height: '14px', border: '2px solid rgba(255,255,255,0.3)', borderTopColor: '#fff', borderRadius: '50%' }}></div>
                                                        <span>Generating Weekly Syllabus...</span>
                                                      </>
                                                    ) : (
                                                      <>
                                                        <span>🗺️</span> Generate Weekly Syllabus & Roadmap
                                                      </>
                                                    )}
                                                  </button>
                                                  {roadmapError[career.role] && (
                                                    <span style={{ fontSize: '0.75rem', color: '#f87171', marginTop: '0.25rem' }}>
                                                      ⚠️ {roadmapError[career.role]}
                                                    </span>
                                                  )}
                                                </div>
                                              </div>
                                            </div>
                                          )}
                                        </>
                                      );
                                    })()}
                                  </>
                                ) : (
                                  <div style={{ color: '#f87171', fontStyle: 'italic', fontSize: '0.85rem', textAlign: 'center', padding: '0.5rem', display: 'flex', flexDirection: 'column', gap: '0.5rem', alignItems: 'center' }}>
                                    <span>Failed to retrieve detailed gap analysis report.</span>
                                    {gapErrors[career.role] && (
                                      <span style={{ fontSize: '0.75rem', backgroundColor: 'rgba(239, 68, 68, 0.1)', padding: '0.25rem 0.75rem', borderRadius: '4px', border: '1px solid rgba(239, 68, 68, 0.2)', fontFamily: 'monospace', color: '#f87171' }}>
                                        Error: {gapErrors[career.role]}
                                      </span>
                                    )}
                                  </div>
                                )}
                              </div>
                            )}
                          </div>

                          {/* Related Careers */}

                          {career.related_careers.length > 0 && (
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Related Paths:</span>
                              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                                {career.related_careers.map((rel, rIdx) => (
                                  <span key={rIdx} style={{ 
                                    fontSize: '0.75rem', 
                                    backgroundColor: 'rgba(255,255,255,0.03)', 
                                    border: '1px solid var(--border-color)', 
                                    color: 'var(--text-muted)',
                                    padding: '0.2rem 0.5rem',
                                    borderRadius: '4px'
                                  }}>
                                    {rel}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}

                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'raw' && (
            <div>
              <div style={{ marginBottom: '1.5rem', fontSize: '0.95rem', color: 'var(--text-muted)' }}>
                <p><strong>Page Count:</strong> {parsedData.page_count}</p>
              </div>
              
              <div>
                <h3 style={{ marginBottom: '1rem', color: 'var(--text-muted)', fontSize: '1.1rem' }}>Extracted Plain Text:</h3>
                <div style={{ 
                  backgroundColor: 'var(--bg-dark)', 
                  padding: '1.5rem', 
                  borderRadius: '8px', 
                  maxHeight: '500px', 
                  overflowY: 'auto',
                  whiteSpace: 'pre-wrap',
                  fontFamily: 'monospace',
                  fontSize: '0.9rem',
                  color: '#cbd5e1',
                  border: '1px solid var(--border-color)',
                  lineHeight: '1.6'
                }}>
                  {parsedData.text_content}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
      {activeRoadmap && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          backgroundColor: 'var(--bg-dark)',
          zIndex: 9999,
          overflowY: 'auto'
        }}>
          <RoadmapDashboard 
            roadmapData={activeRoadmap} 
            onClose={() => setActiveRoadmap(null)} 
            candidateName={cleanCandidateName(parsedData?.candidate_name)}
          />
        </div>
      )}
    </div>
  );
};

export default AnalyzerPage;
