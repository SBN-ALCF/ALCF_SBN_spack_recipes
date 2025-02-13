import os
import sys
from dataclasses import dataclass

def undr_to_dot(version):
    return version.replace("_",".").replace("v","",1)

def dot_to_undr(version):
    return "v"+version.replace(".","_") 

def undr_to_dash(version):
    return version.replace("_","-") 

def GetSpackLoc(name):
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

    # Check builtin for undr
    tmp = os.popen("find ../spack/var/spack/repos/builtin/packages -type d -name \'"+name+"\'").read()
    if(tmp):
        return tmp.rstrip()

    # Check builtin for dashed
    tmp = os.popen("find ../spack/var/spack/repos/builtin/packages -type d -name \'"+undr_to_dash(name)+"\'").read()
    if(tmp):
        return tmp.rstrip()

    print("No spack package match found for: ", name)

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

def GetPackages(input_file):
    Manifest = []
    with open(input_file) as f:
        for line in f:
            if line:
                name = line.split()[0]
                package = line.split()[1]
                Manifest.append(Package(name, package))
    return Manifest

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if(sys.argv[1] == '-h' or sys.argv[1] == "--help"):
            print("Usage: -i, --input")
            exit()
        elif(sys.argv[1] == '-i' or sys.argv[1] == "--input"):
            input_file = sys.argv[2]
        else:
            print("Unknown parameter(s): ", sys.argv)
            exit()
    Manifest = GetPackages(input_file)
