CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE migrations (
    uuid uuid DEFAULT uuid_generate_v4(),
    name varchar(150) NOT NULL,
    created_at timestamp NOT NULL DEFAULT NOW(),
    PRIMARY KEY (uuid)
);

CREATE TABLE groups (
    uuid uuid DEFAULT uuid_generate_v4(),
    name varchar(100) NOT NULL,
    created_at timestamp DEFAULT NOW()
);

CREATE TABLE users (
    uuid uuid DEFAULT uuid_generate_v4(),
    name varchar(255) NOT NULL,
    cpf varchar(11) NOT NULL,
    email varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    salt varchar(255) NOT NULL,
    created_at timestamp DEFAULT NOW(),
    updated_at timestamp,
    deleted_at timestamp,
    PRIMARY KEY (uuid)
);

INSERT INTO migrations (name)
VALUES ('groups'), ('users');
