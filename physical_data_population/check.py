print(type(True))
import os
current_dir = os.path.abspath(os.path.dirname(__file__))
consolidated_antenna_files = os.path.join(current_dir, "temp_artifact\\from_compl_conf")

print(consolidated_antenna_files)
