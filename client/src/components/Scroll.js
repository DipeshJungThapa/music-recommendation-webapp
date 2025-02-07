import React from 'react';
import './Scroll.css';

const Scroll = ({ children }) => {
  return (
    <div className="scroll-container">
      {children}
    </div>
  );
};

export default Scroll;
