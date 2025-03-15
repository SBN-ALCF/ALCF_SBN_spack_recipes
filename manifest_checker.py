import os
import sys
from dataclasses import dataclass
import json
from versioning_tools import *

def GetSpackLoc(name):
    print("Searching for "+name)
    # Check ALCF_SBN_spack_recipes for undr
    tmp = os.popen("find . -type d -name \'"+name+"\'").read()
    if(tmp):
        for t in tmp.split():
            if "mirrors" not in t:
                tmp = t
        return tmp.rstrip()

    # Check ALCF_SBN_spack_recipes for dashed
    tmp = os.popen("find . -type d -name \'"+undr_to_dash(name)+"\'").read()
    if(tmp):
        for t in tmp.split():
            if "mirrors" not in t:
                tmp = t
        return tmp.rstrip()

    # Check ALCF_SBN_spack_recipes for dashed python packages
    tmp = os.popen("find . -type d -name \'py-"+undr_to_dash(name)+"\'").read()
    if(tmp):
        for t in tmp.split():
            if "mirrors" not in t:
                tmp = t
        return tmp.rstrip()

    # Check builtin for undr
    tmp = os.popen("find ../spack/var/spack/repos/builtin/packages -type d -name \'"+name+"\'").read()
    if(tmp):
        return tmp.rstrip()

    # Check builtin for dashed
    tmp = os.popen("find ../spack/var/spack/repos/builtin/packages -type d -name \'"+undr_to_dash(name)+"\'").read()
    if(tmp):
        return tmp.rstrip()

    # Check builtin for dashed python packages
    tmp = os.popen("find ../spack/var/spack/repos/builtin/packages -type d -name \'py-"+undr_to_dash(name)+"\'").read()
    if(tmp):
        return tmp.rstrip()

    print("No spack package match found for: ", name)
    return None

def GetSpackVersion(self):
    tmp = os.popen("grep \"version(\\\""+ self.version_undr + "\" " + self.spack_loc + "/package.py").read()
    if(tmp):
        return self.version_undr
    elif(not tmp):
        tmp = os.popen("grep \"version(\\\""+ self.version_dot + "\" " + self.spack_loc + "/package.py").read()
        if(tmp):
            return self.version_dot
        else:
            print("No spack version match found for: ", self.name , self.version_undr)
            return None

@dataclass
class Package:
    name: str
    version_dot: str
    version_undr: str
    spack_loc: str
    spack_version: str

    def __init__(self, name: str, version: str):
        self.name = name
        self.version_undr = version
        self.version_dot = undr_to_dot(version) 
        tmp = GetSpackLoc(name)
        if(tmp): 
            self.spack_loc = tmp
            self.spack_version = GetSpackVersion(self)
        else:
            self.spack_loc = None
            self.spack_version = None

def GetPackages(input_file):
    Manifest = []
    with open(input_file) as f:
        for line in f:
            if line:
                name = line.split()[0]
                package = line.split()[1]
                Manifest.append(Package(name, package))
    return Manifest

def OutputJson(input_file, output_file):
    OutDict = {}
    for package in input_file:
        if package.spack_version == None:
            OutDict.update({package.name: [{"new_version":package.version_dot,
                                           "location":package.spack_loc}]})
    if not (output_file == None):
        with open(output_file, 'w') as f:
            json.dump(OutDict, f, indent=4)
    else:
        print(json.dumps(OutDict))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if(sys.argv[1] == '-h' or sys.argv[1] == "--help"):
            print("Usage: -i, --input \n\
                          -o, --output")
            exit()

        if(sys.argv[1] == '-i' or sys.argv[1] == "--input"):
            input_file = sys.argv[2]
            output_file = None
        else:
            print("Unknown parameter(s): ", sys.argv)
            print("Usage: -i, --input \n\
                          -o, --output")
            exit()

        if(sys.argv[3] == '-o' or sys.argv[3] == "--output"):
            output_file = sys.argv[4]

    Manifest = GetPackages(input_file)
    OutputJson(Manifest, output_file)
