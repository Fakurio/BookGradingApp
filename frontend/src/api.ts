import axios from 'axios';
import type {Book, BookCreate, BookUpdate, ReviewCreate} from './types';
const API_URL = import.meta.env.VITE_SERVER_HOST;

const api = axios.create({
    baseURL: API_URL,
});

export const getBooks = async () => {
    const response = await api.get<Book[]>('/books');
    return response.data;
};

export const getBook = async (id: string) => {
    const response = await api.get<Book>(`/books/${id}`);
    return response.data;
};

export const createBook = async (book: BookCreate) => {
    const response = await api.post<Book>('/books', book);
    return response.data;
};

export const updateBook = async (id: number, book: BookUpdate) => {
    const response = await api.put<Book>(`/books/${id}`, book);
    return response.data;
};

export const deleteBook = async (id: number) => {
    await api.delete(`/books/${id}`);
};

export const addReview = async (bookId: number, review: ReviewCreate) => {
    const response = await api.post(`/reviews/${bookId}`, review);
    return response.data;
};