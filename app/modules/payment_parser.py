import pandas as pd
from datetime import datetime

from app.modules.helper import extract_names_from_column, extract_loan_ids_from_column
import streamlit as st


def get_response(message):
    return {
        "predictions": message,
        "status": 200
    }


def get_predictions(file):
    try:
        # Ensure that file is not None and is a valid Excel file
        if file is not None:
            # Check if the file is a list of uploaded files
            if isinstance(file, list):
                file = file[0]  # Take the first file from the list

            # Read the Excel file data into a DataFrame
            df = pd.read_excel(file)

            # Perform operations on the DataFrame
            df = extract_names_from_column(df, 'Description')
            df = extract_loan_ids_from_column(df, 'Description')

            # Save the modified DataFrame to a new Excel file
            processed_filename = f'extracted_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            # df.to_excel(processed_filename, index=False)

            # Return the modified DataFrame and the processed filename
            return df, processed_filename
        else:
            st.error("Invalid file format. Please upload a valid Excel file.")
            return None, None
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None, None

    # def get_predictions(df):
#     df = pd.read_excel(df)
#     df = extract_names_from_column(df, 'Description')
#     df = extract_loan_ids_from_column(df, 'Description')
#     df.to_excel('extracted_results.xlsx', index=False)
#     # return get_response("predictions completed")
