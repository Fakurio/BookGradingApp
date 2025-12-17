// @ts-ignore
export enum GenreEnum {
    FICTION = "Fiction",
    SCI_FI = "Science Fiction",
    FANTASY = "Fantasy",
    MYSTERY = "Mystery",
    BIOGRAPHY = "Biography",
    HISTORY = "History",
    ROMANCE = "Romance",
}

export interface Review {
    id: number;
    rating: number;
    comment: string;
}

export interface Genre {
    name: GenreEnum;
}

export interface Book {
    id: number;
    title: string;
    author: string;
    description: string;
    year_published: number;
    pages: number;
    genres: Genre[];
    reviews: Review[];
}

export interface BookCreate {
    title: string;
    author: string;
    description: string;
    year_published: number;
    pages: number;
    genres: GenreEnum[];
}

export interface BookUpdate extends Partial<BookCreate> {}

export interface ReviewCreate {
    rating: number;
    comment: string;
}

export interface AppStats {
    total_books: number;
    total_reviews: number;
}