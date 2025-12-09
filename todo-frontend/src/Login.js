import React, { useState } from 'react';
import api from './api';

const Login = ({ setToken }) => {
  const [credentials, setCredentials] = useState({
    email: '',
    password: ''
  });

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/token', credentials);
      localStorage.setItem('token', response.data.access_token);  // Save token to localStorage
      setToken(response.data.access_token);  // Pass token to the parent component
    } catch (error) {
      console.error('Login error', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" name="email" value={credentials.email} onChange={handleChange} placeholder="Email" />
      <input type="password" name="password" value={credentials.password} onChange={handleChange} placeholder="Password" />
      <button type="submit">Login</button>
    </form>
  );
};

export default Login;