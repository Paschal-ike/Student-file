import React, { useState } from 'react';
import axios from '../utils/axiosInstance';
import { toast } from 'react-toastify';
import './Register.css';  // Import the CSS file

const AdminRegister = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleRegister = async () => {
    if (password !== confirmPassword) {
      toast.error("Passwords don't match!");
      return;
    }

    try {
      const response = await axios.post('/admin/register/', {
        username,
        email,
        password,
      });
      toast.success('Registration successful! You can now log in.');
    } catch (error) {
      toast.error('Registration failed!');
    }
  };

  return (
    <div className="register-container">
      <h2>Admin Register</h2>
      <div className="register-form">
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
        <button onClick={handleRegister}>Register</button>
      </div>
    </div>
  );
};

export default AdminRegister;
