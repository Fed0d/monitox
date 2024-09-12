from enum import Enum as PyEnum

from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    Boolean,
    Column,
    Enum,
    Float,
    ForeignKey,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

from monitox.settings import config

BaseModel = declarative_base()


class ToxicityAnalysis(BaseModel):
    __tablename__ = "toxicity_analysis"

    query_id = Column(
        BigInteger, ForeignKey("query.id"), primary_key=True, nullable=False
    )

    flagged = Column(Boolean, nullable=False)

    # Categories
    sexual = Column(Boolean, nullable=False)
    hate = Column(Boolean, nullable=False)
    harassment = Column(Boolean, nullable=False)
    self_harm = Column(Boolean, nullable=False)
    sexual_minors = Column(Boolean, nullable=False)
    hate_threatening = Column(Boolean, nullable=False)
    violence_graphic = Column(Boolean, nullable=False)
    self_harm_intent = Column(Boolean, nullable=False)
    self_harm_instructions = Column(Boolean, nullable=False)
    harassment_threatening = Column(Boolean, nullable=False)
    violence = Column(Boolean, nullable=False)
    illegal = Column(Boolean, nullable=False)
    child_abuse = Column(Boolean, nullable=False)
    hate_violence_harassment = Column(Boolean, nullable=False)
    malware = Column(Boolean, nullable=False)
    physical_harm = Column(Boolean, nullable=False)
    economic_harm = Column(Boolean, nullable=False)
    fraud = Column(Boolean, nullable=False)
    adult = Column(Boolean, nullable=False)
    political = Column(Boolean, nullable=False)
    privacy = Column(Boolean, nullable=False)
    unqualified_law = Column(Boolean, nullable=False)
    unqualified_financial = Column(Boolean, nullable=False)
    unqualified_health = Column(Boolean, nullable=False)


class VulnerabilityAnalysis(BaseModel):
    __tablename__ = "vulnerability_analysis"

    query_id = Column(
        BigInteger, ForeignKey("query.id"), primary_key=True, nullable=False
    )

    flagged = Column(Boolean, nullable=False)

    # Categories
    benign = Column(Float, nullable=False)
    jailbreak = Column(Float, nullable=False)
    prompt_injection = Column(Float, nullable=False)


class Query(BaseModel):
    __tablename__ = "query"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    request = Column(
        Text,
        nullable=False,
    )
    user_id = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    llm = Column(Text, nullable=False)


class UserRole(PyEnum):
    ROLE_ADMIN = 1
    ROLE_USER = 2


class Role(BaseModel):
    __tablename__ = "role"

    user_id = Column(
        BigInteger,
        primary_key=True,
    )
    role = Column(
        Enum(UserRole, name="user_role"),
        primary_key=True,
    )


engine = create_engine(config.postgres.uri, echo=True)
Session = sessionmaker(bind=engine)
