-- Create the table 'users' if it doesn't already exist
CREATE TABLE IF NOT EXISTS users (
    -- 'id' column: an integer that auto-increments and is the primary key of the table
    id INT NOT NULL AUTO_INCREMENT,
    
    -- 'email' column: a string with a maximum length of 255 characters, cannot be null, and must be unique
    email VARCHAR(255) NOT NULL,
    
    -- 'name' column: a string with a maximum length of 255 characters, can be null
    name VARCHAR(255),
    
    -- Define 'id' as the primary key
    PRIMARY KEY (id),
    
    -- Ensure that 'email' is unique across all rows
    UNIQUE (email)
) ENGINE=InnoDB;
