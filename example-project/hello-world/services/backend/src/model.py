from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List
class Company(BaseModel):
        id: int
        name: str
        category: str
        founding_year: int
        employees: int
        profit: List
        def to_json(self):
            return jsonable_encoder(self, exclude_none=True)
class Poem(BaseModel):
      text: str
      def to_json(self):
            return jsonable_encoder(self, exclude_none=True)
class CompanyAnalysis(BaseModel):
      text: str
      def to_json(self):
            return jsonable_encoder(self, exclude_none=True)