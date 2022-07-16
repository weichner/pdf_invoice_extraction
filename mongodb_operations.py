from mongodb_connection import invoices_mongodb
from database_connection import invoices_db
from helpers import extract_data_invoice_a, extract_data_invoice_b, extract_data_invoice_c, generate_invoice_from_tuple
from schemas import InvoiceTypes, GetManyInvoicesResponse, InvoicesMongo, GetManyInvoicesResponseMongo


async def create_invoice(path_to_pdf: str, invoice_type: InvoiceTypes) -> InvoicesMongo:
    # extraer la informacion del pdf
    extract_data_by_type = {
        InvoiceTypes.a: extract_data_invoice_a,
        InvoiceTypes.b: extract_data_invoice_b,
        InvoiceTypes.c: extract_data_invoice_c
    }

    invoice_info: dict = extract_data_by_type[invoice_type](path_to_pdf)
    full_invoice_info = {**invoice_info, **{'invoice_type': invoice_type}}
    # insercion de la base de mongodb
    invoice_result = await invoices_mongodb.insert_one(document=InvoicesMongo(**full_invoice_info).dict())
    print(f'mongodb result = {invoice_result}')
    return InvoicesMongo(**full_invoice_info)


async def get_invoices_by_type(invoice_type: InvoiceTypes):
    filtered_invoices = await invoices_mongodb.get_by_type(invoice_type)
    invoices = []
    for invoice in filtered_invoices['docs']:
        invoices.append(InvoicesMongo(**invoice))
    invoices_result_dict = {
        'invoices': invoices,
        'count': filtered_invoices['count'],
    }
    return GetManyInvoicesResponseMongo(**invoices_result_dict)


async def get_all_invoices():
    filtered_invoices = await invoices_mongodb.get_all()
    invoices = []
    for invoice in filtered_invoices['docs']:
        invoices.append(InvoicesMongo(**invoice))
    invoices_result_dict = {
        'invoices': invoices,
        'count': filtered_invoices['count'],
    }
    return GetManyInvoicesResponseMongo(**invoices_result_dict)


async def delete(invoice_id):
    delete_invoice = invoices_db.delete_one(invoice_id)
    return delete_invoice

