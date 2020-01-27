import os
import shutil


class NetworkReader(object):

    def __init__(self, network_home, network_dir_list):
        self.network_home = network_home
        self.network_dir_list = network_dir_list

    @staticmethod
    def filter_dir(dir_name: str):
        if dir_name.split("-")[0] == 'COMPLETE_CONFIGURATION':
            return True
        else:
            return False

    def get_most_recent_cmpl_conf_dir_list(self):
        network_dir_vs_compl_conf = {}  # We will populate this dict and return it.
        for directory in self.network_dir_list:
            abs_network_directory = os.path.join(self.network_home, directory)
            compl_conf_dirs_list = filter(self.filter_dir, os.listdir(abs_network_directory))
            # recent_compl_dir = compl_conf_dirs_list.__next__()
            recent_date_time: int = 000
            recent_compl_dir_under_this_NE = None
            for compl_dir in compl_conf_dirs_list:  # this loop is running as nest of each network-NE directory.
                compl_dir_numeric_part = compl_dir.split("[")[0].strip(" ").split("-")
                date_n_time_part = int("{}{}".format(compl_dir_numeric_part[1].lstrip("0"), compl_dir_numeric_part[2]))
                if date_n_time_part > recent_date_time:
                    recent_date_time = date_n_time_part
                    recent_compl_dir_under_this_NE = compl_dir
            network_dir_vs_compl_conf[abs_network_directory] = recent_compl_dir_under_this_NE
        return network_dir_vs_compl_conf

    def get_list_of_antennas_and_lte_carriers_txt_files_to_be_stitched(self):
        network_dir_compl_conf = self.get_most_recent_cmpl_conf_dir_list()
        antennas_txt_list = []
        lte_carriers_list = []
        for abs_ne, compl_dir in network_dir_compl_conf.items():
            abs_path_compl_dir = os.path.join(abs_ne, compl_dir)
            abs_path_antennas_txt = os.path.join(abs_path_compl_dir, 'antennas.txt')
            abs_path_lte_carrier_txt = os.path.join(abs_path_compl_dir, 'lte-carriers.txt')
            antennas_txt_list.append(abs_path_antennas_txt)
            lte_carriers_list.append(abs_path_lte_carrier_txt)
        return antennas_txt_list, lte_carriers_list


class FileStitcher(object):

    def __init__(self, network_home, network_dir_list):
        self.network_home = network_home
        self.network_dir_list = network_dir_list
        self.network_reader_ob = NetworkReader(self.network_home, self.network_dir_list)
        self.antennas_txt_files_list, self.lte_carriers_files_list = self.network_reader_ob.get_list_of_antennas_and_lte_carriers_txt_files_to_be_stitched()
        self.current_dir = os.path.abspath(os.path.dirname(__file__))
        self.consolidated_files_dir = os.path.join(self.current_dir, "temp_artifact\\from_compl_conf")

    def stitch_antennas_txt(self):
        # print(self.antennas_txt_files_list)
        if os.path.isdir(self.consolidated_files_dir):
            pass
        else:
            os.mkdir(self.consolidated_files_dir)

        consolidated_antennas_txt_temp = "{}\\{}".format(self.consolidated_files_dir, "antennas_temp.txt")
        consolidated_antennas_txt = "{}\\{}".format(self.consolidated_files_dir, "antennas.txt")
        # Directly copy the first file at temp_file directory
        shutil.copy(self.antennas_txt_files_list[0], consolidated_antennas_txt_temp)
        for antennas_txt_index in range(1, len(self.antennas_txt_files_list)):
            with open(consolidated_antennas_txt_temp, 'a') as temp_antennas_file_ob:
                with open(self.antennas_txt_files_list[antennas_txt_index], 'r') as one_of_antennas_txt_ob:
                    all_lines = one_of_antennas_txt_ob.readlines()
                    number_of_lines = len(all_lines)
                    for line_nbr in range(1, number_of_lines):
                        temp_antennas_file_ob.write(all_lines[line_nbr])
        shutil.move(consolidated_antennas_txt_temp, consolidated_antennas_txt)

    def stitch_lte_carriers_txt(self):
        # print(self.lte_carriers_files_list)
        if os.path.isdir(self.consolidated_files_dir):
            pass
        else:
            os.mkdir(self.consolidated_files_dir)
        consolidated_lte_carrier_txt_temp = "{}\\{}".format(self.consolidated_files_dir, "lte_carrier_temp.txt")
        consolidated_lte_carrier_txt = "{}\\{}".format(self.consolidated_files_dir, "lte_carriers.txt")
        # Directly copy the first file at temp_file directory
        shutil.copy(self.lte_carriers_files_list[0], consolidated_lte_carrier_txt_temp)
        for lte_carrier_txt_index in range(1, len(self.lte_carriers_files_list)):
            with open(consolidated_lte_carrier_txt_temp, 'a') as temp_antennas_file_ob:
                with open(self.lte_carriers_files_list[lte_carrier_txt_index], 'r') as one_of_lte_carrier_txt_ob:
                    all_lines = one_of_lte_carrier_txt_ob.readlines()
                    number_of_lines = len(all_lines)
                    for line_nbr in range(1, number_of_lines):
                        temp_antennas_file_ob.write(all_lines[line_nbr])
        shutil.move(consolidated_lte_carrier_txt_temp, consolidated_lte_carrier_txt)


if __name__ == "__main__":
    pass
