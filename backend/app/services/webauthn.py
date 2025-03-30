import base64
import os
from typing import Dict, List, Optional, Tuple, Any

from sqlalchemy.orm import Session
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response,
    options_to_json,
    base64url_to_bytes,
)
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    UserVerificationRequirement,
    RegistrationCredential,
    AuthenticationCredential,
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialType,
)

from app.core.config import settings
from app.models.user import User
from app.models.webauthn import WebAuthnCredential


def generate_challenge() -> bytes:
    """Generate a random challenge for WebAuthn registration and authentication."""
    return os.urandom(32)


def generate_registration_options_for_user(user: User) -> Dict[str, Any]:
    """Generate WebAuthn registration options for a user."""
    
    challenge = generate_challenge()
    
    authenticator_selection = AuthenticatorSelectionCriteria(
        user_verification=UserVerificationRequirement.PREFERRED,
        # Additional options can be set here
    )
    
    options = generate_registration_options(
        rp_id=settings.WEBAUTHN_RP_ID,
        rp_name=settings.WEBAUTHN_RP_NAME,
        user_id=str(user.id),
        user_name=user.email,
        user_display_name=user.full_name,
        challenge=challenge,
        authenticator_selection=authenticator_selection,
    )
    
    # Convert to JSON-serializable dictionary
    return options_to_json(options)


def verify_registration_response_for_user(
    user: User,
    credential: Dict[str, Any],
    expected_challenge: bytes,
    db: Session
) -> WebAuthnCredential:
    """Verify WebAuthn registration response and save credential."""
    
    # Prepare credential for verification
    registration_credential = RegistrationCredential.parse_raw(credential)
    
    # Verify the registration response
    verification = verify_registration_response(
        credential=registration_credential,
        expected_challenge=expected_challenge,
        expected_origin=settings.WEBAUTHN_RP_ORIGIN,
        expected_rp_id=settings.WEBAUTHN_RP_ID,
    )
    
    # Create and save credential in database
    new_credential = WebAuthnCredential(
        user_id=user.id,
        credential_id=base64.b64encode(verification.credential_id).decode("utf-8"),
        public_key=verification.credential_public_key,
        sign_count=verification.sign_count,
        attestation_type=verification.attestation_type,
        aaguid=verification.aaguid,
        credential_name=f"Credential for {user.email}",
    )
    
    db.add(new_credential)
    db.commit()
    db.refresh(new_credential)
    
    return new_credential


def generate_authentication_options_for_user(
    user: User, db: Session
) -> Dict[str, Any]:
    """Generate WebAuthn authentication options for a user."""
    
    challenge = generate_challenge()
    
    # Get user credentials from database
    credentials = db.query(WebAuthnCredential).filter(
        WebAuthnCredential.user_id == user.id
    ).all()
    
    if not credentials:
        raise ValueError("No WebAuthn credentials found for user")
    
    # Convert to the format needed for WebAuthn
    allow_credentials = []
    for credential in credentials:
        credential_id_bytes = base64.b64decode(credential.credential_id)
        allow_credentials.append(
            PublicKeyCredentialDescriptor(
                id=credential_id_bytes,
                type=PublicKeyCredentialType.PUBLIC_KEY,
            )
        )
    
    options = generate_authentication_options(
        rp_id=settings.WEBAUTHN_RP_ID,
        challenge=challenge,
        allow_credentials=allow_credentials,
        user_verification=UserVerificationRequirement.PREFERRED,
    )
    
    # Convert to JSON-serializable dictionary
    return options_to_json(options)


def verify_authentication_response_for_user(
    credential: Dict[str, Any],
    expected_challenge: bytes,
    db: Session
) -> Tuple[WebAuthnCredential, User]:
    """Verify WebAuthn authentication response."""
    
    # Prepare credential for verification
    auth_credential = AuthenticationCredential.parse_raw(credential)
    
    # Get credential from database
    credential_id = base64.b64encode(auth_credential.raw_id).decode("utf-8")
    webauthn_credential = db.query(WebAuthnCredential).filter(
        WebAuthnCredential.credential_id == credential_id
    ).first()
    
    if not webauthn_credential:
        raise ValueError("Credential not found")
    
    # Get user from database
    user = db.query(User).filter(User.id == webauthn_credential.user_id).first()
    
    if not user:
        raise ValueError("User not found")
    
    # Verify the authentication response
    verification = verify_authentication_response(
        credential=auth_credential,
        expected_challenge=expected_challenge,
        expected_origin=settings.WEBAUTHN_RP_ORIGIN,
        expected_rp_id=settings.WEBAUTHN_RP_ID,
        credential_public_key=webauthn_credential.public_key,
        credential_current_sign_count=webauthn_credential.sign_count,
    )
    
    # Update sign count in database
    webauthn_credential.sign_count = verification.new_sign_count
    db.commit()
    
    return webauthn_credential, user 