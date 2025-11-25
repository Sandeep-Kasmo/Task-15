from extract import *
from transform import *
from load import *
from config import *
def main():
    try:
        # Read data from raw file
        raw_text_content = read_raw_text_from_file(LOCAL_TEXT_FILE)

        # Transform the extracted data and create a dataframe
        structured_df = parse_resume_text(raw_text_content)

        # Print the dataframe
        print("\n--- Final Structured DataFrame ---")
        print(structured_df.T.to_string())
        
        # Save to CSV
        structured_df.to_csv('parsed_resume_output.csv', index=False)
        print("\n Parsed DataFrame saved to 'parsed_resume_output.csv'.\n")

        #load data
        establish_connection()
        load_data(structured_df,'parsed_resume')
        close_connection()

        
    except FileNotFoundError as e:
        print(f"\nFATAL ERROR: {e}")
        print("Please ensure the extraction script ran successfully and created the file.")
    except Exception as e:
        print(f"\nFATAL ERROR during Parsing: {e}")

if __name__=='__main__':
    main()