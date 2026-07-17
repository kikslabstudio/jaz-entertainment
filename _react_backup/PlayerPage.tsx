
import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ArrowLeft, ExternalLink, RotateCcw } from 'lucide-react';
import { movieService } from '../services/movieService';

const PlayerPage = () => {
  const { id } = useParams<{ id: string }>();
  const movieId = parseInt(id || '0');
  const [currentSourceIndex, setCurrentSourceIndex] = useState(0);
  const [hasError, setHasError] = useState(false);

  const { data: movie, isLoading } = useQuery({
    queryKey: ['movie', movieId],
    queryFn: () => movieService.getMovieDetails(movieId),
    enabled: !!movieId,
  });

  // Multiple streaming sources for fallback
  const getStreamingSources = (movieId: number) => [
    `https://vidsrc.to/embed/movie/${movieId}`,
    `https://www.2embed.to/embed/tmdb/movie?id=${movieId}`,
    `https://autoembed.co/movie/tmdb/${movieId}`,
    `https://smashystream.com/playere.php?tmdb=${movieId}`
  ];

  const streamingSources = movie ? getStreamingSources(movie.id) : [];
  const currentStreamUrl = streamingSources[currentSourceIndex];

  // Try next streaming source
  const tryNextSource = () => {
    if (currentSourceIndex < streamingSources.length - 1) {
      setCurrentSourceIndex(prev => prev + 1);
      setHasError(false);
    }
  };

  // Reset to first source
  const resetSources = () => {
    setCurrentSourceIndex(0);
    setHasError(false);
  };

  // Disable right-click and keyboard shortcuts for better UX
  useEffect(() => {
    const handleContextMenu = (e: MouseEvent) => e.preventDefault();
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && e.key === 'I')) {
        e.preventDefault();
      }
    };

    document.addEventListener('contextmenu', handleContextMenu);
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('contextmenu', handleContextMenu);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  if (isLoading || !movie) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-white text-center">
          <div className="w-16 h-16 border-4 border-red-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p>Loading player...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-50 p-4 bg-gradient-to-b from-black/80 to-transparent">
        <div className="flex items-center justify-between">
          <Link 
            to={`/movie/${movie.id}`}
            className="flex items-center text-white hover:text-red-400 transition-colors"
          >
            <ArrowLeft className="h-5 w-5 mr-2" />
            Back to Details
          </Link>
          
          <div className="text-center">
            <h1 className="text-xl font-bold">{movie.title}</h1>
            <p className="text-sm text-gray-300">
              {movie.release_date ? new Date(movie.release_date).getFullYear() : 'N/A'} • 
              ★ {movie.vote_average.toFixed(1)}
            </p>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={tryNextSource}
              disabled={currentSourceIndex >= streamingSources.length - 1}
              className="px-3 py-1 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 rounded text-sm transition-colors"
            >
              Try Another Server
            </button>
            <button
              onClick={resetSources}
              className="p-2 bg-gray-600 hover:bg-gray-700 rounded transition-colors"
            >
              <RotateCcw className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Video Player */}
      <div className="w-full h-screen">
        {hasError ? (
          <div className="w-full h-full flex items-center justify-center bg-gray-900">
            <div className="text-center">
              <p className="text-xl mb-4">Failed to load video</p>
              <button
                onClick={tryNextSource}
                disabled={currentSourceIndex >= streamingSources.length - 1}
                className="px-6 py-3 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 rounded transition-colors mr-4"
              >
                Try Another Server
              </button>
              <button
                onClick={resetSources}
                className="px-6 py-3 bg-gray-600 hover:bg-gray-700 rounded transition-colors"
              >
                Reset Sources
              </button>
            </div>
          </div>
        ) : (
          <iframe
            key={currentSourceIndex} // Force re-render when source changes
            src={currentStreamUrl}
            className="w-full h-full"
            frameBorder="0"
            allowFullScreen
            allow="autoplay; encrypted-media; picture-in-picture"
            title={`Watch ${movie.title}`}
            onError={() => setHasError(true)}
          />
        )}
      </div>

      {/* Fallback message */}
      <div className="absolute bottom-4 left-4 right-4 text-center text-sm text-gray-400">
        <p className="mb-2">
          Server {currentSourceIndex + 1} of {streamingSources.length} • 
          Having trouble? Try opening in a new tab:
        </p>
        <a 
          href={currentStreamUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center text-red-400 hover:text-red-300 transition-colors"
        >
          <ExternalLink className="h-4 w-4 mr-1" />
          Open in New Tab
        </a>
      </div>
    </div>
  );
};

export default PlayerPage;
