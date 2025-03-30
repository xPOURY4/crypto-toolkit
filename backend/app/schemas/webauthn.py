from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from app.schemas.base import BaseSchema


class WebAuthnCredential(BaseSchema):
    credential_id: str
    user_id: int
    sign_count: int
    attestation_type: str
    transport: Optional[str] = None
    aaguid: Optional[str] = None
    credential_name: Optional[str] = None


class WebAuthnRegistrationOptions(BaseModel):
    rp_id: str
    rp_name: str
    user_id: str
    user_name: str
    user_display_name: str
    challenge: str
    pubkey_cred_params: List[Dict[str, Any]]
    timeout: int
    attestation: str
    authenticator_selection: Dict[str, Any]
    extensions: Optional[Dict[str, Any]] = None


class WebAuthnRegistrationResponse(BaseModel):
    credential_id: str
    attestation_type: str
    transport: Optional[str] = None
    aaguid: Optional[str] = None
    credential_name: Optional[str] = None


class WebAuthnAuthenticationOptions(BaseModel):
    rp_id: str
    challenge: str
    timeout: int
    allow_credentials: List[Dict[str, Any]]
    user_verification: str
    extensions: Optional[Dict[str, Any]] = None


class WebAuthnAuthenticationResponse(BaseModel):
    credential_id: str
    sign_count: int 