CREATE TABLE users
(
    uid    SERIAL PRIMARY KEY,
    uname  VARCHAR(255) UNIQUE NOT NULL,
    uemail VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE auth
(
    id   SERIAL PRIMARY KEY,
    uid  INTEGER      NOT NULL,
    hash VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    FOREIGN KEY (uid) REFERENCES users (uid) ON DELETE CASCADE
);

CREATE TABLE otp
(
    id            SERIAL PRIMARY KEY,
    uid           INTEGER   NOT NULL,
    otp           VARCHAR(6),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_date   TIMESTAMP NOT NULL,
    FOREIGN KEY (uid) REFERENCES users (uid) ON DELETE CASCADE
);

CREATE TABLE tokens
(
    id            SERIAL PRIMARY KEY,
    uid           INTEGER            NOT NULL,
    token         VARCHAR(40) UNIQUE NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uid) REFERENCES users (uid) ON DELETE CASCADE
);

CREATE TABLE media
(
    id            SERIAL PRIMARY KEY,
    uid           INTEGER             NOT NULL,
    media_id      VARCHAR(255) UNIQUE NOT NULL,
    media_name    VARCHAR(255)        NOT NULL,
    media_url     VARCHAR(255)        NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    aid           INTEGER,
    FOREIGN KEY (aid) REFERENCES agentstore (aid) ON DELETE CASCADE,
    FOREIGN KEY (uid) REFERENCES users (uid) ON DELETE CASCADE
);
CREATE TYPE capacity_enum AS ENUM ('process', 'store', 'dual');

CREATE TABLE keystore
(
    aid                SERIAL PRIMARY KEY,
    keyid              SERIAL UNIQUE,
    init_key           TEXT NOT NULL,
    initkey_validation BOOLEAN DEFAULT FALSE,
    pem_priv           TEXT,
    pem_pub            TEXT,
    agent_pem_pub      TEXT
);

-- Create the agentstore table
CREATE TABLE agentstore
(
    aid        INTEGER,
    keyid      INTEGER,
    aip        VARCHAR(50),
    aport      INTEGER,
    verified   BOOLEAN DEFAULT FALSE,
    last_call  DATE,
    capacity   capacity_enum,
    storage    FLOAT,
    identifier VARCHAR(250),
    PRIMARY KEY (aid),
    FOREIGN KEY (aid) REFERENCES keystore (aid) ON DELETE CASCADE,
    FOREIGN KEY (keyid) REFERENCES keystore (keyid)
);

-- Create the trigger function
CREATE
OR REPLACE FUNCTION insert_into_agentstore()
RETURNS TRIGGER AS $$
BEGIN
INSERT INTO agentstore (aid, keyid)
VALUES (NEW.aid, NEW.keyid);
RETURN NEW;
END;
$$
LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER after_keystore_insert
    AFTER INSERT
    ON keystore
    FOR EACH ROW
    EXECUTE FUNCTION insert_into_agentstore();