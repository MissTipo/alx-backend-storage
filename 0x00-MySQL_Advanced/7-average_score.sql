-- reates a stored procedure that computes and store the average score for a student
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
  DECLARE avg_score FLOAT;
  SET avg_score = (SELECT AVG(score) FROM corrections AS c WHERE c.user_id = user_id);
UPDATE users SET avarage_score = avg_score WHERE id = user_id;
END
//
