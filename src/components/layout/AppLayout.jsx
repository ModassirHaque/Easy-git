import React from 'react';
// import Header from '@/components/layout/Header';
import Header from './Header';
// import Sidebar from '@/components/layout/Sidebar';
import Sidebar from './Sidebar';
// import StatusPanel from '@/components/layout/StatusPanel';
import StatusPanel from './StatusPanel';

const AppLayout = ({ children }) => {
  return (
    <div className="h-screen flex flex-col">
      <Header />
      <div className="flex-1 flex overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-auto">
          {children}
        </main>
        <StatusPanel />
      </div>
    </div>
  );
};

export default AppLayout;

