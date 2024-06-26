
CREATE TABLE OTP (
    ID SERIAL PRIMARY KEY,
    UID INTEGER REFERENCES USERS(UID) ON DELETE CASCADE,
    OTP VARCHAR(6),
    CREATION_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    EXPIRY_DATE TIMESTAMP NOT NULL
);

CREATE TABLE TOKEN(
    ID SERIAL PRIMARY KEY,
    UID INTEGER REFERENCES USERS(UID) ON DELETE CASCADE,
    TOKEN VARCHAR(255) NOT NULL,
    CREATION_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

CREATE TABLE MEDIA (
    ID SERIAL PRIMARY KEY,
    UID INTEGER REFERENCES USERS(UID) ON DELETE CASCADE,
    MID INTEGER NOT NULL,
    MEDIA_NAME TEXT NOT NULL,
    MEDIA_URL TEXT NOT NULL,
    CREATION_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);