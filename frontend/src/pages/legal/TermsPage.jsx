import { useEffect } from 'react';

export const TermsPage = () => {
  useEffect(() => { window.scrollTo(0, 0); }, []);

  return (
    <div className="page-content page-enter" style={{ minHeight: '100vh', paddingBottom: 'var(--space-16)' }}>
      <div className="container" style={{ maxWidth: 800 }}>
        
        <div style={{ textAlign: 'center', margin: 'var(--space-12) 0' }}>
          <h1 style={{ fontSize: 'clamp(2rem, 5vw, 3rem)', marginBottom: 'var(--space-4)' }}>
            Terms & Conditions
          </h1>
          <p className="text-muted text-lg">
            Last Updated: July 2026
          </p>
        </div>

        <div className="premium-card mb-8">
          <h3 className="mb-4 text-xl">1. Acceptance of Terms</h3>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            By accessing or using ILMORA, you agree to be bound by these Terms and Conditions. If you do not agree with any part of these terms, you may not use our services.
          </p>

          <h3 className="mb-4 text-xl mt-8">2. User Responsibilities</h3>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            You are responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account. You agree to provide accurate, current, and complete information during the registration process.
          </p>

          <h3 className="mb-4 text-xl mt-8">3. Acceptable Use</h3>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            You agree not to use the platform to:
          </p>
          <ul className="text-secondary mb-4" style={{ lineHeight: '1.7', paddingLeft: '1.5rem' }}>
            <li>Upload malicious files, viruses, or harmful code.</li>
            <li>Attempt to reverse-engineer, decompile, or hack the AI modules or backend systems.</li>
            <li>Use the service for any illegal or unauthorized purpose.</li>
            <li>Spam, overload, or disrupt the integrity of the platform.</li>
          </ul>

          <h3 className="mb-4 text-xl mt-8">4. Intellectual Property</h3>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            All original content, features, functionality, and design elements of ILMORA are owned by ILMORA and are protected by international copyright, trademark, and other intellectual property laws. You retain full ownership of the resumes and data you upload.
          </p>

          <h3 className="mb-4 text-xl mt-8">5. Disclaimer of Warranties</h3>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            ILMORA is provided on an "AS IS" and "AS AVAILABLE" basis. While our AI aims to provide highly accurate career advice and ATS analysis, we do not guarantee employment, specific interview outcomes, or complete error-free operation.
          </p>

          <h3 className="mb-4 text-xl mt-8">6. Limitation of Liability</h3>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            In no event shall ILMORA, nor its directors, employees, or partners, be liable for any indirect, incidental, special, consequential, or punitive damages arising out of your use of the service.
          </p>

          <h3 className="mb-4 text-xl mt-8">7. Account Termination</h3>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            We reserve the right to suspend or terminate your account immediately, without prior notice or liability, for any reason whatsoever, including without limitation if you breach the Terms.
          </p>

          <h3 className="mb-4 text-xl mt-8">8. Contact Information</h3>
          <p className="text-secondary mb-4" style={{ lineHeight: '1.7' }}>
            For any legal inquiries regarding these Terms, please contact us at <strong>support@ilmora.com</strong>.
          </p>
        </div>

      </div>
    </div>
  );
};

export default TermsPage;
