CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE migrations (
    uuid uuid DEFAULT uuid_generate_v4(),
    name varchar(150) NOT NULL,
    created_at timestamp NOT NULL DEFAULT NOW(),
    PRIMARY KEY (uuid)
);

DO
    $do$
        BEGIN
            IF (SELECT COUNT(*) <= 0 FROM migrations WHERE name = 'groups')
                THEN
                    CREATE TABLE groups (
                        uuid uuid DEFAULT uuid_generate_v4() UNIQUE,
                        name varchar(100) NOT NULL,
                        created_at timestamp DEFAULT NOW()
                    );

                    INSERT INTO migrations (name)
                    VALUES ('groups');
            END IF;
        END;
    $do$;



DO
    $do$
        BEGIN
            IF (SELECT COUNT(*) <= 0 FROM migrations WHERE name = 'users')
                THEN
                    CREATE TABLE users (
                        uuid uuid DEFAULT uuid_generate_v4() UNIQUE,
                        name varchar(255) NOT NULL,
                        cpf varchar(11) NOT NULL UNIQUE,
                        email varchar(255) NOT NULL UNIQUE,
                        password varchar(255) NOT NULL,
                        active boolean DEFAULT true,
                        group_uuid uuid,
                        created_at timestamp DEFAULT NOW(),
                        updated_at timestamp,
                        deleted_at timestamp,
                        PRIMARY KEY (uuid),
                        CONSTRAINT fk_user_groups
                            FOREIGN KEY (group_uuid)
                                REFERENCES groups(uuid)
                    );

                    INSERT INTO migrations (name)
                    VALUES ('users');
            END IF;
        END;
    $do$;
