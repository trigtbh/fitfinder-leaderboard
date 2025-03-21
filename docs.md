### Endpoint Documentation

---

#### **Endpoint:** `/users/register`
- **Method:** POST  
- **Parameters:**  
  - `username` (string) — The desired username.  
  - `password` (string) — The user's password.  
  - `full_name` (string) — The user's full name.  
  - `email` (string) — The user's email address.  
  - `phone_number` (string) — The user's phone number.  
- **Description:**  
  Registers a new user if the provided username is available.  
- **Returns:**  
  - Success response if registration is successful.  
  - Error if the username is taken or any internal issue occurs.  

---

#### **Endpoint:** `/users/check_username`
- **Method:** POST  
- **Parameters:**  
  - `username` (string) — The username to check for availability.  
- **Description:**  
  Checks if a given username is available for registration.  
- **Returns:**  
  - JSON `{ "available": true }` if the username is available.  
  - JSON `{ "available": false }` if the username is taken.  
  - Error for any internal issue.  

---

#### **Endpoint:** `/users/follow`
- **Method:** GET  
- **Parameters:**  
  - `token` (string) — The user's authentication token.  
  - `other` (string) — The user ID of the person to follow.  
- **Description:**  
  Allows a user to follow another user.  
- **Returns:**  
  - Success response if the operation is successful.  
  - Error if the target user does not exist or any internal issue occurs.  

---

#### **Endpoint:** `/users/unfollow`
- **Method:** GET  
- **Parameters:**  
  - `token` (string) — The user's authentication token.  
  - `other` (string) — The user ID of the person to unfollow.  
- **Description:**  
  Allows a user to unfollow another user.  
- **Returns:**  
  - Success response if the operation is successful.  
  - Error if the target user does not exist or any internal issue occurs.  

---

#### **Endpoint:** `/users/upload_pfp`
- **Method:** GET  
- **Parameters:**  
  - `token` (string) — The user's authentication token.  
  - `image` (string) — Base64 encoded profile picture.  
- **Description:**  
  Uploads a profile picture for the authenticated user.  
- **Returns:**  
  - Success response if the profile picture is updated.  
  - Error for any internal issue.  

---

#### **Endpoint:** `/users/followers`
- **Method:** GET  
- **Parameters:**  
  - `token` (string) — The user's authentication token.  
- **Description:**  
  Retrieves a list of followers for the authenticated user.  
- **Returns:**  
  - JSON `{ "followers": [...] }` containing the list of follower IDs.  
  - Error for any internal issue.  

---

#### **Endpoint:** `/users/following`
- **Method:** GET  
- **Parameters:**  
  - `token` (string) — The user's authentication token.  
- **Description:**  
  Retrieves a list of users the authenticated user is following.  
- **Returns:**  
  - JSON `{ "following": [...] }` containing the list of followed user IDs.  
  - Error for any internal issue.  

---

#### **Endpoint:** `/users/get`
- **Method:** GET  
- **Parameters:**  
  - `token` (string) — The user's authentication token.  
  - `other` (string) — The user ID to retrieve.  
- **Description:**  
  Fetches the public profile data of a specified user.  
- **Returns:**  
  - JSON with `user_id`, `username`, `bio_text`, and `profile_pic_url`.  
  - Error if the target user does not exist or any internal issue occurs.  

---

#### **Endpoint:** `/tags/add`
- **Method:** GET  
- **Parameters:**  
  - `token` (string) — The user's authentication token.  
  - `tag_id` (string) — The tag ID to add (Base64 encoded).  
- **Description:**  
  Adds a specified tag to the user's profile if authorized.  
- **Returns:**  
  - Success response if the tag is added.  
  - Error if the tag is invalid, unauthorized, or a database issue occurs.  

---

#### **Endpoint:** `/tags/remove`
- **Method:** GET  
- **Parameters:**  
  - `token` (string) — The user's authentication token.  
  - `tag_id` (string) — The tag ID to remove (Base64 encoded).  
- **Description:**  
  Removes a specified tag from the user's profile if authorized.  
- **Returns:**  
  - Success response if the tag is removed.  
  - Error if the tag is not present, unauthorized, or a database issue occurs.  

---

#### **Endpoint:** `/tags/get`
- **Method:** GET  
- **Parameters:**  
  - `token` (string) — The user's authentication token.  
- **Description:**  
  Retrieves all allowed tag IDs associated with the user.  
- **Returns:**  
  - JSON containing a list of tag IDs.  
  - Error if the token is invalid or a database issue occurs.  

---

#### **Endpoint:** `/posts/upload`
- **Method:** POST  
- **Parameters:**  
  - `token` (string) — The user's authentication token.  
  - `image` (string) — Base64-encoded image data.  
  - `caption` (string) — The caption for the post.  
- **Description:**  
  Uploads a new post with an image and caption.  
- **Returns:**  
  - Success message if the post is uploaded successfully.  
  - Error if any required fields are missing or if the database query fails.  

---

#### **Endpoint:** `/posts/like`
- **Method:** POST  
- **Parameters:**  
  - `token` (string) — The user's authentication token.  
  - `post_id` (string) — The ID of the post to like.  
- **Description:**  
  Likes a post and updates the associated like count.  
- **Returns:**  
  - Success message if the like is registered successfully.  
  - Error if the post does not exist or any database operation fails.  

---

#### **Endpoint:** `/posts/unlike`
- **Method:** POST  
- **Parameters:**  
  - `token` (string) — The user's authentication token.  
  - `post_id` (string) — The ID of the post to unlike.  
- **Description:**  
  Removes a like from a post.  
- **Returns:**  
  - Success message if the like is removed successfully.  
  - Error if the post does not exist or if there is an issue with the database operation.  

---

#### **Endpoint:** `/posts/comment`
- **Method:** POST  
- **Parameters:**  
  - `token` (string) — The user's authentication token.  
  - `post_id` (string) — The ID of the post to comment on.  
  - `comment` (string) — The comment text.  
- **Description:**  
  Adds a comment to a post.  
- **Returns:**  
  - Success message if the comment is added successfully.  
  - Error if the post does not exist or the comment cannot be inserted.  

---

#### **Endpoint:** `/posts/next`
- **Method:** POST  
- **Parameters:**  
  - `token` (string) — The user's authentication token.  
- **Description:**  
  Retrieves the next post that the user has not yet seen.  
- **Returns:**  
  - Success message with the ID of the next unseen post.  
  - Error if no new posts are available or if any database operation fails.  

---

#### **Endpoint:** `/login`
- **Method:** POST  
- **Parameters:**  
  - `username` (string) — The username of the user attempting to log in.  
  - `password` (string) — The password of the user, hashed using SHA-256.  
  - `sys_uuid` (string) — The system UUID.  
- **Description:**  
  Authenticates a user by checking the provided credentials (username and password). Returns a token if valid, along with encrypted cache data for token reuse.
- **Returns:**  
  - JSON with a `token`, `cache`, `user_id`, and `username` if successful.  
  - Error message with status 403 if the credentials are invalid.  
  - Error message with status 500 if any internal issue occurs.

---

#### **Endpoint:** `/login/bypass`
- **Method:** POST  
- **Parameters:**  
  - `cache` (string) — Encrypted token data for bypassing login.  
  - `sys_uuid` (string) — The system UUID used to decrypt the cache.  
- **Description:**  
  Allows bypassing the standard login process by using a cached token. Verifies the token and returns the corresponding user details if valid.
- **Returns:**  
  - JSON with `token`, `user_id`, and `username` if successful.  
  - Error message with status 403 if the token is invalid.  
  - Error message with status 500 if any internal issue occurs.

---

#### **Endpoint:** `/leaderboard/update`
- **Method:** POST  
- **Parameters:**  
  - `id` (string) — The user ID to update the score for.  
  - `score` (integer) — The new score to assign.  
- **Description:**  
  Updates the score of a specified user in the leaderboard. This endpoint is restricted to requests from the local server (`127.0.0.1`).  
- **Returns:**  
  - `"OK"` if the update was successful.  
  - Error if the request is not from the allowed address.

---

#### **Endpoint:** `/leaderboard/score`
- **Method:** GET  
- **Parameters:**  
  - `id` (string) — The user ID to retrieve the score for.  
- **Description:**  
  Fetches the score of a specified user from the leaderboard.  
- **Returns:**  
  - The score of the user as a string.  
  - Error if the user does not exist.

---

#### **Endpoint:** `/leaderboard/adjacent`
- **Method:** POST  
- **Parameters:**  
  - `id` (string) — The user ID to retrieve adjacent leaderboard positions for.  
- **Description:**  
  Fetches the adjacent positions (before and after) for the specified user in the leaderboard.  
- **Returns:**  
  - The adjacent positions as a string.  
  - Error if the user does not exist or any internal issue occurs.

---

#### **Endpoint:** `/leaderboard/top_ten`
- **Method:** GET  
- **Parameters:** None  
- **Description:**  
  Retrieves the top 10 users in the leaderboard.  
- **Returns:**  
  - A string with the top 10 leaderboard positions.  
  - Error if there is an issue retrieving the data.

---

#### **Endpoint:** `/leaderboard/increment`
- **Method:** POST  
- **Parameters:**  
  - `id` (string) — The user ID to increment the score for.  
  - `increment` (integer) — The value by which to increment the user's score.  
- **Description:**  
  Increments the score of a specified user by a given value. This endpoint is restricted to requests from the local server (`127.0.0.1`).  
- **Returns:**  
  - `"OK"` if the increment was successful.  
  - Error if the request is not from the allowed address.

---

#### **Endpoint:** `/leaderboard/placement`
- **Method:** GET  
- **Parameters:**  
  - `id` (string) — The user ID to retrieve the placement for.  
- **Description:**  
  Fetches the current leaderboard placement of a specified user.  
- **Returns:**  
  - The placement of the user as a string.  
  - Error if the user does not exist.

---
