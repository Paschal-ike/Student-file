// ProtectedRoute.jsx
import React from 'react';
import { Route, Navigate } from 'react-router-dom';

const ProtectedRoute = ({ component: Component, ...rest }) => {
  const token = localStorage.getItem('token');

  return (
    <Route
      {...rest}
      element={
        token ? (
          <Component />
        ) : (
          <Navigate to="/login" />
        )
      }
    />
  );
};

export default ProtectedRoute;
