
import React from 'react';
import { useQuery } from '@tanstack/react-query';
import Header from '../components/Header';
import MovieGrid from '../components/MovieGrid';
import { movieService } from '../services/movieService';

const AnimePage = () => {
  const { data: animeList = [], isLoading } = useQuery({
    queryKey: ['anime'],
    queryFn: movieService.getAnime,
  });

  // Get featured anime (first one)
  const featuredAnime = animeList[0];

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Header />
      
      {/* Hero Section for Featured Anime */}
      {featuredAnime && (
        <div className="relative h-96 mt-16">
          <div className="absolute inset-0">
            <img
              src={movieService.getBackdropUrl(featuredAnime.backdrop_path)}
              alt={featuredAnime.title}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-r from-black/80 via-black/50 to-transparent" />
          </div>
          
          <div className="relative container mx-auto px-4 h-full flex items-center">
            <div className="max-w-2xl">
              <div className="bg-red-600/20 text-red-400 px-3 py-1 rounded-full text-sm font-semibold mb-4 inline-block">
                Featured Anime
              </div>
              <h1 className="text-4xl md:text-5xl font-bold mb-4">
                {featuredAnime.title}
              </h1>
              <div className="flex items-center space-x-4 mb-4">
                <span className="bg-yellow-500 text-black px-2 py-1 rounded text-sm font-semibold">
                  ★ {featuredAnime.vote_average.toFixed(1)}
                </span>
                <span className="text-gray-300">
                  {featuredAnime.release_date ? new Date(featuredAnime.release_date).getFullYear() : 'N/A'}
                </span>
              </div>
              <p className="text-lg text-gray-300 mb-6 leading-relaxed line-clamp-3">
                {featuredAnime.overview}
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="container mx-auto px-4 py-8 space-y-12">
        <MovieGrid 
          title="Popular Anime" 
          movies={animeList}
          isLoading={isLoading}
          priority={true}
        />
      </div>
    </div>
  );
};

export default AnimePage;
