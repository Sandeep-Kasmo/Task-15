import boto3
import PyPDF2
import io
import os

S3_BUCKET_NAME = "s3-bucket-for-resume-parsing"
S3_SOURCE_KEY = "incoming/resume1.pdf"
LOCAL_TEXT_FILE = "temp_resume_text.txt"

def extract_and_save_text(bucket_name, source_key, local_path):

    s3 = boto3.client('s3')
    
    try:
        print(f"1. Downloading {source_key} from S3...")
        response = s3.get_object(Bucket=bucket_name, Key=source_key)
        
        # Read the file content as bytes
        pdf_bytes = response['Body'].read()
        
        # 2. Extract Text from PDF (using PyPDF2)
        print("2. Extracting text from PDF...")
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text()
            
        if not full_text:
            raise ValueError("Could not extract any text from the PDF.")

        # 3. Save Text Locally for Parsing
        with open(local_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
            
        print(f"Extracted text saved to {local_path}")
        return full_text
        
    except Exception as e:
        print(f" Extraction Error: {e}")
        return None

# # Example Call (Uncomment to test)
raw_resume_text = extract_and_save_text(S3_BUCKET_NAME, S3_SOURCE_KEY, LOCAL_TEXT_FILE)