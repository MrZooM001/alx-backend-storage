-- SQL script that creates a stored procedure AddBonus
-- that adds a new correction for a student.
DELIMITER //

CREATE PROCEDURE AddBonus(
    IN p_user_id INT,
    IN p_project_name VARCHAR(255),
    IN p_score INT
)
BEGIN
    DECLARE var_project_id INT;
    SELECT id INTO var_project_id
    FROM projects
    WHERE name = p_project_name;
    IF var_project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (p_project_name);
        SET var_project_id = LAST_INSERT_ID();
    END IF;
    INSERT INTO corrections (user_id, project_id, score) VALUES (p_user_id, var_project_id, p_score);
    UPDATE users
    SET average_score = (SELECT AVG(score) FROM corrections WHERE user_id = p_user_id)
    WHERE id = p_user_id;
END;

// DELIMITER ;
