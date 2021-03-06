import databases
import sqlalchemy

metadata = sqlalchemy.MetaData()

register = sqlalchemy.Table(
    "invoices",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("vendor_name", sqlalchemy.String(length=500), nullable=False),
    sqlalchemy.Column("contact_method", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("amount_spent", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("purchase_date", sqlalchemy.DateTime(), nullable=False),
    sqlalchemy.Column("payment_information", sqlalchemy.String(length=500), nullable=True),
    sqlalchemy.Column("vendor_address", sqlalchemy.String(length=500), nullable=True),
    sqlalchemy.Column("invoice_number", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("units_by_product", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("products_names", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("invoice_type", sqlalchemy.String, nullable=False)
)

DATABASE_URL = "sqlite:///backend/store.db"
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)
