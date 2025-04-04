#!/usr/bin/env spack-python
import argparse
import json
import sys
import os

import spack
import llnl
from llnl.util import tty
from llnl.string import plural
from spack.util.format import get_version_lines
from spack.cmd.checksum import add_versions_to_package
from spack.version import VersionList, GitVersion
import spack.fetch_strategy as fs
from urllib.request import urlretrieve
from urllib.request import urlparse
from urllib.request import urlsplit


sys.path.insert(1, '/grand/neutrinoGPU/software/spack_builds/ALCF_SBN_spack_recipes')
from versioning_tools import *

def UpdateGH(pkg, github_url, version):
    checksum = 'searching'
    commit, tag = find_version_info(github_url, version)
    version_lines = "    version(\""+version+"\",commit=\""+commit+"\", tag=\""+tag+"\")"
    add_versions_to_package(pkg, version_lines, False)
    sys.exit()

def find_version_info(github_url, requested_version):
   direct_output = os.popen("git -c 'versionsort.suffix=-' ls-remote --tags --sort='v:refname' " + github_url).read()
   if direct_output == "": return "BadURL", "BadURL" # return BadURL for case of bad github url
   match_found = False
   for item in direct_output.split("\n"):
       if any([v in item for v in all_versioning_styles(requested_version)]):
           match_found = True
           commit = item.strip().split()[0]
           matching_version = item.strip().split()[1].split('/')[-1]
           return commit, matching_version
   if not match_found:
       print("Version "+requested_version+" not found!")
       return 'searching', 'searching'

def add_checksum(package, version):
    spec = spack.spec.Spec(package)
    pkg: PackageBase = spack.repo.PATH.get_pkg_class(spec.name)(spec)

    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    pref = VersionList(pkg_cls.versions).preferred()
    if isinstance(fs.for_package_version(pkg, pref), spack.fetch_strategy.GitFetchStrategy):
        UpdateGH(pkg, pkg_cls.git_base, version)
        return True

    url_dict: Dict[StandardVersion, str] = {} 
    url = pkg.find_valid_url_for_version(version)

    if url is not None:
        url_dict[version] = url
    else:
        remote_versions = pkg.fetch_remote_versions()
        if version in remote_versions:
            url_dict[version] = remote_versions[version]

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

    add_versions_to_package(pkg, version_lines, False)
    sys.exit()

    return True

def auto_inputs(input_file):
    for package in input_file.keys():
        version = input_file[package]
        print("Grabbing: ", package, version)
        if(not add_checksum(package, version)):
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for updating spack packages.")
    parser.add_argument('-i', '--input', type=str, help="Input json file of packages which need updates. Output of check_installed.py.")
    args = parser.parse_args()

    # leave room for addition of manual inputs later.
    if args.input is not None:
        with open(args.input) as f:
            auto_inputs(json.load(f))
