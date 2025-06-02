
import React, { useState } from 'react';

interface OptimizedImageProps {
  src: string;
  alt: string;
  className?: string;
  priority?: boolean;
}

const OptimizedImage: React.FC<OptimizedImageProps> = ({ 
  src, 
  alt, 
  className = '', 
  priority = false 
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [hasError, setHasError] = useState(false);

  // Create optimized URL for Netlify or fallback
  const optimizedSrc = src.startsWith('http') 
    ? `${src}?w=500&format=webp&quality=80`
    : src;

  // Generate blurhash-style placeholder
  const placeholderClass = "bg-gradient-to-br from-gray-700 to-gray-800";

  return (
    <div className={`relative overflow-hidden ${className}`}>
      {/* Placeholder */}
      {!isLoaded && !hasError && (
        <div className={`absolute inset-0 ${placeholderClass} animate-pulse`}>
          <div className="flex items-center justify-center h-full">
            <div className="w-12 h-12 border-2 border-gray-600 border-t-gray-400 rounded-full animate-spin"></div>
          </div>
        </div>
      )}
      
      {/* Error fallback */}
      {hasError && (
        <div className={`absolute inset-0 ${placeholderClass} flex items-center justify-center`}>
          <div className="text-gray-400 text-center p-4">
            <div className="text-2xl mb-2">🎬</div>
            <div className="text-sm">Image not available</div>
          </div>
        </div>
      )}
      
      {/* Actual image */}
      <img
        src={optimizedSrc}
        alt={alt}
        className={`${className} transition-opacity duration-300 ${
          isLoaded ? 'opacity-100' : 'opacity-0'
        }`}
        loading={priority ? 'eager' : 'lazy'}
        onLoad={() => setIsLoaded(true)}
        onError={() => setHasError(true)}
        style={{ 
          imageRendering: 'auto',
          backfaceVisibility: 'hidden',
          transform: 'translateZ(0)'
        }}
      />
    </div>
  );
};

export default OptimizedImage;
