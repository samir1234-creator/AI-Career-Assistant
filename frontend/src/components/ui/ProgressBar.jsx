import { memo, useCallback } from "react";

/**
 * ProgressBar
 * Animated width transition on mount with color coding by value.
 * 
 * @param {number} value  - 0 to 100
 * @param {string} color  - override color (optional)
 * @param {number} height - bar height in px (default 8)
 * @param {boolean} showLabel - show percentage text
 * @param {boolean} animate  - animate on mount (default true)
 */
const ProgressBar = memo(({
  value = 0,
  color,
  height = 8,
  showLabel = false,
  animate = true,
  className = '',
  style = {},
}) => {
  const clamped = Math.max(0, Math.min(100, value));

  const getColor = useCallback((v) => {
    if (color) return color;
    if (v >= 70) return 'linear-gradient(90deg, #10b981, #059669)';
    if (v >= 40) return 'linear-gradient(90deg, #f59e0b, #d97706)';
    return 'linear-gradient(90deg, #ef4444, #dc2626)';
  }, [color]);

  return (
    <div className={className} style={{ width: '100%', ...style }}>
      {showLabel && (
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          marginBottom: '0.4rem',
          fontSize: 'var(--text-xs)',
          color: 'var(--text-muted)',
          fontWeight: 600
        }}>
          <span />
          <span>{clamped}%</span>
        </div>
      )}
      <div
        className="progress-track"
        style={{ height }}
        role="progressbar"
        aria-valuenow={clamped}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div
          className="progress-fill"
          style={{
            width: animate ? `${clamped}%` : `${clamped}%`,
            background: getColor(clamped),
            height: '100%',
          }}
        />
      </div>
    </div>
  );
});

ProgressBar.displayName = 'ProgressBar';
export default ProgressBar;
