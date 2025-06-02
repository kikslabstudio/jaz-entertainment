
import React from 'react';
import { Play, Info } from 'lucide-react';
import { Link } from 'react-router-dom';
import OptimizedImage from './OptimizedImage';
import { movieService, Movie } from '../services/movieService';

interface HeroSectionProps {
  featuredMovie: Movie;
}

const HeroSection: React.FC<HeroSectionProps> = ({ featuredMovie }) => {
  return (
    <div className="relative h-screen flex items-center">
      <div className="absolute inset-0">
        <OptimizedImage
          src={movieService.getBackdropUrl(featuredMovie.backdrop_path)}
          alt={featuredMovie.title}
          className="w-full h-full object-cover"
          priority={true}
        />
        <div className="absolute inset-0 bg-gradient-to-r from-black/80 via-black/50 to-transparent" />
        <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-transparent to-transparent" />
      </div>
      
      <div className="relative container mx-auto px-4 z-10">
        <div className="max-w-2xl">
          <h1 className="text-5xl md:text-7xl font-bold mb-4 leading-tight">
            {featuredMovie.title}
          </h1>
          <div className="flex items-center space-x-4 mb-6">
            <span className="bg-yellow-500 text-black px-2 py-1 rounded text-sm font-semibold">
              ★ {featuredMovie.vote_average.toFixed(1)}
            </span>
            <span className="text-gray-300">
              {featuredMovie.release_date ? new Date(featuredMovie.release_date).getFullYear() : 'N/A'}
            </span>
            <span className="bg-red-600 px-2 py-1 rounded text-sm">HD</span>
          </div>
          <p className="text-lg text-gray-300 mb-8 leading-relaxed line-clamp-3">
            {featuredMovie.overview}
          </p>
          <div className="flex space-x-4">
            <Link 
              to={`/player/${featuredMovie.id}`}
              className="bg-red-600 hover:bg-red-700 px-8 py-3 rounded-md font-semibold transition-all transform hover:scale-105 flex items-center space-x-2"
            >
              <Play className="h-5 w-5" />
              <span>Watch Now</span>
            </Link>
            <Link 
              to={`/movie/${featuredMovie.id}`}
              className="bg-gray-800/80 hover:bg-gray-700 px-8 py-3 rounded-md font-semibold transition-colors border border-gray-600 flex items-center space-x-2"
            >
              <Info className="h-5 w-5" />
              <span>More Info</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;
