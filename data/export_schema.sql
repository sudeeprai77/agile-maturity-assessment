--
-- File generated with SQLiteStudio v3.4.21 on Fri Jan 30 22:44:24 2026
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: areas
CREATE TABLE IF NOT EXISTS areas (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    principle_id INTEGER NOT NULL,
    name         TEXT    NOT NULL,
    weight       INTEGER DEFAULT 0,
    FOREIGN KEY (
        principle_id
    )
    REFERENCES principles (id),
    UNIQUE (
        principle_id,
        name
    )
);


-- Table: assessments
CREATE TABLE IF NOT EXISTS assessments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT    NOT NULL,
    description     TEXT,
    project_id      INTEGER,
    assessed_by,
    assessment_date
);


-- Table: principles
CREATE TABLE IF NOT EXISTS principles (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name   TEXT    UNIQUE
                   NOT NULL,
    weight INTEGER NOT NULL
);


-- Table: projects
CREATE TABLE IF NOT EXISTS projects (
    id         INTEGER  PRIMARY KEY AUTOINCREMENT,
    name       TEXT     NOT NULL,
    created_by INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (
        created_by
    )
    REFERENCES users (id) 
);


-- Table: question_answers
CREATE TABLE IF NOT EXISTS question_answers (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id  INTEGER NOT NULL,
    answer_order INTEGER NOT NULL
                         CHECK (answer_order BETWEEN 1 AND 5),
    answer_text  TEXT    NOT NULL,
    FOREIGN KEY (
        question_id
    )
    REFERENCES questions (id),
    UNIQUE (
        question_id,
        answer_order
    )
);


-- Table: questions
CREATE TABLE IF NOT EXISTS questions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    question    TEXT    UNIQUE
                        NOT NULL,
    option_type TEXT    NOT NULL
                        DEFAULT 'CUSTOM_5'
);


-- Table: responses
CREATE TABLE IF NOT EXISTS responses (
    id            INTEGER   PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER,
    assessment_id INTEGER,
    score         INTEGER,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (
        user_id
    )
    REFERENCES users (id),
    FOREIGN KEY (
        assessment_id
    )
    REFERENCES assessments (id) 
);


-- Table: sessions
CREATE TABLE IF NOT EXISTS sessions (
    id         INTEGER   PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER   NOT NULL,
    token      TEXT      UNIQUE
                         NOT NULL,
    expiry     TEXT      NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (
        user_id
    )
    REFERENCES users (id) 
);


-- Table: users
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER   PRIMARY KEY AUTOINCREMENT,
    username      TEXT      UNIQUE
                            NOT NULL,
    password_hash TEXT      NOT NULL,
    role          TEXT      NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
