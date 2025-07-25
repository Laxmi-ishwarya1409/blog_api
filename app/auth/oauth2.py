# The goal here is to extract the current user from the JWT token and make them available in routes.



from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.token import verify_access_token
from app.database import get_session
from app.crud import get_user_by_email
from app.schemas import UserRead

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
# Tells FastAPI to expect an Authorization header like:
# Authorization: Bearer <your_token>
# tokenUrl="/login" refers to your login endpoint where the token is originally issued. This is needed for API docs (Swagger UI) to show the login flow correctly


async def get_current_user(
        token : str = Depends(oauth2_scheme),  # This grabs the JWT token from the request header using the OAuth2 scheme.
        db : AsyncSession = Depends(get_session)  # This injects the database session, so we can query the user.
):
    email = verify_access_token(token)
    user = await get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    user_data = UserRead(
        id=user.id,
        name=user.name,
        email=user.email
    )
    return user_data