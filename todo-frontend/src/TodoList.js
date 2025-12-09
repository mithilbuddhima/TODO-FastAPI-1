import React, { useEffect, useState } from 'react';
import api from './api';

const TodoList = ({ token }) => {
  const [todos, setTodos] = useState([]);

  useEffect(() => {
    const fetchTodos = async () => {
      try {
        const response = await api.get('/todos/', {
          headers: {
            Authorization: `Bearer ${token}`  // Attach token for secure access
          }
        });
        setTodos(response.data);
      } catch (error) {
        console.error('Error fetching todos', error);
      }
    };
    fetchTodos();
  }, [token]);

  return (
    <div>
      <h3>Your ToDo List</h3>
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>{todo.title}</li>
        ))}
      </ul>
    </div>
  );
};

export default TodoList;