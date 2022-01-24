import utils as ut

def get_email_idxs(df, email):
    df_email = df.loc[df[ut.email_header].str.contains(email, case=False)]
    return df_email.index

def get_ao_ad(prefix):
    df_dashboard = ut.get_dashboard()
    df_prefix = df_dashboard.loc[df_dashboard[ut.pf_header] == prefix]
    return df_prefix.iloc[:, ut.start_ao_ad:ut.end_ao_ad]

def display_prefixes(df, email_idx, disp_ao_ad=False):
    print('prefixes for ', ut.get_cell_val(df, email_idx, ut.get_col_idx(df, ut.email_header))+':')
    prefixes = ut.get_cell_val(df, email_idx, ut.get_col_idx(df, ut.pf_header))
    pfs = prefixes.split()
    for pf in pfs:
        if disp_ao_ad:
            print(pf, end=' ')
            df_ao_ad = get_ao_ad(pf)
            print(df_ao_ad.values)
        else:
            print(pf)
    print()

def display_cc(df, email_idx):
    print('Email: ', ut.get_cell_val(df, email_idx, ut.get_col_idx(df, ut.email_header)))
    print('cc: ', ut.get_cell_val(df, email_idx, ut.get_col_idx(df, ut.cc_header)))

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
            if user_input == 'e':
                break
            print("Please enter an integer")
        user_input = ut.input_prompt("Please enter the email index to process or exit(e): ")

    return user_input

def prefix_migrate(df):
    df_to_do = df.loc[df[ut.status_header] == ut.default_status]
    email_col_idx = df.columns.get_loc(ut.email_header)
    
    while True:
        df_t5 = df_to_do.head(5)
        print(df_t5)
        email_idx_input = index_input(list(df_t5.index.values))

        if type(email_idx_input) is int:
            email = ut.get_cell_val(df, email_idx_input, email_col_idx)
            email_idxs = get_email_idxs(df, email)

            for e_idx in email_idxs:
                display_prefixes(df, e_idx, True)

            cont = ut.input_prompt("continue to process...(y/n) ")
            print()

            if cont.lower() == 'y':
                for e_idx in email_idxs:
                    display_cc(df, e_idx)
                    display_prefixes(df, e_idx)

                upst_util(df, email, "waiting for Samer")
                df_to_do = df.loc[df[ut.status_header] == ut.default_status]
            print()
        else:
            break

def upst_util(df, email, new_status):
    df.loc[df[ut.email_header].str.contains(email, case=False), ut.status_header] = new_status

def email_exist(df, email):
    df_email = df.loc[df[ut.email_header].str.contains(email, case=False)]
    return not df_email.empty

def get_email_input(df):
    user_input = input("Please enter an email: ")
    while not email_exist(df, user_input):
        print("Sorry the email entered does not exist")
        user_input = input("Please enter an email or exit(e): ")
        if(user_input in ['exit', 'e']):
            user_input = ''
            break
    return user_input

def update_status(df, email_input):
    status_input = ut.input_prompt("Please ente the new status: ")
    upst_util(df, email_input, status_input)
    print(email_input+": update status successful...")

def email_actions(df):
    email_input = get_email_input(df)

    if not not email_input:
        action = ut.input_prompt(ut.email_acton_msg)
        while action in ["1", "2", "3"]:
            if(action == "1"):
                update_status(df, email_input)
            elif(action == "2"):
                display_ao_ad = ut.input_prompt("Show AO* and AD*...(y/n) ")
                email_idxs = get_email_idxs(df, email_input)
                for e_idx in email_idxs:
                    display_prefixes(df, e_idx, display_ao_ad == 'y')
            elif(action == "3"):
                email_idxs = get_email_idxs(df, email_input)
                for e_idx in email_idxs:
                    display_cc(df, e_idx)
            action = ut.input_prompt(ut.email_acton_msg)

def main():
    in_file_dir = ut.input_prompt("Please enter the file dir to process: ")
    action = ut.input_prompt(ut.action_msg)

    switcher = {"1":prefix_migrate,
                "2":email_actions}

    df = ut.load_csv(in_file_dir)

    while action in ["1", "2"]:
        switcher[action](df)
        print()
        action = ut.input_prompt(ut.action_msg)

    ut.save_df_csv(df, in_file_dir)

main()