# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Larsimrad(CMakePackage, FnalGithubPackage):
    """larsimrad"""

    repo = "LArSoft/larsimrad"
    version_patterns = ["v09_00_00", "09.08.18"]

    version("10.00.12", sha256="9d79deea2318d52e0974e9a53201756ee2ea8881a66779971de5c55264baf635") # FIXME
    version("09.09.11", sha256="f0a22b39fc77eeadb2a20bf0adc74813e680420b745cccd34fb2705a2e67656e")
    version("09.09.05", sha256="a1bc6bfbbc375593b1dc018cd6e658d0236e2165f723ea59684aa872a04191be")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("bxdecay0")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("clhep")
    depends_on("fhicl-cpp")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataobj", when="@:09.09.05.01")
    depends_on("lardata")
    depends_on("larsim")
    depends_on("nugen")
    depends_on("nurandom")
    depends_on("nusimdata")
    depends_on("root")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
