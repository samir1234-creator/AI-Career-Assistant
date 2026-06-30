import React, { useState } from 'react';
import { startInterviewSession } from '../../services/api';
import InterviewSession from './InterviewSession';

const COMPANIES = [
  { id: 'Google', icon: '🔵', tier: 'FAANG', color: '#4285f4', style: 'Algorithm-heavy + System Design + Googleyness' },
  { id: 'Microsoft', icon: '🟦', tier: 'FAANG', color: '#00a4ef', style: 'Problem solving + Growth mindset + Culture fit' },
  { id: 'Amazon', icon: '🟠', tier: 'FAANG', color: '#ff9900', style: 'Leadership Principles (STAR) + System Design at scale' },
  { id: 'Meta', icon: '🔷', tier: 'FAANG', color: '#1877f2', style: 'Scalability + Product thinking + Impact-focused behavioral' },
  { id: 'Apple', icon: '⬜', tier: 'FAANG', color: '#a2aaad', style: 'Attention to detail + Technical excellence + Design thinking' },
  { id: 'Netflix', icon: '🔴', tier: 'FAANG', color: '#e50914', style: 'High performance culture + Streaming tech + Data-driven' },
  { id: 'Adobe', icon: '🟥', tier: 'Top Tech', color: '#ff0000', style: 'Collaborative + Creative + User-centered problem solving' },
  { id: 'Oracle', icon: '🔶', tier: 'Top Tech', color: '#f80000', style: 'Database internals + Java + Enterprise architecture' },
  { id: 'IBM', icon: '🔳', tier: 'Top Tech', color: '#054ada', style: 'Enterprise AI + Cloud consulting + Innovation' },
  { id: 'OpenAI', icon: '🤍', tier: 'AI Labs', color: '#74aa9c', style: 'LLMs + AI Safety + Research-oriented + Systems' },
  { id: 'Infosys', icon: '🟤', tier: 'IT Services', color: '#007cc3', style: 'Fundamentals + OOP + Database + Process adherence' },
  { id: 'TCS', icon: '🔵', tier: 'IT Services', color: '#0052cc', style: 'Aptitude + Core programming + Communication' },
  { id: 'Accenture', icon: '🟣', tier: 'IT Services', color: '#a100ff', style: 'Consulting mindset + Agile + Tech solutions' },
  { id: 'Capgemini', icon: '🟢', tier: 'IT Services', color: '#0070ad', style: 'Cloud + Digital transformation + Teamwork' },
  { id: 'Wipro', icon: '🟡', tier: 'IT Services', color: '#352269', style: 'Core CS fundamentals + Testing + Communication' },
];

const TIERS = ['All', 'FAANG', 'Top Tech', 'AI Labs', 'IT Services'];

export default function CompanyInterviewPage() {
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [selectedTier, setSelectedTier] = useState('All');
  const [sessionData, setSessionData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const filtered = selectedTier === 'All' ? COMPANIES : COMPANIES.filter(c => c.tier === selectedTier);

  const handleStart = async () => {
    if (!selectedCompany) { setError('Please select a company.'); return; }
    setLoading(true); setError('');
    try {
      const data = await startInterviewSession({ interview_type: 'company', company: selectedCompany, count: 6 });
      setSessionData(data);
    } catch (e) { setError(e.message); }
    finally { setLoading(false); }
  };

  if (sessionData) return <InterviewSession sessionData={sessionData} interviewType="company" onBack={() => setSessionData(null)} />;

  const company = COMPANIES.find(c => c.id === selectedCompany);

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f1f5f9', margin: '0 0 0.375rem' }}>🏢 Company-Specific Interview</h2>
        <p style={{ color: '#64748b', fontSize: '0.85rem', margin: 0 }}>Tailored questions matching each company's actual interview style and culture</p>
      </div>

      {/* Tier filter */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.25rem', flexWrap: 'wrap' }}>
        {TIERS.map(t => (
          <button key={t} onClick={() => setSelectedTier(t)}
            style={{ background: selectedTier === t ? 'rgba(99,102,241,0.2)' : 'rgba(255,255,255,0.03)', border: `1px solid ${selectedTier === t ? '#6366f1' : 'rgba(255,255,255,0.06)'}`, borderRadius: '9999px', padding: '0.375rem 0.875rem', cursor: 'pointer', color: selectedTier === t ? '#a5b4fc' : '#94a3b8', fontSize: '0.78rem', fontWeight: selectedTier === t ? 700 : 500, transition: 'all 0.2s' }}
          >{t}</button>
        ))}
      </div>

      {/* Company grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '0.75rem', marginBottom: '1.5rem' }}>
        {filtered.map(c => (
          <button key={c.id} id={`company-${c.id.toLowerCase()}`}
            onClick={() => setSelectedCompany(c.id)}
            style={{ background: selectedCompany === c.id ? `${c.color}15` : 'rgba(255,255,255,0.03)', border: `1.5px solid ${selectedCompany === c.id ? c.color : 'rgba(255,255,255,0.06)'}`, borderRadius: '0.875rem', padding: '1rem 1.25rem', cursor: 'pointer', textAlign: 'left', transition: 'all 0.2s ease' }}
            onMouseEnter={e => { if (selectedCompany !== c.id) { e.currentTarget.style.borderColor = `${c.color}50`; e.currentTarget.style.background = `${c.color}08`; }}}
            onMouseLeave={e => { if (selectedCompany !== c.id) { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.06)'; e.currentTarget.style.background = 'rgba(255,255,255,0.03)'; }}}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '0.5rem' }}>
              <span style={{ fontSize: '1.1rem' }}>{c.icon}</span>
              <span style={{ color: selectedCompany === c.id ? c.color : '#f1f5f9', fontSize: '0.9rem', fontWeight: 700 }}>{c.id}</span>
              <span style={{ background: `${c.color}15`, color: c.color, fontSize: '0.62rem', fontWeight: 600, padding: '0.1rem 0.375rem', borderRadius: '0.25rem', marginLeft: 'auto' }}>{c.tier}</span>
            </div>
            <p style={{ color: '#64748b', fontSize: '0.72rem', margin: 0, lineHeight: 1.4 }}>{c.style}</p>
          </button>
        ))}
      </div>

      {/* Selected company details */}
      {company && (
        <div style={{ background: `linear-gradient(135deg, ${company.color}15, ${company.color}08)`, border: `1px solid ${company.color}30`, borderRadius: '1rem', padding: '1.25rem', marginBottom: '1.5rem' }}>
          <h3 style={{ color: company.color, fontSize: '1rem', fontWeight: 700, marginBottom: '0.5rem' }}>{company.icon} {company.id} Interview Style</h3>
          <p style={{ color: '#d1d5db', fontSize: '0.82rem', margin: 0 }}>{company.style}</p>
          <p style={{ color: '#94a3b8', fontSize: '0.75rem', marginTop: '0.5rem', margin: '0.5rem 0 0' }}>6 curated questions will be generated matching {company.id}'s actual interview format.</p>
        </div>
      )}

      {error && <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: '0.625rem', padding: '0.75rem', color: '#fca5a5', fontSize: '0.82rem', marginBottom: '1rem' }}>⚠️ {error}</div>}

      <button id="start-company-btn" onClick={handleStart} disabled={loading || !selectedCompany}
        style={{ background: !selectedCompany || loading ? '#1e293b' : `linear-gradient(135deg, ${company?.color || '#6366f1'}, #6366f1)`, color: !selectedCompany || loading ? '#475569' : '#fff', border: 'none', borderRadius: '0.875rem', padding: '0.875rem 2.5rem', fontSize: '0.95rem', fontWeight: 700, cursor: !selectedCompany || loading ? 'not-allowed' : 'pointer', transition: 'all 0.2s ease' }}
      >{loading ? '⏳ Preparing...' : `🏢 Start ${selectedCompany || 'Company'} Interview`}</button>
    </div>
  );
}
