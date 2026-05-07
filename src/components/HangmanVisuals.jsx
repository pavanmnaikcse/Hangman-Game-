import React from 'react';

const HangmanVisuals = ({ mistakes }) => {
    return (
        <svg width="200" height="250" viewBox="0 0 200 250" className="hangman-svg">
            <defs>
                <filter id="glow">
                    <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
            {/* Base structure (always visible) */}
            <line x1="20" y1="230" x2="180" y2="230" stroke="#4a4a4a" strokeWidth="8" />
            <line x1="50" y1="230" x2="50" y2="20" stroke="#4a4a4a" strokeWidth="8" />
            <line x1="46" y1="20" x2="140" y2="20" stroke="#4a4a4a" strokeWidth="8" />
            <line x1="140" y1="16" x2="140" y2="40" stroke="#6b4423" strokeWidth="4" />
            
            {/* Rope & Head (Mistake 1) */}
            {mistakes >= 1 && <line x1="140" y1="40" x2="140" y2="60" stroke="#c2b280" strokeWidth="3" />}
            {mistakes >= 1 && <circle cx="140" cy="80" r="20" stroke="#ff4444" strokeWidth="4" fill="none" filter="url(#glow)" />}
            
            {/* Body (Mistake 2) */}
            {mistakes >= 2 && <line x1="140" y1="100" x2="140" y2="160" stroke="#ff4444" strokeWidth="4" filter="url(#glow)" />}
            
            {/* Left Arm (Mistake 3) */}
            {mistakes >= 3 && <line x1="140" y1="120" x2="110" y2="150" stroke="#ff4444" strokeWidth="4" filter="url(#glow)" />}
            
            {/* Right Arm (Mistake 4) */}
            {mistakes >= 4 && <line x1="140" y1="120" x2="170" y2="150" stroke="#ff4444" strokeWidth="4" filter="url(#glow)" />}
            
            {/* Left Leg (Mistake 5) */}
            {mistakes >= 5 && <line x1="140" y1="160" x2="110" y2="200" stroke="#ff4444" strokeWidth="4" filter="url(#glow)" />}
            
            {/* Right Leg (Mistake 6) */}
            {mistakes >= 6 && <line x1="140" y1="160" x2="170" y2="200" stroke="#ff4444" strokeWidth="4" filter="url(#glow)" />}
        </svg>
    );
};
export default HangmanVisuals;
