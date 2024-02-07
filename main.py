import warnings
import streamlit as st
from app.modules.payment_parser import get_predictions
warnings.filterwarnings('ignore')


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_excel(index=False)


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

        download_link = convert_df(predictions_df)
        st.download_button(
                        label="Download data as Excel",
                        data=download_link,
                        file_name=processed_filename,
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    )


if __name__ == "__main__":
    main()
