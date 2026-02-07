from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.api.deps import get_db
from app.models.user import User, UserCreate, Token
from app.services.auth import authenticate_user, create_access_token, get_password_hash
from datetime import timedelta
from app.core.config import settings
import logging
import traceback

# Configure logger for authentication
logger = logging.getLogger(__name__)
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))

router = APIRouter()

router = APIRouter()

@router.post("/signup", response_model=Token)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    logger.info("=== SIGNUP REQUEST STARTED ===")
    
    try:
        # Log the incoming request data (sanitized)
        logger.info(f"Signup attempt for username: {user_in.username}")
        logger.info(f"UserCreate model received - username: {user_in.username}, password_length: {len(user_in.password) if user_in.password else 0}")
        
        # Step 1: Check for existing user
        logger.info("Step 1: Checking for existing user...")
        user = db.exec(select(User).where(User.username == user_in.username)).first()
        if user:
            logger.warning(f"Signup failed: Username '{user_in.username}' already exists")
            raise HTTPException(status_code=400, detail="Username already registered")
        logger.info("Step 1: No existing user found, proceeding...")

        # Step 2: Hash password
        logger.info("Step 2: Hashing password...")
        try:
            hashed_password = get_password_hash(user_in.password)
            logger.info("Step 2: Password hashed successfully")
        except Exception as e:
            logger.error(f"Step 2: Password hashing failed: {str(e)}")
            logger.error(f"Password hashing traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail="Password processing failed")

        # Step 3: Create user object
        logger.info("Step 3: Creating user object...")
        try:
            db_user = User(
                username=user_in.username,
                hashed_password=hashed_password
            )
            logger.info(f"Step 3: User object created for username: {db_user.username}")
        except Exception as e:
            logger.error(f"Step 3: User object creation failed: {str(e)}")
            logger.error(f"User creation traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail="User object creation failed")

        # Step 4: Save to database
        logger.info("Step 4: Saving user to database...")
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            logger.info(f"Step 4: User saved to database with ID: {db_user.id}")
        except Exception as e:
            logger.error(f"Step 4: Database save failed: {str(e)}")
            logger.error(f"Database save traceback: {traceback.format_exc()}")
            db.rollback()
            raise HTTPException(status_code=500, detail="Database save failed")

        # Step 5: Generate access token
        logger.info("Step 5: Generating access token...")
        try:
            access_token = create_access_token(data={"sub": str(db_user.username)})
            logger.info("Step 5: Access token generated successfully")
        except Exception as e:
            logger.error(f"Step 5: Token generation failed: {str(e)}")
            logger.error(f"Token generation traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail="Token generation failed")

        # Step 6: Return response
        logger.info("Step 6: Preparing response...")
        response = {"access_token": access_token, "token_type": "bearer"}
        logger.info(f"=== SIGNUP SUCCESS for username: {user_in.username} ===")
        return response

    except HTTPException as he:
        # Re-raise HTTP exceptions (these are expected errors)
        logger.error(f"=== SIGNUP HTTP ERROR: {he.status_code} - {he.detail} ===")
        raise he
    except Exception as e:
        # Catch any unexpected errors
        logger.error(f"=== SIGNUP UNEXPECTED ERROR: {str(e)} ===")
        logger.error(f"Unexpected error traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error during signup")

@router.post("/login", response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.exec(select(User).where(User.username == form_data.username)).first()
    from app.services.auth import verify_password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.username)})
    return {"access_token": access_token, "token_type": "bearer"}
