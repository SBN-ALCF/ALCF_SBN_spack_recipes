import os
import sys
import json
from versioning_tools import *
import readline
import argparse

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
    if direct_output == "": return "BadURL", "BadURL" # return BadURL for case of bad github url
    match_found = False
    for item in direct_output.split("\n"):
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
    if(len(directories) == 0):
        print("No matching directories found!")
        sys.exit()
    else:
        for directory in directories:
            print("Found directory: ", directory)
            if(input("Use this directory? (y/n/s): ") == "y"): return directory
        print("No directory match! Skipping package.")
        return None

def edit_package_py(package, version, directory, checksum, commit, github_url):
    file = directory+"/package.py"
    new_text = "##########################################################################\n"+\
               "###################### DELETE ME WHEN DONE ###############################\n"+\
               "# Current File: " + file +"\n"+\
               "# Package: " + package +"\n"+\
               "# Requested Version: " + version +"\n"+\
               "# Found Checksum: " + checksum +"\n"+\
               "# corresponding commit: " + commit +"\n"+\
               "# url = \"" + github_url +"\"\n"+\
               "# version(\""+version+"\", sha256=\""+checksum+"\")\n"+\
               "###################### DELETE ME WHEN DONE ###############################\n"+\
               "##########################################################################\n"
    tmp_file_str = "/tmp/"+file.split("/")[-1]+".tmp"
    os.system("{ echo -n '"+new_text+"'; cat "+file+"; } > " + tmp_file_str)
    os.system("mv "+tmp_file_str+" "+ file)
    os.system("vim "+file)

def manual_inputs():
    checksum = 'searching'
    package = input("Enter spack package name: ")
    while(checksum == 'searching'):
        github_url = input_with_prefill("Enter github url: ", "https://github.com/")
        version = input("Enter new version: ")
        checksum, commit = find_version_info(github_url, version)

    directory = find_spack_package(package)
    if (directory != None):
        edit_package_py(package, version, directory, checksum, commit, github_url)

def auto_inputs(input_file):
    for package in input_file.keys():
        checksum = 'searching'
        github_url = ''
        while((checksum == 'searching' or checksum == "BadURL") and github_url != "s"):
            checksum = 'searching' # reset checksum in while loop in case we had BadURL
            github_url = input_with_prefill("Enter "+package+" github url or skip using \"s\": ", "https://github.com/")
            if github_url != "s":
                version = input_file[package][0]['new_version']
                for v in [dot_to_undr(version), undr_to_dot(version), undr_to_dash(version)]:
                    if checksum != "BadURL": # if we have a bad url, don't bother with different version formats.
                        checksum, commit = find_version_info(github_url, v)
                        if checksum != 'searching': 
                            version = v
                            break
            
        if (github_url != "s" and checksum != "BadURL"):
            edit_package_py(package, version, input_file[package][0]['location'], 
                            checksum, commit, github_url)
        elif github_url == "s":
            print("Skipping "+package+" by request")
        else:
            print("No spack recipe for "+package+". Skipping!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for updating spack packages.")
    parser.add_argument('-i', '--input', type=str, help="Input json file of packages which need updates. Output of check_installed.py.")
    args = parser.parse_args()

    if args.input is not None:
        with open(args.input) as f:
            auto_inputs(json.load(f))
    else:
       manual_inputs()
