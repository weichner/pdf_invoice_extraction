import shutil
from typing import List
from fastapi import FastAPI, UploadFile, status
from fastapi.params import File
from fastapi.responses import JSONResponse
import database_operations as sqldb
import mongodb_operations as mongodb
from schemas import Invoices, InvoiceTypes, GetManyInvoicesResponse, GetManyInvoicesResponseMongo
from exceptions import InvoiceInsertionError

app = FastAPI()


@app.post("/upload_invoice", status_code=status.HTTP_201_CREATED)
async def handle_form(invoice_type: InvoiceTypes, invoice: UploadFile = File(...)):
    path_to_pdf = f"invoices/{invoice_type}/{invoice.filename}"
    with open(path_to_pdf, "wb") as buffer:
        shutil.copyfileobj(invoice.file, buffer)

    try:
        invoice_data = await sqldb.create_invoice(path_to_pdf=path_to_pdf,
                                            invoice_type=invoice_type)

    except InvoiceInsertionError as e:
        return JSONResponse(status_code=e.status_code, content=e.detail)

    return invoice_data


@app.post("/upload_invoice_mongo", status_code=status.HTTP_201_CREATED)
async def handle_form_mongo(invoice_type: InvoiceTypes, invoice: UploadFile = File(...)):
    path_to_pdf = f"invoices/{invoice_type}/{invoice.filename}"
    with open(path_to_pdf, "wb") as buffer:
        shutil.copyfileobj(invoice.file, buffer)

    try:
        invoice_data = await mongodb.create_invoice(path_to_pdf=path_to_pdf,
                                            invoice_type=invoice_type)

    except InvoiceInsertionError as e:
        return JSONResponse(status_code=e.status_code, content=e.detail)

    return invoice_data


@app.get('/register/', response_model=GetManyInvoicesResponse)
async def get_all():
    invoice = await sqldb.get_all_invoices()
    return invoice


@app.get('/register_mongo/', response_model=GetManyInvoicesResponseMongo)
async def get_all_mongo():
    invoice = await mongodb.get_all_invoices()
    return invoice


@app.get('/register_by_id/{invoice_id}', response_model=Invoices)
async def get_one(invoice_id: int):
    invoice = await sqldb.get_one_invoice(invoice_id)
    return invoice


@app.get('/register_by_type/', response_model=GetManyInvoicesResponse)
async def get_by_type(invoice_type: InvoiceTypes):
    invoices = await sqldb.get_invoices_by_type(invoice_type)
    return invoices


@app.get('/register_by_type_mongo/', response_model=GetManyInvoicesResponseMongo)
async def get_by_type_mongo(invoice_type: InvoiceTypes):
    invoices = await mongodb.get_invoices_by_type(invoice_type)
    return invoices


@app.delete('/register/{invoice_id}')
async def delete_one_invoice(invoice_id: int):
    await sqldb.delete(invoice_id)
    return JSONResponse(content=f"Invoice ID:{invoice_id} has been successfully deleted",
                        status_code=status.HTTP_200_OK)

