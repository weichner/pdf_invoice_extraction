import datetime
from enum import Enum
from typing import Union, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class InvoiceTypes(str, Enum):
    a = "a"
    b = "b"
    c = "c"


class Invoices(BaseModel):
    vendor_name: str
    contact_method: str
    amount_spent: float
    purchase_date: datetime.date
    payment_information: Optional[str]
    vendor_address: Optional[str]
    invoice_number: str
    units_by_product: str
    products_names: str
    invoice_type: InvoiceTypes


class GetManyInvoicesResponse(BaseModel):
    invoices: list[Invoices]
    count: int


class InvoicesMongo(BaseModel):
    vendor_name: str
    contact_method: str
    amount_spent: float
    purchase_date: datetime.datetime
    payment_information: Optional[str]
    vendor_address: Optional[str]
    invoice_number: str
    units_by_product: list
    products_names: list
    invoice_type: InvoiceTypes
