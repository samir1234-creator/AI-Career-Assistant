import { useState } from 'react';
import FeedbackModal from './FeedbackModal';

export const FloatingFeedback = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button 
        onClick={() => setIsOpen(true)}
        style={{
          position: 'fixed',
          bottom: 'var(--space-6)',
          right: 'var(--space-6)',
          zIndex: 900,
          background: 'var(--gradient-primary)',
          color: 'var(--text-primary)',
          border: 'none',
          borderRadius: '50px',
          padding: '0.75rem 1.5rem',
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--space-2)',
          fontSize: 'var(--text-sm)',
          fontWeight: 600,
          boxShadow: '0 4px 15px rgba(139, 92, 246, 0.4)',
          cursor: 'pointer',
          transition: 'transform 0.2s, box-shadow 0.2s',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'translateY(-2px)';
          e.currentTarget.style.boxShadow = '0 6px 20px rgba(139, 92, 246, 0.5)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'none';
          e.currentTarget.style.boxShadow = '0 4px 15px rgba(139, 92, 246, 0.4)';
        }}
      >
        <span aria-hidden="true" style={{ fontSize: '1.25rem' }}>💬</span>
        Feedback
      </button>

      {isOpen && <FeedbackModal onClose={() => setIsOpen(false)} />}
    </>
  );
};

export default FloatingFeedback;
