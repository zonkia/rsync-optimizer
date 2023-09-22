import os
import subprocess
import time

parent_dir = "/mnt/source"
destination_dir = "/mnt/destination"
script_path = os.path.dirname(os.path.abspath(__file__))
exceptions = ["#recyle"]

try:
    with open(f'{script_path}/already_done.txt', encoding='utf8') as f:
        lines = f.readlines()
    already_done_from_file = lines[0].split(",")
except:
    lines = ""
    already_done_from_file = []

already_done = set()

for file in already_done_from_file:
    filename = file.replace("{'","").replace("'}","").replace(" '","")
    if "'" == filename[-1]:
        filename = filename[:-1]
    already_done.add(filename)

os.chdir(os.path.abspath(parent_dir))
folders = sorted(os.listdir())

for folder in folders:
    if folder in already_done or os.path.isfile(os.path.abspath(folder)) or folder in exceptions:
        print(folder, "already in list\n---")
        continue
    os.chdir(os.path.abspath(folder))
    subfolders = sorted(os.listdir())
    for subfolder in subfolders:
        if str(folder + "/" + subfolder) in already_done or folder in exceptions or subfolder in exceptions:
            print(folder + "/" + subfolder + " already in list\n---")
            continue
        if os.path.isfile(os.path.abspath(subfolder)):
            #subfolder is file!
            result = "Error"
            print(f"---\nRSYNC file: {folder}/{subfolder}")
            while result != "Ok":
                result = str(subprocess.run(['rsync', '--ignore-existing',  '-vrh', f'/{parent_dir}/{folder}/{subfolder}', f'/{destination_dir}/{folder}/'], check=False).returncode).replace("0", "Ok")
                if result != "Ok":
                    time.sleep(5)
            already_done.add(str(folder + "/" + subfolder))
            with open(f'{script_path}/already_done.txt', 'w', encoding='utf8') as file:
                file.write(str(already_done))
            continue
        os.chdir(os.path.abspath(subfolder))
        print(os.listdir())
        subsubfolders = sorted(os.listdir())
        for subsubfolder in subsubfolders:
            if str(folder + "/" + subfolder + "/" + subsubfolder) in already_done or folder in exceptions or subfolder in exceptions or subsubfolder in exceptions:
                print(folder + "/" + subfolder + "/" + subsubfolder + " already in list\n---")
                continue
            result = "Error"
            print(f"---\nRSYNC directory: {folder}/{subfolder}/{subsubfolder}")
            subprocess.run(['mkdir', '-p', f'{destination_dir}/{folder}'], check=False)
            while result != "Ok":
                result = str(subprocess.run(['rsync', '--ignore-existing',  '-vrh', f'{parent_dir}/{folder}/{subfolder}/{subsubfolder}', f'{destination_dir}/{folder}/{subfolder}/'], check=False).returncode).replace("0", "Ok")
                if result != "Ok":
                    time.sleep(5)
            already_done.add(str(folder + "/" + subfolder + "/" + subsubfolder))
            with open(f'{script_path}/already_done.txt', 'w', encoding='utf8') as file:
                file.write(str(already_done))
        os.chdir(os.path.abspath(f'{parent_dir}/{folder}'))
    os.chdir(os.path.abspath(parent_dir))
    already_done.add(str(folder))
    with open(f'{script_path}/already_done.txt', 'w', encoding='utf8') as file:
        file.write(str(already_done))

