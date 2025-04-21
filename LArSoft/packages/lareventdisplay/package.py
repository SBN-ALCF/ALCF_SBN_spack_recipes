# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Lareventdisplay(CMakePackage, FnalGithubPackage):
    """Lareventdisplay"""

    repo = "LArSoft/lareventdisplay"
    version_patterns = ["v09_00_00", "09.10.19"]

    version("10.00.12", sha256="714839a4002f8045685f3e15f97d92657f7de8a9acffdc3c82254ea9517983d6") # FIXME
    version("10.00.11", sha256="f6a0c694a97636ac79edafe884c8cf8a7674fbd985524328882029efdcf04f2e") # FIXME
    version("10.00.09", sha256="dad20b9224e2778b4ec9b2e029490c4913efcc101cc6958f6c5de6c75339bc33") # FIXME
    version("09.11.14", sha256="8b4f8dc4006014801795c9455718031c6de302150b49dbf08ec55fe6c801668a")
    version("09.11.05", sha256="ed021c8b5632e435026b5ebe4eb33dfceaed8764e2fa90d9735d764e93938253")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("eigen")
    depends_on("fhicl-cpp")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataalg")
    depends_on("lardataobj")
    depends_on("lardata")
    depends_on("larevt")
    depends_on("larsim")
    depends_on("messagefacility")
    depends_on("nuevdb")
    depends_on("nusimdata")
    depends_on("root")

    with when("@:09.11.05.01"):
        depends_on("art-root-io")
        depends_on("zlib")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
        return (flags, None, None)
