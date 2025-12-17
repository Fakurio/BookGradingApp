import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { BookList } from './components/BookList';
import { BookForm } from './components/BookForm';
import { BookDetail } from './components/BookDetail';
import type { AppStats } from './types';

const WS_URL = import.meta.env.VITE_SERVER_HOST.replace(/^http/, 'ws') + '/ws';

function App() {
  const [stats, setStats] = useState<AppStats | null>(null);

  useEffect(() => {
    const ws = new WebSocket(WS_URL);

    ws.onopen = () => {
      console.log('Connected to WebSocket stats');
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setStats(data);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    return () => {
      if (ws.readyState === 1) {
        ws.close();
      }
    };
  }, []);

  return (
    <Router>
      <nav style={styles.nav}>
        <Link to="/" style={styles.logo}>📚 Book Grader</Link>
        {stats && (
          <div style={styles.stats}>
            <span>Books: <strong>{stats.total_books}</strong></span>
            <span>Reviews: <strong>{stats.total_reviews}</strong></span>
          </div>
        )}
      </nav>

      <Routes>
        <Route path="/" element={<BookList />} />
        <Route path="/add" element={<BookForm />} />
        <Route path="/edit/:id" element={<BookForm />} />
        <Route path="/book/:id" element={<BookDetail />} />
      </Routes>
    </Router>
  );
}

const styles = {
  nav: {
    background: '#333',
    padding: '15px 20px',
    marginBottom: '20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    color: '#fff'
  },
  logo: {
    color: '#fff',
    textDecoration: 'none',
    fontWeight: 'bold',
    fontSize: '1.2rem'
  },
  stats: {
    display: 'flex',
    gap: '20px',
    fontSize: '0.9rem',
    background: 'rgba(255,255,255,0.1)',
    padding: '5px 15px',
    borderRadius: '20px'
  }
};

export default App;