# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Lardataalg(CMakePackage, FnalGithubPackage):
    """Lardataalg"""

    repo = "LArSoft/lardataalg"
    version_patterns = ["v09_00_00", "09.17.00"]


    # version("10.00.00", sha256="4ffbad40ad4dd5c4db0b7249eabd602644f536585dc86880f52f155a94438395")
    version("09.17.03", sha256="51097ce209b23101a05ea4b50b7ec5e936ba1762985f5f996d5f4de6b9cbe911")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    depends_on("boost+test")
    depends_on("canvas")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("fhicl-cpp")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("lardataobj")
    depends_on("messagefacility")
    depends_on("nusimdata")
    depends_on("root")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_build_environment(self, env):
        prefix = Prefix(self.build_directory)
        env.prepend_path("PATH", prefix.bin)
        env.prepend_path("FHICL_FILE_PATH", prefix.job)

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)
