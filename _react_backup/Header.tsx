
import React, { useState } from 'react';
import { Film, Search, ChevronDown } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from './ui/dropdown-menu';

const Header = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
      setSearchQuery('');
    }
  };

  const categories = [
    { name: 'Action', id: 28 },
    { name: 'Comedy', id: 35 },
    { name: 'Drama', id: 18 },
    { name: 'Horror', id: 27 },
    { name: 'Romance', id: 10749 },
    { name: 'Sci-Fi', id: 878 },
    { name: 'Thriller', id: 53 },
    { name: 'Adventure', id: 12 },
    { name: 'Animation', id: 16 },
    { name: 'Crime', id: 80 }
  ];

  const handleCategorySelect = (categoryName: string) => {
    navigate(`/search?genre=${encodeURIComponent(categoryName.toLowerCase())}`);
  };

  return (
    <header className="bg-black/80 backdrop-blur-md fixed top-0 w-full z-50 border-b border-gray-800">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-2">
          <Film className="h-8 w-8 text-red-600" />
          <h1 className="text-2xl font-bold bg-gradient-to-r from-red-600 to-orange-500 bg-clip-text text-transparent">
            KIKSLAB STUDIO
          </h1>
        </Link>
        
        <nav className="hidden md:flex items-center space-x-6">
          <Link to="/" className="hover:text-red-400 transition-colors">Home</Link>
          <Link to="/search" className="hover:text-red-400 transition-colors">Movies</Link>
          <Link to="/anime" className="hover:text-red-400 transition-colors">Anime</Link>
          <DropdownMenu>
            <DropdownMenuTrigger className="flex items-center space-x-1 hover:text-red-400 transition-colors">
              <span>Category</span>
              <ChevronDown className="h-4 w-4" />
            </DropdownMenuTrigger>
            <DropdownMenuContent className="bg-gray-800 border-gray-700 z-50">
              {categories.map((category) => (
                <DropdownMenuItem 
                  key={category.id}
                  className="text-white hover:bg-gray-700 focus:bg-gray-700 cursor-pointer"
                  onClick={() => handleCategorySelect(category.name)}
                >
                  {category.name}
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>
        </nav>
        
        <div className="flex items-center space-x-4">
          <form onSubmit={handleSearch} className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search movies..."
              className="bg-gray-800 text-white pl-10 pr-4 py-2 rounded-full w-64 focus:outline-none focus:ring-2 focus:ring-red-600"
            />
          </form>
        </div>
      </div>
    </header>
  );
};

export default Header;
