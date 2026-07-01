import { memo } from "react";
import ProgressBar from './ProgressBar';

/**
 * StatCard – metric display card
 * @param {string}  icon     - emoji or small element
 * @param {string}  label    - card label (uppercase caption)
 * @param {string}  value    - primary value to display
 * @param {string}  subtext  - secondary line below value
 * @param {number}  progress - optional 0–100 progress bar
 * @param {string}  accentColor - border-left accent color
 * @param {function} onClick  - optional click handler
 */
const StatCard = memo(({
  icon,
  label,
  value,
  subtext,
  progress,
  accentColor,
  onClick,
  className = '',
  style = {}
}) => {
  return (
    <div
      className={`stat-card premium-card ${className}`}
      onClick={onClick}
      style={{
        cursor: onClick ? 'pointer' : 'default',
        borderLeft: accentColor ? `3px solid ${accentColor}` : undefined,
        ...style
      }}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={onClick ? (e) => e.key === 'Enter' && onClick(e) : undefined}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
        {icon && (
          <div style={{
            width: 38,
            height: 38,
            background: accentColor ? `${accentColor}18` : 'var(--primary-light)',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.1rem',
            flexShrink: 0,
          }} aria-hidden="true">
            {icon}
          </div>
        )}
        <p style={{
          fontSize: 'var(--text-xs)',
          color: 'var(--text-muted)',
          textTransform: 'uppercase',
          letterSpacing: '0.06em',
          fontWeight: 700,
          margin: 0
        }}>
          {label}
        </p>
      </div>

      <p style={{
        fontSize: '1.75rem',
        fontWeight: 800,
        color: 'var(--text-primary)',
        margin: 0,
        fontFamily: 'var(--font-display)',
        letterSpacing: '-0.02em',
      }}>
        {value ?? '—'}
      </p>

      {subtext && (
        <p style={{
          fontSize: 'var(--text-xs)',
          color: 'var(--text-subtle)',
          margin: 0,
          lineHeight: 'var(--leading-relaxed)',
        }}>
          {subtext}
        </p>
      )}

      {typeof progress === 'number' && (
        <ProgressBar value={progress} height={6} />
      )}
    </div>
  );
});

StatCard.displayName = 'StatCard';
export default StatCard;
