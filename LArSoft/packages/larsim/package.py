# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Larsim(CMakePackage, FnalGithubPackage):
    """Larsim"""

    repo = "LArSoft/larsim"
    version_patterns = ["v09_00_00", "09.40.01"]

    version("10.04.00", sha256="96bb0c265631cbac56583aafea5a8a20d3bc8ba2de7deac356ff7053f6e3cc36")
    version("10.03.00", sha256="3d2ea5a8c88dc21a116bf4b9f556ed6bbe7fe2726bf26d7dd25c097ad94a9ea5")
    version("10.02.03", sha256="3d8aad7e298605a4e0c2a61848d75997d1eda6f027bf91fdb0181b9668daef79")
    version("10.02.02", sha256="68e7cee38dbe2b57dc06a9a81350ae615f92ab37ee1fcb5192cd8506149e0b5c")
    version("10.02.01", sha256="9fe7579d14d08b8100dd751b66af7d9dd171e28a7b1170f15461cabe011b2050")
    version("10.02.00", sha256="0b0fa0a1852ba6894acf27f3c1698238cd6d9a4faf80fcf246b669a7607f8ab5")
    version("10.01.00", sha256="522a2d8ce5c653328f6ad5c88707af91c9dd0b0c3313eb0ab834badad9df1cf2")
    version("10.00.00", sha256="9f4369420f5250ebbf3b8c32927c9d4aaaab69a7383a43451b0ee54a106a8d30")
    version("10.00.02", sha256="2d0d1d6656021003191b1ab768a6e06c3ffdfd63bc851e77639ebc2cd85cdffe")
    version("09.45.00", sha256="71a8a0f5db0aae4d18057d55735ec4ef03be23b98c03f09fce0c3eab8ac8322f")
    version("09.44.01", sha256="862619a46a871c199be6b07da4ff544d399887a9725750b3a5fe2997e2add48e")
    version("09.43.00", sha256="c8a37c9f98cd3c7059ba3a52d5647411c8dfa83f7227d8e4ec0ed4cb43e701f1")
    version("09.38.06", sha256="be8cc87ea901a5efdcfb91bb9810eee94a0cf860316174ab6ab1cf20c147883b")
    version("09.38.03", sha256="e16fd69ed9acc368563334efbc986d73fb7a085c8201670822d97a314566f52b")
    version("09.38.00", sha256="7f68cacf3cc838f4d5e94f8cc9a59f678fea202694f5c837295d5682e09bd5aa")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("artg4tk")
    depends_on("boost+math")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("clhep")
    depends_on("cry")
    depends_on("dk2nudata")
    depends_on("dk2nugenie")
    depends_on("fhicl-cpp")
    depends_on("geant4")
    depends_on("genie")
    depends_on("ifdhc")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataalg")
    depends_on("lardataobj")
    depends_on("lardata")
    depends_on("larevt")
    depends_on("larsoft-data")
    depends_on("log4cpp")
    depends_on("marley")
    depends_on("messagefacility")
    depends_on("nufinder")
    depends_on("nug4")
    depends_on("nugen")
    depends_on("nurandom")
    depends_on("nusimdata")
    depends_on("nutools")
    depends_on("ppfx")
    depends_on("range-v3")
    depends_on("root")
    depends_on("sqlite")

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
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
        env.prepend_path("FW_SEARCH_PATH", prefix.G4)
        env.prepend_path("FW_SEARCH_PATH", prefix.gdml)

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)
        env.prepend_path("FW_SEARCH_PATH", self.prefix.G4)
        env.prepend_path("FW_SEARCH_PATH", self.prefix.gdml)
