from physical_data_population.profile_reader import *
from physical_data_population.file_readers import *
import datetime


class DataProcessor(FileReader):

    def __init__(self, technology: str, lte_carrier_path, sd_file_path,planner_file_path,cgi_file_path, competitive_model_path, planner_or_gis: str = "", gis_type='airtel_kol'):
        # I am creating only one type  of DataReader object considering we support only csv now,
        # also we have only one type param input_type
        super().__init__(technology,lte_carrier_path, sd_file_path,planner_file_path,cgi_file_path, competitive_model_path, planner_or_gis, gis_type)
        # We can have another data reader object if planner and SD are of different type
        # self.data_planner_object = self.data_reader_ob.read_planner_file()
        self.competitive_ant_model_dict = self.read_competitive_model_list()
        # self.competitive_ant_model_dict = {"ODV065R17M18JJJGIN":"DBXLH6565BVTM","ODV05R17M18JJJGIN":"DBXLH6565BVTM","AANBmMIMOAAS64T64R":"DBXLH6565BVTM","AANBmMIMOAAS4T64R":"DBXLH6565BVTM","RV465DM":"DBXLH6565BVTM","AXCM824960171021706516.518iAD":"DBXLH6565BVTM"}

    def search_profile_for_each_change_in_tilt(self, base_tilt, tilt_change, _antenna_model_vs_profile_map, model, band):
        change = tilt_change
        etilt = base_tilt
        up_tilt = etilt + change
        if up_tilt <= 10:
            ant_model_etilt_band_key_tolerance = "{}-{}-{}".format(model, up_tilt, band)
            print("searching profile with {}".format(ant_model_etilt_band_key_tolerance))
            try:
                antenna_model_profile = _antenna_model_vs_profile_map[ant_model_etilt_band_key_tolerance]
                return antenna_model_profile
            except KeyError:
                down_tilt = etilt - change
                if down_tilt >= 0:
                    print("searching profile with {}".format(ant_model_etilt_band_key_tolerance))
                    ant_model_etilt_band_key_tolerance = "{}-{}-{}".format(model, down_tilt, band)
                    try:
                        antenna_model_profile = _antenna_model_vs_profile_map[
                            ant_model_etilt_band_key_tolerance]
                        return antenna_model_profile
                    except KeyError:
                        # TODO search with compatiable model, it is Not correct place
                        pass
        else:
            down_tilt = etilt - change
            if down_tilt >= 0:
                ant_model_etilt_band_key_tolerance = "{}-{}-{}".format(model, down_tilt, band)
                print("searching profile with {}".format(ant_model_etilt_band_key_tolerance))
                try:
                    antenna_model_profile = _antenna_model_vs_profile_map[
                        ant_model_etilt_band_key_tolerance]
                    return antenna_model_profile
                except KeyError:
                    # TODO search with compatiable model, it is Not correct place
                    pass

    def get_profile_for_a_model_etilt_band_key(self, antenna_model, antenna_e_tilt, band, _antenna_model_vs_profile_map: dict, tolerance: int):
        model = antenna_model
        etilt = int(antenna_e_tilt)
        band = str(band)
        ant_model_etilt_band_key = "{}-{}-{}".format(model, etilt, band)
        print("ant_model_etilt_band_key = {}".format(ant_model_etilt_band_key))
        tolerance = int(tolerance)
        print("Start searching profile with {}".format(ant_model_etilt_band_key))
        try:
            antenna_model_profile = _antenna_model_vs_profile_map[ant_model_etilt_band_key]
            return antenna_model_profile
        except KeyError:
            print("No profile found with {}, trying with band and tilt tolarance".format(ant_model_etilt_band_key))
            # TODO def search_with_band_n_tilt_tolerance(tolerance)
            if tolerance > 0:
                for change in range(1, tolerance+1, 1):
                    antenna_model_profile = self.search_profile_for_each_change_in_tilt(etilt, change, _antenna_model_vs_profile_map, model,band)
                    if antenna_model_profile is not None:
                        print("Derived antenna-model-profile is = {}".format(antenna_model_profile))
                        return antenna_model_profile
                # If for loop is complete without break/return, i.e. there is no match found into the above loop
                else:
                    print("Not getting profile after tile tolerance, applying band tolerance with it")
                    # TODO def search_profile_for_different_band()
                    bands = ['900', '1800', '2100', '2300']
                    band_position = bands.index(band)
                    min_band_index = 0
                    max_band_index = 3
                    if band_position == min_band_index:
                        for band_index1 in range(min_band_index + 1, max_band_index + 1, 1):
                            current_band = bands[band_index1]
                            # common part start
                            ant_model_etilt_band_key_tolerance = "{}-{}-{}".format(model, etilt, current_band)
                            print("searching with band: {}, and search key is: {}".format(current_band, ant_model_etilt_band_key_tolerance))
                            try:
                                antenna_model_profile = _antenna_model_vs_profile_map[
                                    ant_model_etilt_band_key_tolerance]
                                return antenna_model_profile
                            except KeyError:
                                print("No profile found for key : {}, trying with tilt tolerance for band : {}".format(ant_model_etilt_band_key_tolerance, current_band))
                                for change in range(1, tolerance + 1, 1):
                                    antenna_model_profile = self.search_profile_for_each_change_in_tilt(etilt, change,
                                                                                                        _antenna_model_vs_profile_map,
                                                                                                        model, current_band)
                                    if antenna_model_profile is not None:
                                        print("Derived antenna-model-profile is = {}".format(antenna_model_profile))
                                        return antenna_model_profile
                                else:
                                    print("No profile was found after changing band to {}".format(current_band))
                            # common part end
                    elif band_position == max_band_index:
                        for band_index2 in range(max_band_index - 1, min_band_index - 1, -1):
                            current_band = bands[band_index2]
                            # common part start
                            ant_model_etilt_band_key_tolerance = "{}-{}-{}".format(model, etilt, current_band)
                            print("searching with band: {}, and search key is: {}".format(current_band,
                                                                                          ant_model_etilt_band_key_tolerance))
                            try:
                                antenna_model_profile = _antenna_model_vs_profile_map[
                                    ant_model_etilt_band_key_tolerance]
                                return antenna_model_profile
                            except KeyError:
                                print("No profile found for key : {}, trying with tilt tolerance for band : {}".format(
                                    ant_model_etilt_band_key_tolerance, current_band))
                                for change in range(1, tolerance + 1, 1):
                                    antenna_model_profile = self.search_profile_for_each_change_in_tilt(etilt, change,
                                                                                                        _antenna_model_vs_profile_map,
                                                                                                        model,
                                                                                                        current_band)
                                    if antenna_model_profile is not None:
                                        print("Derived antenna-model-profile is = {}".format(antenna_model_profile))
                                        return antenna_model_profile
                                else:
                                    print("No profile was found after changing band to {}".format(current_band))
                            # common part end
                    else:
                        count = 0
                        while True:
                            count += 1
                            upper_index = band_position + count
                            if upper_index <= max_band_index:
                                upper_band = bands[upper_index]
                                current_band = upper_band
                                # common part start
                                ant_model_etilt_band_key_tolerance = "{}-{}-{}".format(model, etilt, current_band)
                                print("searching with band: {}, and search key is: {}".format(current_band,
                                                                                              ant_model_etilt_band_key_tolerance))
                                try:
                                    antenna_model_profile = _antenna_model_vs_profile_map[
                                        ant_model_etilt_band_key_tolerance]
                                    return antenna_model_profile
                                except KeyError:
                                    print(
                                        "No profile found for key : {}, trying with tilt tolerance for band : {}".format(
                                            ant_model_etilt_band_key_tolerance, current_band))
                                    for change in range(1, tolerance + 1, 1):
                                        antenna_model_profile = self.search_profile_for_each_change_in_tilt(etilt,
                                                                                                            change,
                                                                                                            _antenna_model_vs_profile_map,
                                                                                                            model,
                                                                                                            current_band)
                                        if antenna_model_profile is not None:
                                            print("Derived antenna-model-profile is = {}".format(antenna_model_profile))
                                            return antenna_model_profile
                                    else:
                                        print("No profile was found after changing band to {}".format(current_band))
                                # common part end

                                        lower_index = band_position - count
                                        if lower_index >= min_band_index:
                                            lower_band = bands[lower_index]
                                            current_band = lower_band
                                            ####
                                            # common part start
                                            ant_model_etilt_band_key_tolerance = "{}-{}-{}".format(model, etilt,
                                                                                                   current_band)
                                            print("searching with band: {}, and search key is: {}".format(current_band,
                                                                                                          ant_model_etilt_band_key_tolerance))
                                            try:
                                                antenna_model_profile = _antenna_model_vs_profile_map[
                                                    ant_model_etilt_band_key_tolerance]
                                                return antenna_model_profile
                                            except KeyError:
                                                print(
                                                    "No profile found for key : {}, trying with tilt tolerance for band : {}".format(
                                                        ant_model_etilt_band_key_tolerance, current_band))
                                                for change in range(1, tolerance + 1, 1):
                                                    antenna_model_profile = self.search_profile_for_each_change_in_tilt(
                                                        etilt,
                                                        change,
                                                        _antenna_model_vs_profile_map,
                                                        model,
                                                        current_band)
                                                    if antenna_model_profile is not None:
                                                        print("Derived antenna-model-profile is = {}".format(
                                                            antenna_model_profile))
                                                        return antenna_model_profile
                                                else:
                                                    print("No profile was found after changing band to {}".format(
                                                        current_band))
                                            # common part end

                                        else:
                                            continue

                            else:
                                lower_index = band_position - count
                                if lower_index >= min_band_index:
                                    lower_band = bands[lower_index]
                                    current_band = lower_band

                                    # common part start
                                    ant_model_etilt_band_key_tolerance = "{}-{}-{}".format(model, etilt, current_band)
                                    print("searching with band: {}, and search key is: {}".format(current_band,
                                                                                                  ant_model_etilt_band_key_tolerance))
                                    try:
                                        antenna_model_profile = _antenna_model_vs_profile_map[
                                            ant_model_etilt_band_key_tolerance]
                                        return antenna_model_profile
                                    except KeyError:
                                        print(
                                            "No profile found for key : {}, trying with tilt tolerance for band : {}".format(
                                                ant_model_etilt_band_key_tolerance, current_band))
                                        for change in range(1, tolerance + 1, 1):
                                            antenna_model_profile = self.search_profile_for_each_change_in_tilt(etilt,
                                                                                                                change,
                                                                                                                _antenna_model_vs_profile_map,
                                                                                                                model,
                                                                                                                current_band)
                                            if antenna_model_profile is not None:
                                                print("Derived antenna-model-profile is = {}".format(
                                                    antenna_model_profile))
                                                return antenna_model_profile
                                        else:
                                            print("No profile was found after changing band to {}".format(current_band))
                                    # common part end
                                else:
                                    return None
            else:
                print("Tilt is = 0 so no more searching for profile")
                return None

    def search_at_lte_carrier_and_cgi_file(self, sd_input_row, lte_carrier_ob,sd_rnc_sector_key, gsi_file_ob, sd_ob_out, n, report, _antenna_model_vs_profile_map,e_tilt_tolerance ):
        # Among the input only n is a immutable object, we need to return the new object referred by n
        try:
            lte_carrier_input = lte_carrier_ob[sd_rnc_sector_key]
            print("Key {} was FOUND into lte_carrier".format(sd_rnc_sector_key))
            # Assuming:  MCC, MNC as FOUND into lte_carrierand Sector-carrier-name should be there in lte-carrier's each record
            mcc = lte_carrier_input['MCC']
            mnc = lte_carrier_input['MNC']
            sector_carrier_name = lte_carrier_input['Sector Carrier Name']
            mcc_mnc_sector_carrier_key = self.get_mcc_mnc_sector_carrier_key(sector_carrier_name, mcc, mnc)
        except KeyError:
            print("Key {} not even found into lte_carrier, so not updating physical data for this sector".format(
                sd_rnc_sector_key))
            report_line = "RNC-Sector\t{0}\thas No match in 1st-level-planner and not even in lte_carrier file".format(
                sd_rnc_sector_key)
            report[sd_rnc_sector_key].append(report_line)
            report_line = "RNC-Sector\t{0}\thas missing fields = NodeB Longitude, NodeB Latitude,Antenna Longitude, Antenna Latitude, Height, Mechanical DownTilt, Azimuth, Antenna Model".format(
                sd_rnc_sector_key)
            report[sd_rnc_sector_key].append(report_line)
            # TODO populate_sd_row_by_blank()
            self.update_input_row_by_blank(sd_input_row)  # This method modify directly the object sd_input_row
            sd_ob_out[n] = sd_input_row
            n += 1
        else:
            print("Key for next level CGI file lookup is {}".format(mcc_mnc_sector_carrier_key))
            try:
                matching_cgi_data_input = gsi_file_ob[mcc_mnc_sector_carrier_key]
            except KeyError:
                print("Key {} was not found into CGI file".format(mcc_mnc_sector_carrier_key))
                report_line = "RNC-Sector\t{0}\tthere was match in lte_carrier, but corresponding ##MCC-MNC-SECTOR_CARRIER## key\t{1}\tnot in GIS file,".format(
                    sd_rnc_sector_key, mcc_mnc_sector_carrier_key)
                report[sd_rnc_sector_key].append(report_line)
                self.report_missing_attributes(report, sd_input_row, sd_rnc_sector_key)
                self.update_input_row_by_blank(sd_input_row)
                sd_ob_out[n] = sd_input_row
                n += 1
            else:
                print("Key {} was FOUND into CGI file, and matching_cgi_data_input is {}".format(
                    mcc_mnc_sector_carrier_key, matching_cgi_data_input))
                self.update_input_row_by_cgi(sd_input_row, matching_cgi_data_input, sd_rnc_sector_key, report, _antenna_model_vs_profile_map, e_tilt_tolerance)
                sd_ob_out[n] = sd_input_row
                n += 1
                self.report_missing_attributes(report, sd_input_row, sd_rnc_sector_key)
        return n

    def remove_special_char(self, input_string):
        special_chars = "-_ /\\?:;+~"
        input_string = input_string
        out_string = ""
        for c in input_string:
            if c not in special_chars:
                out_string += c
        return out_string

    def update_input_row_by_cgi(self, sd_input_row, matching_cgi_row, sd_rnc_sector_key, report, _antenna_model_vs_profile_map, e_tilt_tolerance):
        print("matching_cgi_row = {}".format(matching_cgi_row))
        # print("antenna-model field name from cgi_required_fields = {}".format(self.data_reader_ob.cgi_file_fields_required[9]))
        sd_input_row[self.SD_fields_need_to_update[2]] = matching_cgi_row[self.cgi_file_fields_required[2]]
        sd_input_row[self.SD_fields_need_to_update[3]] = matching_cgi_row[self.cgi_file_fields_required[3]]
        sd_input_row[self.SD_fields_need_to_update[4]] = matching_cgi_row[self.cgi_file_fields_required[4]]
        sd_input_row[self.SD_fields_need_to_update[5]] = matching_cgi_row[self.cgi_file_fields_required[5]]
        height = matching_cgi_row[self.cgi_file_fields_required[6]]
        if isinstance(height, str):
            print("Report: Incorrect input for height {}, updating by 0.0 ".format(height))
            sd_input_row[self.SD_fields_need_to_update[6]] = float("0.0")
        else:
            sd_input_row[self.SD_fields_need_to_update[6]] = height

        mtilt = matching_cgi_row[self.cgi_file_fields_required[7]]
        if isinstance(mtilt, str):
            print("Report: Incorrect input for height {}, updating by 0.0 ".format(mtilt))
            sd_input_row[self.SD_fields_need_to_update[7]] = float("0.0")
        else:
            sd_input_row[self.SD_fields_need_to_update[7]] = mtilt

        azimuth = matching_cgi_row[self.cgi_file_fields_required[8]]
        if isinstance(azimuth, str):
            print("Report: Incorrect input for height {}, updating by 0.0 ".format(azimuth))
            sd_input_row[self.SD_fields_need_to_update[8]] = float("0.0")
        else:
            sd_input_row[self.SD_fields_need_to_update[8]] = azimuth
        # 9th field is antenna-model, 10th field was a late requirement so remain un-arranged
        active_status = matching_cgi_row[self.cgi_file_fields_required[12]]
        if active_status.upper() == 'ACTIVE':
            sd_input_row[self.SD_fields_need_to_update[10]] = 'true'
        else:
            sd_input_row[self.SD_fields_need_to_update[10]] = 'false'
        tower_type = matching_cgi_row[self.cgi_file_fields_required[13]]
        if tower_type != 'IBS':
            in_building = 'False'
        else:
            in_building = 'True'
        sd_input_row[self.SD_fields_need_to_update[11]] = in_building

        antenna_model = self.remove_special_char(matching_cgi_row[self.cgi_file_fields_required[9]])
        antenna_e_tilt = matching_cgi_row[self.cgi_file_fields_required[10]]
        band: int = matching_cgi_row[self.cgi_file_fields_required[11]] # only numbers are extracted from band by reader method
        print("band derived from cgi_row is {}".format(band))
        antenna_model_antenna_e_tilt_key = "{}-{}-{}".format(antenna_model, antenna_e_tilt, band)

        try:
            antenna_model_profile = self.get_profile_for_a_model_etilt_band_key(antenna_model, antenna_e_tilt, band,
                                                                                _antenna_model_vs_profile_map,
                                                                                tolerance=e_tilt_tolerance)
        except :
            print(
                "Profile from planner {} was not found into source of profiles files, trying with competitive antenna-model".format(
                    antenna_model_antenna_e_tilt_key))
            # TODO try with compititive antenna model
            try:
                compititive_ant_model = self.competitive_ant_model_dict[antenna_model]
                antenna_model_antenna_e_tilt_key = "{}-{}-{}".format(compititive_ant_model, antenna_e_tilt, band)
                print("Lookup Key with competitive antenna-model is = {}".format(antenna_model_antenna_e_tilt_key))
                antenna_model_profile = self.get_profile_for_a_model_etilt_band_key(compititive_ant_model,
                                                                                    antenna_e_tilt, band,
                                                                                    _antenna_model_vs_profile_map,
                                                                                    tolerance=e_tilt_tolerance)
                if antenna_model_profile is None:
                    print("Profile from planner {} was not found into source of profiles files".format(
                        antenna_model_antenna_e_tilt_key))
                    sd_input_row[self.SD_fields_need_to_update[9]] = 'dummy/dummy'
                else:
                    sd_input_row[self.SD_fields_need_to_update[9]] = antenna_model_profile
            except ValueError as ve:
                print(ve)
                print("Ignoring exception while looking for a profile, updating by dummy/dummy")
                sd_input_row[self.SD_fields_need_to_update[9]] = 'dummy/dummy'
            except KeyError:
                print("No competitive antenna-model was found, updating by dummy/dummy")
                sd_input_row[self.SD_fields_need_to_update[9]] = 'dummy/dummy'

        else:
            if antenna_model_profile is None:
                print(
                    "Antenna-Model from planner {} was not found into source of profiles files, trying with competitive antenna-model".format(
                        antenna_model_antenna_e_tilt_key))
                # TODO try with compititive antenna model
                try:
                    compititive_ant_model = self.competitive_ant_model_dict[antenna_model]
                    antenna_model_antenna_e_tilt_key = "{}-{}-{}".format(compititive_ant_model, antenna_e_tilt, band)
                    print("Lookup Key with competitive antenna-model is = {}".format(antenna_model_antenna_e_tilt_key))
                    antenna_model_profile = self.get_profile_for_a_model_etilt_band_key(compititive_ant_model,
                                                                                        antenna_e_tilt, band,
                                                                                        _antenna_model_vs_profile_map,
                                                                                        tolerance=e_tilt_tolerance)
                    if antenna_model_profile is None:
                        print("Competitive Antenna-Model {} was not found into source of profiles files".format(
                            antenna_model_antenna_e_tilt_key))
                        sd_input_row[self.SD_fields_need_to_update[9]] = 'dummy/dummy'
                    else:
                        sd_input_row[self.SD_fields_need_to_update[9]] = antenna_model_profile
                except ValueError as ve:
                    print(ve)
                    print("Ignoring exception while looking for a profile, updating by dummy/dummy")
                    sd_input_row[self.SD_fields_need_to_update[9]] = 'dummy/dummy'
                except KeyError:
                    print("No competitive antenna-model was found for {}, so more searching, updating by dummy/dummy".format(antenna_model))
                    sd_input_row[self.SD_fields_need_to_update[9]] = 'dummy/dummy'
            else:
                sd_input_row[self.SD_fields_need_to_update[9]] = antenna_model_profile

    def update_input_row_by_planner(self, sd_input_row, planner_input_row, _antenna_model_vs_profile_map_local, e_tilt_tolerance):  # It will work on the row found on that occation.
        print("Planner input row is : {}".format(planner_input_row))
        sd_input_row[self.SD_fields_need_to_update[2]] = planner_input_row[self.planner_fields_required[2]]
        sd_input_row[self.SD_fields_need_to_update[3]] = planner_input_row[self.planner_fields_required[3]]
        sd_input_row[self.SD_fields_need_to_update[4]] = planner_input_row[self.planner_fields_required[4]]
        sd_input_row[self.SD_fields_need_to_update[5]] = planner_input_row[self.planner_fields_required[5]]
        height = planner_input_row[self.cgi_file_fields_required[6]]
        if isinstance(height, str):
            print("Report: Incorrect input for height {}, updating by 0.0 ".format(height))
            sd_input_row[self.SD_fields_need_to_update[6]] = float("0.0")
        else:
            sd_input_row[self.SD_fields_need_to_update[6]] = height

        mtilt = planner_input_row[self.cgi_file_fields_required[7]]
        if isinstance(mtilt, str):
            print("Report: Incorrect input for height {}, updating by 0.0 ".format(mtilt))
            sd_input_row[self.SD_fields_need_to_update[7]] = float("0.0")
        else:
            sd_input_row[self.SD_fields_need_to_update[7]] = mtilt

        azimuth = planner_input_row[self.cgi_file_fields_required[8]]
        if isinstance(azimuth, str):
            print("Report: Incorrect input for height {}, updating by 0.0 ".format(azimuth))
            sd_input_row[self.SD_fields_need_to_update[8]] = float("0.0")
        else:
            sd_input_row[self.SD_fields_need_to_update[8]] = azimuth
        # print("sd_input_row_updated = {}".format(sd_input_row))
        # We populate antenna/profile at antenna-Model field
        antenna_model = self.remove_special_char(planner_input_row[self.planner_fields_required[9]])
        antenna_e_tilt = planner_input_row[self.planner_fields_required[10]]
        alphanumeric_band = planner_input_row[self.planner_fields_required[11]]
        band = self.remove_all_except_number(alphanumeric_band)
        print("Band is : {}".format(band))
        antenna_model_antenna_e_tilt_key = "{}-{}-{}".format(antenna_model, antenna_e_tilt, band)
        try:
            antenna_model_profile = self.get_profile_for_a_model_etilt_band_key(antenna_model, antenna_e_tilt, band, _antenna_model_vs_profile_map_local, tolerance=e_tilt_tolerance)
            if antenna_model_profile is None:
                print("Profile from planner {} was not found into source of profiles files, trying with competitive antenna-model".format(
                    antenna_model_antenna_e_tilt_key))
                # TODO try with compititive antenna model
                try:
                    compititive_ant_model = self.competitive_ant_model_dict[antenna_model]
                    antenna_model_antenna_e_tilt_key =  "{}-{}-{}".format(compititive_ant_model, antenna_e_tilt, band)
                    print("Competitive antenna_model_antenna_e_tilt_key is = {}".format(antenna_model_antenna_e_tilt_key))
                    antenna_model_profile = self.get_profile_for_a_model_etilt_band_key(compititive_ant_model, antenna_e_tilt, band, _antenna_model_vs_profile_map_local, tolerance=e_tilt_tolerance)
                    if antenna_model_profile is None:
                        print("Profile from planner {} was not found into source of profiles files".format(
                            antenna_model_antenna_e_tilt_key))
                        sd_input_row[self.SD_fields_need_to_update[9]] = 'dummy/dummy'
                    else:
                        sd_input_row[self.SD_fields_need_to_update[9]] = antenna_model_profile
                except ValueError:
                    print("Ignoring exception while looking for a profile, updating by dummy/dummy")
                    sd_input_row[self.SD_fields_need_to_update[9]] = 'dummy/dummy'
                except KeyError:
                    print("No competitive antenna-model was found, updating by dummy/dummy")
                    sd_input_row[self.SD_fields_need_to_update[9]] = 'dummy/dummy'
            else:
                sd_input_row[self.SD_fields_need_to_update[9]] = antenna_model_profile
        except ValueError:
            print("Ignoring exception while looking for a profile, updating by dummy/dummy")
            sd_input_row[self.SD_fields_need_to_update[9]] = 'dummy/dummy'

    def update_input_row_by_blank(self, sd_input_row: dict):  # This method modify directly the object, sd_input_row
        print("No match found for sector {}, updating fields by 0, or 0.0 or dummy/dummy based on their data type".format(sd_input_row[self.SD_fields_need_to_update[1]]))
        sd_input_row[self.SD_fields_need_to_update[2]] = float("0.0")   # 'NodeB Longitude'
        sd_input_row[self.SD_fields_need_to_update[3]] = float("0.0")   # 'NodeB Latitude'
        sd_input_row[self.SD_fields_need_to_update[4]] = float("0.0")   # 'Antenna Longitude'
        sd_input_row[self.SD_fields_need_to_update[5]] = float("0.0")   # 'Antenna Latitude'
        sd_input_row[self.SD_fields_need_to_update[6]] = int("0")   # 'Height'
        sd_input_row[self.SD_fields_need_to_update[7]] = int("0")   # 'Mechanical DownTilt'
        sd_input_row[self.SD_fields_need_to_update[8]] = int("0")   # 'Azimuth'
        sd_input_row[self.SD_fields_need_to_update[9]] = 'dummy/dummy'   # 'Antenna Model'
        sd_input_row[self.SD_fields_need_to_update[10]] = int("0")  # 'Active'

    @staticmethod
    def get_mcc_mnc_sector_carrier_key(sector_carrier_name, mcc, mnc):
        if "-" in sector_carrier_name:
            required_part_of_sector_carrier = sector_carrier_name.split('-')
            required_part_of_sector_carrier_1 = required_part_of_sector_carrier[1]
            required_part_of_sector_carrier_2 = required_part_of_sector_carrier[2]
            mcc_mnc_sector_carrier_key = '{0}{1}{2}{3}'.format(mcc, mnc, required_part_of_sector_carrier_1,
                                                                   required_part_of_sector_carrier_2)
        else:
            print("Found NOKIA GIS format of sector_carrier_name = {}".format(sector_carrier_name))
            sector_carrier_name = int(sector_carrier_name)
            int_part = sector_carrier_name // 256
            required_part_of_sector_carrier_1 = str(int_part)
            remainder = sector_carrier_name.__mod__(256)
            required_part_of_sector_carrier_2 = str(remainder)
            mcc_mnc_sector_carrier_key = '{0}{1}{2}{3}'.format(mcc, mnc, required_part_of_sector_carrier_1,
                                                                   required_part_of_sector_carrier_2)
        return mcc_mnc_sector_carrier_key

    def report_missing_attributes(self, report_dict, sd_input_row,sd_rnc_sector_key ):
        missing_attributes = []
        for index in range(2, 10):
            field_name =self.SD_fields_need_to_update[index]
            field_value = sd_input_row[self.SD_fields_need_to_update[index]]
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

    def update_sd_by_planner_step1(self, profile_root_path_p, e_tilt_tolerance):
        # TODO if self.planner_file_path or self.cgi_file_path are not provided then need to change some logic to be handled
        sd_ob_out = {}
        report = {}
        n = 0
        # self.planner_or_gis
        if self.planner_or_gis == 'NP' or self.planner_or_gis == 'NPNG':
            planner_object = None
        else:
            planner_object = self.read_planner_file()

        if self.planner_or_gis == 'NG' or self.planner_or_gis == 'NPNG':
            gsi_file_ob = None
            # print(gsi_file_ob)
        else:
            gsi_file_ob = self.read_gsi_file()

        sd_object = self.read_sd_antennas_file()
        lte_carrier_ob = self.read_lte_carrier()
        # Here the planner_object and sd_object are dictionary
        _profile_root_path = profile_root_path_p
        _profile_reader = ProfileReader(_profile_root_path)
        _antenna_model_vs_profile_map = _profile_reader.create_antenna_model_vs_profile_map()
        print("_antenna_model_vs_profile_map from profile directory:- \n {}".format(_antenna_model_vs_profile_map))
        for sd_rnc_sector_key, sd_input_row in sd_object.items():
            if sd_input_row[self.SD_fields_need_to_update[12]] == self.technology:
                report[sd_rnc_sector_key] = []
                # take a key from SD-ob
                if planner_object is not None:
                    try:
                        # search for the key at planner-ob
                        matching_planner_input = planner_object[sd_rnc_sector_key]
                        # Now I have corresponding records from planner and SD, they are OrderDict object
                        print("Match found for {} into planner ".format(sd_rnc_sector_key))
                        planner_input_row = matching_planner_input
                        self.update_input_row_by_planner(sd_input_row, planner_input_row, _antenna_model_vs_profile_map, e_tilt_tolerance)
                        sd_ob_out[n] = sd_input_row
                        n += 1
                        self.report_missing_attributes(report, sd_input_row, sd_rnc_sector_key)
                    except KeyError:
                        print("Key {} not found into Planner ".format(sd_rnc_sector_key))
                        report_line = "RNC-Sector\t{0}\thas No match in 1st-level-planner file, process will look for lte_carrier, and GSI files".format(
                            sd_rnc_sector_key)
                        report[sd_rnc_sector_key].append(report_line)
                        # TODO need to add lookup with lte_carrier and SGI-file
                        if self.planner_or_gis != 'NG' and self.planner_or_gis != 'NPNG':
                            n = self.search_at_lte_carrier_and_cgi_file(sd_input_row, lte_carrier_ob, sd_rnc_sector_key, gsi_file_ob, sd_ob_out, n, report, _antenna_model_vs_profile_map, e_tilt_tolerance=e_tilt_tolerance)
                        else:
                            print("GSI file not provided, so looking for next entry into SD ")
                            continue
                else:
                    if self.planner_or_gis != 'NG' and self.planner_or_gis != 'NPNG':
                        n = self.search_at_lte_carrier_and_cgi_file(sd_input_row, lte_carrier_ob, sd_rnc_sector_key,
                                                                    gsi_file_ob, sd_ob_out, n, report, _antenna_model_vs_profile_map, e_tilt_tolerance=e_tilt_tolerance)
                    else:
                        print("No planner no GIS file provided ")
                        break
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
        print("outpfield_valueut file name is {}".format(out_put_file))
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


# if __name__ == "__main__":
#     print(DataProcessor.remove_special_char("asfddsaf_?;:werqwre_-/\?"))
