import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate, useParams } from 'react-router-dom';
import { createBook, getBook, updateBook } from '../api';
import type { BookCreate } from '../types';
import { GenreEnum } from '../types';

export const BookForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const isEditMode = !!id;

    const { register, handleSubmit, setValue, formState: { errors } } = useForm<BookCreate>();

    useEffect(() => {
        if (isEditMode) {
            getBook(id!).then((book) => {
                setValue('title', book.title);
                setValue('author', book.author);
                setValue('description', book.description);
                setValue('year_published', book.year_published);
                setValue('pages', book.pages);
                setValue('genres', book.genres.map(g => g.name));
            });
        }
    }, [id, isEditMode, setValue]);

    const onSubmit = async (data: BookCreate) => {
        try {
            if (isEditMode) {
                await updateBook(Number(id), data);
            } else {
                await createBook(data);
            }
            navigate('/');
        } catch (error) {
            console.error("Error saving book", error);
            alert("Failed to save book. Check console for details.");
        }
    };

    return (
        <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
            <h2>{isEditMode ? 'Edit Book' : 'Add New Book'}</h2>
            <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>

                <div>
                    <label>Title</label>
                    <input {...register("title", { required: true, maxLength: 150 })} style={styles.input} />
                    {errors.title && <span style={styles.error}>Title is required (max 150)</span>}
                </div>

                <div>
                    <label>Author</label>
                    <input {...register("author", { required: true, maxLength: 100 })} style={styles.input} />
                    {errors.author && <span style={styles.error}>Author is required (max 100)</span>}
                </div>

                <div>
                    <label>Description</label>
                    <textarea {...register("description", { required: true, minLength: 10 })} style={{ ...styles.input, height: '100px' }} />
                    {errors.description && <span style={styles.error}>Min length 10 chars</span>}
                </div>

                <div style={{ display: 'flex', gap: '20px' }}>
                    <div style={{ flex: 1 }}>
                        <label>Year</label>
                        <input type="number" {...register("year_published", { required: true, min: 1800, max: new Date().getFullYear() })} style={styles.input} />
                        {errors.year_published && <span style={styles.error}>{`Year should be in range 1800 - ${new Date().getFullYear()}`}</span>}
                    </div>
                    <div style={{ flex: 1 }}>
                        <label>Pages</label>
                        <input type="number" {...register("pages", { required: true, min: 1 })} style={styles.input} />
                        {errors.pages && <span style={styles.error}>Pages need to be greater than 1</span>}
                    </div>
                </div>

                <div>
                    <label>Genres (Select multiple)</label>
                    <select multiple {...register("genres")} style={{ ...styles.input, height: '150px' }}>
                        {Object.values(GenreEnum).map((genre) => (
                            <option key={genre} value={genre}>{genre}</option>
                        ))}
                    </select>
                    <small>Hold Ctrl (Cmd) to select multiple</small>
                </div>

                <button type="submit" style={styles.btnSave}>{isEditMode ? 'Update' : 'Create'}</button>
            </form>
        </div>
    );
};

const styles = {
    input: { width: '100%', padding: '8px', marginTop: '5px', borderRadius: '4px', border: '1px solid #ccc' },
    error: { color: 'red', fontSize: '12px' },
    btnSave: { background: '#28a745', color: '#fff', padding: '10px', border: 'none', borderRadius: '5px', cursor: 'pointer', fontSize: '16px' }
};