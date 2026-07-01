import { useEffect } from 'react';

export const PrivacyPage = () => {
  useEffect(() => { window.scrollTo(0, 0); }, []);

  return (
    <div className="page-content page-enter" style={{ minHeight: '100vh', paddingBottom: 'var(--space-16)' }}>
      <div className="container" style={{ maxWidth: 800 }}>
        
        <div style={{ textAlign: 'center', margin: 'var(--space-12) 0' }}>
          <h1 style={{ fontSize: 'clamp(2rem, 5vw, 3rem)', marginBottom: 'var(--space-4)' }}>
            Privacy Policy
          </h1>
          <p className="text-muted text-lg">
            Last Updated: July 2026
          </p>
        </div>

        <div className="premium-card mb-8">
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            At ILMORA, we take your privacy and data security seriously. This Privacy Policy outlines how we collect, use, process, and protect your information when you use our AI Career Assistant platform.
          </p>

          <h3 className="mb-4 text-xl mt-8">1. User Authentication</h3>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            We use Firebase Authentication to securely manage user sign-ups and logins. We collect basic profile information (such as your email address and display name) provided by your authentication provider (e.g., Google).
          </p>

          <h3 className="mb-4 text-xl mt-8">2. Resume Uploads & Data Collection</h3>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            When you upload your resume for ATS Analysis, we securely extract text and structural data. The PDF documents are temporarily processed and then securely stored in our Supabase storage buckets, accessible only to you.
          </p>

          <h3 className="mb-4 text-xl mt-8">3. AI Processing</h3>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            ILMORA utilizes the Gemini AI Engine to provide career roadmaps, interview simulations, and coaching. Your data is sent to these models strictly for processing your requests. <strong>We do not use your personal resumes or generated roadmaps to train public AI models.</strong>
          </p>

          <h3 className="mb-4 text-xl mt-8">4. Data Processing & Supabase Usage</h3>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            Your career goals, interview history, and generated roadmaps are stored in a secure PostgreSQL database hosted on Supabase. All data in transit is encrypted using industry-standard TLS.
          </p>

          <h3 className="mb-4 text-xl mt-8">5. Cookies & Tracking</h3>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            We use essential cookies to maintain your session securely. We may also use minimal analytics to improve the user experience, but we do not sell your data to third-party advertisers.
          </p>

          <h3 className="mb-4 text-xl mt-8">6. Security Measures</h3>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            We implement continuous security monitoring, secure JWT validation on our backend, and role-based access control (RLS) on our database to ensure that only you can access your career data.
          </p>

          <h3 className="mb-4 text-xl mt-8">7. User Rights</h3>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            You have the right to access, rectify, or request deletion of your personal data at any time. If you wish to delete your account and all associated data, you may do so from your profile settings or by contacting us.
          </p>

          <h3 className="mb-4 text-xl mt-8">8. Contact Information</h3>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            If you have any questions or concerns about this Privacy Policy, please contact our Data Protection Officer at <strong>support@ilmora.com</strong>.
          </p>
        </div>

      </div>
    </div>
  );
};

export default PrivacyPage;
