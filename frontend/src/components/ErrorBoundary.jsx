import React from 'react';
import Error500Page from '../pages/errors/Error500Page';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an uncaught rendering error:", error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      return <Error500Page error={this.state.error} resetErrorBoundary={this.handleRetry} />;
    }
    return this.props.children;
  }
}

export class LocalErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  componentDidCatch(error, errorInfo) {
    console.error("LocalErrorBoundary caught:", error, errorInfo);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          padding: '1.5rem',
          backgroundColor: 'rgba(239, 68, 68, 0.05)',
          border: '1px dashed rgba(239, 68, 68, 0.2)',
          borderRadius: '12px',
          color: '#fca5a5',
          fontSize: '0.85rem',
          textAlign: 'center',
          margin: '0.5rem 0'
        }}>
          ⚠️ Section failed to load. {this.props.fallbackText || 'Please reload.'}
        </div>
      );
    }
    return this.props.children;
  }
}
