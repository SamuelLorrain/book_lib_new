CREATE TABLE edition(
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE author(
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE genre(
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE subject(
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE filetype(
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE authorbook(
    author_id INTEGER,
    book_id INTEGER,
    PRIMARY KEY(author_id,book_id),
    FOREIGN KEY(author_id) REFERENCES author(rowid)
        ON DELETE CASCADE,
    FOREIGN KEY(book_id) REFERENCES book(rowid)
        ON DELETE CASCADE
);
CREATE TABLE genrebook(
    genre_id INTEGER,
    book_id INTEGER,
    PRIMARY KEY(genre_id,book_id),
    FOREIGN KEY(genre_id) REFERENCES genre(rowid)
        ON DELETE CASCADE,
    FOREIGN KEY(book_id) REFERENCES book(rowid)
        ON DELETE CASCADE
);
CREATE TABLE subjectbook(
    subject_id INTEGER,
    book_id INTEGER,
    PRIMARY KEY(subject_id,book_id),
    FOREIGN KEY(subject_id) REFERENCES subject(rowid)
        ON DELETE CASCADE,
    FOREIGN KEY(book_id) REFERENCES book(rowid)
        ON DELETE CASCADE
);
CREATE TABLE book(
name TEXT NOT NULL UNIQUE,
note INTEGER,
date DATE,
lu BOOLEAN,
commence BOOLEAN,
physic BOOLEAN,
resume BOOLEAN,
filetype_id INTEGER,
edition_id INTEGER,
complement BOOLEAN,
FOREIGN KEY(edition_id) REFERENCES edition(rowid) ON DELETE CASCADE,
FOREIGN KEY(filetype_id) REFERENCES filetype(rowid) ON DELETE CASCADE
);
