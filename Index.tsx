
import React, { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import Header from '../components/Header';
import HeroSection from '../components/HeroSection';
import MovieGrid from '../components/MovieGrid';
import { movieService } from '../services/movieService';

const Index = () => {
  const [featuredMovieIndex, setFeaturedMovieIndex] = useState(0);

  const { data: trendingMovies = [], isLoading: trendingLoading } = useQuery({
    queryKey: ['trending'],
    queryFn: movieService.getTrending,
  });

  const { data: popularMovies = [], isLoading: popularLoading } = useQuery({
    queryKey: ['popular'],
    queryFn: movieService.getPopular,
  });

  const { data: nowPlayingMovies = [], isLoading: nowPlayingLoading } = useQuery({
    queryKey: ['nowPlaying'],
    queryFn: movieService.getNowPlaying,
  });

  // Shuffle featured movie every 5 seconds
  useEffect(() => {
    if (trendingMovies.length === 0) return;

    const interval = setInterval(() => {
      setFeaturedMovieIndex(prev => {
        const nextIndex = (prev + 1) % trendingMovies.length;
        return nextIndex;
      });
    }, 5000); // 5 seconds

    return () => clearInterval(interval);
  }, [trendingMovies]);

  const featuredMovie = trendingMovies[featuredMovieIndex];

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Header />
      {featuredMovie && <HeroSection featuredMovie={featuredMovie} />}
      <div className="container mx-auto px-4 py-8 space-y-12">
        <MovieGrid 
          title="Trending Now" 
          movies={trendingMovies}
          isLoading={trendingLoading}
          priority={true}
        />
        <MovieGrid 
          title="Popular Movies" 
          movies={popularMovies}
          isLoading={popularLoading}
        />
        <MovieGrid 
          title="Now Playing" 
          movies={nowPlayingMovies}
          isLoading={nowPlayingLoading}
        />
      </div>
    </div>
  );
};

export default Index;
