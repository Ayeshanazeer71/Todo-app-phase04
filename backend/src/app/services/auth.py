from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt
from sqlmodel import Session
from app.core.config import settings
import logging

# Configure logger for auth service
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def get_password_hash(password: str) -> str:
    logger.debug("Starting password hashing...")
    try:
        if not password:
            logger.error("Empty password provided for hashing")
            raise ValueError("Password cannot be empty")
        
        logger.debug(f"Generating salt for password of length: {len(password)}")
        salt = bcrypt.gensalt()
        logger.debug("Salt generated successfully")
        
        logger.debug("Hashing password with bcrypt...")
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        logger.debug("Password hashed successfully")
        
        result = hashed.decode('utf-8')
        logger.debug(f"Password hash decoded, result length: {len(result)}")
        return result
    except Exception as e:
        logger.error(f"Password hashing failed: {str(e)}")
        raise

def authenticate_user(db: Session, username: str, password: str):
    from app.models.user import User
    from sqlmodel import select
    user = db.exec(select(User).where(User.username == username)).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    logger.debug("Starting access token creation...")
    try:
        if not data:
            logger.error("Empty data provided for token creation")
            raise ValueError("Token data cannot be empty")
        
        logger.debug(f"Token data received: {list(data.keys())}")  # Log keys only, not values
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
            logger.debug(f"Using custom expiration delta: {expires_delta}")
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
            logger.debug("Using default 15-minute expiration")
        
        to_encode.update({"exp": expire})
        logger.debug(f"Token will expire at: {expire}")
        
        logger.debug("Encoding JWT token...")
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
        logger.debug(f"JWT token created successfully, length: {len(encoded_jwt)}")
        
        return encoded_jwt
    except Exception as e:
        logger.error(f"Token creation failed: {str(e)}")
        raise

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception
