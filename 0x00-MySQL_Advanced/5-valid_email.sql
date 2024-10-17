-- Create the trigger that resets valid_email when email changes
DELIMITER //

CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- Check if the email has changed
    IF NEW.email <> OLD.email THEN
        -- Reset valid_email to 0 when the email is modified
        SET NEW.valid_email = 0;
    END IF;
END;
//

DELIMITER ;
