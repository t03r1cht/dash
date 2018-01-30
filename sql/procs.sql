-- Stored Proc: dash_board_db.check_for_user_existence()

DELIMITER $$

CREATE PROCEDURE dash_board_db.check_for_user_existence(
  IN p_email VARCHAR(250)
)
READS SQL DATA
  BEGIN
    SELECT
      username,
      email,
      password,
      uid,
      role_id
    FROM dash_board_db.dash_users
    WHERE email = p_email;
  END$$


-- Stored Proc: dash_board_db.add_new_user()

DELIMITER $$

CREATE PROCEDURE dash_board_db.add_new_user(
  IN p_username      VARCHAR(100),
  IN p_email         VARCHAR(250),
  IN p_password      VARCHAR(150),
  IN p_creation_date DATETIME,
  IN p_role_id       INT(11),
  IN p_profile_data  VARCHAR(5000)
)
MODIFIES SQL DATA
  BEGIN
    INSERT INTO dash_board_db.dash_users (username, email, password, creation_date, role_id, profile_data)
    VALUES (p_username, p_email, p_password, p_creation_date, p_role_id, p_profile_data);
  END$$

-- Stored Proc: dash_board_db.get_section_list()

DELIMITER $$

CREATE PROCEDURE dash_board_db.get_section_list()
READS SQL DATA
  BEGIN
    SELECT
      section_id,
      section_name
    FROM dash_board_db.dash_forum_sections;
  END$$

-- Stored Proc: dash_board_db.get_subsections_for_section_id()

DELIMITER $$

CREATE PROCEDURE dash_board_db.get_subsections_for_section_id(
  IN p_section_id INT(11)
)
READS SQL DATA
  BEGIN
    SELECT
      subsection_id,
      subsection_name,
      subsection_desc
    FROM dash_board_db.dash_forum_subsections
    WHERE section_id = p_section_id;
  END$$