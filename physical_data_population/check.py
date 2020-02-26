import os
current_dir = os.path.abspath(os.path.dirname(__file__))
consolidated_antenna_files = os.path.join(current_dir, "temp_artifact\\from_compl_conf")

print(consolidated_antenna_files)

path = r"D:\D_drive_BACKUP\MENTOR\Airtel\For_Analysis\test\HBXX-6516DS-VTM_Port 1 +45_00DT_1785.txt"
# path = r"D:\D_drive_BACKUP\MENTOR\Airtel\For_Analysis\Airtel Production Antenna Model\LDX-6516DS-VTM\LBX-6515DS-VTM_900_00.txt"


def check_return(n):
    for i in range(10):
        if i == n:
            return i
        else:
            continue


band = '2100'
bands = ['900', '1800', '2100', '2300']
band_position = bands.index(band)
min_band_index = 0
max_band_index = 3

print(band_position)

if band_position == min_band_index:
    for band_index1 in range(min_band_index+1, max_band_index+1, 1):
        print(bands[band_index1])

elif band_position == max_band_index:
    for band_index2 in range(max_band_index-1, min_band_index-1, -1):
        print(bands[band_index2])

else:
    for band_index3 in range(band_position+1, max_band_index+1, 1):
        print(bands[band_index3])

    for band_index4 in range(band_position-1, min_band_index-1, -1):
        print(bands[band_index4])



