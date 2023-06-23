-- Drop tables if they exist
DROP TABLE IF EXISTS hrjobdescription;
DROP TABLE IF EXISTS faqs;
DROP TABLE IF EXISTS form;
DROP TABLE IF EXISTS application;
DROP TABLE IF EXISTS job;
DROP TABLE IF EXISTS users;

-- Create new tables
CREATE TABLE users (
  id INT AUTO_INCREMENT,
  username VARCHAR(255),
  email VARCHAR(255),
  hashed_password VARCHAR(255),
  company_name VARCHAR(255),
  role VARCHAR(255),
  PRIMARY KEY (id)
);

CREATE TABLE job (
  id INT AUTO_INCREMENT,
  jobname VARCHAR(255),
  description TEXT,
  active BOOLEAN,
  job_link VARCHAR(255),
  img_url VARCHAR(255),
  userid INT,
  PRIMARY KEY (id),
  FOREIGN KEY (userid) REFERENCES users(id)
);

CREATE TABLE application (
  id INT AUTO_INCREMENT,
  file MEDIUMBLOB,
  skills TEXT,
  similarity FLOAT,
  experience INT,
  jobid INT,
  PRIMARY KEY (id),
  FOREIGN KEY (jobid) REFERENCES job(id) ON DELETE CASCADE
);

CREATE TABLE form (
  id INT AUTO_INCREMENT,
  name VARCHAR(255),
  email VARCHAR(255),
  education TEXT,
  skills TEXT,
  address VARCHAR(255),
  phone_number VARCHAR(255),
  projects TEXT,
  experience TEXT,
  similarity FLOAT,
  jobid INT,
  PRIMARY KEY (id),
  FOREIGN KEY (jobid) REFERENCES job(id)
);

CREATE TABLE faqs (
  id INT AUTO_INCREMENT,
  question TEXT,
  answer TEXT,
  PRIMARY KEY (id)
);
