# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Larreco(CMakePackage, FnalGithubPackage):
    """Larreco"""

    repo = "LArSoft/larreco"
    version_patterns = ["v09_00_00", "09.23.09"]

    version("10.01.12", sha256="c6dfdcfd9e769a307d9f68b13689a4dbb5e22ebe76807a4192425b61c65eb128")
    version("10.01.09", sha256="095b37678ea454eb69096ffa39e9155ad95bf4cf58d4e5e002459c4f3d3ca446")
    version("10.01.08", sha256="31599864d63280b42d668c1af0b7deec919e64d7c7824b9660d56f12e925498b")
    version("10.01.06", sha256="08a8d460fbfa2a9ebbfff38b639239adbee3c735dc3e239abacddff10808be36")
    version("10.00.00", sha256="9f2c5febc9d3215bd4dcbd85273c0c4d7267d78c1ec5716adc003726f6e01205")
    version("09.26.02", sha256="27eb51df70238fbea3b2745f770c29e3a606ec5dbf63b9d12c412c3a9a2e250c")
    version("09.25.00", sha256="cae4f414b02a61d2cc0e1f915f71c0a6337418737e2939be0d01df931e73bc77")
    version("09.25.04", sha256="b9bafb8d36856351f4d5b4d47bf6075eb9fa8d28ebbb9f226efa3a33b2e42fd3")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("boost")
    depends_on("canvas-root-io", when="@:09.25.00.01")
    depends_on("cetlib-except")
    depends_on("cetlib")
    depends_on("clhep")
    depends_on("eigen")
    depends_on("fhicl-cpp")
    depends_on("geant4")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataalg")
    depends_on("lardataobj")
    depends_on("lardata")
    depends_on("larsim")
    depends_on("larvecutils")
    depends_on("messagefacility")
    depends_on("nug4")
    depends_on("nurandom")
    depends_on("nusimdata")
    depends_on("range-v3")
    depends_on("root+tmva")
    depends_on("rstartree")
    depends_on("tbb")

    patch('09.25.00.patch', when='@09.25.00')

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
            self.define("RStarTree_INCLUDE_DIR", self.spec["rstartree"].prefix.include),
        ]

    @sanitize_paths
    def setup_build_environment(self, env):
        prefix = Prefix(self.build_directory)
        env.prepend_path("PATH", prefix.bin)  # Binaries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", prefix.job)

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)
