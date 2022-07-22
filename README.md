# pdf_invoice_extraction

___
___

**About:**

This application takes one of the invoice you choose (A, B, or C). The invoice you are uploading and add it to a SQL database and NOSQL database.
This helps the user to be able to see the invoice information in a better way and saves that information in
a database.
The application was developed with Python and FastAPI using libraries like PDFplumber, REgex.
For the SQL database I used SQLite and SQLAlchemy and for the NoSQL database I used MongoDB and MongoDB engine. 
The application consists of 9 Endpoints such as POST, GET and DELETE

📌 Link to the application:

[PDF Invoice Extraction](https://extract-pdf-weichner.herokuapp.com/docs#/)
___
___

**Invoices Models:**

#### Invoice A

![image info](https://github.com/weichner/resources/raw/main/facturaA_1-1.png)

#### Invoice B

![image_info](https://github.com/weichner/resources/raw/main/images/facturaB_1-1.png)

#### Invoice C

![image_info](https://github.com/weichner/resources/raw/main/images/FacturaC_1-1.png)
___
___
**Invoice data you will be saving:**

| Vendor name  | Contact method | Amount spend  | Purchase date | Payment information | Vendor address | Vendor address | Units by product | Products names | Invoice type | 
| ------------- | -------------- |------------- | ------------- | ------------------- | -------------- | -------------- | ---------------- | -------------- |--------------|
___
___

**Endpoints used for the FastAPI:**

* Post for upload invoice for SQLalchemy
* Post for upload invoice for MongoDB
* Get all invoices for SQLalchemy
* Get one of the invoices for SQlalchemy
* Get invoice by type for SQlalchemy 
* Get all invoices for MongoDB
* Get invoice by type for MongoDB
* Delete one invoice for SQLalchemy
* Delete one invoice for MongoDB

___
___

**How to use this application**

1. You need to download one of the model of invoices (A, B, or C).
2. You can change and write the information you want to. 
3. After you have the changes you want, go to the API and upload the file with endpoint Post.
4. You can choose whether to upload to have the information in SQLalchemy database, MongoDB or both of them.
5. After this you will have your information uploaded into a database.

___
___

**Why I created this app**

Since the first moment I decided to become a developer was because I wanted to innovate and create good things which are
going to help other developers/people/companies.
I found very interesting to create this application because is very useful to be able to detail every important point of
the invoice you are using and be able to keep that data in a database is simply wonderful.


___
___

**Made with:**

✔️Python

✔️FastAPI

✔️SQLalchemy

✔️MongoDB

___
___

**Contact:**

Werner F. Eichner G. 

+351 911 053 792

LinkedIn: https://www.linkedin.com/in/weichner/
