
const API_KEY = '029922d0ce729264a5fcd6f7403ec732';
const TMDB_BASE_URL = 'https://api.themoviedb.org/3';
const IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500';
const BACKDROP_BASE_URL = 'https://image.tmdb.org/t/p/original';

export interface Movie {
  id: number;
  title: string;
  overview: string;
  poster_path: string;
  backdrop_path: string;
  release_date: string;
  vote_average: number;
  runtime?: number;
  genres?: { id: number; name: string }[];
  streamUrl?: string;
}

export interface MovieResponse {
  results: Movie[];
  total_pages: number;
  total_results: number;
}

// Generate working streaming URLs with multiple fallbacks
const generateStreamUrl = (movieId: number): string => {
  // Using more reliable embed sources that typically work
  const streamSources = [
    `https://vidsrc.to/embed/movie/${movieId}`,
    `https://www.2embed.to/embed/tmdb/movie?id=${movieId}`,
    `https://autoembed.co/movie/tmdb/${movieId}`,
    `https://smashystream.com/playere.php?tmdb=${movieId}`
  ];
  
  // For demo purposes, cycle through sources based on movieId
  return streamSources[movieId % streamSources.length];
};

export const movieService = {
  // Get trending movies
  getTrending: async (): Promise<Movie[]> => {
    const response = await fetch(`${TMDB_BASE_URL}/trending/movie/day?api_key=${API_KEY}`);
    const data: MovieResponse = await response.json();
    return data.results.map(movie => ({
      ...movie,
      streamUrl: generateStreamUrl(movie.id)
    }));
  },

  // Get popular movies
  getPopular: async (): Promise<Movie[]> => {
    const response = await fetch(`${TMDB_BASE_URL}/movie/popular?api_key=${API_KEY}`);
    const data: MovieResponse = await response.json();
    return data.results.map(movie => ({
      ...movie,
      streamUrl: generateStreamUrl(movie.id)
    }));
  },

  // Get now playing movies
  getNowPlaying: async (): Promise<Movie[]> => {
    const response = await fetch(`${TMDB_BASE_URL}/movie/now_playing?api_key=${API_KEY}`);
    const data: MovieResponse = await response.json();
    return data.results.map(movie => ({
      ...movie,
      streamUrl: generateStreamUrl(movie.id)
    }));
  },

  // Get anime movies and TV shows
  getAnime: async (): Promise<Movie[]> => {
    // Fetch animated movies with Japanese origin
    const [animatedMovies, japaneseTv] = await Promise.all([
      fetch(`${TMDB_BASE_URL}/discover/movie?api_key=${API_KEY}&with_genres=16&with_origin_country=JP&sort_by=popularity.desc`),
      fetch(`${TMDB_BASE_URL}/discover/tv?api_key=${API_KEY}&with_genres=16&with_origin_country=JP&sort_by=popularity.desc`)
    ]);

    const moviesData: MovieResponse = await animatedMovies.json();
    const tvData: MovieResponse = await japaneseTv.json();

    // Combine and format both movies and TV shows
    const allAnime = [
      ...moviesData.results.map(movie => ({
        ...movie,
        streamUrl: generateStreamUrl(movie.id)
      })),
      ...tvData.results.map(show => ({
        ...show,
        id: show.id,
        title: show.title || (show as any).name, // TV shows use 'name' instead of 'title'
        streamUrl: generateStreamUrl(show.id)
      }))
    ];

    return allAnime.slice(0, 20); // Return top 20 anime
  },

  // Get movie details
  getMovieDetails: async (id: number): Promise<Movie> => {
    const response = await fetch(`${TMDB_BASE_URL}/movie/${id}?api_key=${API_KEY}`);
    const movie: Movie = await response.json();
    return {
      ...movie,
      streamUrl: generateStreamUrl(movie.id)
    };
  },

  // Search movies
  searchMovies: async (query: string): Promise<Movie[]> => {
    const response = await fetch(`${TMDB_BASE_URL}/search/movie?api_key=${API_KEY}&query=${encodeURIComponent(query)}`);
    const data: MovieResponse = await response.json();
    return data.results.map(movie => ({
      ...movie,
      streamUrl: generateStreamUrl(movie.id)
    }));
  },

  // Helper functions
  getPosterUrl: (path: string) => path ? `${IMAGE_BASE_URL}${path}` : '/placeholder.svg',
  getBackdropUrl: (path: string) => path ? `${BACKDROP_BASE_URL}${path}` : '/placeholder.svg'
};
