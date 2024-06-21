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
    FOREIGN KEY (uid) REFERENCES users (uid) ON DELETE CASCADE
);

CREATE TABLE keystore
(
    aid                SERIAL,
    keyid              SERIAL,
    init_key           TEXT NOT NULL,
    initkey_validation BOOLEAN DEFAULT FALSE,
    pem_priv           TEXT,
    pem_pub            TEXT,
    agent_pem_pub      TEXT,
    PRIMARY KEY (aid, keyid)
);
