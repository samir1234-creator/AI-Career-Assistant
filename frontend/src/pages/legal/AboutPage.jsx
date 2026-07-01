import { useEffect } from 'react';
import { LogoIcon } from '../../components/ui/LogoIcon';

export const AboutPage = () => {
  useEffect(() => { window.scrollTo(0, 0); }, []);

  return (
    <div className="page-content page-enter" style={{ minHeight: '100vh', paddingBottom: 'var(--space-16)' }}>
      <div className="container" style={{ maxWidth: 800 }}>
        
        <div style={{ textAlign: 'center', margin: 'var(--space-12) 0' }} className="aurora-bg">
          <div className="aurora-content">
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 'var(--space-4)' }}>
              <LogoIcon size={64} style={{ boxShadow: '0 0 30px var(--primary-glow)', borderRadius: 'var(--radius-lg)' }} />
            </div>
            <h1 style={{ fontSize: 'clamp(2rem, 5vw, 3.5rem)', marginBottom: 'var(--space-4)' }}>
              What is <span style={{ color: 'var(--primary)' }}>ILMORA</span>?
            </h1>
            <p className="text-muted text-lg" style={{ maxWidth: 600, margin: '0 auto', lineHeight: '1.8' }}>
              We are building the definitive AI Career Assistant, designed to transform how ambitious professionals analyze their skills, plan their roadmaps, and land their dream roles.
            </p>
          </div>
        </div>

        <div className="premium-card mb-8">
          <h2 className="mb-4">Mission & Vision</h2>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            <strong>Mission:</strong> To democratize career advancement by providing enterprise-grade AI tools directly to individuals.
          </p>
          <p className="text-secondary" style={{ lineHeight: '1.7' }}>
            <strong>Vision:</strong> A world where every professional has a highly intelligent, 24/7 career copilot guiding them towards their true potential.
          </p>
        </div>

        <div className="premium-card mb-8">
          <h2 className="mb-4">Why ILMORA Was Created</h2>
          <p className="text-secondary" style={{ lineHeight: '1.7' }}>
            The modern job market is chaotic. Resumes get lost in ATS black holes, skill gaps are hard to identify, and interviews are anxiety-inducing. ILMORA was born out of the necessity to bring order, strategy, and confidence to the job search process using state-of-the-art AI.
          </p>
        </div>

        <div className="grid-auto-md mb-8">
          <div className="premium-card" style={{ padding: 'var(--space-5)' }}>
            <div className="mb-2" style={{ fontSize: '2rem' }}>⚡</div>
            <h3 className="mb-2 text-lg">Core Features</h3>
            <ul className="text-secondary" style={{ lineHeight: '1.7', paddingLeft: '1.2rem' }}>
              <li>Deep ATS Analysis</li>
              <li>Dynamic Career Roadmaps</li>
              <li>Real-time AI Mock Interviews</li>
              <li>Personalized Career Coach</li>
            </ul>
          </div>
          <div className="premium-card" style={{ padding: 'var(--space-5)' }}>
            <div className="mb-2" style={{ fontSize: '2rem' }}>🛠️</div>
            <h3 className="mb-2 text-lg">Tech Stack</h3>
            <ul className="text-secondary" style={{ lineHeight: '1.7', paddingLeft: '1.2rem' }}>
              <li>React & Modern CSS</li>
              <li>FastAPI & Python</li>
              <li>Gemini AI Engine</li>
              <li>Supabase & Firebase Auth</li>
            </ul>
          </div>
        </div>

        <div className="premium-card mb-8" style={{ borderLeft: '4px solid var(--accent)' }}>
          <h2 className="mb-4">Security & Future Plans</h2>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            Your data security is paramount. We do not use your resumes to train public models, and all data is encrypted. Moving forward, we plan to introduce direct LinkedIn integration, salary negotiation simulators, and peer-to-peer mock interviews.
          </p>
          <a href="/contact" className="btn-primary" style={{ display: 'inline-block', textDecoration: 'none' }}>
            Contact Us
          </a>
        </div>

      </div>
    </div>
  );
};

export default AboutPage;
