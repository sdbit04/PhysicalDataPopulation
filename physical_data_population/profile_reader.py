import os


class ProfileReader(object):

    def __init__(self, antenna_profile_directory):
        self.profile_root_path = antenna_profile_directory

    def read_profile(self, profile_path_p):
        profile_dict = {}
        profile_path = profile_path_p
        with open(profile_path, 'r', newline='') as profile_ob:
            for line in profile_ob.readlines():
                line_item = line.split(' ')
                # print("{}".format(line_item[0]))
                if line_item[0] == 'ELECTRICAL_TILT':
                    profile_dict[line_item[0]] = line_item[1]
                elif line_item[0] == 'FREQUENCY':
                    profile_dict[line_item[0]] = line_item[1]
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
                # print(profile_file_data_dict)
                band = self.get_band_for_a_frequency(float(profile_file_data_dict['FREQUENCY']))
                ELECTRICAL_TILT_band = "{}/{}".format(profile_file_data_dict['ELECTRICAL_TILT'], band)
                antenna_model_eTilt_combination = "{}/{}".format(model_dir, ELECTRICAL_TILT_band)
                # ELECTRICAL_TILT = "{}".format(profile_file_data_dict['ELECTRICAL_TILT'])
                # antenna_model_eTilt_combination = "{}/{}".format(model_dir, ELECTRICAL_TILT)
                try:
                    # just to check if there is exception to get value, we are not using value1 identifier in future.
                    value1 = antenna_model_vs_profile_map[antenna_model_eTilt_combination]
                except KeyError:
                    antenna_model_vs_profile_map[antenna_model_eTilt_combination] = antenna_model_profile_combination
                # else:
                #     print("Key {} is already exist, overwriting by new value".format(antenna_model_eTilt_combination))
                #     antenna_model_vs_profile_map[antenna_model_eTilt_combination] = antenna_model_profile_combination

        return antenna_model_vs_profile_map


if __name__ == "__main__":
    profile_root_path = r'D:\D_drive_BACKUP\Study\PycharmProjects\PhysicalDataPopulation\Input_data_deep\Ant Model'
    profile_reader = ProfileReader(profile_root_path)
    # profile_reader.create_antenna_model_vs_profile_map()
    antenna_model_vs_profile_map = profile_reader.create_antenna_model_vs_profile_map()
    print(antenna_model_vs_profile_map)

