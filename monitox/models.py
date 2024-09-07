from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    Boolean,
    Column,
    Float,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

from monitox.settings import config

BaseModel = declarative_base()


class ToxicityAnalysis(BaseModel):  # type: ignore[misc,valid-type]
    __tablename__ = "toxicity_analysis"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
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

    # Category Scores
    sexual_score = Column(Float, nullable=False)
    hate_score = Column(Float, nullable=False)
    harassment_score = Column(Float, nullable=False)
    self_harm_score = Column(Float, nullable=False)
    sexual_minors_score = Column(Float, nullable=False)
    hate_threatening_score = Column(Float, nullable=False)
    violence_graphic_score = Column(Float, nullable=False)
    self_harm_intent_score = Column(Float, nullable=False)
    self_harm_instructions_score = Column(Float, nullable=False)
    harassment_threatening_score = Column(Float, nullable=False)
    violence_score = Column(Float, nullable=False)


class Query(BaseModel):  # type: ignore[misc,valid-type]
    __tablename__ = "query"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    request = Column(
        Text,
        nullable=False,
    )
    user_id = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    llm = Column(Text, nullable=False)


class Roles(BaseModel):  # type: ignore[mis,valid-typec]
    __tablename__ = "role"

    user_id = Column(
        BigInteger,
        primary_key=True,
    )
    role = Column(
        Text,
        primary_key=True,
    )


engine = create_engine(config.postgres.uri, echo=True)
Session = sessionmaker(bind=engine)
