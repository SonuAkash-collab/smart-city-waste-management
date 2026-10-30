"""Application settings read from environment variables.

Copy ``backend/.env.example`` to ``.env`` or set these in the shell.
"""

import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-secret-change-me")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))  # SCW-SEC-002
BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", "12"))
