from typing import List

from pydantic import BaseModel


class NounItemResponse(BaseModel):
    noun: str
    count: int


class NounFrequencyResponse(BaseModel):
    video_id: str
    total_comment_count: int
    total_noun_count: int
    top_n: int
    nouns: List[NounItemResponse]
