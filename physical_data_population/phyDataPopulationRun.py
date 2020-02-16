"""
Sometime we use use a .py file as module.
However sometime we use a .py file as script.

While running the file as a script, there is no meaning of calculating root of the module path.
While calling the file as module, then need to identify the root of the module.

Argument:
    There are two types of arguments:
        Positional parameter 
        Optional parameter

parser.add_argument("square", type=int, help="display a square of a given number")
parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
args = parser.parse_args()
"""
import argparse
from physical_data_population.read_configuration import *
from physical_data_population.data_processor import *
from physical_data_population.network_reader import *


def run_physical_data_population(config_path_p):
    __config_path = config_path_p
    configuration_ob, plan_gis = read_configuration(__config_path)
    print("plan_or_gis={}".format(plan_gis))
    technology = configuration_ob["technology"]
    networks_base_dir = configuration_ob["Network_directory_path"]
    list_of_network_dir = configuration_ob["Directory_names_for_NE"].split(",")
    # NG ,
    if plan_gis != 'NG' and plan_gis != 'NPNG':
        cgi_file = configuration_ob["GSI_file_xlsb"]
    else:
        cgi_file = None
    if plan_gis != 'NP' and plan_gis != 'NPNG':
        planning_file = configuration_ob["planning_file_csv"]
    else:
        planning_file = None


    profile_root_path = configuration_ob["profile_root_path"]
    out_put_data_dict_dir = configuration_ob["out_put_data_dict_dir"]
    ###########################################################
    # Create antennas.txt and lte_carrier.txt from networks_base_dir, list_of_network_dir provided by user
    # list_of_network_dir may be already a list, need to convert into list.
    # TODO next few line of code are for file stitcher
    file_stitcher = FileStitcher(networks_base_dir, list_of_network_dir)
    file_stitcher.stitch_antennas_txt()
    file_stitcher.stitch_lte_carriers_txt()
    sd_path = "{}\\{}".format(file_stitcher.consolidated_files_dir, "antennas.txt")
    lte_carrier_file = "{}\\{}".format(file_stitcher.consolidated_files_dir, "lte_carriers.txt")

    # We can take the output i.e. temp_files directory as an input for consolidated antennas.txt and lte_carriers.txt
    # TODO next few line of code are to take antennas.txt and lte_carrier.txt without running file stitcher
    """
    current_dir = os.path.abspath(os.path.dirname(__file__))
    temp_dir = os.path.join(current_dir, "temp_artifact\\from_compl_conf")
    sd_path = "{}\\{}".format(temp_dir, "antennas.txt")
    lte_carrier_file = "{}\\{}".format(temp_dir, "lte_carriers.txt")
    # NOTE: we are getting technology, lte_carrier_file, sd_path, planning_file, cgi-file, planner_or_gis, and gis_type
    # from configuration file
    """
    ###############################
    data_processor = DataProcessor(technology, lte_carrier_file, sd_path, planning_file, cgi_file, planner_or_gis=plan_gis, gis_type='airtel_kol')
    out_put_data_dict, report_dict = data_processor.update_sd_by_planner_step1(profile_root_path_p=profile_root_path)
    # print(type(out_put_data_dict))
    # print(out_put_data_dict)
    data_writer(out_put_data_dict, out_put_data_dict_dir)
    write_report(report_dict, out_put_data_dict_dir)


def main_method():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("config_path", help="Please provide the path of the configuration file")
    # args = parser.parse_args()
    # config_path_r = args.config_path
    config_path_r = input("Please provide the absolute path of configuration file, please see a sample configuration "
                          "file at the installation location \\config\\sample_config.ini")
    run_physical_data_population(config_path_r)


if __name__ == "__main__":

    main_method()