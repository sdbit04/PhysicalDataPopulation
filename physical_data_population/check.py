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


print(check_return(70))

