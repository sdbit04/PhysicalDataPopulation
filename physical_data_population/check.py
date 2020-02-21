import os
current_dir = os.path.abspath(os.path.dirname(__file__))
consolidated_antenna_files = os.path.join(current_dir, "temp_artifact\\from_compl_conf")

print(consolidated_antenna_files)

path = r"D:\D_drive_BACKUP\MENTOR\Airtel\For_Analysis\test\HBXX-6516DS-VTM_Port 1 +45_00DT_1785.txt"
# path = r"D:\D_drive_BACKUP\MENTOR\Airtel\For_Analysis\Airtel Production Antenna Model\LDX-6516DS-VTM\LBX-6515DS-VTM_900_00.txt"


def read_profile(profile_path):
    profile_dict = {}
    path = profile_path
    with open(path, 'r', newline="") as profile_1:
        collected_values = 0
        Name_line = ""
        Frequency_line = ""
        E_tilt_line = ""
        for i in range(1,15):
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
        print("Collected_values = {}".format(collected_values))

        if collected_values == 3:
            # print(Name_line)
            # print(Frequency_line)
            # print(E_tilt_line)
            print("We are good")
            ANT_MODEL_ITEMS_OF_NAME = Name_line.split()[1:]
            print("ANTENNA_MODEL_ITEMS:{}".format(ANT_MODEL_ITEMS_OF_NAME))
            ANT_MODEL_ITEMS_STRING = ""
            for item in ANT_MODEL_ITEMS_OF_NAME:
                ANT_MODEL_ITEMS_STRING += item
            ANT_MODEL = ANT_MODEL_ITEMS_STRING.split("_")[0]

            FREQUENCY = Frequency_line.split()[1]
            ELECTRICAL_TILT = E_tilt_line.split()[1]
            # print("FREQUENCY={} ELECTRICAL_TILT:{} ANTENNA_MODEL:{}".format(FREQUENCY, ELECTRICAL_TILT,ANT_MODEL ))
            profile_dict['FREQUENCY'] = FREQUENCY
            profile_dict['ELECTRICAL_TILT'] = ELECTRICAL_TILT
            profile_dict['ANTENNA_MODEL'] = ANT_MODEL
        else:
            # print(Name_line)
            # print(Frequency_line)
            # print(E_tilt_line)
            print("We need to find Electrical tilt from Name")
            FREQUENCY = Frequency_line.split()[1]
            E_TILT_ITEMS_OF_NAME = Name_line.split()[-1].split("_")
            print("ELECTRICAL_TILT_ITEMS:{}".format(E_TILT_ITEMS_OF_NAME))
            ANT_MODEL_ITEMS_OF_NAME = Name_line.split()[1:]
            print("ANTENNA_MODEL_ITEMS:{}".format(ANT_MODEL_ITEMS_OF_NAME))
            ANT_MODEL_ITEMS_STRING = ""
            for item in ANT_MODEL_ITEMS_OF_NAME:
                ANT_MODEL_ITEMS_STRING += item
            ANT_MODEL = ANT_MODEL_ITEMS_STRING.split("_")[0]

            ELECTRICAL_TILT = ""
            for ITEM in E_TILT_ITEMS_OF_NAME:
                if "DT" in ITEM.upper():
                    ELECTRICAL_TILT = ITEM
            ELECTRICAL_TILT = remove_alphabate(ELECTRICAL_TILT)
            # print("FREQUENCY={} ELECTRICAL_TILT:{} ANTENNA_MODEL:{}".format(FREQUENCY, ELECTRICAL_TILT, ANT_MODEL))
            profile_dict['FREQUENCY'] = FREQUENCY
            profile_dict['ELECTRICAL_TILT'] = ELECTRICAL_TILT
            profile_dict['ANTENNA_MODEL'] = ANT_MODEL
    return profile_dict


input_va = '06'
int_input = int(input_va)
print(input_va)
print(int_input)

