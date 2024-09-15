import React from 'react';
import FileUpload from '../components/FileUpload';

import './Dashboard.css';  // Import the CSS file

const Dashboard = () => {
  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Admin Dashboard</h1>
      </header>
      <div className="dashboard-content">
        <FileUpload />
        {/* <StudentTable /> */}
      </div>
    </div>
  );
};

export default Dashboard;
