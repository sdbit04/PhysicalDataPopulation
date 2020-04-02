import csv
from pyxlsb import *
import xlrd
import os


class FileReader(object):

    def __init__(self, technology: str, lte_carrier_path,sd_file_path,planner_file_path,cgi_file_path, competitive_model_path, planner_or_gis: str = "", gis_type='airtel_kol'):
        self.lte_carrier_path = lte_carrier_path
        self.cgi_file_path = cgi_file_path
        self.planner_file_path = planner_file_path
        self.sd_file_path = sd_file_path
        self.technology = technology
        self.planner_or_gis = planner_or_gis
        self.gis_type = gis_type
        self.competitive_model_path = competitive_model_path
        print(self.technology)
        print(self.planner_or_gis)
        print(self.gis_type)

        if self.technology.upper() == 'LTE' and self.planner_or_gis == "" and self.gis_type == 'airtel_kol':
            # Note - Please don't insert any value into the below lists, the index of the fields are used in program
            self.SD_fields_need_to_update = ['RNC Id', 'Sector Name', 'NodeB Longitude', 'NodeB Latitude','Antenna Longitude', 'Antenna Latitude', 'Height', 'Mechanical DownTilt', 'Azimuth', 'Antenna Model', 'Active', 'In Building', 'Technology']
            self.planner_fields_required = ['RNC Id', 'Sector Name', 'eNodeB Longitude', 'eNodeB Latitude','Antenna Longitude', 'Antenna Latitude', 'Height', 'Mechanical DownTilt','Azimuth', 'Antenna Model', 'Antenna Tilt-Electrical', 'Band']
            # Note - Please don't insert any value into the below lists, the index of the fields are used in program
            # TODO based on formula lat long calculation will be done from GIS
            self.cgi_file_fields_required = ['LTE CGI', 'dummy', 'Longitude', 'Latitude', 'Longitude', 'Latitude',                       'Antenna Height (m)', 'Mechanical DownTilt', 'Azimuth', 'Antenna Model', 'Antenna Tilt-Electrical', 'Band', 'Status Active / Locked', 'Tower Type']
            self.lte_carrier_fields_required = ['TAC', 'Sector Name', 'MCC', 'MNC', 'Sector Carrier Name']
            # Note - Please don't insert any value into the below lists, the index of the fields are used in program
        elif self.technology.upper() == 'LTE' and self.planner_or_gis == "NG" and self.gis_type == 'airtel_kol':
            # Note - Please don't insert any value into the below lists, the index of the fields are used in program
            self.SD_fields_need_to_update = ['RNC Id', 'Sector Name', 'NodeB Longitude', 'NodeB Latitude','Antenna Longitude', 'Antenna Latitude', 'Height', 'Mechanical DownTilt', 'Azimuth', 'Antenna Model', 'Active', 'In Building', 'Technology']
            self.planner_fields_required = ['RNC Id', 'Sector Name', 'eNodeB Longitude', 'eNodeB Latitude','Antenna Longitude', 'Antenna Latitude', 'Height', 'Mechanical DownTilt', 'Azimuth', 'Antenna Model', 'Antenna Tilt-Electrical', 'Band']
            # Note - Please don't insert any value into the below lists, the index of the fields are used in program
            # TODO based on formula lat long calculation will be done from GIS
            self.cgi_file_fields_required = ['LTE CGI', 'dummy', 'Longitude', 'Latitude', 'Longitude', 'Latitude',                       'Antenna Height (m)', 'Mechanical DownTilt', 'Azimuth', 'Antenna Model', 'Antenna Tilt-Electrical', 'Band', 'Status Active / Locked', 'Tower Type']
            self.lte_carrier_fields_required = ['TAC', 'Sector Name', 'MCC', 'MNC', 'Sector Carrier Name']
            # Note - Please don't insert any value into the below lists, the index of the fields are used in program
        elif self.technology.upper() == 'LTE' and self.planner_or_gis == "NP" and self.gis_type == 'airtel_kol':
            # Note - Please don't insert any value into the below lists, the index of the fields are used in program
            self.SD_fields_need_to_update = ['RNC Id', 'Sector Name', 'NodeB Longitude', 'NodeB Latitude','Antenna Longitude', 'Antenna Latitude', 'Height', 'Mechanical DownTilt', 'Azimuth', 'Antenna Model', 'Active', 'In Building', 'Technology']
            self.planner_fields_required = ['RNC Id', 'Sector Name', 'eNodeB Longitude', 'eNodeB Latitude','Antenna Longitude', 'Antenna Latitude', 'Height', 'Mechanical DownTilt', 'Azimuth', 'Antenna Model', 'Antenna Tilt-Electrical', 'Band']
            # Note - Please don't insert any value into the below lists, the index of the fields are used in program
            # TODO based on formula lat long calculation will be done from GIS
            self.cgi_file_fields_required = ['LTE CGI', 'dummy', 'Longitude', 'Latitude', 'Longitude', 'Latitude',                       'Antenna Height (m)', 'Mechanical DownTilt', 'Azimuth', 'Antenna Model', 'Antenna Tilt-Electrical', 'Band', 'Status Active / Locked', 'Tower Type']
            self.lte_carrier_fields_required = ['TAC', 'Sector Name', 'MCC', 'MNC', 'Sector Carrier Name']
            # Note - Please don't insert any value into the below lists, the index of the fields are used in program
        else:
            raise ("{} technology is not supported ".format(self.technology))

    def remove_all_except_number(self, alphanumeric_input):
        numeric_out = ''
        for c in alphanumeric_input:
            if c.isnumeric():
                numeric_out = "{0}{1}".format(numeric_out, c)
        return numeric_out

    def csv_from_excel(self, xlsx_file_path, csv_file_path):
        technology = self.technology
        wb = xlrd.open_workbook(xlsx_file_path)
        sh = wb.sheet_by_name(technology)
        with open(csv_file_path, 'w') as your_csv_file:
            wr = csv.writer(your_csv_file)
            for rownum in range(sh.nrows):
                wr.writerow(sh.row_values(rownum))

    def __validate_fields(self, csv_sd_planner_path):
        # csv_sd_planner_path = csv_sd_planner_path
        if self.technology.upper() == 'UMTS':
            # check if all the fields at SD_fields_need_to_update are into the file
            return True
        elif self.technology.upper() == 'LTE':
            # check if all the fields at SD_fields_need_to_update are into the file
            return True

    def __read_csv_sd(self, csv_sd_path):
        """
        read planner file and return a dictionary having RNC-ID and Sector-name as key for each row of the input csv
        :param csv_sd_path:
        :param separator:
        :return:
        """
        # TODO at present I have only UMTS data
        sd_dict_out = {}
        with open(csv_sd_path, mode='r', encoding='utf-8') as sd_ob:
            # As we know the delimiter for parsed SD antennas.txt is tab, So I made it hard coded
            sd_dict = csv.DictReader(sd_ob, delimiter='\t')
            for row in sd_dict:
                rnc_id_sector_key = "{}-{}".format(row[self.SD_fields_need_to_update[0]],
                                                   row[self.SD_fields_need_to_update[1]])
                sd_dict_out[rnc_id_sector_key] = row
            return sd_dict_out

    def __read_csv_planner(self, csv_planner_path):
        """
        read planner file and return a dictionary having RNC-ID and Sector-name as key for each row of the input csv
        :param csv_planner_path:
        :param separator:
        :return:
        """
        planner_dict_out = {}
        try:
            with open(csv_planner_path, mode='r') as sd_ob:
                # , encoding='utf-8'
                # As we convert the planner.xlsx file into a tab delimited file, So I made it hard coded in next line
                # sd_dict = csv.DictReader(sd_ob, delimiter='\t')
                sd_dict = csv.DictReader(sd_ob, delimiter=',')
                print(sd_dict)
                for row in sd_dict:
                    print(row)
                    rnc_id_sector_key = "{}-{}".format(row[self.planner_fields_required[0]],
                                                       row[self.planner_fields_required[1]])
                    # Insert data into dict, having rnc_id_sector_key as key for each top level dict item
                    planner_dict_out[rnc_id_sector_key] = row
                return planner_dict_out
        except UnicodeDecodeError:
            with open(csv_planner_path, mode='r', encoding='utf-8') as sd_ob:
                sd_dict = csv.DictReader(sd_ob, delimiter='\t')
                for row in sd_dict:
                    rnc_id_sector_key = "{}-{}".format(row[self.planner_fields_required[0]],
                                                       row[self.planner_fields_required[1]])
                    # Insert data into dict, having rnc_id_sector_key as key for each top level dict item
                    planner_dict_out[rnc_id_sector_key] = row
                return planner_dict_out

    def read_sd_antennas_file(self):
        if self.__validate_fields(self.sd_file_path):
            sd_dict_out = self.__read_csv_sd(self.sd_file_path)
            return sd_dict_out
        else:
            raise NotImplementedError("SD input file was not valid, should be in tab separated csv file")

    def read_planner_file(self):
        currnet_path = os.path.dirname(__file__)
        print("current path = {}".format(currnet_path))
        temp_csv_file_path = os.path.join(currnet_path, "temp_artifact\\planner\\planner.csv")
        print("temp_csv_file_path = {}".format(temp_csv_file_path))
        self.csv_from_excel(self.planner_file_path, temp_csv_file_path)

        if self.__validate_fields(temp_csv_file_path):
            planner_dict_out = self.__read_csv_planner(temp_csv_file_path)
            return planner_dict_out
        else:
            raise NotImplementedError("Planner Input file was not valid, should be in tab separated csv file")

    def read_lte_carrier(self):
        lte_carrier_dict_out = {}
        try:
            with open(self.lte_carrier_path, 'r') as lte_carrier_ob:
                lte_carrier_dict = csv.DictReader(lte_carrier_ob, delimiter='\t')
                # print(lte_carrier_dict.__next__())
                for row in lte_carrier_dict:
                    lte_carrier_rncid_sector_key = "{}-{}".format(row[self.lte_carrier_fields_required[0]],
                                                                  row[self.lte_carrier_fields_required[1]])
                    # TODO In the line below, I have assigned whole row to the key, I can only assign required fields
                    lte_carrier_dict_out[lte_carrier_rncid_sector_key] = row
            return lte_carrier_dict_out
        except:
            raise Exception("Lte_carrier file was not readable")

    def read_gsi_file(self):
        file_path = self.cgi_file_path
        col_name_position = {}
        data_dict = {}
        with open_workbook(file_path) as GSI_file:
            sheet = GSI_file.get_sheet(1)  # Index of first row is 1
            rows_iter = iter(sheet.rows())
            head_row = next(rows_iter)  # Header record only
            for cell in head_row:  # Speed linearly depends on number of columns into the GSI file
                if cell.v == self.cgi_file_fields_required[0]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[1]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[2]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[3]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[4]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[5]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[6]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[7]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[8]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[9]:
                    col_name_position[cell.v] = cell.c

                elif str(cell.v).__contains__(self.cgi_file_fields_required[10]):
                    print("CGI 10th field is {}".format(self.cgi_file_fields_required[10]))
                    # print(str(cell.v))
                    col_name_position[self.cgi_file_fields_required[10]] = cell.c
                elif cell.v == self.cgi_file_fields_required[11]:
                    col_name_position[cell.v] = cell.c
                elif cell.v == self.cgi_file_fields_required[12]:
                    col_name_position[cell.v] = cell.c
                elif str(cell.v).__contains__(self.cgi_file_fields_required[13]):
                    col_name_position[self.cgi_file_fields_required[13]] = cell.c
                else:
                    pass
            # Following statement will print the header with their column position as key:value pair
            print(col_name_position)

            for row in rows_iter:  # accessing all data rows
                col_name_data = {}  # dict for each data row
                # print(row[22])
                # print(row[3])  ==>  Cell(r=1, c=3, v='EKOL0000KONG')
                tower_type = None
                for col_name, position in col_name_position.items():
                    cell_object_1 = row[position]
                    # Note tower type
                    if col_name == self.cgi_file_fields_required[13]:
                        tower_type = str(cell_object_1.v)

                for col_name, position in col_name_position.items():  # Seems a quadratic, but this iteration is
                    # constant in count
                    cell_object = row[position]  # getting the cell using cell_position as an index of row, it is a constant
                    # time operation, output like -> Cell(r=1, c=3, v='EKOL0000KONG')
                    # Next Band should be replaced by index of cgi_fields

                    if col_name == self.cgi_file_fields_required[11] and cell_object.v is not None:
                        # print(int(cell.v))
                        # print("band read from cgi, and before removing nonnumeric  is {}".format(cell_object.v))
                        band = self.remove_special_char(str(cell_object.v))
                        # print("band read from cgi, and after removing nonnumeric  is {}".format(band))
                        col_name_data[col_name] = int(band.split(".")[0])
                    # TODO Next etilt is, this value need some exception handling
                    elif col_name == self.cgi_file_fields_required[10] and cell_object.v is not None and cell_object.v != 'NA':
                        # print("etilt is {}".format(cell_object.v), end="\t")
                        etilt = self.remove_special_char(str(cell_object.v))
                        try:
                            col_name_data[col_name] = int(etilt.split(".")[0])
                        except ValueError:
                            print("Etilt {} was not valid, setting it as 0".format(cell_object.v))
                            col_name_data[col_name] = 0
                    elif col_name == self.cgi_file_fields_required[0] and cell_object.v is not None:
                        # print(col_name)
                        lte_cgi = str(cell_object.v)
                        # print(lte_cgi)
                        lte_cgi_striped = self.remove_all_except_number(lte_cgi)
                        # print("lte_cgi_stipped = {}".format(lte_cgi_striped))
                        col_name_data[col_name] = lte_cgi_striped
                    elif col_name == self.cgi_file_fields_required[7]:
                        mtilt = cell_object.v
                        if tower_type == "IBS" or tower_type.lower() == "indoor":
                            try:
                                mtilt = float(mtilt)
                            except ValueError:
                                mtilt = float("0.0")
                        else:
                            try:
                                mtilt = float(mtilt)
                            except ValueError:
                                mtilt = str(mtilt)  # TODO This string into mtilt need to be handled during updation of antennas.txt
                        col_name_data[col_name] = mtilt
                    elif col_name == self.cgi_file_fields_required[6]:
                        hight = cell_object.v
                        if tower_type == "IBS" or tower_type.lower() == "indoor":
                            try:
                                hight = float(hight)
                            except ValueError:
                                hight = float("0.0")
                        else:
                            try:
                                hight = float(hight)
                            except ValueError:
                                hight = str(hight)  # TODO This string into mtilt need to be handled during updation of antennas.txt
                        col_name_data[col_name] = hight
                    elif col_name == self.cgi_file_fields_required[8]:
                        azimuth = cell_object.v
                        if tower_type == "IBS" or tower_type.lower() == "indoor":
                            try:
                                azimuth = float(azimuth)
                            except ValueError:
                                azimuth = float("0.0")
                        else:
                            try:
                                azimuth = float(azimuth)
                            except ValueError:
                                azimuth = str(azimuth)  # TODO This string into mtilt need to be handled during updation of antennas.txt
                        col_name_data[col_name] = azimuth
                    elif col_name == self.cgi_file_fields_required[2]:
                        longitude = cell_object.v
                        if longitude == "" or longitude is None or longitude == "NA":
                            longitude = float("0.0")
                        else:
                            longitude = float(longitude)
                        col_name_data[col_name] = longitude
                    elif col_name == self.cgi_file_fields_required[3]:
                        latitude = cell_object.v
                        if latitude == "" or latitude is None or latitude == "NA":
                            latitude = float("0.0")
                        else:
                            latitude = float(latitude)
                        col_name_data[col_name] = latitude

                    else:
                        col_name_data[col_name] = str(cell_object.v)
                # Next line we are making the first field 'LTE_CGI' as key for each record
                data_dict["{0}".format(col_name_data[self.cgi_file_fields_required[0]])] = col_name_data
        return data_dict

    def remove_special_char(self, input_string):
        input_string = input_string
        out_string = ""
        special_char = "_-/ ?+~"
        for c in input_string:
            if c not in special_char:
                out_string += c
        return out_string

    def read_competitive_model_list(self):
        competitive_model_dist = {}
        try:
            with open(self.competitive_model_path, 'r') as competitive_model_ob:
                model_list = competitive_model_ob.readlines()
                for line in model_list:
                    line = line.strip("\n")
                    line_items = line.split(":")
                    existing_model = self.remove_special_char(line_items[0])
                    comp_model = self.remove_special_char(line_items[1])
                    competitive_model_dist[existing_model] = comp_model
        except TypeError:
            return {}
        else:
            return competitive_model_dist


if __name__ == "__main__":
    # CGI_file = "D:\\D_drive_BACKUP\\Study\\PycharmProjects\\PhysicalDataPopulation\\Input_data_deep\\New\\4G GIS Data Kolkata.xlsb"
    # lte_carrier = "D:\\D_drive_BACKUP\\Study\\PycharmProjects\\PhysicalDataPopulation\\Input_data_deep\\New\\lte-carriers.txt"
    # planner_file = "D:\\D_drive_BACKUP\\Study\\PycharmProjects\\PhysicalDataPopulation\\Input_data_deep\\Planning_input_4G.txt"
    # competitive_model = "D:\\D_drive_BACKUP\MENTOR\\Airtel\\For_Analysis\\Competitive_model\\competitive_profile.txt"
    # reader = FileReader(technology='LTE', lte_carrier_path=lte_carrier, sd_file_path=lte_carrier, planner_file_path=lte_carrier, cgi_file_path=CGI_file, competitive_model_path=competitive_model )
    # competitive_model_dict = reader.read_competitive_model_list()
    # print(competitive_model_dict)
    dir = os.path.dirname(__file__)
    print(dir)