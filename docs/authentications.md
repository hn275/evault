# OAuth Flow with GitHub

## Web

- User is redirected to `/api/auth?device_type=web`.
- Server responds with 302 status code and a `Location` header containing the URL of the GitHub OAuth url.
- GitHub provider redirects user back to `/auth/github` (front-end), where a `GET` request is issued to `/api/auth/token` with the required parameters.
- Server sets a cookie with the session ID, mapping to the OAuth token granted to the user by GitHub in Redis.
- Server sends a CSRF token as plaintext in the response body. Client stores this token **in memory**.
  - These tokens are ephemeral and session-bound, does not required persistent storage.
  - The current implementation stores the token within the defined `axios` instance.

