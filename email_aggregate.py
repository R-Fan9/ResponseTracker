import utils as ut

def group_by_col(df, col_name):
    grouped_df = df.groupby([col_name])
    return grouped_df

def get_email_prefixes(df, email_dict):
    email_prefixes = []
    cc_col_idx = df.columns.get_loc(ut.cc_header)
    pf_col_idx = df.columns.get_(ut.pf_header)
    for e in list(email_dict.keys()):
        email_prefixes.append([
            e, 
            ut.concat_val(df, email_dict[e], cc_col_idx), 
            ut.concat_val(df, email_dict[e], pf_col_idx), 
            ut.default_status
            ])

    return email_prefixes

def main():
    ut.display_msg("email aggregation started...")
    in_file_dir = ut.input_prompt("Please enter the file dir to process: ")

    df_email = ut.load_csv(in_file_dir)
    df_email_group = group_by_col(df_email, ut.email_header)

    email_prefixes = get_email_prefixes(df_email, df_email_group.groups)
    df_agg = ut.create_df(email_prefixes, [ut.email_header, ut.cc_header, ut.pf_header, ut.status_header])

    ut.display_msg("email aggregation completed...")
    out_file_dir = ut.input_prompt("Please enter the file dir to save the data: ")
    ut.save_df_csv(df_agg, out_file_dir)

main()
