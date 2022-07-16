from backend.database_connection import invoices_db
from backend.helpers import extract_data_invoice_a, extract_data_invoice_b, extract_data_invoice_c, generate_invoice_from_tuple
from backend.schemas import InvoiceTypes, Invoices, GetManyInvoicesResponse, InvoicesMongo
from backend.exceptions import InvoiceInsertionError
from fastapi import status


async def create_invoice(path_to_pdf: str, invoice_type: InvoiceTypes) -> Invoices:
    # extraer la informacion del pdf
    extract_data_by_type = {
        InvoiceTypes.a: extract_data_invoice_a,
        InvoiceTypes.b: extract_data_invoice_b,
        InvoiceTypes.c: extract_data_invoice_c
    }

    invoice_info: dict = extract_data_by_type[invoice_type](path_to_pdf)
    full_invoice_info = {**invoice_info, **{'invoice_type': invoice_type}}
    full_invoice_info_sql = full_invoice_info.copy()
    full_invoice_info_sql['products_names'] = str(full_invoice_info_sql['products_names'])
    full_invoice_info_sql['units_by_product'] = str(full_invoice_info_sql['units_by_product'])
    invoice_data_for_sql = Invoices(**full_invoice_info_sql)
    print(invoice_data_for_sql)

    # insercion en la base de SQL
    invoices_db.insert_one(invoice_data_for_sql.dict())
    if invoices_db is None:
        raise InvoiceInsertionError(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Insertion to database has an error.")
    return invoice_data_for_sql


async def get_one_invoice(invoice_id: int):
    filtered_invoices = invoices_db.get_one(invoice_id)
    invoice = generate_invoice_from_tuple(filtered_invoices[0])
    return invoice


async def get_invoices_by_type(invoice_type: InvoiceTypes):
    filtered_invoices = invoices_db.get_by_type(invoice_type)
    invoices = []
    for invoice in filtered_invoices:
        invoices.append(generate_invoice_from_tuple(invoice))
        print(invoice)
    invoices_result_dict = {
        'invoices': invoices,
        'count': len(invoices),
    }
    return GetManyInvoicesResponse(**invoices_result_dict)


async def get_all_invoices():
    filtered_invoices = invoices_db.get_all()
    invoices = []
    for invoice in filtered_invoices:
        invoices.append(generate_invoice_from_tuple(invoice))
        print(invoice)
    invoices_result_dict = {
        'invoices': invoices,
        'count': len(invoices),
    }
    return GetManyInvoicesResponse(**invoices_result_dict)


async def delete(invoice_id):
    delete_invoice = invoices_db.delete_one(invoice_id)
    return delete_invoice

