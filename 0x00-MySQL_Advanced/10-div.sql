-- t creates a function SafeDiv that divides (and returns) the first by the second number or returns 0 if the second number is equal to 0

DELIMITER //
CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS FLOAT DETERMINISTIC
BEGIN
	DECLARE result FLOAT;
	SET result = CASE WHEN b = 0 THEN 0 ELSE a / b END;
	RETURN result;
END;
//
DELIMITER ;
