import { useState, useEffect } from 'react';

const faqData = [
  {
    q: 'What is ILMORA?',
    a: 'ILMORA is a premium AI Career Assistant that helps professionals analyze their resumes against modern ATS systems, plan strategic career roadmaps, and practice mock interviews using cutting-edge generative AI.'
  },
  {
    q: 'How ATS Analysis Works?',
    a: 'Our system extracts text from your uploaded PDF resume and compares it against industry-standard benchmarks and job descriptions. The AI evaluates keywords, structure, impact metrics, and formatting to provide an actionable score and improvement suggestions.'
  },
  {
    q: 'Is my resume secure?',
    a: 'Absolutely. We encrypt all data in transit and at rest. Your resume is never used to train public AI models and is strictly associated with your authenticated account.'
  },
  {
    q: 'Does ILMORA store resumes?',
    a: 'Yes, we securely store your resume in your personal Supabase storage bucket so you can easily track your ATS history over time. You can delete your data at any time.'
  },
  {
    q: 'How Career Roadmap works?',
    a: 'By analyzing your current skills and your target career goal, the Gemini AI engine generates a dynamic, step-by-step learning roadmap, complete with study hours, milestones, and project recommendations.'
  },
  {
    q: 'How Interview works?',
    a: 'The Interview module generates personalized technical and behavioral questions based on your resume. You can answer them via text or speech, and the AI evaluates your response, providing immediate feedback on clarity, accuracy, and confidence.'
  },
  {
    q: 'How PDF Export works?',
    a: 'You can export your career roadmaps and ATS analysis results directly to a beautifully formatted PDF, powered by our backend PDF generation service, so you can share it with mentors or save it locally.'
  },
  {
    q: 'Is Google Login secure?',
    a: 'Yes, we use Firebase Authentication, which handles Google Login using OAuth 2.0. We never see your Google password, only the secure authentication token provided by Google.'
  },
  {
    q: 'How to contact support?',
    a: 'You can reach out to us at support@ilmora.com or use the Feedback button floating at the bottom right of the screen!'
  }
];

export const FAQPage = () => {
  useEffect(() => { window.scrollTo(0, 0); }, []);
  const [openIndex, setOpenIndex] = useState(null);

  const toggleAccordion = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="page-content page-enter" style={{ minHeight: '100vh', paddingBottom: 'var(--space-16)' }}>
      <div className="container" style={{ maxWidth: 800 }}>
        
        <div style={{ textAlign: 'center', margin: 'var(--space-12) 0' }}>
          <h1 style={{ fontSize: 'clamp(2rem, 5vw, 3rem)', marginBottom: 'var(--space-4)' }}>
            Frequently Asked Questions
          </h1>
          <p className="text-muted text-lg">
            Everything you need to know about the product and how it works.
          </p>
        </div>

        <div className="premium-card" style={{ padding: '0' }}>
          {faqData.map((faq, index) => {
            const isOpen = openIndex === index;
            return (
              <div 
                key={index} 
                style={{ 
                  borderBottom: index < faqData.length - 1 ? '1px solid var(--border-color)' : 'none',
                }}
              >
                <button
                  onClick={() => toggleAccordion(index)}
                  style={{
                    width: '100%',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: 'var(--space-5)',
                    background: 'transparent',
                    border: 'none',
                    color: 'var(--text-primary)',
                    fontSize: 'var(--text-lg)',
                    fontWeight: 600,
                    textAlign: 'left',
                    cursor: 'pointer',
                    transition: 'color var(--transition-fast)'
                  }}
                  onMouseEnter={(e) => e.target.style.color = 'var(--primary-hover)'}
                  onMouseLeave={(e) => e.target.style.color = 'var(--text-primary)'}
                  aria-expanded={isOpen}
                >
                  {faq.q}
                  <span style={{ transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.3s ease', fontSize: '1.25rem', color: 'var(--primary)' }}>
                    ▼
                  </span>
                </button>
                
                <div 
                  style={{
                    maxHeight: isOpen ? '500px' : '0',
                    overflow: 'hidden',
                    transition: 'all 0.3s ease-in-out',
                    opacity: isOpen ? 1 : 0,
                    padding: isOpen ? '0 var(--space-5) var(--space-5) var(--space-5)' : '0 var(--space-5)',
                  }}
                >
                  <p className="text-secondary" style={{ lineHeight: '1.7', margin: 0 }}>
                    {faq.a}
                  </p>
                </div>
              </div>
            );
          })}
        </div>

      </div>
    </div>
  );
};

export default FAQPage;
