import sqlalchemy as db
from fastapi import Depends


from schemas import Invoices, InvoiceTypes


class SQLClient:
    def __init__(self, connection_string: str, table_name: str):
        self.engine = db.create_engine(connection_string, connect_args={"check_same_thread": False})
        self.metadata = db.MetaData()
        self.invoices = db.Table(table_name, self.metadata, autoload=True, autoload_with=self.engine)

    def get_one(self, invoice_id: int):
        query = db.select([self.invoices]).where(self.invoices.c.id == invoice_id)
        with self.engine.connect() as conn:
            result = conn.execute(query)
            row = result.fetchall()
        return row

    def get_by_type(self, invoice_type: str):
        query = db.select([self.invoices]).where(self.invoices.c.invoice_type == invoice_type)
        with self.engine.connect() as conn:
            result = conn.execute(query)
            rows = result.fetchall()
        return rows

    def get_all(self):
        query = db.select([self.invoices])
        with self.engine.connect() as conn:
            result = conn.execute(query)
            rows = result.fetchall()
        return rows

    def insert_one(self, invoice_body):
        query = db.insert(self.invoices).values(invoice_body)
        with self.engine.connect() as conn:
            result = conn.execute(query)
        return result

    def update_one(self, invoices, invoice_id: int, doc: Invoices = Depends()):
        # TODO: CHECK OTHER WAY OF PASSING PARAMETERS
        query = self.invoices.update(self.invoices).values(
            vendor_name=doc.vendor_name,
            contact_method=doc.contact_method,
            amount_spent=doc.amount_spent,
            purchase_date=doc.purchase_date,
            payment_method=doc.payment_method,
            company_address=doc.vendor_address,
            invoice_number=doc.invoice_number,
            total_products=doc.total_products,
            products_names=doc.products_names,
            invoice_type=doc.invoice_type
        )
        query = query.where(invoices.c.id == invoice_id)
        with self.engine.connect() as conn:
            result = conn.execute(query)
        return result

    def delete_one(self, invoice_id):
        query = self.invoices.delete()
        query = query.where(self.invoices.c.id == invoice_id)
        with self.engine.connect() as conn:
            result = conn.execute(query)
        return result

    def delete_many(self, invoice_id):
        pass


invoices_db = SQLClient("sqlite:///store.db", "invoices")
