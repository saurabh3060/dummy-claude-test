import React, { useState } from 'react';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(`Username: ${username}, Password: ${password}`);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor='username'>Username:</label>
      <input type='text' id='username' value={username} onChange={(event) => setUsername(event.target.value)} />
      <br />
      <label htmlFor='password'>Password:</label>
      <input type='password' id='password' value={password} onChange={(event) => setPassword(event.target.value)} />
      <br />
      <button type='submit'>Login</button>
    </form>
  );
}

export default Login;