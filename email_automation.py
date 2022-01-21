import utils as ut

def get_ao_ad(df_dashboard, prefix):
    df_prefix = df_dashboard.loc[df_dashboard[ut.pf_header] == prefix]
    return df_prefix.iloc[:, 1:3]

def display_prefixes(df_dashboard, prefixes, disp_ao_ad=False):
    pfs = prefixes.split()
    for pf in pfs:
        if disp_ao_ad:
            print(pf, end=' ')
            df_ao_ad = get_ao_ad(df_dashboard, pf)
            print(df_ao_ad.values)
        else:
            print(pf)
    print()

def index_input(indexes):
    user_input = ut.input_prompt("Please enter the email index to process or exit(e): ")
    while True:
        try:
            user_input = int(user_input)
            if user_input in indexes:
                break
            else:
                print("index is not in range")
        except:
            break
        user_input = ut.input_prompt("Please enter the email index to process or exit(e): ")

    return user_input

def prefix_migrate(df):
    df_to_do = df.loc[df[ut.status_header] == ut.default_status]
    pf_col_idx = df.columns.get_loc(ut.pf_header)
    email_col_idx = df.columns.get_loc(ut.email_header)
    df_dashboard = ut.get_dashboard()

    while True:
        df_t5 = df_to_do.head(5)
        print(df_t5)
        email_idx = index_input(list(df_t5.index.values))

        if type(email_idx) is int:
            display_prefixes(
                df_dashboard, 
                ut.get_cell_val(df, email_idx, pf_col_idx), 
                True)

            cont = ut.input_prompt("continue to process...(y/n) ")
            print()

            if cont.lower() == 'y':
                print(ut.get_cell_val(df, email_idx, email_col_idx))
                display_prefixes(df_dashboard, df.iloc[email_idx, pf_col_idx])
                upst_util(
                    df, 
                    ut.get_cell_val(df, email_idx, email_col_idx), 
                    "waiting for Samer")

                df_to_do = df.loc[df[ut.status_header] == ut.default_status]
            print()
        else:
            break

def upst_util(df, email, new_status):
    df.loc[df[ut.email_header].str.contains(email, case=False), ut.status_header] = new_status

def get_email(df):
    user_input = input("Please enter an email: ")
    df_email = df.loc[df[ut.email_header].str.contains(user_input, case=False)]
    while df_email.empty:
        print("Sorry the email entered does not exist")
        user_input = input("Please enter an email or exit(e): ")
        if(user_input in ['exit', 'e']):
            return ''
        df_email = df.loc[df[ut.email_header].str.contains(user_input, case=False)]

    return user_input

def update_status(df):
    email_input = get_email(df)

    if not not email_input:
        print()
        status_input = ut.input_prompt("Please ente the new status: ")
        upst_util(df, email_input, status_input)
        print(email_input+": update status successful...")

def main():
    in_file_dir = ut.input_prompt("Please enter the file dir to process: ")
    action = ut.input_prompt(ut.action_msg)

    switcher = {"1":prefix_migrate,
                "2":update_status}

    df = ut.load_csv(in_file_dir)

    while action != "3":
        switcher[action](df)
        print()
        action = ut.input_prompt(ut.action_msg)

    ut.save_df_csv(df, in_file_dir)

main()