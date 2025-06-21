# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Larrecodnn(CMakePackage, FnalGithubPackage):
    """Larrecodnn"""

    repo = "LArSoft/larrecodnn"
    version_patterns = ["v09_00_00", "09.21.21"]

    version("10.01.10", sha256="86a54b2cdf067a5bcf4e494c2be1162d1e8aa6f58ea37a446962792bc962d334") # FIXME
    version("10.01.06", sha256="b0938afb0cfa838bdcef51637ce3f969ef3145f3b6abab4906b2abca7e2df471")
    version("10.00.00", sha256="c194751f84569ed4e6306af8583a4812ed923819511e7b0cacf849c150bda337")
    version("09.23.10", sha256="b90ea794e199da9aee975beb1c26e30612249b3bfd0e4103b2b017847a6c88ec")
    version("09.23.00", sha256="cbf64222f14879cda5eaa2adb7ed8c07bef82afd86a3925b31cc1719fd17e236")
    version("develop", branch="develop", get_full_repo=True)

    patch('spack.patch')
    patch('10.00.00.patch', when='@10.00.00')
    patch('09.23.00.patch', when='@09.23.00')
    patch('09.23.00.patch', when='@09.23.10')
    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")
    depends_on("larfinder", type="build")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("canvas")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("clhep")
    depends_on("delaunator-cpp")
    depends_on("grpc")
    depends_on("hdf5")
    depends_on("hep-hpc")
    depends_on("postgresql")
    depends_on("range-v3")
    depends_on("re2")
    depends_on("eigen")
    depends_on("larcore", when="@:10.00.00")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("lardataobj")
    depends_on("lardata")
    depends_on("larevt")
    depends_on("larreco")
    depends_on("nutools")
    depends_on("nug4")
    depends_on("larsim")
    depends_on("messagefacility")
    depends_on("nurandom")
    depends_on("nusimdata")
    depends_on("protobuf", when="@:09.23.00")
    depends_on("py-tensorflow", type=('build', 'run'))
    depends_on("py-torch")
    depends_on("torch-scatter")
    depends_on("root")
    depends_on("tbb")
    depends_on("triton")
    depends_on("zlib")
    depends_on("giflib")

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define(
                "CMAKE_PREFIX_PATH",
                "{0}/lib/python{1}/site-packages/torch".format(
                    self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2)
                ),
            ),
            self.define(
                "Torch_DIR",
                "{0}/lib/python{1}/site-packages/torch/share/cmake/Torch".format(
                    self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2)
                ),
            ),
            self.define(
                "DELAUNATOR_INC",
                self.spec["delaunator-cpp"].prefix.include
            ),
            self.define(
                "CMAKE_PREFIX_PATH",
                join_path(
                self.spec["py-tensorflow"].prefix.lib,
                "python{0}/site-packages/tensorflow".format(
                    self.spec["python"].version.up_to(2)
                ),
              )
            ),
            self.define(
                "TensorFlow_LIBRARIES",
                join_path(
                self.spec["py-tensorflow"].prefix.lib,
                "python{0}/site-packages/tensorflow".format(
                    self.spec["python"].version.up_to(2)
                ),
              ),
            ),
        ]

    @sanitize_paths
    def setup_build_environment(self, env):
        env.set("TRITON_DIR", self.spec["triton"].prefix.lib)
        env.set("TENSORFLOW_DIR", self.spec["py-tensorflow"].prefix.lib)
        env.set(
                "Torch_DIR",
                "{0}/lib/python{1}/site-packages/torch/share/cmake/Torch".format(
                    self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2)
                ),
            )

        env.set(
            "TENSORFLOW_INC",
            join_path(
                self.spec["py-tensorflow"].prefix.lib,
                "python{0}/site-packages/tensorflow/include".format(
                    self.spec["python"].version.up_to(2)
                ),
            ),
        )
        env.prepend_path("CMAKE_PREFIX_PATH", self.spec["zlib"].prefix)

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)
        env.prepend_path("FW_SEARCH_PATH", self.prefix.config_data)

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
            flags.append("-Wno-error=ignored-attributes")
        return (flags, None, None)
