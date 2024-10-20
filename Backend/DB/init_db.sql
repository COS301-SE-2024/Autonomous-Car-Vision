CREATE TYPE CAPACITY_ENUM AS
   ENUM ('process', 'store', 'dual');
   
   CREATE TABLE CORPORATIONS ( CID SERIAL PRIMARY KEY, CNAME VARCHAR(255) UNIQUE NOT NULL);
   INSERT INTO CORPORATIONS (
      CNAME
   ) VALUES (
      'dev'
   );
 
   CREATE TABLE USERS ( UID SERIAL PRIMARY KEY, UNAME VARCHAR(255) UNIQUE NOT NULL, UEMAIL VARCHAR(255) UNIQUE NOT NULL, CID INTEGER NOT NULL REFERENCES CORPORATIONS(CID) ON DELETE CASCADE, IS_ADMIN BOOLEAN DEFAULT FALSE, LAST_SIGNIN TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
 
   CREATE TABLE TOKENCORPORATION (TID SERIAL PRIMARY KEY, TOKEN VARCHAR(255) NOT NULL, EMAIL VARCHAR(255) NOT NULL);
 
   CREATE TABLE KEYSTORE ( AID SERIAL PRIMARY KEY, KEYID SERIAL UNIQUE, INIT_KEY TEXT NOT NULL, INITKEY_VALIDATION BOOLEAN DEFAULT FALSE, PEM_PRIV TEXT, PEM_PUB TEXT, AGENT_PEM_PUB TEXT );
 
   CREATE TABLE AUTH ( ID SERIAL PRIMARY KEY, UID INTEGER NOT NULL, HASH VARCHAR(255) NOT NULL, SALT VARCHAR(255) NOT NULL, FOREIGN KEY (UID) REFERENCES USERS (UID) ON DELETE CASCADE );
 
   CREATE TABLE OTP ( ID SERIAL PRIMARY KEY, UID INTEGER NOT NULL, OTP VARCHAR(6), CREATION_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP, EXPIRY_DATE TIMESTAMP NOT NULL, FOREIGN KEY (UID) REFERENCES USERS (UID) ON DELETE CASCADE );
   
   CREATE TABLE TOKENS ( ID SERIAL PRIMARY KEY, UID INTEGER NOT NULL, TOKEN VARCHAR(40) UNIQUE NOT NULL, CREATION_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (UID) REFERENCES USERS (UID) ON DELETE CASCADE );
 
   CREATE TABLE AGENTSTORE ( AID INTEGER, KEYID INTEGER, AIP VARCHAR(50), APORT INTEGER, VERIFIED BOOLEAN DEFAULT FALSE, LAST_CALL DATE, CAPACITY CAPACITY_ENUM, STORAGE FLOAT, IDENTIFIER VARCHAR(250), PRIMARY KEY (AID), FOREIGN KEY (AID) REFERENCES KEYSTORE (AID) ON DELETE CASCADE, FOREIGN KEY (KEYID) REFERENCES KEYSTORE (KEYID), CORPORATION VARCHAR(255));
 
   CREATE TABLE MEDIA ( ID SERIAL PRIMARY KEY, UID INTEGER NOT NULL, MID VARCHAR(255) UNIQUE NOT NULL, MEDIA_NAME VARCHAR(255) NOT NULL, MEDIA_URL VARCHAR(255) NOT NULL, CREATION_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP, AID INTEGER, FOREIGN KEY (AID) REFERENCES AGENTSTORE (AID) ON DELETE CASCADE, FOREIGN KEY (UID) REFERENCES USERS (UID) ON DELETE CASCADE );
   
   CREATE OR REPLACE FUNCTION INSERT_INTO_AGENTSTORE() RETURNS TRIGGER AS
      $$
      BEGIN
         INSERT INTO AGENTSTORE (
            AID,
            KEYID
         ) VALUES (
            NEW.AID,
            NEW.KEYID
         );
         RETURN NEW;
      END;

      $$ LANGUAGE PLPGSQL;
 
   CREATE TRIGGER AFTER_KEYSTORE_INSERT AFTER INSERT ON KEYSTORE FOR EACH ROW EXECUTE FUNCTION INSERT_INTO_AGENTSTORE(
   );