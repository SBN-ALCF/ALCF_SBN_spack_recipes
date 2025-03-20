import os
import sys
from dataclasses import dataclass
import json
import argparse
from versioning_tools import *

ignorable_packages = [
        "cigetcert",
        "cigetcertlibs",
        "jobsub_client",
        "kx509",
        "mrb",
        "sbndutil",
        "ups",
        "upd",
        "gitflow",
        "larbatch",
        "toyExperiment", # https://github.com/drbenmorgan/fnal-toyExperiment/tree/develop
        "fhiclpy", # literally just 4 cmake files, not in official larsoft spack
        "larutils", # scripts only, not in offical larsoft spack
        "golang", # not in official larsoft spack
        "guideline_sl", # not in offifial larsoft spack
        "studio", # not in offifial larsoft spack
        "inclxx", # putting this here for now... unsure if needed or not.
        ]

# some packages have slightly different names on ups vs spack
renamed_packages = {
        "g4neutron" : "g4ndl", # G4NDL
        "g4nucleonxs" : "g4saiddata", # G4SAIDDATA
        "g4nuclide" : "g4ensdfstate", # G4ENSDFSTATE
        "g4photon" : "g4photonevaporation", # G4PhotonEvaporation
        "g4radiative" : "g4radioactivedecay", # G4RadioactiveDecay
        "g4surface" : "g4realsurface", # G4RealSurface
        "catch" : "catch2", 
        "delaunator" : "delaunator-cpp",
        "fhiclcpp" : "fhicl-cpp",
        "gojsonnet" : "go-jsonnet",
        "libtorch" : "py-torch", # libtorch comes with py-torch
        "pythia" : "pythia6",
        "range" : "range-v3",
        "tbb" : "intel-tbb",
        "TRACE" : "trace"
        }

# this is done in a way that agrees with scisoft spack builds
renamed_versions = {
        "cry" : {"v1_7q" : "v1_7"},
        "dk2nudata" : {"v01_10_01h" : "v01_10_01"},
        "dk2nugenie" : {"v01_10_01r" : "v01_10_01"},
        "eigen" : {"v23_08_01_66e8f" : "3.4.0"},
        "geant4" : {"v4_10_6_p01g" : "10.6.1"},
        "genie" : {"v3_04_02a" : "v3_04_02"},
        "grpc" : {"v1_35_0c" : "v1_35_0"},
        "hdf5" : {"v1_12_2a" : "1.14.3"}, # match version used in their spack builds
        "jsoncpp" : {"v1_9_5a" : "v1_9_5"},
        "py-torch" : {"v2_1_1b" : "v2_1_1"}, # also disagrees btwn spack and ups?
        "libwda" : {"v2_30_0a" : "v2_30_0"},
        "log4cpp" : {"v1_1_3e" : "v1_1_3"},
        "marley" : {"v1_2_1d" : "v1_2_1"},
        "pandora" : {"v03_16_00l" : "v03_16_00"},
        "protobuf" : {"v3_21_12a" : "v3_21_12"},
        "pygccxml" : {"v2_2_1b" : "v2_2_1"},
        "pythia8" : {"v8_3_10" : "8.311"},
        "pythia6" : {"v6_4_28x" : "v6_4_28"},
        "range-v3" : {"v3_0_12_0" : "v0_12_0"},
        "rstartree" : {"v2016_07" : "0.2"},
        "scitokens" : {"v1_0_1a" : "1.1.1"}, # also disagrees btwn spack and ups
        "sqlite" : {"v3_40_01_00" : "3.43.2"}, # also disagrees btwn spack and ups
        "srproxy" : {"v00.44" : "00.44"}, 
        "torch_scatter" : {"v2_1_2a" : "2_1_2"}, 
        "triton" : {"v2_25_0d" : "23.09"}, # don't understand this naming convention... 
        "xerces_c" : {"v3_2_3e" : "v3_2_3"}, 
        "xrootd" : {"v5_5_5a" : "5.6.9"} # also disagrees btwn spack and ups
        }

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
    tmp = os.popen("grep -oz \"version(\\s*\\\""+ self.version_undr + "\" " + self.spack_loc + "/package.py").read()
    if(tmp):
        return self.version_undr
    elif(not tmp):
        tmp = os.popen("grep  -oz \"version(\\s*\\\""+ self.version_dot + "\" " + self.spack_loc + "/package.py").read()
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
                if name in renamed_packages.keys():
                    name = renamed_packages[name]
                if(not name in ignorable_packages):
                    package = line.split()[1]
                    if name in renamed_versions:
                        if package in renamed_versions[name]:
                            package = renamed_versions[name][package]
                    Manifest.append(Package(name, package))
    return Manifest

# Output json with info for packages which need updates
def OutputUnfinishedJson(input_file, output_file):
    OutDict = {}
    for package in input_file:
        if package.spack_version == None:
            OutDict.update({package.name: [{"new_version":package.version_dot,
                                           "location":package.spack_loc}]})
    if len(OutDict) > 0:
        if not (output_file == None):
            print("Some packages need updates. Saved these to: NeedsUpdate-" + output_file)
            with open("NeedsUpdate-"+output_file+".json", 'w') as f:
                json.dump(OutDict, f, indent=4)
        else:
            print("Some packages need updates. Printing since no output given.")
            print(json.dumps(OutDict))
        return True
    else:
        return False

def OutputFinishedSpec(packages, output_file):
    return_str = ''
    for package in packages:
        if not package.spack_version == None:
            if package.name == "sbndcode" or package.name == "icaruscode":
                print("Creating spec for " + package.name)
                return_str = package.name + "@"+ package.spack_version + return_str
            else:
                return_str += " ^" + package.name + "@"+ package.spack_version + return_str
    with open(output_file, 'w') as f:
        f.write(return_str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for checking for \
                                     available versions of spack packages.")

    parser.add_argument('-i', '--input', type=str, help="Input manifest from \
                        pullProducts. Might change to another input format later...")

    parser.add_argument('-o', '--output', type=str, help="Output file. \
                        Two files output: NeedsUpdate-{your output} and \
                        {your output} corresponding to packages which need \
                        an update and all packages. These are inputs to \
                        update_packages.py and spec_maker.py respectively.")

    parser.add_argument('-f', '--force', action=argparse.BooleanOptionalAction, 
                        help="Force output spec. Normally, a spec will only \
                        be output if no packages or versions are missing. \
                        This argument overrides it.")

    args = parser.parse_args()

    if args.input is not None:
        Manifest = GetPackages(args.input)
        returned_unfinished = OutputUnfinishedJson(Manifest, args.output)
        if not returned_unfinished or args.force:
            OutputFinishedSpec(Manifest, args.output)
