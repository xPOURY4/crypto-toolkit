from sqlalchemy import Column, ForeignKey, String, LargeBinary, BigInteger, Integer
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class WebAuthnCredential(BaseModel):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    credential_id = Column(String, unique=True, index=True, nullable=False)
    public_key = Column(LargeBinary, nullable=False)
    sign_count = Column(BigInteger, default=0, nullable=False)
    attestation_type = Column(String, nullable=False)
    transport = Column(String, nullable=True)
    aaguid = Column(String, nullable=True)
    credential_name = Column(String, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="webauthn_credentials") 