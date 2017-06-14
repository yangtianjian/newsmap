use news;
DROP PROCEDURE IF EXISTS rearrange_id;
DELIMITER //

CREATE PROCEDURE rearrange_id()
BEGIN
	DECLARE I INT DEFAULT 1;
    DECLARE L INT DEFAULT (SELECT COUNT(*) FROM news);
    DECLARE K INT;
    WHILE I <= L DO
		SELECT MIN(id - I) INTO K FROM news WHERE id - I >= 0;
        IF K > 0 THEN
			UPDATE news SET id = I WHERE id - I = K;
        END IF;
        SET I = I + 1;
    END WHILE;
END //

DELIMITER ;

CALL rearrange_id();

