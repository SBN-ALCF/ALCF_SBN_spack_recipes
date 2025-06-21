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

sys.path.insert(1, '/grand/neutrinoGPU/software/spack_builds/ALCF_SBN_spack_recipes')
from versioning_tools import *

def GetSpackStyle(package, manifest_version):
    spec = spack.spec.Spec(package)
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.fullname)
    pkg = pkg_cls(spec)
    spack_pkg = 'empty'
    i = 0

    while not any(char.isdigit() for char in spack_pkg):
        spack_pkg = list(pkg.versions.keys())[i].string
        i += 1
    ret = manifest_version
    if '.' in spack_pkg:
        ret = undr_to_dot(ret)
    elif '_' in spack_pkg:
        ret = dot_to_undr(ret)
        if(spack_pkg[0] == 'v' and ret[0] != 'v'):
            ret = 'v' + ret
        elif(spack_pkg[0] != 'v' and ret[0] == 'v'):
            ret = ret[1:]
    return ret

def GetSpackName(name):
    # spack does not use underscore in packages
    name = undr_to_dash(name)
    if name in renamed_packages.keys():
        name = renamed_packages[name]

    try:
        spec = spack.spec.Spec(name)
        spack.repo.PATH.get_pkg_class(spec.fullname)
        return name, True
    except:
        print("No spack package match found for: ", name,", trying py-* variant...")

    try:
        spec = spack.spec.Spec('py-'+name)
        spack.repo.PATH.get_pkg_class(spec.fullname)
        return 'py-'+name, True
    except:
        print("No spack package match found for: ", name)

    return name, False

def GetSpackVersion(self, manifest_version):
    # If version has been identified as weird exception
    # just use what is in the dict verbatim. Otherwise
    # check style of previous versions.
    if self.name in renamed_versions and manifest_version in renamed_versions[self.name].keys():
        version = renamed_versions[self.name][manifest_version]
    else:
        version = GetSpackStyle(self.name, manifest_version)

    spec = spack.spec.Spec(self.name)
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.fullname)
    pkg = pkg_cls(spec)
    avail = pkg.versions.keys()

    if version in [a.string for a in avail]:
        return version, True

    if patch(version) in [a.string for a in avail]:
        return version, True

    print("No spack version match found for: ", self.name , version)
    return version, False

class SpackPackage:
    name: str
    version: str
    manifest_name: str
    manifest_version: str
    found_package: bool
    found_version: bool

    def __init__(self, manifest_name: str, manifest_version: str):
        self.manifest_name = manifest_name
        self.manifest_version = manifest_version
        self.name, self.found_package = GetSpackName(manifest_name)
        if self.found_package:
            self.version, self.found_version = GetSpackVersion(self, manifest_version)
        else:
            self.version = None
            self.found_version = False

class ManifestPackage:
    name: str
    version: str
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version

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
        OutDict.update({p.name: p.version})

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
        single_package = SpackPackage(package.name, package.version)

        if single_package.name in ignorable_packages:
            continue

        if(not single_package.found_package):
            MissingPackages.append(single_package.manifest_name)
        elif(not single_package.found_version):
            MissingVersions.append(single_package)
        else:
            FoundVersions.append(single_package)
    return FoundVersions, MissingVersions, MissingPackages

def OutputFinishedSpec(packages, output_file):
    return_str = ''
    for package in packages:
        if(not package.name+"@" in return_str):
           if package.name == "sbndcode" or package.name == "icaruscode":
               print("Creating spec for " + package.name)
               return_str = package.name + "@"+ package.version + return_str
           elif package.name == "root":
                return_str += " ^" + package.name + "@" + package.version +" cxxstd==17 ~jemalloc +spectrum ~davix ~postgres"
           elif package.name == "wirecell":
                return_str += " ^" + package.name + "@" + package.version +" +root +cuda +torch ~emacs"
           elif package.name == "py-torch":
                return_str += " ^" + package.name + "@" + package.version +" cuda_arch=80 "
           elif package.name == "larsoft":
                return_str += " ^" + package.name + "@" + package.version +" ^cmake ~qtgui "
           #elif package.name == "pythia8":
           #     return_str += " ^" + package.name + "@" + package.version +" ~evtgen "

           else:
               return_str += " ^" + package.name + "@"+ package.version

    return_str += " ^openmpi schedulers=none" # openmpi gets included as dep of pytorch. turn off schedulers for this.
    print("Final spec output to:", output_file)
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
                for m in MissingPackages:
                    print("Some packages do not have spack packages:")
                    print(m)
