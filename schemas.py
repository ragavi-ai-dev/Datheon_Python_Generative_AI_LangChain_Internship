
from pydantic import BaseModel
from typing import Optional, List


class ResumeData(BaseModel):

    name: str

    email: Optional[str] = None

    phone: Optional[str] = None

    skills: List[str]

    education: List[str]

    experience: List[str]


class InvoiceData(BaseModel):

    invoice_number: str

    customer_name: str

    total_amount: float

    date: str


print("Resume and Invoice schemas created successfully!")
