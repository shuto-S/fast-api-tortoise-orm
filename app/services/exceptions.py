from fastapi import HTTPException, status


HTTP_400_BAD_REQUEST = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bad request"
)

HTTP_401_UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid Authenticate",
    headers={"WWW-Authenticate": "Bearer"},
)

HTTP_404_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found"
)
