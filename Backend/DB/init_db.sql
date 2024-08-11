CREATE TYPE CAPACITY_ENUM AS
   ENUM ('process', 'store', 'dual');
 
   -- Create the corporations table
   CREATE TABLE CORPORATIONS ( CID SERIAL PRIMARY KEY, CNAME VARCHAR(255) UNIQUE NOT NULL);
 
   -- Create the users table
   CREATE TABLE USERS ( UID SERIAL PRIMARY KEY, UNAME VARCHAR(255) UNIQUE NOT NULL, UEMAIL VARCHAR(255) UNIQUE NOT NULL, CID INTEGER NOT NULL REFERENCES CORPORATIONS(CID) ON DELETE CASCADE, IS_ADMIN BOOLEAN DEFAULT FALSE );
 
   -- Create the tokenCorporation table
   CREATE TABLE TOKENCORPORATION (TID SERIAL PRIMARY KEY, TOKEN VARCHAR(255) NOT NULL, EMAIL VARCHAR(255) NOT NULL);
 
   -- Create the keystore table
   CREATE TABLE KEYSTORE ( AID SERIAL PRIMARY KEY, KEYID SERIAL UNIQUE, INIT_KEY TEXT NOT NULL, INITKEY_VALIDATION BOOLEAN DEFAULT FALSE, PEM_PRIV TEXT, PEM_PUB TEXT, AGENT_PEM_PUB TEXT );
 
   -- Create the auth table
   CREATE TABLE AUTH ( ID SERIAL PRIMARY KEY, UID INTEGER NOT NULL, HASH VARCHAR(255) NOT NULL, SALT VARCHAR(255) NOT NULL, FOREIGN KEY (UID) REFERENCES USERS (UID) ON DELETE CASCADE );
 
   -- Create the otp table
   CREATE TABLE OTP ( ID SERIAL PRIMARY KEY, UID INTEGER NOT NULL, OTP VARCHAR(6), CREATION_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP, EXPIRY_DATE TIMESTAMP NOT NULL, FOREIGN KEY (UID) REFERENCES USERS (UID) ON DELETE CASCADE );
 
   -- Create the tokens table
   CREATE TABLE TOKENS ( ID SERIAL PRIMARY KEY, UID INTEGER NOT NULL, TOKEN VARCHAR(40) UNIQUE NOT NULL, CREATION_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (UID) REFERENCES USERS (UID) ON DELETE CASCADE );
 
   -- Create the agentstore table
   CREATE TABLE AGENTSTORE ( AID INTEGER, KEYID INTEGER, AIP VARCHAR(50), APORT INTEGER, VERIFIED BOOLEAN DEFAULT FALSE, LAST_CALL DATE, CAPACITY CAPACITY_ENUM, STORAGE FLOAT, IDENTIFIER VARCHAR(250), PRIMARY KEY (AID), FOREIGN KEY (AID) REFERENCES KEYSTORE (AID) ON DELETE CASCADE, FOREIGN KEY (KEYID) REFERENCES KEYSTORE (KEYID) );
 
   -- Create the media table
   CREATE TABLE MEDIA ( ID SERIAL PRIMARY KEY, UID INTEGER NOT NULL, MID VARCHAR(255) UNIQUE NOT NULL, MEDIA_NAME VARCHAR(255) NOT NULL, MEDIA_URL VARCHAR(255) NOT NULL, CREATION_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP, AID INTEGER, FOREIGN KEY (AID) REFERENCES AGENTSTORE (AID) ON DELETE CASCADE, FOREIGN KEY (UID) REFERENCES USERS (UID) ON DELETE CASCADE );
 
   -- Create the trigger function
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
 
      -- Create the trigger
      CREATE TRIGGER AFTER_KEYSTORE_INSERT AFTER INSERT ON KEYSTORE FOR EACH ROW EXECUTE FUNCTION INSERT_INTO_AGENTSTORE(
      );