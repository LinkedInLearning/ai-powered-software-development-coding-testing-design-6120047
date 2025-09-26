from pydantic import BaseModel
from typing import Dict


class SummaryReport(BaseModel):
    total: float
    by_category: Dict[str, float]
