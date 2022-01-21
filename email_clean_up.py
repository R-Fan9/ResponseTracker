import utils as ut

def filter_col_regex(df, col_name):
    return df.loc[df[col_name].str.contains(ut.email_regex, case=False, regex=True, na=False)]

def clean_up(df):
    for idx, row in df.iterrows():
        email_str = row[ut.email_header]
        email_list = ut.extract_emails(email_str)
        print(idx, email_list)
        print()
        email = email_list[0]
        df.at[idx, ut.email_header] = email
        if(len(email_list) > 1):
            emails = ' '.join(email_list[1:]);
            df.at[idx, ut.cc_header] = emails

def main():
    ut.display_msg("email clean up started...")
    in_file_dir = ut.input_prompt("Please enter the file dir to process: ")

    df = ut.load_csv(in_file_dir)

    df_email = filter_col_regex(df, ut.email_header)
    df_email.reset_index(drop=True, inplace=True)
    df_email[ut.cc_header] = ''
    print(df_email)
    clean_up(df_email)

    ut.display_msg("email clean up completed...")
    out_file_dir = ut.input_prompt("Please enter the file dir to save the data: ")

    ut.save_df_csv(df_email, out_file_dir)

main()