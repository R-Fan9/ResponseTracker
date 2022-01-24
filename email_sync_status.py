import utils as ut

def sync_status(df1, df2):
    for idx, row in df2.iterrows():
        email = ut.extract_emails(row[ut.email_header])[0]
        df1.loc[
            df1[ut.email_header].str.contains(email, case=False), 
            ut.status_header
            ] = row[ut.status_header]

def main():
    ut.display_msg("status synchronization started...")
    file_data = ut.input_prompt("Please enter the file dir to process: ")
    file_status = ut.input_prompt("Please enter the file dir that contains the status: ")

    df_data = ut.load_csv(file_data)
    df_status = ut.load_csv(file_status, dl=" - ")

    sync_status(df_data, df_status)

    ut.save_df_csv(df_data, file_data)
    ut.display_msg("status synchronization completed...")

main()






