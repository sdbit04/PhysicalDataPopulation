import time
from physical_data_population.custom_logger import *


class ProfileReader(object):

    def __init__(self, antenna_profile_directory):
        self.profile_root_path = antenna_profile_directory

    logger = create_custom_logger(logging.INFO)

    def remove_special_char(self, input_string):
        input_string = input_string
        out_string = ""
        special_char = "_-/ ?+~"
        for c in input_string:
            if c not in special_char:
                out_string += c
        return out_string

    def remove_char(self, input_string):
        input_string = input_string
        out_string = ""
        for c in input_string:
            if c.isnumeric():
                out_string += c
        return out_string

    def read_profile(self, profile_path):
        profile_dict = {}
        path = profile_path
        with open(path, 'r', newline="") as profile_1:
            collected_values = 0
            Name_line = None
            Frequency_line = None
            E_tilt_line = None
            for i in range(1, 15):
                line = profile_1.readline().rstrip("\n")
                if line.startswith("NAME"):
                    # print("line {} = {}".format(i, line))
                    Name_line = line
                    collected_values += 1
                    continue
                if line.startswith("FREQUENCY"):
                    # print("line {} = {}".format(i, line))
                    Frequency_line = line
                    collected_values += 1
                    continue
                if line.startswith("ELECTRICAL_TILT"):
                    # print("line {} = {}".format(i, line))
                    E_tilt_line = line
                    collected_values += 1
                    continue
            print("Total number of items collected from profile is {}".format(collected_values))
            print("Collected_values = {}".format(collected_values))
            print("Name line from profile = {}".format(Name_line))
            print("Frequency line from profile = {}".format(Frequency_line))
            print("E_tilt_line from profile = {}".format(E_tilt_line))

            if E_tilt_line is None:
                print("We need to find Electrical tilt from Name")
                if Name_line is not None:
                    E_TILT_ITEMS_OF_NAME = Name_line.split()[-1].split("_")
                    print("ELECTRICAL_TILT_ITEMS:{}".format(E_TILT_ITEMS_OF_NAME))
                    ELECTRICAL_TILT = ""
                    for ITEM in E_TILT_ITEMS_OF_NAME:
                        if "DT" in ITEM.upper():
                            ELECTRICAL_TILT = ITEM
                    ELECTRICAL_TILT = self.remove_char(ELECTRICAL_TILT)
                else:
                    print("Name line was not into profile ")
                    ELECTRICAL_TILT = None
            else:
                ELECTRICAL_TILT = E_tilt_line.split()[1]

            if Name_line is not None:
                ANT_MODEL_ITEMS_OF_NAME = Name_line.split()[1:]
                print("ANTENNA_MODEL_ITEMS_FROM_NAME:{}".format(ANT_MODEL_ITEMS_OF_NAME))
                ANT_MODEL_ITEMS_STRING = ""
                for item in ANT_MODEL_ITEMS_OF_NAME:
                    ANT_MODEL_ITEMS_STRING += item
                print("ANT_MODEL_ITEMS_STRING = {}".format(ANT_MODEL_ITEMS_STRING))
                ANT_MODEL = ANT_MODEL_ITEMS_STRING.split("_")[0]
                ANTENNA_MODEL = self.remove_special_char(ANT_MODEL)
            else:
                print("Name line was not into profile ")
                ANTENNA_MODEL = None

            if Frequency_line is not None:
                FREQUENCY = Frequency_line.split()[1]
            else:
                print("Frequency_line not into profile")
                FREQUENCY = None

            print("FREQUENCY={} ELECTRICAL_TILT:{} ANTENNA_MODEL:{}".format(FREQUENCY, ELECTRICAL_TILT, ANTENNA_MODEL))
            profile_dict['FREQUENCY'] = FREQUENCY
            profile_dict['ELECTRICAL_TILT'] = ELECTRICAL_TILT
            profile_dict['ANTENNA_MODEL'] = ANTENNA_MODEL
        return profile_dict

    def get_band_for_a_frequency(self, frequency):
        frequency_input = frequency
        # band = 900
        if 2100 <= frequency_input <= 2199:
            band = 2100
        elif 850 <= frequency_input <= 999:
            band = 900
        elif 1700 <= frequency_input <= 1899:
            band = 1800
        elif 2300 <= frequency_input <= 2399:
            band = 2300
        else:
            band = 900
        return band

    def create_antenna_model_vs_profile_map(self):
        antenna_model_vs_profile_map = {}
        antenna_models_list = os.listdir(self.profile_root_path)
        os.chdir(self.profile_root_path)
        # print(os.getcwd())
        for model_dir in antenna_models_list:
            model_dir_abs = os.path.join(self.profile_root_path, model_dir)
            # print(model_dir_abs)
            for profile in os.listdir(model_dir_abs):
                # print(profile)
                profile_path_abs = os.path.join(model_dir_abs, profile)
                # TODO if model_dir contain omni then antenna_model_profile_combination will be like IBS/profile-name
                if str(model_dir).upper().__contains__('OMNI'):
                    model_dir = 'IBS'
                antenna_model_profile_combination = "{}/{}".format(model_dir, profile.rstrip(".txt"))
                # print(antenna_model_profile_combination)
                profile_file_data_dict = self.read_profile(profile_path_abs)
                self.logger.info("{}".format(profile_file_data_dict))
                # print(profile_file_data_dict)
                try:
                # print(profile_file_data_dict)
                    band = self.get_band_for_a_frequency(float(profile_file_data_dict['FREQUENCY']))
                    ELECTRICAL_TILT_band = "{}-{}".format(int(profile_file_data_dict['ELECTRICAL_TILT']), band)
                    antenna_model_eTilt_combination = "{}-{}".format(self.remove_special_char(model_dir), ELECTRICAL_TILT_band)
                    antenna_model_eTilt_combination_name = "{}-{}".format(profile_file_data_dict.get('ANTENNA_MODEL'), ELECTRICAL_TILT_band)
                except KeyError:
                    self.logger.error("Profile {} has incorrect format, ignoring".format(profile_path_abs))
                    # print("Profile {} has incorrect format, ignoring".format(profile_path_abs))
                    continue
                # ELECTRICAL_TILT = "{}".format(profile_file_data_dict['ELECTRICAL_TILT'])
                # antenna_model_eTilt_combination = "{}/{}".format(model_dir, ELECTRICAL_TILT)
                try:
                    # just to check if there is exception to get value, we are not using value1 identifier in future.
                    value1 = antenna_model_vs_profile_map[antenna_model_eTilt_combination]
                except KeyError:
                    antenna_model_vs_profile_map[antenna_model_eTilt_combination] = antenna_model_profile_combination
                try:
                    value2 = antenna_model_vs_profile_map[antenna_model_eTilt_combination_name]
                except KeyError:
                    antenna_model_vs_profile_map[antenna_model_eTilt_combination_name] = antenna_model_profile_combination
                # else:
                #     print("Key {} is already exist, overwriting by new value".format(antenna_model_eTilt_combination))
                #     antenna_model_vs_profile_map[antenna_model_eTilt_combination] = antenna_model_profile_combination

        return antenna_model_vs_profile_map


if __name__ == "__main__":
    profile_root_path = r'D:\D_drive_BACKUP\MENTOR\Airtel\collect\Airtel Production Antenna Model'
    # profile_root_path = r'C:\C_DriveData\Python\Developement\PhysicalDataPopulation_15-Feb\collect\Airtel Production Antenna Model'
    profile_reader = ProfileReader(profile_root_path)
    profile_reader.create_antenna_model_vs_profile_map()
    antenna_model_vs_profile_map = profile_reader.create_antenna_model_vs_profile_map()
    # print(antenna_model_vs_profile_map)
    # print(profile_reader.read_profile(r'C:\C_DriveData\Python\Developement\PhysicalDataPopulation\collect\Airtel Production Antenna Model\932DG65T2EKL\932DG65T2EKL_02DT_1810.txt'))
    print(profile_reader.get_band_for_a_frequency(1785))

