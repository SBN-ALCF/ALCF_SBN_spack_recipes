# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *
from spack.package import *


class OtsdaqComponents(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/otsdaq_components/archive/refs/tags/v2_06_08.tar.gz"
    git = "https://github.com/art-daq/otsdaq_components.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v2_08_02", commit="3b4c2043bee1409df8922b900e5e07e6358c842a")
    version("v2_08_01", commit="3be5282e5ed9d525c36df3ca5967e5942b09077c")
    version("v2_08_00", commit="75945ea1fc9f363e2a01bfb61d31c599d880069d")
    version("v2_07_00", sha256="8f0b7056b6d7a8030fa172fe606ee57b103feabebcc4417646a6e828e24622ce")
    version("v2_06_11", sha256="4c2a970a6b4a69fd64766b48aa4fb500ef3f50599d88fce2ef841541dd0dfabd")
    version("v2_06_10", sha256="8ddb188223df272c295b0745d4c9e3a6f33a7fdad624506a781d622d64ea9616")
    version("v2_06_09", sha256="425a6dcc78394f2fa46a70cac1cd9f627846a024c71e9335ff69518be6d5482e")
    version("v2_06_08", sha256="59bdb4fd6aab1fc97072890824530cf8c9db7e57bd9d9647faf8f32aaaada4a5")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/otsdaq_components/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@:v2_06_10"        
    )
    variant(
        "cxxstd",
        default="20",
        values=("17", "20"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
        when="@v2_06_10:"        
    )

    depends_on("cetmodules", type="build")

    depends_on("otsdaq")
    depends_on("otsdaq-utilities")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]
        if os.path.exists("CMakePresets.cmake"):
            args.extend(["--preset", "default"])
        else:
            self.define("artdaq_core_OLD_STYLE_CONFIG_VARS", True)
        return args


