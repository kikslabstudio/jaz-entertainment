
import { Movie } from '../services/movieService';

// This file now serves as backup/sample data
// The main data comes from TMDB API via movieService

export const sampleMovieData: {
  featured: Movie;
  trending: Movie[];
  bollywood: Movie[];
  hollywood: Movie[];
  anime: Movie[];
} = {
  featured: {
    id: 550,
    title: "Avatar: The Way of Water",
    overview: "Set more than a decade after the events of the first film, Avatar: The Way of Water begins to tell the story of the Sully family, the trouble that follows them, and the lengths they go to keep each other safe.",
    poster_path: "/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg",
    backdrop_path: "/s16H6tpK2utvwDtzZ8Qy4qm5Emw.jpg",
    release_date: "2022-12-14",
    vote_average: 8.2,
    runtime: 192,
    streamUrl: "https://vidsrc.to/embed/movie/550"
  },
  trending: [],
  bollywood: [],
  hollywood: [],
  anime: []
};

// Export the legacy movieData for backward compatibility
export const movieData = sampleMovieData;
