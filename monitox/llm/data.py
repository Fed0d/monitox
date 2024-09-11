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
    illegal: bool
    child_abuse: bool
    hate_violence_harassment: bool
    malware: bool
    physical_harm: bool
    economic_harm: bool
    fraud: bool
    adult: bool
    political: bool
    privacy: bool
    unqualified_law: bool
    unqualified_financial: bool
    unqualified_health: bool


class ToxicityAnalysis(BaseModel):
    flagged: bool
    categories: Categories


class AnalysisResponse(BaseModel):
    answer: str
    toxicity_analysis: ToxicityAnalysis
