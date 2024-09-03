import warnings
import streamlit as st
from app.modules.payment_parser import get_predictions

warnings.filterwarnings('ignore')
import os


def convert_df(df, csv_filename):
    if df is not None:
        # Print DataFrame content for debugging
        st.write("DataFrame content:", df)

        # Verify the file path where CSV file will be saved
        st.write("CSV file path:", csv_filename)

        # Write the DataFrame to a CSV file
        df.to_csv(csv_filename, index=False)

        # Check if the CSV file was successfully saved
        if os.path.exists(csv_filename):
            return csv_filename
        else:
            st.warning("CSV file was not saved.")
            return None
    else:
        st.warning("DataFrame is empty.")
        return None


# Streamlit app
def main():
    st.set_page_config(page_title="Extract Payment Information", page_icon=":books:")
    st.header("Payment Parser")

    with st.sidebar:
        st.subheader("Your documents")
        file = st.file_uploader(
            "Upload your Excel (.xlsx) file here and click 'Process'", accept_multiple_files=True)

    # Process and download button
    if st.button("Process") and file is not None:
        with st.spinner("Processing"):
            # Process the file and get predictions
            predictions_df, processed_filename = get_predictions(file)

        # Display predictions if available
        if predictions_df is not None:
            st.subheader("Predictions:")
            st.write(predictions_df)

            # Button to download predictions as Excel
            download_link = convert_df(predictions_df, processed_filename)
            if download_link is not None:
                st.write("File Ready to Download....")

                st.download_button(
                    label="Download data as Csv",
                    data=download_link,
                    file_name=processed_filename,
                    mime='text/csv'
                )
            else:
                st.warning("No data to download.")
        else:
            st.error("No predictions to display.")


if __name__ == "__main__":
    main()
