import React, { useState } from 'react';
import { ResumeUpload } from '../components/ResumeUpload/ResumeUpload';
import { formatFileSize } from '../utils/formatters';
import { extractResumeInfo, classifySkills } from '../services/api';

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

export const AnalyzerPage = () => {
  const [parsedData, setParsedData] = useState(null);
  const [extractedData, setExtractedData] = useState(null);
  const [enrichedSkills, setEnrichedSkills] = useState([]);
  const [isExtracting, setIsExtracting] = useState(false);
  const [extractionError, setExtractionError] = useState(null);
  const [activeTab, setActiveTab] = useState('profile'); // 'profile' or 'raw'

  const handleUploadSuccess = async (data) => {
    setParsedData(data);
    setIsExtracting(true);
    setExtractionError(null);
    setExtractedData(null);
    setEnrichedSkills([]);
    
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
    setExtractionError(null);
    setActiveTab('profile');
  };

  const groupedSkills = React.useMemo(() => {
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


  const processedData = React.useMemo(() => {
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
    </div>
  );
};
