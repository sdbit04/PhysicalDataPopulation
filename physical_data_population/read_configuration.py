import json
import time
import traceback
import os

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
             "Network_directory_path": "D:\\Physical_data_creation\\data\\network",
             "Directory_names_for_NE": "OSS4_SF,OSS5_SF,OSS6_SF,OSS7_SF,OSS8_SF,OSS9_SF,OSS10_SF,OSS11_SF",
             "GSI_file_xlsb" : "D:\\D_drive_BACKUP\\MENTOR\\TEOCO\\Kolkata\\Plan Data1\\Planning Kolkata.xlsb",
             "planning_file_xlsx" : "D:\\D_drive_BACKUP\\MENTOR\\TEOCO\\Kolkata\\Plan Data1\\Kolkata.xlsx",
             "out_put_data_dict_dir" : "D:\\D_drive_BACKUP\\MENTOR\\TEOCO\\Kolkata\\out",
             "profile_root_path": "D:\\D_drive_BACKUP\\MENTOR\\TEOCO\\For_Analysis\\TEOCO Production Antenna Model",
             "Tolerance_of_E_tilt": 5
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
                planning_file = config_json_ob["planning_file_xlsx"]
                print(planning_file)
            except KeyError:
                planning_or_gis = "{}{}".format(planning_or_gis, 'NP')
                print(planning_or_gis)
                print("Planner file was not given, so Look-up will be based on GSI file only")

            try:
                CGI_file = config_json_ob["GSI_file_xlsb"]
                print(CGI_file)
            except KeyError:
                planning_or_gis = "{}{}".format(planning_or_gis, 'NG')
                print(planning_or_gis)
                print("GSI.xlsb file were not given")

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
                print("Neither Planner nor GIS file was provided, stopping the process")
                exit(1)
            return config_json_ob, planning_or_gis


# if __name__ == "__main__":
#     config_path = './config/config.ini'
#     config_json_ob, p_or_g = read_configuration(config_path)
#     print("plan_or_gis is {}".format(p_or_g))

