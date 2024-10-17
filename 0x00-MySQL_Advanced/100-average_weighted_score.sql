DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN input_user_id INT)
BEGIN
    DECLARE total_weight INT DEFAULT 0;
    DECLARE weighted_score FLOAT DEFAULT 0;
    
    -- Calculate the total weighted score and total weight
    SELECT SUM(c.score * p.weight) INTO weighted_score
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = input_user_id;

    SELECT SUM(p.weight) INTO total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = input_user_id;

    -- Calculate average weighted score
    IF total_weight > 0 THEN
        SET weighted_score = weighted_score / total_weight;
    ELSE
        SET weighted_score = 0; -- Avoid division by zero
    END IF;

    -- Update the user's average score
    UPDATE users
    SET average_score = weighted_score
    WHERE id = input_user_id;
END //

DELIMITER ;
