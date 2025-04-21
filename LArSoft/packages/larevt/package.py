# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Larevt(CMakePackage, FnalGithubPackage):
    """Larevt"""

    repo = "LArSoft/larevt"
    version_patterns = ["v09_00_00", "09.10.00"]

    version("10.00.06", sha256="cb0720f23589d757ef00876b3898a87e0fad451191553b145e398c686614e9d6") # FIXME
    version("10.00.05", sha256="772d2c9cf891d1abc3920c8e9f627560feec2871c9c9a0763d68832033259444") # FIXME
    version("09.10.07", sha256="f8827eee1aec519a7b13c11460b505278df00fcd911abd008001fdf64dcf5762")
    version("09.10.03", sha256="3165ae94c7dab00d5e783be9c63a485ebbca435d9d43f0e19d6b822e98a17c3c")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("canvas-root-io", when="@:09.10.03")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("fhicl-cpp")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataobj")
    depends_on("lardata")
    depends_on("libwda")
    depends_on("messagefacility")
    depends_on("nusimdata")
    depends_on("root")
    depends_on("sqlite")

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
        ]

    @sanitize_paths
    def setup_build_environment(self, env):
        prefix = Prefix(self.build_directory)
        env.prepend_path("PATH", prefix.bin)  # Binaries
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)
