#!/usr/bin/env spack-python
import argparse
import json

import spack
import llnl
from llnl.util import tty
from llnl.string import plural
from spack.util.format import get_version_lines
from spack.cmd.checksum import add_versions_to_package

def all_versioning_styles(v):
    return [dot_to_undr(v), undr_to_dot(v), undr_to_dash(v), patch(dot_to_undr(v))]

def undr_to_dot(version):
    return version.replace("_",".").replace("v","",1)

def dot_to_undr(version):
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

def custom_checksum(package, version):
    spec = spack.spec.Spec(package)
    pkg: PackageBase = spack.repo.PATH.get_pkg_class(spec.name)(spec)
    url_dict: Dict[StandardVersion, str] = {} 
    url = pkg.find_valid_url_for_version(version)
    if url is not None:
        url_dict[version] = url

    url_changed_for_version = set()
    for version, url in url_dict.items():
        possible_urls = pkg.all_urls_for_version(version)
        if url not in possible_urls:
            for possible_url in possible_urls:
                if web_util.url_exists(possible_url):
                    url_dict[version] = possible_url
                    break
            else:
                url_changed_for_version.add(version)

    if not url_dict:
        return False
    elif len(url_dict) > 1:
        filtered_url_dict = spack.stage.interactive_version_filter(
            url_dict,
            pkg.versions,
            url_changes=url_changed_for_version,
            initial_verion_filter=spec.versions,
        )
        if not filtered_url_dict:
            exit(0)
        url_dict = filtered_url_dict
    else:
        tty.info(f"Found {llnl.string.plural(len(url_dict), 'version')} of {pkg.name}")

    version_hashes = spack.stage.get_checksums_for_versions(
        url_dict, pkg.name, keep_stage=False, fetch_options=pkg.fetch_options
    )
    version_lines = get_version_lines(version_hashes, url_dict)

    path = spack.repo.PATH.filename_for_package_name(pkg.name)
    add_versions_to_package(pkg, version_lines, True)

    return True

def auto_inputs(input_file):
    for package in input_file.keys():
        version = input_file[package][0]['new_version']
        for v in all_versioning_styles(version):
            if(custom_checksum(package, v)):
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for updating spack packages.")
    parser.add_argument('-i', '--input', type=str, help="Input json file of packages which need updates. Output of check_installed.py.")
    args = parser.parse_args()

    # leave room for addition of manual inputs later.
    if args.input is not None:
        with open(args.input) as f:
            auto_inputs(json.load(f))
