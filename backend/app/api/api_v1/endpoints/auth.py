from datetime import timedelta
from typing import Any, Dict

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core.config import settings
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate
from app.schemas.webauthn import (
    WebAuthnRegistrationOptions,
    WebAuthnRegistrationResponse,
    WebAuthnAuthenticationOptions,
    WebAuthnAuthenticationResponse,
)
from app.services import user as user_service
from app.services import webauthn as webauthn_service

router = APIRouter()


@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    Get an access token for future requests using username and password
    """
    user = user_service.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user_service.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": create_access_token(
            subject=user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/register", response_model=Token)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Register a new user
    """
    user = user_service.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )
    
    user = user_service.create(db, obj_in=user_in)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": create_access_token(
            subject=user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


# WebAuthn Registration
@router.post("/webauthn/register/options", response_model=Dict[str, Any])
def webauthn_register_options(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get WebAuthn registration options for the current user
    """
    options = webauthn_service.generate_registration_options_for_user(current_user)
    
    # In a real application, the challenge should be stored in a secure way
    # Here we are simplifying and would need to implement a proper challenge store
    
    return options


@router.post("/webauthn/register/verify", response_model=Dict[str, Any])
def webauthn_register_verify(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    credential: Dict[str, Any] = Body(...),
    expected_challenge: str = Body(...),
) -> Any:
    """
    Verify WebAuthn registration for the current user
    """
    try:
        # In a real application, retrieve the challenge from a secure store
        webauthn_credential = webauthn_service.verify_registration_response_for_user(
            current_user,
            credential,
            bytes.fromhex(expected_challenge),
            db,
        )
        
        return {"status": "success", "credential_id": webauthn_credential.credential_id}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"WebAuthn registration failed: {str(e)}",
        )


# WebAuthn Authentication
@router.post("/webauthn/login/options", response_model=Dict[str, Any])
def webauthn_login_options(
    *,
    db: Session = Depends(deps.get_db),
    email: str = Body(..., embed=True),
) -> Any:
    """
    Get WebAuthn authentication options for a user
    """
    user = user_service.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    try:
        options = webauthn_service.generate_authentication_options_for_user(user, db)
        return options
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not generate authentication options: {str(e)}",
        )


@router.post("/webauthn/login/verify", response_model=Token)
def webauthn_login_verify(
    *,
    db: Session = Depends(deps.get_db),
    credential: Dict[str, Any] = Body(...),
    expected_challenge: str = Body(...),
) -> Any:
    """
    Verify WebAuthn authentication
    """
    try:
        # In a real application, retrieve the challenge from a secure store
        _, user = webauthn_service.verify_authentication_response_for_user(
            credential,
            bytes.fromhex(expected_challenge),
            db,
        )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        return {
            "access_token": create_access_token(
                subject=user.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"WebAuthn authentication failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        ) 