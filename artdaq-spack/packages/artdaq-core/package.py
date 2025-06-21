# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *
from spack.package import *


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)

class ArtdaqCore(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq_core/archive/refs/tags/v3_09_04.tar.gz"
    git = "https://github.com/art-daq/artdaq_core.git"
    
    version("v3_11_00", commit="5dcbc0400e6bedd10f43e8201e7fc32fff0be5a9")
    version("v3_10_03", commit="32e7447b789e6e1a376ff9e1653e2e5510e8dcc1")
    version("v3_10_02", commit="aec92f2c0d0889e14f60e089eb2326e42b6bf2a0")
    version("3.10.02", commit="aec92f2c0d0889e14f60e089eb2326e42b6bf2a0")
    version("v3_10_01", commit="7d6acf8b30342e1046ae9efdfd3d1b85ba678834")
    version("v3_09_16", sha256="07f6b6d5e26350089976b820f62bbee37a3361e94c4e4f1f8d62a276e388bb9b")
    version("v3_09_15", sha256="08404c2592292cd9e90bb3e1a0999e62d05412a2a0c949982a24ada43b900388")
    version("v3_09_13", sha256="53b952cc973d6ba1bceeeafa874e8d56758f41f6362b0244999cbb9749906051")
    version("v3_09_12", sha256="267a9da649d7ea5e38a5e710f1c680b65eb701b0e8bbb9b4896bbf01309558b4")
    version("v3_09_11", sha256="8d4e413bbe09c786e85e48246f87133205910b94312e66152b0baf7444d9c0c6")
    version("v3_09_09", sha256="c4a820a26f9fb3a5d3fc4a25e53f0dc4a2d15fb5594264c3e50bd0936f232c77")
    version("v3_09_08", sha256="5689cdf8384276835be9dfd50489917d3729242833f9f2da115445d9245978b2")
    version("v3_09_07", sha256="3bf9285171c86e9f039e5d48a99b577544ab4a17d6f4a4f1a79d6bfb797eeede")
    version("v3_09_04", sha256="8d4315e0ebe7b663d171352d8e08dd87393d34319f672837eb8c93ea83b8ba63")
    version("develop", branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@:v3_09_12"            
    )
    variant(
        "cxxstd",
        default="20",
        values=("17", "20"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@v3_09_12:"            
    )
        
    variant("doc", default=False, description="Build documentation with Doxygen.")

    # art dependencies
    depends_on("canvas-root-io")
    depends_on("cetmodules", type="build")

    # artdaq dependencies
    depends_on("trace+mf")
    depends_on("doxygen", when="+doc")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq_core/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]
        if os.path.exists("CMakePresets.cmake"):
            args.extend(["--preset", "default"])
        else:
            self.define("artdaq_core_OLD_STYLE_CONFIG_VARS", True)
        return args

    def setup_build_environment(self, env):
        if self.spec.satisfies("~doc"):
            env.set("DISABLE_DOXYGEN", 1)

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")
