# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Lardataobj(CMakePackage, FnalGithubPackage):
    """Lardataobj"""

    repo = "LArSoft/lardataobj"
    version_patterns = ["v09_00_00", "09.18.00"]

    version("10.00.04", sha256="07be6a3d3f2b1d5eee905058b68066d39f2083c22ab2d9d595f5181b3a80e3ff") # FIXME
    version("10.00.03", sha256="b6fa481c9eb3a519b74731c85ba6697bf28f3623edbcdc02cef6c04d545cbc9d") # FIXME
    version("09.19.00", sha256="8e689900cef678fb25c161f7fc676be25b64f1d79e65a9839d4c7e5b1a7c1040")
    version("09.18.03", sha256="032a4c48473dc87c204c3aaef4bdf4953599de26cd1642cb51fd6f7692adcb6d")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    patch("dk2nu.patch")

    depends_on("cetmodules", type="build")

    depends_on("boost+test")
    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("nusimdata")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("dk2nudata", type="build")
    depends_on("nufinder", type="build")
    depends_on("messagefacility")
    depends_on("root")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_build_environment(self, env):
        prefix = Prefix(self.build_directory)
        env.prepend_path("PATH", prefix.bin)  # Binaries.
        env.prepend_path("FHICL_FILE_PATH", prefix.job)

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)
        env.prepend_path("FW_SEARCH_PATH", self.prefix.compatibility)
