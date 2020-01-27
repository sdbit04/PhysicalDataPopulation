from physical_data_population.profile_reader import *
from physical_data_population.file_readers import *
import datetime


class DataProcessor(FileReader):

    def __init__(self, technology: str, is_gis_planner=False, gis_type='airtel_kol'):
        # I am creating only one type  of DataReader object considering we support only csv now,
        # also we have only one type param input_type
        super().__init__(technology, is_gis_planner, gis_type)
        # We can have another data reader object if planner and SD are of different type
        # self.data_planner_object = self.data_reader_ob.read_planner_file()

    def report_missing_attributes(self, report_dict, sd_input_row,sd_rnc_sector_key ):
        missing_attributes = []
        for index in range(2, 10):
            field_name =self.data_reader_ob.SD_fields_need_to_update[index]
            field_value = sd_input_row[self.data_reader_ob.SD_fields_need_to_update[index]]
            print("field name is ={}".format(field_name))
            print("field_value = {}".format(field_value))
            if field_value is not None and len(str(field_value)) == 0:
                print("adding field into missing attribute report {}".format(field_name))
                missing_attributes.append(field_name)
        print("length of missing_attribute = {}".format(missing_attributes))
        if len(missing_attributes) != 0:
            report_line = "RNC-Sector\t{0}\t missing attributes are {1}".format(
                sd_rnc_sector_key, missing_attributes)
            report_dict[sd_rnc_sector_key].append(report_line)

    def update_sd_by_planner_step1(self, input_planner_file_path, input_sd_file_path, input_lte_carrier_path,
                                   input_sgi_file_path, profile_root_path_p):
        sd_ob_out = {}
        report = {}
        # r = 0
        n = 0
        # travers through planner file
        planner_object = self.data_reader_ob.read_planner_file(input_planner_file_path)
        sd_object = self.data_reader_ob.read_sd_antennas_file(input_sd_file_path)
        lte_carrier_ob = self.data_reader_ob.read_lte_carrier(input_lte_carrier_path)
        sgi_file_ob = self.data_reader_ob.read_gsi_file(input_sgi_file_path)
        # print(sd_object)
        # Here the planner_object and sd_object are dictionary
        profile_root_path = profile_root_path_p
        profile_reader = ProfileReader(profile_root_path)
        antenna_model_vs_profile_map = profile_reader.create_antenna_model_vs_profile_map()
        print("antenna_model_vs_profile_map from profile directory")
        # print(antenna_model_vs_profile_map)
        for sd_rnc_sector_key, sd_input_row in sd_object.items():
            report[sd_rnc_sector_key] = []
            # take a key from SD-ob
            try:
                # search for the key at planner-ob
                matching_planner_input = planner_object[sd_rnc_sector_key]
            except KeyError:
                print("Key {} not found into Planner ".format(sd_rnc_sector_key))
                report_line = "RNC-Sector\t{0}\thas No match in 1st-level-planner file, process will look for lte_carrier, and GSI files".format(
                    sd_rnc_sector_key)
                report[sd_rnc_sector_key].append(report_line)

                # TODO need to add lookup with lte_carrier and SGI-file
                try:
                    lte_carrier_input = lte_carrier_ob[sd_rnc_sector_key]
                    required_part_of_sector_carrier = str(lte_carrier_input['Sector Carrier Name']).split('-')
                    mcc_mnc_sector_carrier_key = '{0}-{1}-{2}-{3}'.format(lte_carrier_input['MCC'], lte_carrier_input['MNC'], required_part_of_sector_carrier[1], required_part_of_sector_carrier[2])
                except KeyError:
                    print(
                        "Key {} not even found into lte_carrier, so not updating physical data for this sector".format(
                            sd_rnc_sector_key))

                    report_line = "RNC-Sector\t{0}\thas No match in 1st-level-planner and not even in lte_carrier file".format(sd_rnc_sector_key)
                    report[sd_rnc_sector_key].append(report_line)
                    report_line = "RNC-Sector\t{0}\thas missing fields = NodeB Longitude, NodeB Latitude,Antenna Longitude, Antenna Latitude, Height, Mechanical DownTilt, Azimuth, Antenna Model".format(sd_rnc_sector_key)
                    report[sd_rnc_sector_key].append(report_line)
                    sd_ob_out[n] = sd_input_row
                    n += 1
                else:
                    print("Key {} was FOUND into lte_carrier".format(sd_rnc_sector_key))
                    print("Key for next level CGI file lookup is {}".format(mcc_mnc_sector_carrier_key))
                    try:
                        matching_cgi_data_input = sgi_file_ob[mcc_mnc_sector_carrier_key]
                    except KeyError:
                        print("Key {} was not found into CGI file".format(mcc_mnc_sector_carrier_key))
                        report_line = "RNC-Sector\t{0}\tthere was match in lte_carrier, but corresponding ##MCC-MNC-SECTOR_CARRIER## key\t{1}\tnot in GIS file,".format(
                            sd_rnc_sector_key, mcc_mnc_sector_carrier_key)
                        report[sd_rnc_sector_key].append(report_line)

                        self.report_missing_attributes(report, sd_input_row, sd_rnc_sector_key)

                        sd_ob_out[n] = sd_input_row
                        n += 1
                    else:
                        print("Key {} was FOUND into CGI file".format(mcc_mnc_sector_carrier_key))
                        print("matching_cgi_data_input is {}".format(matching_cgi_data_input))
                        sd_input_row[self.data_reader_ob.SD_fields_need_to_update[2]] = matching_cgi_data_input[self.data_reader_ob.cgi_file_fields_required[2]]
                        sd_input_row[self.data_reader_ob.SD_fields_need_to_update[3]] = matching_cgi_data_input[self.data_reader_ob.cgi_file_fields_required[3]]
                        sd_input_row[self.data_reader_ob.SD_fields_need_to_update[4]] = matching_cgi_data_input[self.data_reader_ob.cgi_file_fields_required[4]]
                        sd_input_row[self.data_reader_ob.SD_fields_need_to_update[5]] = matching_cgi_data_input[self.data_reader_ob.cgi_file_fields_required[5]]
                        sd_input_row[self.data_reader_ob.SD_fields_need_to_update[6]] = matching_cgi_data_input[self.data_reader_ob.cgi_file_fields_required[6]]
                        sd_input_row[self.data_reader_ob.SD_fields_need_to_update[7]] = matching_cgi_data_input[self.data_reader_ob.cgi_file_fields_required[7]]
                        sd_input_row[self.data_reader_ob.SD_fields_need_to_update[8]] = matching_cgi_data_input[self.data_reader_ob.cgi_file_fields_required[8]]
                        # 9th field is antenna-model, 10th field was a late requirement so remain un-arranged
                        active_status = matching_cgi_data_input[self.data_reader_ob.cgi_file_fields_required[12]]
                        if active_status.upper() == 'ACTIVE':
                            sd_input_row[self.data_reader_ob.SD_fields_need_to_update[10]] = 'true'
                        else:
                            sd_input_row[self.data_reader_ob.SD_fields_need_to_update[10]] = 'false'

                        print("matching_cgi_row = {}".format(matching_cgi_data_input))
                        # print("antenna-model field name from cgi_required_fields = {}".format(self.data_reader_ob.cgi_file_fields_required[9]))
                        antenna_model = matching_cgi_data_input[self.data_reader_ob.cgi_file_fields_required[9]]
                        antenna_e_tilt = matching_cgi_data_input[self.data_reader_ob.cgi_file_fields_required[10]]
                        band: int = matching_cgi_data_input[self.data_reader_ob.cgi_file_fields_required[11]]
                        antenna_model_antenna_e_tilt_key = "{}/{}/{}".format(antenna_model, antenna_e_tilt, band)

                        try:
                            antenna_model_profile = antenna_model_vs_profile_map[antenna_model_antenna_e_tilt_key]
                        except KeyError:
                            print("Profile {} was not found into source of profiles files".format(antenna_model_antenna_e_tilt_key))
                            report_line = "RNC-Sector\t{0}\tthere is a match in GSI file, but corresponding ##ANTENNA-MODEL/E-Tilt/BAND## \t{1}\thas no mathng profile file under profile root,".format(
                                sd_rnc_sector_key, antenna_model_antenna_e_tilt_key)
                            report[sd_rnc_sector_key].append(report_line)

                            self.report_missing_attributes(report, sd_input_row, sd_rnc_sector_key)

                            # print(report)
                            sd_ob_out[n] = sd_input_row
                            n += 1
                        else:
                            sd_input_row[self.data_reader_ob.SD_fields_need_to_update[9]] = antenna_model_profile
                            sd_ob_out[n] = sd_input_row
                            n += 1
                            self.report_missing_attributes(report, sd_input_row, sd_rnc_sector_key)

                            # print(report)
            else:
                # Now I have corresponding records from planner and SD, they are OrderDict object
                planner_input_row = matching_planner_input
                # print(type(planner_input_row))
                # print("planner_input_row = {}".format(planner_input_row))
                # print(type(sd_input_row))
                # print("sd_input_row = {}".fFor RNC-Sectorormat(sd_input_row))
                # print("*********************")
                sd_input_row[self.data_reader_ob.SD_fields_need_to_update[2]] = planner_input_row[self.data_reader_ob.planner_fields_required[2]]
                sd_input_row[self.data_reader_ob.SD_fields_need_to_update[3]] = planner_input_row[self.data_reader_ob.planner_fields_required[3]]
                sd_input_row[self.data_reader_ob.SD_fields_need_to_update[4]] = planner_input_row[self.data_reader_ob.planner_fields_required[4]]
                sd_input_row[self.data_reader_ob.SD_fields_need_to_update[5]] = planner_input_row[self.data_reader_ob.planner_fields_required[5]]
                sd_input_row[self.data_reader_ob.SD_fields_need_to_update[6]] = planner_input_row[self.data_reader_ob.planner_fields_required[6]]
                sd_input_row[self.data_reader_ob.SD_fields_need_to_update[7]] = planner_input_row[self.data_reader_ob.planner_fields_required[7]]
                sd_input_row[self.data_reader_ob.SD_fields_need_to_update[8]] = planner_input_row[self.data_reader_ob.planner_fields_required[8]]
                # print("sd_input_row_updated = {}".format(sd_input_row))
                # We populate antenna/profile at antenna-Model field
                antenna_model = planner_input_row[self.data_reader_ob.planner_fields_required[9]]
                antenna_e_tilt = planner_input_row[self.data_reader_ob.planner_fields_required[10]]
                band = planner_input_row[self.data_reader_ob.planner_fields_required[11]]
                antenna_model_antenna_e_tilt_key = "{}/{}/{}".format(antenna_model, antenna_e_tilt, band)
                try:
                    antenna_model_profile = antenna_model_vs_profile_map[antenna_model_antenna_e_tilt_key]
                except KeyError:
                    print("Profile {} was not found into source of profiles files".format(antenna_model_antenna_e_tilt_key))
                    sd_ob_out[n] = sd_input_row
                    n += 1
                else:
                    sd_input_row[self.data_reader_ob.SD_fields_need_to_update[9]] = antenna_model_profile
                    sd_ob_out[n] = sd_input_row
                    n += 1

                    self.report_missing_attributes(report, sd_input_row, sd_rnc_sector_key)

        return sd_ob_out, report


def data_writer(temp_out_dict, out_put_file_p):
    # temp_out_dict = update_sd_by_planner_step1(planner_ob, sd_ob)
    import time

    try:
        sample_out = temp_out_dict[0]
    except KeyError:
        print("No match between Planner and antennas.txt parsed from SD")
        return
    else:
        out_csv_fields = list(sample_out.keys())
        print("The list of fields into the output antennas.txt file{}".format(out_csv_fields))
        output_file = "antennas{}.txt".format(str(datetime.datetime.utcnow()).split(' ')[0])
        out_put_file = os.path.join(out_put_file_p, output_file)
        print("output file name is {}".format(out_put_file))
        with open(out_put_file, 'w') as out_a:
            pass

        with open(out_put_file, 'a',
                  newline='') as out:
            # Create an writer object for the file
            dict_writers = csv.DictWriter(f=out, fieldnames=out_csv_fields, delimiter='\t')
            dict_writers.writeheader()
            for row in temp_out_dict.values():
                dict_writers.writerow(row)


def write_report(report_dict: dict, out_put_file_p):
    report_file = "report{}.txt".format(str(datetime.datetime.utcnow()).split(' ')[0])
    report_file = os.path.join(out_put_file_p, report_file)
    # with open("D:\D_drive_BACKUP\Study\PycharmProjects\PhysicalDataPopulation_pack\\report.txt", 'w') as report_ob:
    with open(report_file, 'w') as report_ob:
        for ind, line in report_dict.items():
            if isinstance(line, list):
                complete_line = ''
                for speach in line:
                    complete_line = "{}\t{}".format(complete_line, speach)
                line = complete_line
            else:
                pass
            report_ob.write("{}\t{}\n".format(ind, line))
