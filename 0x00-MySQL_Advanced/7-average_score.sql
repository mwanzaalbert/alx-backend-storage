-- Create the ComputeAverageScoreForUser stored procedure
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN input_user_id INT)
BEGIN
    DECLARE avg_score FLOAT;

    -- Calculate the average score from the corrections table for the given user_id
    SELECT AVG(score) INTO avg_score 
    FROM corrections 
    WHERE user_id = input_user_id;

    -- Update the user's average_score in the users table
    UPDATE users 
    SET average_score = avg_score 
    WHERE id = input_user_id;
END;
//

DELIMITER ;
