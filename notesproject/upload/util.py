
import pandas as pd

# if a file extension is not listed, the system will not upload the file
ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preview_csv(filename, row_count=5):
    df = pd.read_csv(filename)
    # this will return the total length of your CSV file
    total_len = len(df)
    # -1 means get them all.
    # if length is less than 5
    if total_len < row_count or row_count == -1:
        csv_values = df.values.tolist()
    else:
        csv_values = df.head(n=row_count).values.tolist()

    # grad column names
    col_names = df.columns.tolist()
    return col_names, csv_values