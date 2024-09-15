// App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AdminLogin from './pages/AdminLogin';
import AdminRegister from './pages/AdminRegister';
import Dashboard from './pages/Dashboard';
import ToastNotification from './components/ToastNotification';
import UploadList from './pages/UploadList';
import ProtectedRoute from './components/ProtectedRoute';
import UploadsList from './pages/UploadList';

const App = () => {
  return (
    <Router>
      <ToastNotification />
      <Routes>
        {/* Redirect "/" to login or dashboard */}
        <Route path="/" element={<Navigate to="/login" />} />
        
        {/* Admin routes */}
        <Route path="/login" element={<AdminLogin />} />
        <Route path="/register" element={<AdminRegister />} />

        {/* Dashboard */}
        <Route
          path="/dashboard"
          element={<ProtectedRoute component={Dashboard} />}
        />
        <Route   
          path="/uploads"
          element={<ProtectedRoute component={UploadsList} />}
        />

        <Route path="/uploads" element={<UploadList />} />

        {/* Catch-all route for undefined paths */}
        <Route path="*" element={<h2>404 Not Found</h2>} />
      </Routes>
    </Router>
  );
};

export default App;
