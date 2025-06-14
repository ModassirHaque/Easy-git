import React from 'react';
import { AppProvider } from './contexts/AppContext';
import AppLayout from './components/layout/AppLayout';
import Dashboard from './components/pages/Dashboard';
import './App.css';
import './index.css';

function App() {
  return (
    <AppProvider>
      <AppLayout>
        <Dashboard />
      </AppLayout>
    </AppProvider>
  );
}

export default App;
