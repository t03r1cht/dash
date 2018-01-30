SELECT
  tralala_posts.post_id,
  tralala_users.email,
  tralala_posts.post_date,
  tralala_posts.post_text,
  tralala_posts.hashtags,
  tralala_posts.upvotes,
  tralala_posts.downvotes
FROM tralala_posts
  INNER JOIN tralala_users ON tralala_posts.uid = tralala_users.uid
WHERE post_id = p_pid;