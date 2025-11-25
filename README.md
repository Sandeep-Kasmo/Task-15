📄 README.md — Resume Parsing ETL Pipeline
🚀 Project Overview

This project automates the end-to-end pipeline of resume extraction, parsing, transformation, and loading into a MySQL database.

The workflow is:

Extract

Fetch resume PDF from AWS S3

Convert PDF to raw text → temp_resume_text.txt

Transform

Parse text using custom regex-based logic

Extract:

Name

Email

Summary

Technical Skills

Internship Experience (numbered blocks supported)

Construct a clean single-row Pandas DataFrame

Load

Create MySQL table dynamically based on DataFrame structure

Convert lists/dicts → JSON strings

Insert parsed data into MySQL

Handle NULLs, datatypes, long text, etc.

🗂️ Project Structure

Resume_Parsing/

│

├── src/

│   ├── extract.py          # Handles S3 download and PDF → text extraction

│   ├── transform.py        # Contains resume text parsing functions

│   ├── load.py             # MySQL table creation + data insertion logic

│   ├── trf.py              # Main driver script (ETL pipeline)

│   ├── temp_resume_text.txt# Generated raw text from resume

│

├── README.md

└── requirements.txt

📥 1. Extraction Module (extract.py)

Responsibilities:

Connect to AWS S3

Download resume PDF

Extract text using PyPDF2

Save to local file:

temp_resume_text.txt


Key Function:

raw_text = extract_and_save_text(bucket_name, source_key, LOCAL_TEXT_FILE)


If the extraction succeeds:

temp_resume_text.txt created successfully

🧠 2. Transformation Module (transform.py)

This module reads the raw text and extracts structured fields.

✔ Extracted Fields

Name — first non-empty line

Email — regex-based

Summary — extracted between OBJECTIVE and next section

Skills — matched from predefined keyword list

Experience_List — extracted from numbered internship blocks

✔ Internship Parsing Logic

Supports:

1. Internship Title (XYZ)
   Description...
2) Another Internship
- Or bullet-style entries


First non-empty line from each block is extracted, cleaned, and converted into:

"AICTE Internship ; Cognizant Agile Internship ; ..."

✔ Output

A single-row Pandas DataFrame:

df = parse_resume_text(raw_text)

🗃️ 3. Load Module (load.py)

This module:

Establishes MySQL connection

Creates a table dynamically based on DataFrame columns

Converts:

lists → JSON strings

NaN → NULL

timestamp → datetime

✔ Example Table Definition
CREATE TABLE parsed_resume (
    Name TEXT,
    Email TEXT,
    Summary TEXT,
    Skills TEXT,
    Experience_List TEXT
);

✔ Insertion Logic
load_data(df, "parsed_resume")


Outputs:

Inserted 1 rows into parsed_resume
Table parsed_resume created successfully

🧪 4. Running the Full ETL Pipeline

Run:

python trf.py


The script performs:

Download from S3

Extract text

Parse into DataFrame

Load into MySQL

🔧 Configuration
📍 AWS S3

Set bucket and key in extract.py:

S3_BUCKET_NAME = "your_bucket"
S3_SOURCE_KEY = "incoming/resume.pdf"

📍 MySQL Credentials

Edit in load.py:

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='PythonLearningDB'
)

📦 Installation

Install dependencies:

pip install pandas boto3 PyPDF2 mysql-connector-python

🚧 Limitations

The resume parser is simple and regex-based.

Different resume formats require adjustments.

The skills list must be expanded manually.

🙌 Future Improvements

Add ML-based parser like spaCy / transformers

Add section-level sentiment / similarity scoring

Support for DOCX resumes

Auto-detection of resume structure

Deploy pipeline using AWS Lambda + RDS

📧 Contact

For improvements or help, reach out anytime.
