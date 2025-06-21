# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install nusystematics
#
# You can edit this file again by typing:
#
#     spack edit nusystematics
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Nusystematics(CMakePackage):

    url = "https://github.com/LArSoft/nusystematics/archive/refs/tags/v01_03_12.tar.gz"

    license("UNKNOWN")

    version("1.05.07", sha256="8d273475c43cd42cb62f5a66f6fd6bcd90c6ad3cb9b8592c0ca24982356a2db5")
    version("1_05_07", sha256="8d273475c43cd42cb62f5a66f6fd6bcd90c6ad3cb9b8592c0ca24982356a2db5")
    version("1_05_02", sha256="c4f2a7ed65d814ae3e20eae3832eb9534618ff0648fa0b57d5012df629bd0bbd")
    version("01_03_12", sha256="53300aa8bc604d06858a8a01f3ca6e59526d524375f24d6ae728f6d21e027898")

    depends_on("nugen")
    depends_on("systematicstools")
    depends_on("nufinder")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")

    def url_for_version(self, version):
        url = "https://github.com/LArSoft/{0}/archive/v{1}.tar.gz"
        print("url_for_version: ",url.format(self.name, version.underscored))
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        args = []
        return args
