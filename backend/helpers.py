from datetime import datetime
from backend.schemas import Invoices
import pdfplumber
import re

def extract_pdf_text(path_to_pdf):
    with pdfplumber.open(path_to_pdf) as pdf:
        pdf_text = ""
        for page in pdf.pages:
            pdf_text += page.extract_text()

    return pdf_text


def generate_invoice_from_tuple(row_tuple):
    invoice_info_dict = {
        "vendor_name": row_tuple[1],
        "contact_method": row_tuple[2],
        "amount_spent": row_tuple[3],
        "purchase_date": row_tuple[4],
        "payment_information": row_tuple[5],
        "vendor_address": row_tuple[6],
        "invoice_number": row_tuple[7],
        "units_by_product": row_tuple[8],
        "products_names": row_tuple[9],
        "invoice_type": row_tuple[10]
    }
    return Invoices(**invoice_info_dict)


def check_empty_list_for_findall(findall_list: list):
    if len(findall_list) == 0:
        return None
    else:
        return findall_list[0]


def extract_data_invoice(path_to_pdf: str, vendor_name_pattern, contact_method_pattern,
                         amount_spent_pattern, purchase_date_pattern,
                         payment_information_pattern, vendor_address_pattern,
                         invoice_number_pattern) -> dict:
    pdf_text = extract_pdf_text(path_to_pdf)
    print(repr(pdf_text))

    patterns = {
        "vendor_name_pattern": re.compile(vendor_name_pattern),
        "contact_method_pattern": re.compile(contact_method_pattern),
        "amount_spent_pattern": re.compile(amount_spent_pattern),
        "purchase_date_pattern": re.compile(purchase_date_pattern),
        "payment_information_pattern": re.compile(payment_information_pattern),
        "vendor_address_pattern": re.compile(vendor_address_pattern),
        "invoice_number_pattern": re.compile(invoice_number_pattern)
    }

    vendor_name_value = check_empty_list_for_findall(patterns["vendor_name_pattern"].findall(pdf_text))
    contact_method_value = check_empty_list_for_findall(patterns["contact_method_pattern"].findall(pdf_text))
    amount_spent_value = check_empty_list_for_findall(patterns["amount_spent_pattern"].findall(pdf_text))
    purchase_date_value = check_empty_list_for_findall(patterns["purchase_date_pattern"].findall(pdf_text))
    payment_information_value = check_empty_list_for_findall(patterns["payment_information_pattern"].findall(pdf_text))
    vendor_address_value = check_empty_list_for_findall(patterns["vendor_address_pattern"].findall(pdf_text))
    invoice_number_value = check_empty_list_for_findall(patterns["invoice_number_pattern"].findall(pdf_text))

    data_dict = {
        "vendor_name": vendor_name_value,
        "contact_method": contact_method_value,
        "amount_spent": amount_spent_value,
        "purchase_date": purchase_date_value,
        "payment_information": payment_information_value,
        "vendor_address": vendor_address_value,
        "invoice_number": invoice_number_value,
    }

    return data_dict


def extract_data_invoice_a(path_to_pdf):
    result = extract_data_invoice(path_to_pdf, vendor_name_pattern=r'\nStudio Shodwe (.+)\n',
                                  contact_method_pattern=r'\nhello@reallygreatsite.com (.+)\n',
                                  amount_spent_pattern=r'\nTotal \$(\d+)\n',
                                  purchase_date_pattern=r'\nDate: (.+)\n',
                                  payment_information_pattern=r'\nPayment method: (.+)\n',
                                  vendor_address_pattern=r'\n123 Anywhere St., Any City (.+)\n',
                                  invoice_number_pattern=r'(\d+)\n')

    result['purchase_date'] = datetime.strptime(result['purchase_date'], "%d %B, %Y")
    text = extract_pdf_text(path_to_pdf)
    lines = text.split('\n')
    index_before_products = lines.index('Item Quantity Price Amount')
    for line in lines:
        if line.startswith('Total'):
            index_after_products = lines.index(line)
    list_products = lines[index_before_products + 1:index_after_products]
    # Para saber cantidad total de productos
    units_by_product = []
    products_names = []
    for info_product in list_products:
        units_by_product.append(int(info_product.split()[-3]))
        product_name = ' '.join(info_product.split()[-4::-1][::-1])
        products_names.append(product_name)

    products_info = {
        "products_names": products_names,
        "units_by_product": units_by_product
    }
    invoice_info = {**result, **products_info}

    return invoice_info


def extract_data_invoice_b(path_to_pdf):
    result = extract_data_invoice(path_to_pdf, vendor_name_pattern=r'\n(.+) Payment Method\n',
                                  contact_method_pattern=r'Payment Method\n(\+\d+\s-\s\d+\s-\s\d+).+\n',
                                  amount_spent_pattern=r'\n\$(\d+)\n',
                                  purchase_date_pattern=r'\nDate : (.+)\n',
                                  payment_information_pattern=r'Payment Method\n\+\d+\s-\s\d+\s-\s\d+(.+)\n',
                                  vendor_address_pattern=r'randompattern1(.)2random',
                                  invoice_number_pattern=r'\nNo : (.+)\n')

    result['purchase_date'] = datetime.strptime(result['purchase_date'], "%m/%d/%Y")
    text = extract_pdf_text(path_to_pdf)
    lines = text.split('\n')
    index_before_products = lines.index('Description Qty Price Total')
    for line in lines:
        if line.replace(" ", "").endswith("Total:"):
            index_after_products = lines.index(line)
    list_products = lines[index_before_products + 1:index_after_products - 1]
    # Para saber cantidad total de productos
    units_by_product = []
    products_names = []
    for info_product in list_products:
        units_by_product.append(int(info_product.split()[-3]))
        product_name = ' '.join(info_product.split()[-4::-1][::-1])
        products_names.append(product_name)

    products_info = {
        "products_names": products_names,
        "units_by_product": units_by_product
    }

    invoice_info = {**result, **products_info}
    return invoice_info


def extract_data_invoice_c(path_to_pdf):
    result = extract_data_invoice(path_to_pdf, vendor_name_pattern=r'\nNAME (.+) DATE .+\n',
                                  contact_method_pattern=r'\nEMAIL (.+) COD .+\n',
                                  amount_spent_pattern=r'\n    TOTAL     (.+)\n',
                                  purchase_date_pattern=r'\nNAME .+ DATE (.+)\n',
                                  payment_information_pattern=r'\nPAYMENT METHOD (.+) BANK ACCOUNT NO.\n',
                                  vendor_address_pattern=r'\nADDRESS (.+) DELIVERY ------\n',
                                  invoice_number_pattern=r'\nEMAIL .+ COD (.+)\n')

    result['purchase_date'] = datetime.strptime(result['purchase_date'], '%d/%m/%Y')
    text = extract_pdf_text(path_to_pdf)
    lines = text.split('\n')
    index_before_products = lines.index('ITEM DESCRIPTION QTY PRICE AMOUNT')
    for line in lines:
        if line.replace(' ', '').startswith('TOTAL'):
            index_after_products = lines.index(line)
    list_products = lines[index_before_products + 1:index_after_products]
    # Para saber cantidad total de productos
    units_by_product = []
    products_names = []
    for info_product in list_products:
        units_by_product.append(int(info_product.split()[-3]))
        product_name = ' '.join(info_product.split()[-4::-1][::-1])
        products_names.append(product_name)

    products_info = {
        "products_names": products_names,
        "units_by_product": units_by_product
    }
    invoice_info = {**result, **products_info}

    return invoice_info

