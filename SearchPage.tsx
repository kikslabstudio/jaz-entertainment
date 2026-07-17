
import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Search } from 'lucide-react';
import Header from '../components/Header';
import MovieGrid from '../components/MovieGrid';
import { movieService } from '../services/movieService';

const SearchPage = () => {
  const [searchParams] = useSearchParams();
  const [query, setQuery] = useState(searchParams.get('q') || '');
  const [debouncedQuery, setDebouncedQuery] = useState(query);

  // Debounce search query
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query);
    }, 500);

    return () => clearTimeout(timer);
  }, [query]);

  const { data: movies = [], isLoading } = useQuery({
    queryKey: ['search', debouncedQuery],
    queryFn: () => movieService.searchMovies(debouncedQuery),
    enabled: debouncedQuery.length > 0,
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Header />
      
      <div className="pt-24 container mx-auto px-4">
        {/* Search Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-6">Search Movies</h1>
          
          <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-6 w-6 text-gray-400" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search for movies..."
                className="w-full bg-gray-800 text-white pl-12 pr-4 py-4 rounded-full text-lg focus:outline-none focus:ring-2 focus:ring-red-600"
                autoFocus
              />
            </div>
          </form>
        </div>

        {/* Search Results */}
        {debouncedQuery.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold mb-6">
              {isLoading ? 'Searching...' : `Results for "${debouncedQuery}"`}
            </h2>
            
            {!isLoading && movies.length === 0 && (
              <div className="text-center py-12">
                <p className="text-xl text-gray-400 mb-4">No movies found</p>
                <p className="text-gray-500">Try searching with different keywords</p>
              </div>
            )}
            
            <MovieGrid 
              title="" 
              movies={movies}
              isLoading={isLoading}
            />
          </div>
        )}

        {/* Default state */}
        {debouncedQuery.length === 0 && (
          <div className="text-center py-12">
            <Search className="h-24 w-24 text-gray-600 mx-auto mb-4" />
            <p className="text-xl text-gray-400 mb-2">Start typing to search</p>
            <p className="text-gray-500">Find your favorite movies and discover new ones</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchPage;
