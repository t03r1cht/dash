INSERT INTO dash_board_db.dash_roles (name, config_board) VALUES ("board_administrator", 0);

INSERT INTO dash_board_db.dash_roles (name, config_board) VALUES ("board_moderator", 1);

INSERT INTO dash_board_db.dash_roles (name, config_board) VALUES ("board_member", 2);

INSERT INTO dash_board_db.dash_users (username, email, password, creation_date, role_id, profile_data) VALUES
  ("quazee", "marc.friedrich94@web.de",
   "pbkdf2:sha256:50000$oaQc7Jqq$c6e5ebc55bfc0b25bc4b7cc30c73ff9c2b21a53899b74378d24a6a66a450986d",
   "2017-12-05 12:34:11", 0, "{'name':'marc', 'value':'friedrich'}");

INSERT INTO dash_board_db.dash_users (username, email, password, creation_date, role_id, profile_data) VALUES
  ("hoaks", "warwickx@web.de",
   "pbkdf2:sha256:50000$oaQc7Jqq$c6e5ebc55bfc0b25bc4b7cc30c73ff9c2b21a53899b74378d24a6a66a450986d",
   "2017-12-05 12:34:11", 1, "{'name':'warwickx', 'value':'nachname'}");

INSERT INTO dash_board_db.dash_forum_sections (section_name, section_creation_date)
VALUES ("General", "2017-12-05 12:34:11");

INSERT INTO dash_board_db.dash_forum_subsections (section_id, subsection_name, subsection_desc, subsection_creation_date)
VALUES (1, "Announcements", "Announcements about the forum and other important news", "2017-12-05 12:34:11");

INSERT INTO dash_board_db.dash_forum_subsections (section_id, subsection_name, subsection_desc, subsection_creation_date)
VALUES (1, "News", "Important news", "2017-12-05 12:34:11");

INSERT INTO dash_board_db.dash_forum_subsections (section_id, subsection_name, subsection_desc, subsection_creation_date)
VALUES (1, "Discussions", "General discussions", "2017-12-05 12:34:11");

INSERT INTO dash_board_db.dash_forum_threads (subsection_id, thread_title, thread_creator, thread_views, thread_replies, thread_status, thread_creation_date)
VALUES (1, "Welcome to Dash", 1, 222, 333, "open", "2017-12-05 12:34:11");

INSERT INTO dash_board_db.dash_forum_threads (subsection_id, thread_title, thread_creator, thread_views, thread_replies, thread_status, thread_creation_date)
VALUES (1, "Hello", 1, 222, 333, "open", "2017-12-05 12:34:11");

INSERT INTO dash_board_db.dash_forum_threads (subsection_id, thread_title, thread_creator, thread_views, thread_replies, thread_status, thread_creation_date)
VALUES (1, "This is my first thread", 1, 222, 333, "open", "2017-12-05 12:34:11");
