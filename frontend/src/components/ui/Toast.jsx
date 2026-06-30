/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useState, useCallback, useRef, memo } from "react";

/* ── Context ──────────────────────────────────────────────── */
const ToastContext = createContext(null);

/* ── Hook ─────────────────────────────────────────────────── */
export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error('useToast must be used within <ToastProvider>');
  return ctx;
}

/* ── Individual Toast ─────────────────────────────────────── */
const ToastItem = memo(({ id, type = 'info', title, message, onClose }) => {
  const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };

  return (
    <div
      className={`toast toast-${type}`}
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      <span className="toast-icon" aria-hidden="true">{icons[type]}</span>
      <div className="toast-body">
        {title && <div className="toast-title">{title}</div>}
        {message && <div className="toast-message">{message}</div>}
      </div>
      <button
        className="toast-close"
        onClick={() => onClose(id)}
        aria-label="Dismiss notification"
      >
        ×
      </button>
    </div>
  );
});
ToastItem.displayName = 'ToastItem';

/* ── Provider ─────────────────────────────────────────────── */
export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);
  const counterRef = useRef(0);

  const dismiss = useCallback((id) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  }, []);

  const toast = useCallback((type, title, message, duration = 4000) => {
    const id = ++counterRef.current;
    setToasts(prev => [...prev, { id, type, title, message }]);
    if (duration > 0) {
      setTimeout(() => dismiss(id), duration);
    }
    return id;
  }, [dismiss]);

  const api = {
    success: (title, message, dur) => toast('success', title, message, dur),
    error:   (title, message, dur) => toast('error',   title, message, dur),
    warning: (title, message, dur) => toast('warning', title, message, dur),
    info:    (title, message, dur) => toast('info',    title, message, dur),
    dismiss,
  };

  return (
    <ToastContext.Provider value={api}>
      {children}
      <div className="toast-container" aria-label="Notifications">
        {toasts.map(t => (
          <ToastItem key={t.id} {...t} onClose={dismiss} />
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export default ToastProvider;
