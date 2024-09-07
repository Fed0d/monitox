from pydantic import BaseModel, Field


class Categories(BaseModel):
    sexual: bool
    hate: bool
    harassment: bool
    self_harm: bool = Field(alias="self-harm")
    sexual_minors: bool = Field(alias="sexual/minors")
    hate_threatening: bool = Field(alias="hate/threatening")
    violence_graphic: bool = Field(alias="violence/graphic")
    self_harm_intent: bool = Field(alias="self-harm/intent")
    self_harm_instructions: bool = Field(alias="self-harm/instructions")
    harassment_threatening: bool = Field(alias="harassment/threatening")
    violence: bool


class CategoryScores(BaseModel):
    sexual: float
    hate: float
    harassment: float
    self_harm: float = Field(alias="self-harm")
    sexual_minors: float = Field(alias="sexual/minors")
    hate_threatening: float = Field(alias="hate/threatening")
    violence_graphic: float = Field(alias="violence/graphic")
    self_harm_intent: float = Field(alias="self-harm/intent")
    self_harm_instructions: float = Field(alias="self-harm/instructions")
    harassment_threatening: float = Field(alias="harassment/threatening")
    violence: float


class ToxicityAnalysis(BaseModel):
    flagged: bool
    categories: Categories
    category_scores: CategoryScores


class AnalysisResponse(BaseModel):
    answer: str
    toxicity_analysis: ToxicityAnalysis
