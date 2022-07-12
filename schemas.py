from datetime import datetime, date
from enum import Enum
from typing import Union
from pydantic import BaseModel, Field


class InvoiceTypes(str, Enum):
    a = "a"
    b = "b"
    c = "c"
    d = "d"
    e = "e"
    f = "f"


class Invoices(BaseModel):
    vendor_name: str
    contact_method: str
    amount_spent: float
    purchase_date: date
    payment_method: str
    vendor_address: str
    invoice_number: int
    total_products: int
    products_names: str
    invoice_type: InvoiceTypes


class GetManyInvoicesResponse(BaseModel):
    invoices: list[Invoices]
    count: int
