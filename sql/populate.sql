INSERT INTO dash_board_db.dash_roles (name, config_board) VALUES("board_administrator", 0);

INSERT INTO dash_board_db.dash_roles (name, config_board) VALUES("board_moderator", 1);

INSERT INTO dash_board_db.dash_roles (name, config_board) VALUES("board_member", 2);

INSERT INTO dash_board_db.dash_users (username, email, password, creation_date, role_id, profile_data) VALUES
  ("quazee", "marc.friedrich94@web.de",
   "pbkdf2:sha256:50000$oaQc7Jqq$c6e5ebc55bfc0b25bc4b7cc30c73ff9c2b21a53899b74378d24a6a66a450986d",
   "2017-12-05 12:34:11", 0, "{'name':'marc', 'value':'friedrich'}");

INSERT INTO dash_board_db.dash_users (username, email, password, creation_date, role_id, profile_data) VALUES
  ("hoaks", "warwickx@web.de",
   "pbkdf2:sha256:50000$oaQc7Jqq$c6e5ebc55bfc0b25bc4b7cc30c73ff9c2b21a53899b74378d24a6a66a450986d",
   "2017-12-05 12:34:11", 1, "{'name':'warwickx', 'value':'nachname'}");
