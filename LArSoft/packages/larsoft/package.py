# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Larsoft(CMakePackage, FnalGithubPackage):
    """Software for Liquid Argon time projection chambers"""

    repo = "LArSoft/larsoft"
    homepage = "https://larsoft.org"
    version_patterns = ["v09_00_00", "09.85.00"]

    version("09.93.01", sha256="0b5a067b69eef569da6431a98f62275e41e5a05344413cc8d9e67a4a96f6a165")
    version("09.91.02", sha256="a485c8ce593cfcf88f182c751594498c82e23d42bc540cfff8bfb584643404a9")
    version("09.90.01", sha256="93dd9ac43a6b21b73e59d9c31a59a3c2037a845348cee4c11add74eb01bd76a0")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")
    variant(
        "eventdisplay",
        default=False,
        description="Include lareventdisplay and root/geant4 with opengl and x.",
    )

    depends_on("cetmodules", type="build")

    depends_on("larfinder")
    depends_on("larsoftobj")
    depends_on("larsoft-data")
    depends_on("larana")
    depends_on("larexamples")
    depends_on("larpandora")
    depends_on("larreco")
    depends_on("larrecodnn")
    depends_on("larsimrad")
    depends_on("larwirecell")

    with when("+eventdisplay"):
        depends_on("lareventdisplay")
        depends_on("larpandoracontent +monitoring")
        depends_on("root +opengl+x")

    with when("~eventdisplay"):
        depends_on("geant4 ~opengl~x11~qt")
        depends_on("larpandoracontent ~monitoring")
        depends_on("root ~opengl~x")

    @cmake_preset
    def cmake_args(self):
        return [
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
        env.set(
                "Torch_DIR",
                "{0}/lib/python{1}/site-packages/torch/share/cmake/Torch".format(
                    self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2)
                ),
            )


    def patch(self):
        with when("@:09.90.01.01 ~eventdisplay"):
            filter_file(r"find_package\( *lareventdisplay.*", "", "CMakeLists.txt")

    @run_after("install")
    def rename_bin_python(self):
        os.rename(
            join_path(self.spec.prefix, "bin/python"),
            join_path(self.spec.prefix, "bin/python-scripts"),
        )
