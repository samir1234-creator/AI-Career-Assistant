import { memo } from "react";

/**
 * Button – shared primary button component
 * Variants: primary | secondary | ghost | danger | success
 * Sizes:    sm | md | lg
 */
const Button = memo(({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  onClick,
  type = 'button',
  className = '',
  style = {},
  icon = null,
  ...props
}) => {
  const classes = [
    'btn',
    `btn-${variant}`,
    `btn-${size}`,
    className
  ].filter(Boolean).join(' ');

  return (
    <button
      type={type}
      className={classes}
      onClick={onClick}
      disabled={disabled || loading}
      aria-disabled={disabled || loading}
      style={style}
      {...props}
    >
      {loading ? (
        <>
          <span
            className="spinner-sm"
            role="status"
            aria-label="Loading"
          />
          <span>Loading...</span>
        </>
      ) : (
        <>
          {icon && <span aria-hidden="true">{icon}</span>}
          {children}
        </>
      )}
    </button>
  );
});

Button.displayName = 'Button';
export default Button;
