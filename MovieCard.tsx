
import React from 'react';
import { Play } from 'lucide-react';
import { Link } from 'react-router-dom';
import OptimizedImage from './OptimizedImage';
import { Movie, movieService } from '../services/movieService';

interface MovieCardProps {
  movie: Movie;
  priority?: boolean;
}

const MovieCard: React.FC<MovieCardProps> = ({ movie, priority = false }) => {
  return (
    <div className="group cursor-pointer transform transition-all duration-300 hover:scale-105 hover:z-10">
      <Link to={`/movie/${movie.id}`}>
        <div className="relative overflow-hidden rounded-lg bg-gray-800 shadow-lg">
          <OptimizedImage
            src={movieService.getPosterUrl(movie.poster_path)}
            alt={movie.title}
            className="w-full h-64 md:h-80 object-cover transition-transform duration-300 group-hover:scale-110"
            priority={priority}
          />
          
          {/* Overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-4">
            <div className="transform translate-y-2 group-hover:translate-y-0 transition-transform duration-300">
              <h3 className="font-semibold text-white mb-1 line-clamp-2">
                {movie.title}
              </h3>
              <div className="flex items-center justify-between mb-2">
                <span className="text-yellow-400 text-sm">★ {movie.vote_average.toFixed(1)}</span>
                <span className="text-gray-300 text-sm">
                  {movie.release_date ? new Date(movie.release_date).getFullYear() : 'N/A'}
                </span>
              </div>
            </div>
          </div>
          
          {/* Play button */}
          <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <Link 
              to={`/player/${movie.id}`}
              className="bg-red-600/90 hover:bg-red-700 text-white p-3 rounded-full transform scale-0 group-hover:scale-100 transition-transform duration-300 shadow-lg"
              onClick={(e) => e.stopPropagation()}
            >
              <Play className="h-6 w-6" />
            </Link>
          </div>
          
          {/* Rating badge */}
          <div className="absolute top-2 right-2 bg-black/70 text-yellow-400 px-2 py-1 rounded text-xs font-semibold">
            ★ {movie.vote_average.toFixed(1)}
          </div>
        </div>
      </Link>
    </div>
  );
};

export default MovieCard;
