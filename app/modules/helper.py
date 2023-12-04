
def extract_loan_ids_from_column(df, column_name):
    pattern1 = r'(?:\bloan\s*id\s*-\s*|loan\s*id\s*:\s*|apploan\s*id\s*|trfloan\s*id\s*|gtb-loan\s*id\s*:\s*|\s*loan\s*id\s*|\s*loan\s*id\s*for\s*dec\s*\d{4}\s*loan\s*repayment\s*ref:|\s*loan\s*id\s*\d{8}\s*ref:|\s*loan\s*id\s*\d{8}\s*-\s*|\s*loan\s*id\s*\d{8}\s*\-\s*|\s*loan\s*id\s*-\s*\d{8}\s*|\s*\d{8}\s*-\s*|\s*\d{8}\s*\-\s*)\s*(\d{8})\b'
    pattern2 = r'(?:loan\s*id\s*-\s*|loan\s*id\s*:\s*|apploan\s*id\s*|trfloan\s*id\s*|gtb-loan\s*id\s*:\s*|\s*loan\s*id\s*for\s*dec\s*\d{4}\s*loan\s*repayment\s*ref:|\s*\d{8}\s*\-\s*|\s*loan\s*id\s*-\s*\d{8}\s*|\s*loan\s*id\s*(\d{8})\b)'
    pattern3 = r'\b(\d{8})\b'
    pattern4 = r'(?i)TRFLoan\s*ID[:\-\s]*([0-9]{8})'

    pattern5 = r'(?:\bloan\s*id\s*-\s*|loan\s*id\s*:\s*|apploan\s*id\s*|trfloan\s*id\s*|gtb-loan\s*id\s*:\s*|\s*loan\s*id\s*|\s*loan\s*id\s*for\s*dec\s*\d{4}\s*loan\s*repayment\s*ref:|\s*loan\s*id\s*\d{9}\s*ref:|\s*loan\s*id\s*\d{9}\s*-\s*|\s*loan\s*id\s*\d{9}\s*\-\s*|\s*loan\s*id\s*-\s*\d{9}\s*|\s*\d{9}\s*-\s*|\s*\d{9}\s*\-\s*)\s*(\d{9})\b'
    pattern6 = r'(?:loan\s*id\s*-\s*|loan\s*id\s*:\s*|apploan\s*id\s*|trfloan\s*id\s*|gtb-loan\s*id\s*:\s*|\s*loan\s*id\s*for\s*dec\s*\d{4}\s*loan\s*repayment\s*ref:|\s*\d{9}\s*\-\s*|\s*loan\s*id\s*-\s*\d{9}\s*|\s*loan\s*id\s*(\d{9})\b)'
    pattern7 = r'\b(\d{9})\b'
    pattern8 = r'(?i)TRFLoan\s*ID[:\-\s]*([0-9]{9})'

    pattern9 = r'\b(\d{8})frm\b'
    pattern10 = r'\b(\d{9})frm\b'
    pattern11 = r'\b(\d{7})frm\b'
    pattern12 = r'(?i)(?<!\d)loan\s?id|id.*?(\d{8}).*?(?=\b|\D|$)'

    pattern13 = r'(?i)(?<!\d)(?:loan\s?id|id)[^\d]*(\d{8})[^\d]*\b'
    pattern14 = r'\b(\d{6})\b'
    pattern15 = r'\b(\d{7})\b'
    pattern16 = r'(?i)(?<!\d)(?:loan\s?id:|id:)\D*(\d{10})\D*\b'

    # Use str.extract to extract the matching group directly for each pattern
    matches1 = df[column_name].str.lower().str.extract(pattern1, expand=False)
    matches2 = df[column_name].str.lower().str.extract(pattern2, expand=False)
    matches3 = df[column_name].str.lower().str.extract(pattern3, expand=False)
    matches4 = df[column_name].str.lower().str.extract(pattern4, expand=False)

    matches5 = df[column_name].str.lower().str.extract(pattern5, expand=False)
    matches6 = df[column_name].str.lower().str.extract(pattern6, expand=False)
    matches7 = df[column_name].str.lower().str.extract(pattern7, expand=False)
    matches8 = df[column_name].str.lower().str.extract(pattern8, expand=False)

    matches9 = df[column_name].str.lower().str.extract(pattern9, expand=False)
    matches10 = df[column_name].str.lower().str.extract(pattern10, expand=False)
    matches11 = df[column_name].str.lower().str.extract(pattern11, expand=False)
    matches12 = df[column_name].str.lower().str.extract(pattern12, expand=False)

    matches13 = df[column_name].str.lower().str.extract(pattern13, expand=False)
    matches14 = df[column_name].str.lower().str.extract(pattern14, expand=False)
    matches15 = df[column_name].str.lower().str.extract(pattern15, expand=False)
    matches16 = df[column_name].str.lower().str.extract(pattern16, expand=False)

    # Combine matches using '|' (OR) to get the first non-null match
    matches = matches1.combine_first(matches2).combine_first(matches3).combine_first(matches4).combine_first(
        matches5).combine_first(matches6).combine_first(matches7).combine_first(matches8).combine_first(
        matches9).combine_first(matches10).combine_first(matches11).combine_first(matches12).combine_first(
        matches13).combine_first(matches14).combine_first(matches15).combine_first(matches16)

    # Add exception handling
    try:
        # Extract Loan IDs
        loan_ids = matches.str.strip()  # strip whitespaces from extracted values
    except AttributeError:
        # If no match is found, return None
        loan_ids = None

    # Create a new column 'loan id' and store the extracted Loan IDs
    df['loan id'] = loan_ids

    return df


def extract_names_from_column(df, column_name):
    # First regex pattern
    pattern1 = r'(?:from|FRM)\s(.*?)\sto\sRENMONEY\sREPAYMENT\sACCOUNT'
    pattern2 = r'(?<=\.|\s)([A-Za-z\s]+)(?=\sREF)'
    pattern3 = r'([A-Z\s]+)(?=-\d{3}-[A-Z]+ REF:)'
    pattern4 = r'FRM\s(.*?)\sTO\sRENMONEY\sREPAYMENT\sACCOUNT'
    pattern5 = r'from\s(.*?)\swith'
    pattern6 = r'\|(.*?)\s(?:Loan\s*ID|loanid|LOANID|Loan\s*iD)'
    pattern7 = r'FRM\s(.*?)\sTO'
    pattern8 = r'\|(.*?)\s(?:REF|Ref)'
    pattern9 = r'from\s(.*?)\s-'
    pattern10 = r'\b\d{8}\s(.*?)\sto\sRENMONEY'
    pattern11 = r'\|(.*?)\s+POS Trf'
    pattern12 = r'\|([^\|]+)REF'
    pattern13 = r';([A-Za-z\s]+)$'
    pattern14 = r':([^:]+):'


    # Use str.extract to extract the matching group directly for each pattern
    matches1 = df[column_name].str.extract(pattern1, expand=False)
    matches2 = df[column_name].str.extract(pattern2, expand=False)
    matches3 = df[column_name].str.extract(pattern3, expand=False)
    matches4 = df[column_name].str.extract(pattern4, expand=False)
    matches5 = df[column_name].str.extract(pattern5, expand=False)
    matches6 = df[column_name].str.extract(pattern6, expand=False)
    matches7 = df[column_name].str.extract(pattern7, expand=False)
    matches8 = df[column_name].str.extract(pattern8, expand=False)
    matches9 = df[column_name].str.extract(pattern9, expand=False)
    matches10 = df[column_name].str.extract(pattern10, expand=False)
    matches11 = df[column_name].str.extract(pattern11, expand=False)
    matches12 = df[column_name].str.extract(pattern12, expand=False)
    matches13 = df[column_name].str.extract(pattern13, expand=False)
    matches14 = df[column_name].str.extract(pattern14, expand=False)

    # combining patterrns
    matches = matches1.combine_first(matches2).combine_first(matches3).combine_first(matches4).combine_first \
        (matches5).combine_first(matches6).combine_first(matches7).combine_first(matches8).combine_first \
        (matches9).combine_first(matches10).combine_first(matches11).combine_first(matches12).combine_first \
        (matches13).combine_first(matches14)
    # Add exception handling
    try:
        # Extract names
        names = matches.str.strip()  # strip whitespaces from extracted values
    except AttributeError:
        # If no match is found, return None
        names = None

    # Create a new column 'names' and store the extracted names
    df['name'] = names

    return df
