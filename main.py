import shutil
from typing import List
from fastapi import FastAPI, UploadFile, status
from fastapi.params import File
from fastapi.responses import JSONResponse
from database_operations import create_invoice, get_all_invoices, get_one_invoice, delete, get_invoices_by_type
from schemas import Invoices, InvoiceTypes, GetManyInvoicesResponse
from exceptions import InvoiceInsertionError

app = FastAPI()


@app.post("/upload_invoice", status_code=status.HTTP_201_CREATED)
async def handle_form(invoice_type: InvoiceTypes, invoice: UploadFile = File(...)):
    path_to_pdf = f"invoices/{invoice_type}/{invoice.filename}"
    with open(path_to_pdf, "wb") as buffer:
        shutil.copyfileobj(invoice.file, buffer)

    try:
        invoice_data = await create_invoice(path_to_pdf=path_to_pdf,
                                            invoice_type=invoice_type)

    except InvoiceInsertionError as e:
        return JSONResponse(status_code=e.status_code, content=e.detail)

    return invoice_data


@app.get('/register/', response_model=GetManyInvoicesResponse)
async def get_all():
    invoice = await get_all_invoices()
    return invoice


@app.get('/register_by_id/{invoice_id}', response_model=Invoices)
async def get_one(invoice_id: int):
    invoice = await get_one_invoice(invoice_id)
    return invoice


@app.get('/register_by_type/', response_model=GetManyInvoicesResponse)
async def get_by_type(invoice_type: InvoiceTypes):
    invoices = await get_invoices_by_type(invoice_type)
    return invoices


@app.delete('/register/{id}', response_model=Invoices)
async def delete(invoice_id: int):
    invoice = await delete(invoice_id)
    return invoice

