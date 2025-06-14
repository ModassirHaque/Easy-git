import React, { createContext, useContext, useState } from 'react';

// Application State Context
const AppContext = createContext();

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};

export const AppProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [currentRepository, setCurrentRepository] = useState(null);
  const [repositories, setRepositories] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [operations, setOperations] = useState({
    isLoading: false,
    currentOperation: null,
    progress: 0,
    errors: []
  });

  const value = {
    user,
    setUser,
    currentRepository,
    setCurrentRepository,
    repositories,
    setRepositories,
    isLoading,
    setIsLoading,
    error,
    setError,
    operations,
    setOperations
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

