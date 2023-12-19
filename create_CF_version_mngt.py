import datetime
import subprocess
from program_mode import get_developer, get_program_mode, set_developer


# Global version information
global version_info
# Automatic version update and descritption system
# version_info = {
#     "major": 0,
#     "minor": 0,
#     "stage": 'T',  # 'T' for Test, 'P' for Production
#     "description": ""
# }
def read_latest_version_info(filename="GoogleSheetAPI_version_info.log"):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1]
                # Example line format: "Version 0.1-T: Description - Timestamp"
                parts = last_line.split(": ")
                version_part, descr_part = parts[0], parts[1].split(" - ")[0]
                
                # Extracting major and minor version numbers and stage
                version_number, stage = version_part.split(" ")[1].split("-")
                major, minor = version_number.split(".")

                return {"major": int(major), "minor": int(minor), "stage": stage, "description": descr_part}
    except FileNotFoundError:
        return {"major": 0, "minor": 0, "stage": 'T', "description": ""}  # Default values if file not found
    
version_info = read_latest_version_info()

# def commit_and_push_version_update(version_info):
#     if get_developer:
#         os.system("git add .")  # Stages all changes in the working directory for the next commit
#         commit_message = f"Update to version {version_info['major']}.{version_info['minor']}-{version_info['stage']}"
#         os.system(f'git commit -m "{commit_message}"')  # Commit the staged changes with a message
#         os.system("git push origin master")  # Push the commit to the remote repository

def run_command(command):
    try:
        result = subprocess.run(command, check=True, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def commit_and_push_version_update(version_info):
    if get_developer():
        # Check for unstaged changes
        if run_command("git status --porcelain"):
            # Stages all changes in the working directory for the next commit
            run_command("git add .")
            commit_message = f"Update to version {version_info['major']}.{version_info['minor']}-{version_info['stage']}"
            # Commit the staged changes with a message
            if run_command(f'git commit -m "{commit_message}"'):
                # Push the commit to the remote repository
                run_command("git push origin master")
            else:
                print("Commit failed. No changes to push.")
        else:
            print("No changes to commit.")

def CF_report_major(descr, TorP):
    global version_info
    TorP = validate_stage(TorP)
    if description_changed(descr):
        version_info["major"] += 1
        version_info["minor"] = 0
        version_info["stage"] = TorP
        version_info["description"] = descr
        append_version_info_to_log()  # Log the version update
        commit_and_push_version_update(version_info)
    return f'{version_info["major"]}.{version_info["minor"]}-{version_info["stage"]}'

def CF_report_minor(descr, TorP):
    global version_info
    TorP = validate_stage(TorP)
    # Check if trying to transition from test (T) to production (P) in a minor update
    if version_info["stage"] == 'T' and TorP == 'P':
        raise ValueError("Transition from test to production must be a major update.")

    # Increment minor version if description changes
    if description_changed(descr):
        version_info["minor"] += 1
        version_info["stage"] = TorP
        version_info["description"] = descr
        append_version_info_to_log()  # Log the version update
        commit_and_push_version_update(version_info)
    return f'{version_info["major"]}.{version_info["minor"]}-{version_info["stage"]}'

def validate_stage(TorP):
    if TorP in ['T', 'P', 'D']:
        return TorP
    else:
        raise ValueError("TorP must be 'T' for test or 'P' for production, or 'D' for development.")
    
def append_version_info_to_log(filename="CF_report_generator_version_info.log"):
    global version_info
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(filename, "a") as file:
        version_string = f"Version {version_info['major']}.{version_info['minor']}-{version_info['stage']}: {version_info['description']} - {current_time}\n"
        file.write(version_string)


def get_version_number():
    """
    returns the version number as a string. Format Major.Minor-Stage
    """
    version_info = read_latest_version_info()
    version_composed = str(version_info['major']) + '.' + str(version_info['minor']) + '-' + str(version_info['stage'])
    return version_composed

def description_changed(descr):
    old_descr = read_latest_version_info()
    print(f'old descrip[tion: {old_descr}, new description: {descr}]')
    return descr != old_descr['description']


# if __name__ == '__main__':
#     version_info = read_latest_version_info()
#     version_composed = str(version_info['major']) + '.' + str(version_info['minor']) + '-' + str(version_info['stage'])
#     print(version_composed)
#     # # Example of updating the version
#     # new_description = "New feature added"
#     # version = CF_report_minor(new_description, 'T')
#     # print(f'Version CF_report_major {version}')


if __name__ == '__main__':
    # GitHub repository
    # https://github.com/HarrydeBont/xxx


    set_developer()
    # Administer the version description
    tester, developer, foo = get_program_mode()
    if developer:
        version_info = read_latest_version_info()
        version = CF_report_minor("test2", 'D')
    print(f'Version CF_report_major {version}')