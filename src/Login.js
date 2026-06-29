import React, { useState } from 'react';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [redirected, setRedirected] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!username || !password) return;
    // Simulate redirect to standard page
    console.log(`Redirecting user from login screen with username: ${username} and password: ${password}`);
    setRedirected(true);
  };

  const handleLoginClick = () => {
    if (!username || !password) return;
    // Actual redirection to dashboard page
    console.log(`User redirected to dashboard with username: ${username}, password: ${password}`);
    setRedirected(true);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Username:
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
      </label>
      <br />
      <label>
        Password:
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      </label>
      <br />
      <button onClick={handleLoginClick}>Login</button>
    </form>
    <button onClick={handleLogout}>Logout</button>
  );
}

export default LoginPage;
