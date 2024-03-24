Generate JWT
Endpoint: POST /auth
Query Parameters:
expired: Optional. Set to true to generate an expired JWT.
Response: JSON object containing the JWT under both jwt and token keys.
Retrieve JWKS
Endpoint: GET /.well-known/jwks.json
Response: JSON Web Key Set (JWKS) containing the public keys used to sign JWTs.
