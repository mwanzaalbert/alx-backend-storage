-- Create the SafeDiv function
DELIMITER $$

CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS FLOAT
BEGIN
    -- Check if the second number is 0, return 0 if true
    IF b = 0 THEN
        RETURN 0;
    ELSE
        -- Otherwise, return the result of a / b
        RETURN a / b;
    END IF;
END$$

DELIMITER ;
