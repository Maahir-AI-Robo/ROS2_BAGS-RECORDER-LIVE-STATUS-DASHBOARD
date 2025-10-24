import { useEffect, useState } from 'react';

function App() {
  const [status, setStatus] = useState('OK');
  useEffect(() => {
    setStatus('Ready');
  }, []);
  return (
    <div style={{ padding: 24, fontFamily: 'system-ui' }}>
      <h1>ROS2 Live Recording Status Dashboard</h1>
      <p>Status: {status}</p>
      <ul>
        <li>Sessions</li>
        <li>Metrics</li>
        <li>Alerts</li>
      </ul>
    </div>
  );
}

export default App;