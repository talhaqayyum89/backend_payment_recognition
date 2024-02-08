import numpy as np
from fuzzywuzzy import process, fuzz
import pandas as pd
from nltk.corpus import stopwords
import streamlit as st
from nltk.tokenize import word_tokenize
import re
import string
import nltk

nltk.download('stopwords')


# Sample DataFrame with 'description' column
def get_filtered_narrations_loanids(narrations):
    # List of words to remove
    stop_words = set(stopwords.words('english'))

    # Function to process each description
    def process_description(description):
        # Convert to lowercase
        description = description.lower()

        # Remove words, symbols, and punctuations
        description = re.sub(r'[^a-zA-Z0-9\s|]', '', description)

        # Tokenize the description
        words = description.split()

        # Remove stop words
        filtered_words = [word for word in words if word not in stop_words]

        # Extract individual 7, 8, 9, or 10-digit numbers
        numbers = re.findall(r'\|(\d{6,14})\|', ' '.join(filtered_words))

        # Join the extracted numbers with a comma
        extracted_numbers = ','.join(numbers)

        return extracted_numbers

    # Apply the processing function to the 'description' column and save the result in a new column
    narrations['extracted_loanids'] = narrations['Description'].apply(process_description)

    # Display the result
    return narrations


# def find_best_matches(description, choices):
#     matches = process.extractBests(description, choices, scorer=fuzz.ratio, score_cutoff=0)
#     return matches


def extract_loan_ids_from_column(db_data, narrations, column_name):
    # Assuming 'Value Date', 'Post Date', 'Description', 'Amount' are the column names
    selected_columns = ['Value Date', 'Post Date', 'Description', 'AMOUNT']

    # Selecting specific columns from the 'narrations' DataFrame
    narrations = narrations[selected_columns]
    narrations = get_filtered_narrations_loanids(narrations)
    st.write(narrations)
    rows = []

    # Iterate over each row in the narrations dataframe
    st.write("searching loanids in db data....")
    for _, row in narrations.iterrows():
        description = row['extracted_loanids']
        if description:
            # Match with 'LoanId'
            st.write("Finding LoanId Match from Description:", description)
            matches_loanid = find_best_matches(description, db_data['LoanId'].astype(str))
            matches_loanid.sort(key=lambda x: x[1], reverse=True)
            top_matches_loanid = matches_loanid[:1]

            # Match with 'ClientId'
            st.write("Finding ClientId Match from Description:", description)
            matches_clientid = find_best_matches(description, db_data['clientID'].astype(str))
            matches_clientid.sort(key=lambda x: x[1], reverse=True)
            top_matches_clientid = matches_clientid[:1]

            # Append the data to the rows list
            for match_loanid in top_matches_loanid:
                for match_clientid in top_matches_clientid:
                    rows.append({
                        'LoanId': match_loanid[0],
                        'clientID': match_clientid[0],
                        'Matched LoanIds from Description': description,
                        'Fuzzy Score (LoanId)': match_loanid[1],
                        'Fuzzy Score (clientID)': match_clientid[1]
                    })
        else:
            # Add a default entry when extracted_loanids is empty
            rows.append({
                'LoanId': "",
                'clientID': "",
                'Matched LoanIds from Description': description,
                'Fuzzy Score (LoanId)': 0,
                'Fuzzy Score (clientID)': 0
            })

    # Convert the list of dictionaries into a DataFrame
    result_df_loanids = pd.DataFrame(rows)

    # Drop rows with missing values and where both Fuzzy Scores are zero
    result_df_loanids = result_df_loanids.dropna()
    result_df_loanids = result_df_loanids[
        (result_df_loanids['Fuzzy Score (LoanId)'] != 0) & (result_df_loanids['Fuzzy Score (clientID)'] != 0)]

    # Reset the index
    result_df_loanids.reset_index(drop=True, inplace=True)
    st.write(result_df_loanids)
    return result_df_loanids


def get_filtered_narrations(narrations):
    # List of words to remove
    stop_words = set(stopwords.words('english'))
    custom_words_to_remove = ['customers', 'dgbnk', 'transfer', 'nibbs', 'mobdgbnkvulte', 'trfrenmoneyfrm',
                              'renmoney repayment',
                              'renmoney', 'repayment', 'account', 'gtworld', 'nibss', 'trf', 'loan', 'acount',
                              'deposit', 'pos', 'gtbank',
                              'limited', 'bank', 'microfinance', 'business', 'plc', 'intra', 'ifo', 'usd', 'payment',
                              'late payment charge',
                              'ussd', 'app', 'switchit', 'ltd', 'mbanking', 'funds', 'trgp', 'union', 'nigeria',
                              'vulte', 'ventures', 'balance', 'frm', 'microfinanc', 'global', 'palmpay', 'services',
                              'lirenmoney',
                              'rev', 'digital', 'nmoney', 'nipre', 'comm', 'includes', 'ref', 'lagos', 'banking',
                              'internet', 'fund', 'venture',
                              'final', 'accounts', 'mob', 'fbnmobile', 'polaris', 'nxg', 'savings', 'nip', 'cash',
                              'micro',
                              'amt vat', 'web remoney', 'fbnile', 'airtime purhase r', 'monthly', 'money', 'oney',
                              'uto', 'trfloan id', 'dominion ent customer',
                              'dominion', 'ent customer at_', 'to gtbank plc renmoney', 'v aella', 'baaa tr aella_fin',
                              'irene imo pmt shortfalls',
                              'irene imo pmt shortfalls', 'gapslite tobi badmus', 'part payment', 'renm', 'atm',
                              'from iti', 'gtb-', 'part', 'diamondxtra']

    def process_description(description):
        # Convert to lowercase
        description = description.lower()

        # Remove numbers
        description = re.sub(r'\d+', '', description)

        # Remove custom words
        for word in custom_words_to_remove:
            description = description.replace(word, '')

        # Tokenize the description using a custom regex to preserve spaces
        words = re.findall(r'\b\w+\b', description)

        # Remove stop words
        filtered_words = [word for word in words if word not in stop_words]

        # Join the filtered words with spaces to maintain spacing
        processed_description = ' '.join(dict.fromkeys(filtered_words))

        return processed_description

    # Apply the processing function to the 'description' column and save the result in a new column
    narrations['processed_description'] = narrations['Description'].apply(process_description)

    return narrations


def find_best_matches(description, choices):
    # Use both fuzz.ratio and Levenshtein distance as scorers
    ratio_matches = process.extractBests(description, choices, scorer=fuzz.ratio, score_cutoff=0)
    levenshtein_matches = process.extractBests(description, choices, scorer=fuzz.partial_ratio, score_cutoff=0)

    # Combine the two sets of matches
    all_matches = ratio_matches + levenshtein_matches

    return all_matches


def extract_names_from_column(db_data, narrations, column_name):
    # Assuming 'Value Date', 'Post Date', 'Description', 'Amount' are the column names
    selected_columns = ['Value Date', 'Post Date', 'Description', 'AMOUNT']

    # Selecting specific columns from the 'narrations' DataFrame
    narrations = narrations[selected_columns]

    db_data = db_data[
        ['ClientFullName', 'clientID', 'LoanId', 'AccountState', 'AccountSubstate', 'Product', 'CreationDate',
         'DisbursementDate', 'DisbMonth', 'Age', 'LoanAmount', 'BureauData', 'RepaymentBank', 'RepaymentMethod', 'Term',
         'TotalNumberOfAccounts', 'TotalNumberOfAccountsInArrs',
         'TotalMonthlyInstallments', 'TotalOutstandingDebt', 'Closeddate', 'MaturityDate', 'Email', 'Channels',
         'InterestRate', 'Acct_Duratn']]

    narrations = get_filtered_narrations(narrations)

    # Initialize an empty list to store the rows
    rows = []
    st.write("searching customers in db data....")

    # Iterate over each row in the narrations dataframe
    for _, row in narrations.iterrows():
        description = row['processed_description']
        payment_date = row['Post Date']
        payment_amount = row['AMOUNT']
        if description:
            # Find matches only when processed_description is not empty
            st.write("Finding Matches for Description:", description)
            matches = find_best_matches(description, db_data['ClientFullName'].astype(str).str.lower())

            # Sort the matches by both fuzzy score and Levenshtein distance
            matches.sort(key=lambda x: (x[1], -fuzz.partial_ratio(description, x[0])), reverse=True)

            # Take the top 3 matches or less if there are fewer matches
            top_matches = matches[:3]

            # Append the results to the rows list
            for match in top_matches:
                rows.append({
                    'Name': match[0],
                    'Matched Name from Description': description,
                    'payment_date': payment_date,
                    'payment_amount': payment_amount,
                    'Fuzzy Score': match[1],
                    'Levenshtein Similarity (%)': fuzz.partial_ratio(description, match[0])
                })
        else:
            # Add a default entry when processed_description is empty
            rows.append({
                'Name': 'Name not found in description',
                'Matched Name from Description': '',
                'payment_date': payment_date,
                'payment_amount': payment_amount,
                'Fuzzy Score': 0,
                'Levenshtein Similarity (%)': 0
            })

    # Create a DataFrame from the rows list
    result_df_names = pd.DataFrame(rows)
    return result_df_names


def get_final_result(db_data, result_df_names, result_df_loanids):
    # Assuming result_df_names, result_df_loanids, and db_data are your dataframes
    st.write("preparing dataset to merge")
    st.write(db_data.columns)
    db_data['ClientFullName'] = db_data['ClientFullName'].str.lower()
    st.write("Finding Matched customer's data....")
    df = pd.merge(left=result_df_names, right=db_data, left_on='Name', right_on='ClientFullName', how='left')
    st.write("Data Found and Merged....")

    # Step 2: Create 'Name Match' column based on Fuzzy Score ranges
    conditions = [
        (df['Fuzzy Score'] >= 90),
        (df['Fuzzy Score'] >= 80),
        (df['Fuzzy Score'] < 80)
    ]
    values = ['Full Name Match', 'Name Partially Matched', 'Name not Matched']
    df['Name Match'] = np.select(conditions, values, default='')

    # Optional: Drop unnecessary columns after merging
    # df.drop(['Name', 'Fuzzy Score'], axis=1, inplace=True)
    df.drop_duplicates(subset='Name', inplace=True)

    # Check if result_df_loanids is not empty before merging
    if not result_df_loanids.empty:
        loanid_match_df = result_df_loanids[result_df_loanids['Fuzzy Score (LoanId)'] == 100].copy()
        ds = pd.merge(df, loanid_match_df[['LoanId', 'Fuzzy Score (LoanId)']], on='LoanId', how='left')
        ds['LoanId Match'] = ds['Fuzzy Score (LoanId)'].apply(lambda x: 'Yes' if x == 100 else 'No')

        clientid_match_df = result_df_loanids[result_df_loanids['Fuzzy Score (clientID)'] == 100].copy()
        final_result = pd.merge(ds, clientid_match_df[['clientID', 'Fuzzy Score (clientID)']], on='clientID', how='left')

        final_result['clientID Match'] = final_result['Fuzzy Score (clientID)'].apply(lambda x: 'Yes' if x == 100 else 'No')
        # Optional: Drop unnecessary columns after merging
        final_result.drop(['Fuzzy Score (LoanId)', 'Fuzzy Score (clientID)'], axis=1, inplace=True)

        # Reset index if needed
        final_result.reset_index(drop=True, inplace=True)
        st.write("Finalizing Results....")

        selected_columns = [
            'ClientFullName', 'Matched Name from Description', 'Name Match',
            'clientID', 'LoanId', 'LoanId Match', 'clientID Match', 'payment_date',
            'payment_amount',
            'AccountState', 'AccountSubstate', 'Product', 'CreationDate',
            'DisbursementDate', 'DisbMonth', 'Age', 'LoanAmount', 'BureauData',
            'RepaymentBank', 'RepaymentMethod', 'Term', 'Closeddate',
            'MaturityDate', 'Email', 'Channels', 'InterestRate'
        ]

        # Create a new DataFrame with only the selected columns
        final_result = final_result[selected_columns]
        return final_result
    else:
        selected_columns = [
            'ClientFullName', 'Matched Name from Description', 'Name Match',
            'clientID', 'LoanId', 'payment_date',
            'payment_amount',
            'AccountState', 'AccountSubstate', 'Product', 'CreationDate',
            'DisbursementDate', 'DisbMonth', 'Age', 'LoanAmount', 'BureauData',
            'RepaymentBank', 'RepaymentMethod', 'Term', 'Closeddate',
            'MaturityDate', 'Email', 'Channels', 'InterestRate'
        ]

        # Create a new DataFrame with only the selected columns
        df = df[selected_columns]
        return df

