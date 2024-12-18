# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Larpandora(CMakePackage, FnalGithubPackage):
    """Larpandora"""

    repo = "LArSoft/larpandora"
    version_patterns = ["v09_00_00", "09.21.20"]

    # version("10.00.00", sha256="f766c0a2eb3b3e6be12f7289fda4479dc92ceb66c17506fddb8bc6e1a9c850c4")
    version(
        "09.22.05.01", sha256="6d63211e74842fe3de783078733092f082df84be7a384b6d17cc42ed61eca33e"
    )
    version("09.22.05", sha256="3c9f4bbbfe7b1653ccf142ee0f5a3437610733bd0efaaf0a413d56f503ae7a5f")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("canvas")
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
    depends_on("larpandoracontent")
    depends_on("larreco")
    depends_on("larsim")
    depends_on("messagefacility")
    depends_on("nusimdata")
    depends_on("pandorasdk")
    depends_on("py-torch")
    depends_on("root")

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define(
                "CMAKE_PREFIX_PATH", self.spec["py-torch"].package.cmake_prefix_paths[0]
            ),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
        ]

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
        return (flags, None, None)

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
        env.prepend_path("FW_SEARCH_PATH", self.prefix.scripts)
