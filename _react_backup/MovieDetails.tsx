
import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Play, ArrowLeft, Star, Calendar, Clock } from 'lucide-react';
import Header from '../components/Header';
import OptimizedImage from '../components/OptimizedImage';
import { movieService } from '../services/movieService';

const MovieDetails = () => {
  const { id } = useParams<{ id: string }>();
  const movieId = parseInt(id || '0');

  const { data: movie, isLoading, error } = useQuery({
    queryKey: ['movie', movieId],
    queryFn: () => movieService.getMovieDetails(movieId),
    enabled: !!movieId,
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white">
        <Header />
        <div className="pt-20 container mx-auto px-4">
          <div className="animate-pulse">
            <div className="bg-gray-800 h-96 rounded-lg mb-8"></div>
            <div className="bg-gray-800 h-8 rounded mb-4 w-1/2"></div>
            <div className="bg-gray-800 h-4 rounded mb-2"></div>
            <div className="bg-gray-800 h-4 rounded mb-2 w-3/4"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !movie) {
    return (
      <div className="min-h-screen bg-gray-900 text-white">
        <Header />
        <div className="pt-20 container mx-auto px-4 text-center">
          <h1 className="text-2xl font-bold mb-4">Movie not found</h1>
          <Link to="/" className="text-red-600 hover:text-red-400">
            Return to Home
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Header />
      
      {/* Hero Section */}
      <div className="relative h-screen">
        <div className="absolute inset-0">
          <OptimizedImage
            src={movieService.getBackdropUrl(movie.backdrop_path)}
            alt={movie.title}
            className="w-full h-full object-cover"
            priority={true}
          />
          <div className="absolute inset-0 bg-gradient-to-r from-black/90 via-black/60 to-transparent" />
        </div>
        
        <div className="relative container mx-auto px-4 h-full flex items-center">
          <div className="flex flex-col md:flex-row items-start md:items-center gap-8 max-w-6xl">
            {/* Poster */}
            <div className="flex-shrink-0">
              <OptimizedImage
                src={movieService.getPosterUrl(movie.poster_path)}
                alt={movie.title}
                className="w-64 h-96 object-cover rounded-lg shadow-2xl"
              />
            </div>
            
            {/* Movie Info */}
            <div className="flex-1">
              <Link 
                to="/"
                className="inline-flex items-center text-gray-300 hover:text-white mb-4 transition-colors"
              >
                <ArrowLeft className="h-5 w-5 mr-2" />
                Back to Home
              </Link>
              
              <h1 className="text-4xl md:text-6xl font-bold mb-4">
                {movie.title}
              </h1>
              
              <div className="flex items-center space-x-6 mb-6">
                <div className="flex items-center space-x-2">
                  <Star className="h-5 w-5 text-yellow-400" />
                  <span className="text-lg font-semibold">{movie.vote_average.toFixed(1)}</span>
                </div>
                
                <div className="flex items-center space-x-2">
                  <Calendar className="h-5 w-5 text-gray-400" />
                  <span>{movie.release_date ? new Date(movie.release_date).getFullYear() : 'N/A'}</span>
                </div>
                
                {movie.runtime && (
                  <div className="flex items-center space-x-2">
                    <Clock className="h-5 w-5 text-gray-400" />
                    <span>{Math.floor(movie.runtime / 60)}h {movie.runtime % 60}m</span>
                  </div>
                )}
              </div>
              
              {movie.genres && (
                <div className="flex flex-wrap gap-2 mb-6">
                  {movie.genres.map(genre => (
                    <span 
                      key={genre.id}
                      className="bg-red-600/20 text-red-400 px-3 py-1 rounded-full text-sm"
                    >
                      {genre.name}
                    </span>
                  ))}
                </div>
              )}
              
              <p className="text-lg text-gray-300 mb-8 leading-relaxed max-w-3xl">
                {movie.overview}
              </p>
              
              <div className="flex space-x-4">
                <Link 
                  to={`/player/${movie.id}`}
                  className="bg-red-600 hover:bg-red-700 px-8 py-3 rounded-md font-semibold transition-all transform hover:scale-105 flex items-center space-x-2"
                >
                  <Play className="h-5 w-5" />
                  <span>Watch Now</span>
                </Link>
                
                <button className="bg-gray-800/80 hover:bg-gray-700 px-8 py-3 rounded-md font-semibold transition-colors border border-gray-600">
                  Add to Watchlist
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MovieDetails;
