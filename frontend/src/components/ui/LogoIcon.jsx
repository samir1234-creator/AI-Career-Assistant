import React from 'react';
import logoIconImg from '../../assets/logo_icon.png';

/**
 * LogoIcon - renders the brand-new Ilmora stylized circuit logo.
 */
export const LogoIcon = ({ size = 32, style = {}, className = '' }) => {
  return (
    <img 
      src={logoIconImg} 
      alt="Ilmora Logo Icon" 
      width={size} 
      height={size} 
      style={{ display: 'block', flexShrink: 0, objectFit: 'contain', ...style }}
      className={className}
    />
  );
};

export default LogoIcon;
