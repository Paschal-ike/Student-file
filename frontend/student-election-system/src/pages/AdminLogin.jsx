import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';  // Import useNavigate
import axios from '../utils/axiosInstance';
import { toast } from 'react-toastify';
import './Login.css';  

const AdminLogin = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();  // Initialize the navigate hook

  const handleLogin = async () => {
    try {
      // Log credentials before sending request
      // console.log('Attempting login with credentials:', { username, password });
      
      // Make the API call
      const response = await axios.post('/admin/login/', { username, password });
      
      // Log the entire response
      // console.log('Login response:', response);

      // Extract and log the access token
      const { access } = response.data;
      // console.log('Access token received:', access);

      if (access) {
        // Remove old token if it exists
        localStorage.removeItem('token');
        // console.log('Old token removed from localStorage');

        // Store the new token
        localStorage.setItem('token', access);
        // console.log('New token stored in localStorage:', access);

        toast.success('Login successful!');
        navigate('/dashboard');
      } else {
        toast.error('Login failed! No access token returned.');
        console.log('Login failed: No access token in response.');
      }
    } catch (error) {
      // Log the error details for debugging
      console.error('Error during login:', error);
      if (error.response) {
        console.error('Error response data:', error.response.data);
        console.error('Error status:', error.response.status);
        console.error('Error headers:', error.response.headers);
      }

      if (error.response && error.response.status === 401) {
        toast.error('Unauthorized! Check your credentials.');
      } else {
        toast.error('Login failed due to an error.');
      }
    }
  };
  
  return (
    <div className="login-container">
      <div className="login-form">
        <h2>Admin Login</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleLogin}>Login</button>
      </div>
    </div>
  );
};

export default AdminLogin;
