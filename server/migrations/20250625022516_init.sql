-- Add migration script here
CREATE TABLE users (
	id INTEGER PRIMARY KEY,
	login CHAR(40) NOT NULL UNIQUE, -- apparently max 39 chars username with GitHub
	name TEXT NOT NULL UNIQUE,
	email TEXT NOT NULL UNIQUE
);

CREATE TABLE repositories (
	id INTEGER PRIMARY KEY,
	name CHAR(100) NOT NULL UNIQUE,
	owner_id INTEGER NOT NULL,
	bucket_addr TEXT,
	password TEXT NOT NULL,
	 CONSTRAINT fk_repositories_user 
			FOREIGN KEY (owner_id) 
			REFERENCES users(id) 
			ON DELETE CASCADE 
);

CREATE TABLE versions (
	id INTEGER PRIMARY KEY,
	file_id TEXT NOT NULL,
	s3_id TEXT NOT NULL,
	version_number INTEGER NOT NULL DEFAULT 1,
	change_description TEXT DEFAULT NULL,
	repository_id INTEGER NOT NULL,
	created_by INTEGER NOT NULL,
	created_at TIMESTAMPTZ DEFAULT NOW(),
	checksum CHAR(64) NOT NULL,
	CONSTRAINT fk_versions_repositories
			FOREIGN KEY (repository_id) 
			REFERENCES repositories(id) 
			ON DELETE CASCADE,
	CONSTRAINT fk_versions_users
			FOREIGN KEY (created_by) 
			REFERENCES users(id) 
);
