#!/usr/bin/env spack-python
import os
import sys
import json
import argparse

import spack.spec
from spack.spec import Spec
import spack.store
import spack.cmd
import sys
import spack.repo

def undr_to_dot(version):
    return version.replace("_",".").replace("v","",1)

def dot_to_undr(version):
    if not "v" in version:
        return "v"+version.replace(".","_")
    else:
        return version.replace(".","_")

def undr_to_dash(version):
    return version.replace("_","-")

def patch(version):
    splt = version.split("_")
    ret = ""
    for i in range(len(splt)):
        if i != len(splt)-1:
            ret += splt[i]+"_"
        else:
            ret += "p"+splt[i]
    return ret


ignorable_packages = [
        "cigetcert",
        "cigetcertlibs",
        "jobsub_client",
        "jobsub-client",
        "kx509",
        "mrb",
        "sbndutil",
        "ups",
        "upd",
        "gitflow",
        "larbatch",
        "scitokens_cpp",
        "scitokens-cpp",
        "toyExperiment", # https://github.com/drbenmorgan/fnal-toyExperiment/tree/develop
        "fhiclpy", # literally just 4 cmake files, not in official larsoft spack
        "larutils", # scripts only, not in offical larsoft spack
        "golang", # not in official larsoft spack
        "guideline_sl", # not in offifial larsoft spack
        "guideline-sl", # not in offifial larsoft spack
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
        "TRACE" : "trace",
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

def GetSpackVersion(self, manifest_version):
    spec = spack.spec.Spec(self.name)
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.fullname)
    pkg = pkg_cls(spec)
    avail = pkg.versions.keys()

    undr_version = dot_to_undr(manifest_version)
    dot_version = undr_to_dot(manifest_version)

    if self.name in renamed_versions:
        for variation in  [undr_version, dot_version, patch(undr_version), 
                           patch(dot_version)]: 
            if variation in renamed_versions[self.name].keys():
                version = renamed_versions[self.name][manifest_version]
                if version in [a.string for a in avail]:
                    return version

    for variation in [undr_version, dot_version, 
                      patch(undr_version), patch(dot_version)]:
        if variation in [a.string for a in avail]:
            return variation

    print("No spack version match found for: ", self.name , undr_version)
    return None

class SpackPackage:
    name: str
    version: str
    manifest_name: str
    manifest_version: str

    def __init__(self, manifest_name: str, manifest_version: str):
        self.manifest_name = manifest_name
        self.manifest_version = manifest_version
        self.name = GetSpackName(manifest_name)
        if self.name != None:
            self.version = GetSpackVersion(self, manifest_version)
        else:
            self.version = None

class ManifestPackage:
    name: str
    version: str
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version

def GetSpackName(name):
    if name in renamed_packages.keys():
        name = renamed_packages[name]

    name = undr_to_dash(name)
    try:
        spec = spack.spec.Spec(name)
        spack.repo.PATH.get_pkg_class(spec.fullname)
        return name
    except:
        print("Spack package not found, trying py-* prefix...")
    try:
        spec = spack.spec.Spec('py-'+name)
        spack.repo.PATH.get_pkg_class(spec.fullname)
        return 'py-'+name
    except:
        print("No spack package match found for: ", name)
        return None

def GetManifestPackages(input_file):
    ManifestPackages = []
    with open(input_file) as f:
        for line in f:
            if line:
                input_name = line.split()[0]
                version = line.split()[1]
                ManifestPackages.append(ManifestPackage(input_name, version))
    return ManifestPackages

# Output json with info for packages which need updates
def OutputUnfinishedJson(MissingVersions, output_file):
    OutDict = {}

    for p in MissingVersions:
        if p.name in renamed_versions.keys():
            if p.manifest_version in renamed_versions[p.name]:
                OutDict.update({p.name: renamed_versions[p.name][p.manifest_version]})
        else:
            OutDict.update({p.name: p.manifest_version})

    if not (output_file == None):
        print("Some packages need updates. Saved these to: NeedsUpdate-" + output_file)
        with open("NeedsUpdate-"+output_file+".json", 'w') as f:
            json.dump(OutDict, f, indent=4)
    else:
        print("Some packages need updates. Printing since no output given.")
        print(json.dumps(OutDict))

def CheckLocalSpack(ManifestPackages):
    MissingPackages = []
    MissingVersions = []
    FoundVersions = []
    
    for package in ManifestPackages:
        if package.name in ignorable_packages:
            continue

        single_package = SpackPackage(package.name, package.version)
        if(single_package.name == None):
            MissingPackages.append(single_package.manifest_name)
        elif(single_package.version == None):
            MissingVersions.append(single_package)
        else:
            FoundVersions.append(single_package)
    return FoundVersions, MissingVersions, MissingPackages

def OutputFinishedSpec(packages, output_file):
    return_str = ''
    for package in packages:
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

    args = parser.parse_args()

    if args.input is not None:
        Manifest = GetManifestPackages(args.input)
        FoundVersions, MissingVersions, MissingPackages = CheckLocalSpack(Manifest)
        if len(MissingVersions) == 0 and len(MissingPackages) == 0:
            OutputFinishedSpec(FoundVersions, args.output)
        else:
            OutputUnfinishedJson(MissingVersions, args.output)
            if len(MissingPackages) > 0:
                print("Missing Packages:")
                for m in MissingPackages:
                    print(m)
