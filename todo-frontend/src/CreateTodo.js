import React, { useState } from 'react';
import api from './api';

const CreateTodo = ({ token }) => {
  const [todo, setTodo] = useState({
    title: '',
    description: '',
    completed: false
  });

  const handleChange = (e) => {
    setTodo({
      ...todo,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/todos/', todo, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
    } catch (error) {
      console.error('Error creating todo', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" name="title" value={todo.title} onChange={handleChange} placeholder="Title" />
      <textarea name="description" value={todo.description} onChange={handleChange} placeholder="Description"></textarea>
      <button type="submit">Create Todo</button>
    </form>
  );
};

export default CreateTodo;