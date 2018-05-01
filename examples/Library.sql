-- Library SQL for use with BreezeBlocks example.

CREATE TABLE Author (
    id INTEGER PRIMARY KEY,
    name VARCHAR(40)
);

CREATE TABLE Genre (
    id INTEGER PRIMARY KEY,
    name VARCHAR(20) UNIQUE
);

CREATE TABLE Book (
    id INTEGER PRIMARY KEY,
    title VARCHAR(60) NOT NULL,
    author_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES Author (id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES Genre (id) ON UPDATE CASCADE ON DELETE SET NULL
);

INSERT INTO Author (name) VALUES
 ('J.R.R. Tolkein'),
 ('J.K. Rowling'),
 ('George Orwell')
;

INSERT INTO Genre (name) VALUES
 ('Science Fiction'),
 ('Fantasy')
;

INSERT INTO Book (author_id, genre_id, title) VALUES
 (1, 2, 'The Lord of the Rings: The Fellowship of the Ring'),
 (1, 2, 'The Lord of the Rings: The Two Towers'),
 (1, 2, 'The Lord of the Rings: The Return of the King'),
 (2, 2, 'Harry Potter and the Philosopher''s Stone'),
 (2, 2, 'Harry Potter and the Chamber of Secrets'),
 (2, 2, 'Harry Potter and the Prisoner of Azkaban'),
 (2, 2, 'Harry Potter and the Goblet of Fire'),
 (2, 2, 'Harry Potter and the Order of the Phoenix'),
 (2, 2, 'Harry Potter and the Half-Blood Prince'),
 (3, 1, 'Animal Farm')
;
