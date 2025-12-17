import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getBooks, deleteBook } from '../api';
import type { Book } from '../types';

export const BookList = () => {
    const [books, setBooks] = useState<Book[]>([]);

    useEffect(() => {
        loadBooks();
    }, []);

    const loadBooks = async () => {
        try {
            const data = await getBooks();
            setBooks(data);
        } catch (error) {
            console.error("Failed to fetch books", error);
        }
    };

    const handleDelete = async (id: number) => {
        if (confirm('Are you sure you want to delete this book?')) {
            await deleteBook(id);
            loadBooks();
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <h2>Library Books</h2>
            <Link to="/add" style={styles.btnPrimary}>+ Add New Book</Link>

            <div style={styles.grid}>
                {books.map((book) => (
                    <div key={book.id} style={styles.card}>
                        <h3>{book.title}</h3>
                        <p><strong>Author:</strong> {book.author}</p>
                        <p><strong>Genres:</strong> {book.genres.map(g => g.name).join(', ')}</p>
                        <div style={styles.actions}>
                            <Link to={`/book/${book.id}`} style={styles.link}>View Details</Link>
                            <Link to={`/edit/${book.id}`} style={styles.link}>Edit</Link>
                            <button onClick={() => handleDelete(book.id)} style={styles.btnDelete}>Delete</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

const styles = {
    grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '20px', marginTop: '20px' },
    card: { border: '1px solid #ddd', padding: '15px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
    actions: { marginTop: '10px', display: 'flex', gap: '10px', alignItems: 'center' },
    btnPrimary: { background: '#007bff', color: '#fff', padding: '10px 15px', textDecoration: 'none', borderRadius: '5px' },
    btnDelete: { background: '#dc3545', color: '#fff', border: 'none', padding: '5px 10px', borderRadius: '5px', cursor: 'pointer' },
    link: { color: '#007bff', textDecoration: 'none' }
};