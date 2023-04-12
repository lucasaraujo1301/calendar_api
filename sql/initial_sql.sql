CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE migrations (
    uuid uuid PRIMARY KEY DEFAULT uuid_generate_v4() UNIQUE,
    name VARCHAR(150) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

DO
    $do$
        BEGIN
            IF (SELECT COUNT(*) <= 0 FROM migrations WHERE name = 'groups')
                THEN
                    CREATE TABLE groups (
                        uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4() UNIQUE,
                        name VARCHAR(100) NOT NULL,
                        created_at TIMESTAMP DEFAULT NOW()
                    );

                    INSERT INTO migrations (name)
                    VALUES ('groups');

                    INSERT INTO groups (name)
                    VALUES ('admin'), ('user');
            END IF;
        END;
    $do$;



DO
    $do$
        BEGIN
            IF (SELECT COUNT(*) <= 0 FROM migrations WHERE name = 'users')
                THEN
                    CREATE TABLE users (
                        uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4() UNIQUE,
                        name VARCHAR(255) NOT NULL,
                        cpf VARCHAR(11) NOT NULL UNIQUE,
                        email VARCHAR(255) NOT NULL UNIQUE,
                        password BYTEA NOT NULL,
                        active BOOLEAN DEFAULT TRUE,
                        group_uuid UUID,
                        created_at TIMESTAMP DEFAULT NOW(),
                        updated_at TIMESTAMP,
                        deleted_at TIMESTAMP,
                        CONSTRAINT fk_user_groups
                            FOREIGN KEY (group_uuid)
                                REFERENCES groups(uuid)
                    );

                    INSERT INTO migrations (name)
                    VALUES ('users');
            END IF;
        END;
    $do$;
