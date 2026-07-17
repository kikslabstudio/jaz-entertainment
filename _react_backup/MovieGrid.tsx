
import React from 'react';
import MovieCard from './MovieCard';
import { Movie } from '../services/movieService';

interface MovieGridProps {
  title: string;
  movies: Movie[];
  isLoading?: boolean;
  priority?: boolean;
}

const MovieGrid: React.FC<MovieGridProps> = ({ title, movies, isLoading = false, priority = false }) => {
  if (isLoading) {
    return (
      <section className="mb-12">
        <h2 className="text-2xl md:text-3xl font-bold mb-6 text-white">
          {title}
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 md:gap-6">
          {Array.from({ length: 6 }).map((_, index) => (
            <div key={index} className="animate-pulse">
              <div className="bg-gray-800 h-64 md:h-80 rounded-lg mb-2"></div>
              <div className="bg-gray-800 h-4 rounded mb-1"></div>
              <div className="bg-gray-800 h-3 rounded w-3/4"></div>
            </div>
          ))}
        </div>
      </section>
    );
  }

  return (
    <section className="mb-12">
      <h2 className="text-2xl md:text-3xl font-bold mb-6 text-white">
        {title}
      </h2>
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 md:gap-6">
        {movies.map((movie, index) => (
          <MovieCard 
            key={movie.id} 
            movie={movie} 
            priority={priority && index < 6}
          />
        ))}
      </div>
    </section>
  );
};

export default MovieGrid;
