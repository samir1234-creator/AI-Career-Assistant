import { memo } from "react";

/**
 * Skeleton loading components
 * Usage:
 *   <Skeleton width="100%" height={20} />
 *   <SkeletonText lines={3} />
 *   <SkeletonCard />
 */

export const Skeleton = memo(({ width = '100%', height = 16, borderRadius, className = '', style = {} }) => (
  <div
    className={`skeleton ${className}`}
    aria-hidden="true"
    style={{
      width,
      height,
      borderRadius: borderRadius ?? undefined,
      flexShrink: 0,
      ...style
    }}
  />
));
Skeleton.displayName = 'Skeleton';

export const SkeletonText = memo(({ lines = 3, lastLineWidth = '70%' }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }} aria-hidden="true">
    {Array.from({ length: lines }).map((_, i) => (
      <Skeleton
        key={i}
        height={14}
        width={i === lines - 1 ? lastLineWidth : '100%'}
      />
    ))}
  </div>
));
SkeletonText.displayName = 'SkeletonText';

export const SkeletonCard = memo(({ height = 120 }) => (
  <div
    className="skeleton"
    aria-hidden="true"
    style={{
      width: '100%',
      height,
      borderRadius: 'var(--radius-lg)',
    }}
  />
));
SkeletonCard.displayName = 'SkeletonCard';

export const SkeletonStatGrid = memo(({ count = 4 }) => (
  <div
    style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: 'var(--space-4)'
    }}
    aria-label="Loading..."
    aria-busy="true"
  >
    {Array.from({ length: count }).map((_, i) => (
      <SkeletonCard key={i} height={110} />
    ))}
  </div>
));
SkeletonStatGrid.displayName = 'SkeletonStatGrid';

export default Skeleton;
