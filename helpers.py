from datetime import datetime

from schemas import Invoices
import pdfplumber
import re
import pandas as pd


def extract_pdf_text(path_to_pdf):
    with pdfplumber.open(path_to_pdf) as pdf:
        pdf_text = ""
        for page in pdf.pages:
            pdf_text += page.extract_text()

    return pdf_text


def extract_data_invoice(path_to_pdf: str, vendor_name_pattern, contact_method_pattern,
                         amount_spent_pattern, purchase_date_pattern,
                         company_name_pattern, company_address_pattern,
                         invoice_number_pattern) -> dict:
    pdf_text = extract_pdf_text(path_to_pdf)
    print(repr(pdf_text))

    patterns = {
        "vendor_name_pattern": re.compile(vendor_name_pattern),
        "contact_method_pattern": re.compile(contact_method_pattern),
        "amount_spent_pattern": re.compile(amount_spent_pattern),
        "purchase_date_pattern": re.compile(purchase_date_pattern),
        "company_name_pattern": re.compile(company_name_pattern),
        "company_address_pattern": re.compile(company_address_pattern),
        "invoice_number_pattern": re.compile(invoice_number_pattern)
    }

    vendor_name_value = patterns["vendor_name_pattern"].findall(pdf_text)[0]
    contact_method_value = patterns["contact_method_pattern"].findall(pdf_text)[0]
    amount_spent_value = patterns["amount_spent_pattern"].findall(pdf_text)[0]
    purchase_date_value = patterns["purchase_date_pattern"].findall(pdf_text)[0]
    company_name_value = patterns["company_name_pattern"].findall(pdf_text)[0]
    company_address_value = patterns["company_address_pattern"].findall(pdf_text)[0]
    invoice_number_value = patterns["invoice_number_pattern"].findall(pdf_text)[0]

    data_dict = {
        "vendor_name": vendor_name_value,
        "contact_method": contact_method_value,
        "amount_spent": amount_spent_value,
        "purchase_date": purchase_date_value,
        "company_name": company_name_value,
        "company_address": company_address_value,
        "invoice_number": invoice_number_value,
    }

    return data_dict


def extract_data_invoice_a(path_to_pdf):
    result = extract_data_invoice(path_to_pdf, vendor_name_pattern=r'\nStudio Shodwe (.+)\n',
                                  contact_method_pattern=r'\nhello@reallygreatsite.com (.+)\n',
                                  amount_spent_pattern=r'\nTotal \$(\d+)\n',
                                  purchase_date_pattern=r'\nDate: (.+)\n',
                                  company_name_pattern=r'\n(.+) Olivia Wilson\n',
                                  company_address_pattern=r'\n(.+) 123 Anywhere St., Any City\n',
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
    total_products = 0
    products_names = []
    for info_product in list_products:
        total_products += int(info_product.split()[-3])
        product_name = ' '.join(info_product.split()[-4::-1][::-1])
        products_names.append(product_name)

    products_info = {
        "products_names": str(products_names),
        "total_products": total_products
    }
    invoice_info = {**result, **products_info}

    return invoice_info


def generate_invoice_from_tuple(row_tuple):
    invoice_info_dict = {
        "vendor_name": row_tuple[1],
        "contact_method": row_tuple[2],
        "amount_spent": row_tuple[3],
        "purchase_date": row_tuple[4],
        "company_name": row_tuple[5],
        "company_address": row_tuple[6],
        "invoice_number": row_tuple[7],
        "total_products": row_tuple[8],
        "products_names": row_tuple[9],
        "invoice_type": row_tuple[10]
    }
    return Invoices(**invoice_info_dict)


def extract_data_invoice_b(path_to_pdf):
    result = extract_data_invoice(path_to_pdf)
    return result

