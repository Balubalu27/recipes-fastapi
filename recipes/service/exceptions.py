from fastapi import HTTPException, status

credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

is_blocked_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Your account is blocked",
)

not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
)

has_not_permissions = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permissions denied",
)
