DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weight INT DEFAULT 0;
    DECLARE weighted_score FLOAT DEFAULT 0;
    
    -- Calculate the total weighted score and total weight
    SELECT SUM(corrections.score * projects.weight) INTO weighted_score
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    SELECT SUM(projects.weight) INTO total_weight
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Calculate average weighted score
    IF total_weight > 0 THEN
        SET weighted_score = weighted_score / total_weight;
    ELSE
        SET weighted_score = 0; -- Avoid division by zero
    END IF;

    -- Update the user's average score
    UPDATE users
    SET average_score = weighted_score
    WHERE id = user_id;
END //

DELIMITER ;
