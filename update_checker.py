import os
import sys
import json
from versioning_tools import *
import readline

def input_with_prefill(prompt, text):
    def hook():
        readline.insert_text(text)
        readline.redisplay()
    readline.set_pre_input_hook(hook)
    result = input(prompt)
    readline.set_pre_input_hook()
    return result

def find_version_info(github_url, requested_version):
    direct_output = os.popen("git -c 'versionsort.suffix=-' ls-remote --tags --sort='v:refname' " + github_url + ".git").read()
    match_found = False
    for item in direct_output.split("\n"):
        print(item)
        if requested_version in item:
            match_found = True
            commit = item.strip().split()[0]
            matching_version = item.strip().split()[1]
            print("Attempting Grab: ", matching_version)

            try:
                os.system("curl -s -L " + github_url + "/archive/"+matching_version+".tar.gz --output "+requested_version+".tar.gz")
                if(os.path.isfile(requested_version+".tar.gz")):
                    checksum = os.popen("sha256sum "+requested_version+".tar.gz").read().split()[0]
                    print("Found checksum: ", checksum)
                    done = input("Use this tag/checksum? (y/n): ")
                    if(done=="y"): return checksum, commit
                    os.system("rm "+requested_version+".tar.gz")
                else:
                    print("Missing file:", matching_version)
            except:
                print("Could not grab: ", matching_version)
    if not match_found:
        print("Version not found!")
        return 'searching', 'searching'

def find_spack_package(package_name):
    directories = os.popen("find . -type d -name \"*"+package_name+"*\"").read().split()
    print(directories)
    if(len(directories) == 0):
        print("No matching directories found!")
        sys.exit()
    else:
        for directory in directories:
            print("Found directory: ", directory)
            if(input("Use this directory? (y/n): ") == "y"): return directory

def edit_package_py(package, version, directory, checksum, commit, github_url):
    file = directory+"/package.py"
    new_text = "##########################################################################\n"+\
               "###################### DELETE ME WHEN DONE ###############################\n"+\
               "# Current File: " + file +"\n"+\
               "# Package: " + package +"\n"+\
               "# Requested Version: " + version +"\n"+\
               "# Found Checksum: " + checksum +"\n"+\
               "# corresponding commit: " + commit +"\n"+\
               "# url = " + github_url +"\n"+\
               "# version(\""+version+"\", sha256=\""+checksum+"\")\n"+\
               "###################### DELETE ME WHEN DONE ###############################\n"+\
               "##########################################################################\n"
    tmp_file_str = "/tmp/"+file.split("/")[-1]+".tmp"
    os.system("{ echo -n '"+new_text+"'; cat "+file+"; } > " + tmp_file_str)
    os.system("mv "+tmp_file_str+" "+ file)
    os.system("vim "+file)

def manual_inputs():
    checksum = 'searching'
    while(checksum == 'searching'):
        github_url = input_with_prefill("Enter github url: ", "https://github.com/")
        version = input("Enter new version: ")
        checksum, commit = find_version_info(github_url, version)
    package = input("Enter spack package name: ")
    directory = find_spack_package(package)
    edit_package_py(package ,version, directory, checksum, commit, github_url)

def auto_inputs(input_file):
    for package in input_file.keys():
        checksum = 'searching'
        while(checksum == 'searching'):
            github_url = input_with_prefill("Enter "+package+" github url: ", "https://github.com/")
            version = input_file[package][0]['new_version']
            for v in [dot_to_undr(version), undr_to_dot(version), undr_to_dash(version)]:
                checksum, commit = find_version_info(github_url, v)
                if checksum != 'searching': break
        edit_package_py(package, version, input_file[package][0]['location'], 
                        checksum, commit, github_url)

if __name__ == "__main__":
    input_file = None
    if len(sys.argv) > 1:
        if(sys.argv[1] == '-h' or sys.argv[1] == "--help"):
            print("Usage: No inputs currently. Runs in CLI.")

        if(sys.argv[1] == '-i' or sys.argv[1] == '--input'):
            print(sys.argv[2])
            with open(sys.argv[2], 'r') as f:
                input_file = json.load(f)
        else:
            print("Unknown parameter(s): ", sys.argv)
    if input_file is None:
        manual_inputs()
    elif input_file is not None:
        auto_inputs(input_file)
