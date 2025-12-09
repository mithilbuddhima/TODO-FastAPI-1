import React, { useState } from 'react';
import api from './api';

const Register = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/register', formData);
      console.log('Registration successful', response);
    } catch (error) {
      console.error('Registration error', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" name="first_name" value={formData.first_name} onChange={handleChange} placeholder="First Name" />
      <input type="text" name="last_name" value={formData.last_name} onChange={handleChange} placeholder="Last Name" />
      <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder="Email" />
      <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="Password" />
      <button type="submit">Register</button>
    </form>
  );
};

export default Register;