# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Larsimdnn(CMakePackage, FnalGithubPackage):
    """Larsim"""

    repo = "LArSoft/larsimdnn"
    version_patterns = ["v09_00_00", "09.05.18"]

    version("10.00.08", sha256="56c3e1ad68d59100837c123d5145c94411902e2461f0140ad9623f197bb7878f") # FIXME
    version("10.00.07", sha256="bf6a6b632ee8449edc9e505a96185b8b1db5396c3f629a46db35bc528b4c9b95") # FIXME
    version("09.06.11", sha256="b220bbc3ee016ceb137a79a1445ec02a5ffc7ff4737e1c58b8b284c15d17a3b9")
    version("09.06.05", sha256="ecd14549917d696332bc05c3b4c23bdf263a99b5e76a3341b19142be5482bbad")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")
    depends_on("larfinder", type="build")

    depends_on("eigen")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataobj")
    depends_on("larevt", when="@:09.06.05.01")
    depends_on("larsim")
    depends_on("py-tensorflow")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_build_environment(self, env):
        env.set(
            "TENSORFLOW_INC",
            join_path(
                self.spec["py-tensorflow"].prefix.lib,
                "python%s/site-packages/tensorflow/include" % self.spec["python"].version.up_to(2),
            ),
        )

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)
        env.prepend_path("FW_SEARCH_PATH", self.prefix.config_data)
