import pandas as pd
import re

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
email_header = 'email'
cc_header = 'cc'
pf_header = 'prefix'
status_header = 'status'
na = 'N/A'
default_status = 'to do'

action_msg = "start migration(1), update status(2), exit and save(3) "

dashboard_file_dir = "dashboard.csv"

def create_df(data, cols):
    df_new = pd.DataFrame(data, columns=cols)
    return df_new

def load_csv(file_dir, dl=None):
    df = pd.read_csv(file_dir, delimiter=dl, engine='python')
    return df

def save_df_csv(df, file_dir):
    df.to_csv(file_dir, index=False)

def get_cell_val(df, row, col, empty_val=""):
    cell_val = df.iloc[row, col]
    return cell_val if not pd.isnull(cell_val) else empty_val

def display_msg(msg):
    print(msg)

def input_prompt(msg):
    user_input = input(msg)
    return user_input

def extract_emails(str):
    return re.findall(email_regex, str)

def concat_val(df, idxs, col_idx):
    vals = ' '.join([str(get_cell_val(df, i, col_idx)) for i in idxs])
    return vals

def get_dashboard():
    return load_csv(dashboard_file_dir)

