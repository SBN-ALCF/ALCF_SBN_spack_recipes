import os
import sys

def find_version_info(github_url, requested_version):
    direct_output = os.popen("git -c 'versionsort.suffix=-' ls-remote --tags --sort='v:refname' " + github_url + ".git").read()
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
    print(directories)
    if(len(directories) == 0):
        print("No matching directories found!")
        sys.exit()
    else:
        for directory in directories:
            print("Found directory: ", directory)
            if(input("Use this directory? (y/n): ") == "y"): return directory

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if(sys.argv[1] == '-h' or sys.argv[1] == "--help"):
            print("Usage: No inputs currently. Runs in CLI.")
        else:
            print("Unknown parameter(s): ", sys.argv)
    checksum = 'searching'
    while(checksum == 'searching'):
        github_url = input("Enter github url: ")
        version = input("Enter new version: ")
        checksum, commit = find_version_info(github_url, version)
    package = input("Enter spack package name: ")
    directory = find_spack_package(package)
    file = directory+"/package.py"
    new_text = "##########################################################################\n"+\
               "###################### DELETE ME WHEN DONE ###############################\n"+\
               "# Current File: " + file +"\n"+\
               "# Package: " + package +"\n"+\
               "# Requested Version: " + version +"\n"+\
               "# Found Checksum: " + checksum +"\n"+\
               "# Found Commit: " + commit +"\n"+\
               "# version(\""+version+"\", sha256=\""+checksum+"\")\n"+\
               "###################### DELETE ME WHEN DONE ###############################\n"+\
               "##########################################################################\n"
    tmp_file_str = "/tmp/"+file.split("/")[-1]+".tmp"
    os.system("{ echo -n '"+new_text+"'; cat "+file+"; } > " + tmp_file_str)
    os.system("mv "+tmp_file_str+" "+ file)
    os.system("vim "+file)
