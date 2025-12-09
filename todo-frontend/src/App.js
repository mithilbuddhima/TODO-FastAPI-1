import React, { useState } from 'react';
import Register from './Register';
import Login from './Login';
import TodoList from './TodoList';
import CreateTodo from './CreateTodo';

const App = () => {
  const [token, setToken] = useState(localStorage.getItem('token') || '');

  return (
    <div>
      {!token ? (
        <div>
          <Register />
          <Login setToken={setToken} />
        </div>
      ) : (
        <div>
          <TodoList token={token} />
          <CreateTodo token={token} />
        </div>
      )}
    </div>
  );
};

export default App;