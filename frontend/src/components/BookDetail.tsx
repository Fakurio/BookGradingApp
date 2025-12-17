import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { getBook, addReview } from '../api';
import type { Book, ReviewCreate } from '../types';

export const BookDetail = () => {
    const { id } = useParams();
    const [book, setBook] = useState<Book | null>(null);
    const { register, handleSubmit, reset } = useForm<ReviewCreate>();

    const fetchBook = async () => {
        if (id) {
            const data = await getBook(id);
            setBook(data);
        }
    };

    useEffect(() => { fetchBook(); }, [id]);

    const onReviewSubmit = async (data: ReviewCreate) => {
        if (book) {
            await addReview(book.id, data);
            reset();
            fetchBook();
        }
    };

    if (!book) return <div>Loading...</div>;

    return (
        <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
            <h1>{book.title}</h1>
            <p><strong>By:</strong> {book.author} ({book.year_published})</p>
            <p>{book.description}</p>
            <hr />

            <h3>Reviews</h3>
            {book.reviews.length === 0 ? <p>No reviews yet.</p> : (
                <ul style={{ listStyle: 'none', padding: 0 }}>
                    {book.reviews.map((r) => (
                        <li key={r.id} style={{ background: '#f9f9f9', padding: '10px', marginBottom: '10px', borderRadius: '5px' }}>
                            <strong>Rating: {r.rating}/5</strong>
                            <p>{r.comment}</p>
                        </li>
                    ))}
                </ul>
            )}

            <div style={{ marginTop: '30px', borderTop: '2px solid #eee', paddingTop: '20px' }}>
                <h4>Add a Review</h4>
                <form onSubmit={handleSubmit(onReviewSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    <select {...register("rating", { required: true })} style={{ padding: '8px' }}>
                        <option value="5">5 - Excellent</option>
                        <option value="4">4 - Good</option>
                        <option value="3">3 - Average</option>
                        <option value="2">2 - Poor</option>
                        <option value="1">1 - Terrible</option>
                    </select>
                    <textarea
                        {...register("comment", { required: true, minLength: 5 })}
                        placeholder="Write your review here..."
                        style={{ padding: '8px', height: '80px' }}
                    />
                    <button type="submit" style={{ padding: '10px', background: '#007bff', color: '#fff', border: 'none', cursor: 'pointer' }}>
                        Submit Review
                    </button>
                </form>
            </div>
        </div>
    );
};