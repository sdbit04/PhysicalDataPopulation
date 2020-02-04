import json
import time
import traceback


def read_configuration(config_path_p):
    config_path = config_path_p
    planning_or_gis = ""
    with open(config_path, 'r') as config_ob:
        try:
            config_json_ob = json.load(config_ob)
        except json.decoder.JSONDecodeError:
            print("""Please check config_phy.ini file, make sure you have "sd_path","planning_file", "out_put_data_dict_dir", "profile_root_path" with their value, each key and value should be in " ",
            Example: 
            {"technology": "LTE",
            "Network_directory_path": "D:\\D_drive_BACKUP\\Study\\PycharmProjects\\PhysicalDataPopulation\\Input_data_deep\\Network",
            "Directory_names_for_NE": "ZTE_LTE_KOL_24, ZTE_LTE_KOL_25",
            "planning_file_csv": "D:\\Input_data_deep\\Planning_input.txt",            
            "GSI_file_xlsb": "D:\\Input_data_deep\\SGI_input.xlsb",
            "profile_root_path": "D:\\Input_data_deep\\Ant Model"
            "out_put_data_dict_dir": "D:\\out_dir",
            }""")
            time.sleep(1)
            raise json.decoder.JSONDecodeError
        else:
            try:
                technology = config_json_ob["technology"]
                print(technology)
            except KeyError as technology_e:
                raise technology_e
            try:
                Network_directory_path = config_json_ob["Network_directory_path"]
                print(Network_directory_path)
            except KeyError as Network_directory_path_e:
                raise Network_directory_path_e
            try:
                Directory_names_for_NE = config_json_ob["Directory_names_for_NE"]
                print(Directory_names_for_NE)
            except KeyError as Directory_names_for_NE_e:
                raise Directory_names_for_NE_e
            try:
                planning_file = config_json_ob["planning_file_csv"]
                print(planning_file)
            except KeyError as planning_file_e:
                planning_or_gis = "{}{}".format(planning_or_gis, 'NP')
                print("Not getting {}".format(planning_file_e))
                print(traceback.print_exc())
            try:
                CGI_file = config_json_ob["GSI_file_xlsb"]
                print(CGI_file)
            except KeyError as CGI_file_e:
                planning_or_gis = "{}{}".format(planning_or_gis, 'NG')
                print("Not getting {}".format(CGI_file_e))

            try:
                profile_root_path = config_json_ob["profile_root_path"]
                print(profile_root_path)
            except KeyError as profile_root_path_e:
                raise profile_root_path_e
            try:
                out_put_data_dict_dir = config_json_ob["out_put_data_dict_dir"]
                print(out_put_data_dict_dir)
            except KeyError as out_put_data_dict_dir_e:
                raise out_put_data_dict_dir_e
            time.sleep(1)
            if planning_or_gis == "NPNG":
                raise ValueError("Neither Planner nor GIS file was provided, stopping the process")
            return config_json_ob, planning_or_gis


# if __name__ == "__main__":
#     config_path = './config/config.ini'
#     config_json_ob, p_or_g = read_configuration(config_path)
#     print("plan_or_gis is {}".format(p_or_g))

