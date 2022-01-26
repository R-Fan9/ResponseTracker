import utils as ut

class Tracker:
    __in_file = ''
    __df = None

    def __init__(self, file_dir):
        self.__in_file = file_dir
        self.__df = ut.load_csv(file_dir)

    def save_data(self):
        ut.save_df_csv(self.__df, self.__in_file)

    def __get_row_idxs(self, header, value):
        df = self.__df
        df_filter = df.loc[df[header].str.contains(value, case=False)]
        return df_filter.index

    def __get_ao_ad(self, prefix):
        df_dashboard = ut.get_dashboard()
        df_prefix = df_dashboard.loc[df_dashboard[ut.pf_header] == prefix]
        return df_prefix.iloc[:, ut.start_ao_ad:ut.end_ao_ad]

    def __display_prefixes(self, email_idx, disp_ao_ad=False):
        df = self.__df
        print('prefixes for', ut.get_cell_val(df, email_idx, ut.get_col_idx(df, ut.email_header))+':')
        prefixes = ut.get_cell_val(df, email_idx, ut.get_col_idx(df, ut.pf_header))
        pfs = prefixes.split()
        for pf in pfs:
            if disp_ao_ad:
                print(pf, end=' ')
                df_ao_ad = self.__get_ao_ad(pf)
                print(df_ao_ad.values)
            else:
                print(pf)

    def __display_info(self, email_idx, header):
        df = self.__df
        print('Email: ', ut.get_cell_val(df, email_idx, ut.get_col_idx(df, ut.email_header)))
        print(header+': ', ut.get_cell_val(df, email_idx, ut.get_col_idx(df, header)))

    def __update_status(self, email, new_status):
        df  = self.__df
        df.loc[df[ut.email_header].str.contains(email, case=False), ut.status_header] = new_status
        self.save_data()
        print(email+" status: "+new_status)

    def __email_exist(self, email):
        df = self.__df
        df_email = df.loc[df[ut.email_header].str.contains(email, case=False)]
        return not df_email.empty

    def __input_email(self):
        user_input = input("Please enter an email: ")
        while not self.__email_exist(user_input):
            print("Sorry the email entered does not exist")
            user_input = input("Please enter an email or exit(e): ")
            if(user_input in ['exit', 'e']):
                user_input = ''
                break
        return user_input
    
    def __input_status(self):
        st_ops = ut.status_ops
        status_prompt_msg = ', '.join([st_ops[i]+'({})'.format(str(i+1)) for i in range(0, len(st_ops))])
        status_input = ut.input_prompt(status_prompt_msg+": ")

        try:
            status_idx = int(status_input)
            return ut.status_ops[status_idx - 1]
        except:
            return status_input

    def email_actions(self):
        email_input = self.__input_email()

        if not not email_input:
            action = ut.input_prompt(ut.email_acton_msg)
            while action in ["1", "2", "3", "4"]:
                if(action == "1"):
                    status_input = self.__input_status()
                    self.__update_status(email_input, status_input)
                else:
                    email_idxs = self.__get_row_idxs(ut.email_header, email_input)
                    if(action == "2"):
                        display_ao_ad = ut.input_prompt("Show AO* and AD*...(y/n) ")
                        for e_idx in email_idxs:
                            self.__display_prefixes(e_idx, display_ao_ad == 'y')
                    elif(action == "3"):
                        for e_idx in email_idxs:
                            self.__display_info(e_idx, ut.cc_header)
                    elif(action == "4"):
                        for e_idx in email_idxs:
                            self.__display_info(e_idx, ut.status_header)
                action = ut.input_prompt(ut.email_acton_msg)

    def __input_index(self,indexes):
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

    def prefix_migrate(self):
        df = self.__df
        df_to_do = df.loc[df[ut.status_header] == ut.default_status]
        email_col_idx = df.columns.get_loc(ut.email_header)
        
        while True:
            df_t5 = df_to_do.head(5)
            print(df_t5)
            email_idx_input = self.__input_index(list(df_t5.index.values))

            if type(email_idx_input) is int:
                email = ut.get_cell_val(df, email_idx_input, email_col_idx)
                email_idxs = self.__get_row_idxs(ut.email_header, email)

                for e_idx in email_idxs:
                    self.__display_prefixes(e_idx, True)

                cont = ut.input_prompt("continue to process...(y/n) ")
                print()

                if cont.lower() == 'y':
                    for e_idx in email_idxs:
                        self.__display_info(e_idx, ut.cc_header)
                        self.__display_prefixes(e_idx)
                    self.__update_status(email, "waiting for Samer")
                    df_to_do = df.loc[df[ut.status_header] == ut.default_status]
                print()
            else:
                break

    

    

    
