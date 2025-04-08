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
#     spack install systematicstools
#
# You can edit this file again by typing:
#
#     spack edit systematicstools
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Systematicstools(CMakePackage):
    url = "https://github.com/LArSoft/systematicstools/archive/refs/tags/v01_04_02.tar.gz"
    version("v01_04_04", sha256="7436341f63ea205d8b901b75859a26ec81f29fd272bf324c7bdcde713a3b937c")
    version("v01_04_02", sha256="0e14b9736b31b7911307e8703d0f386f2a1fb5c1dcaa69a8d7ce9916afb974cd")

    depends_on("art-root-io")
    depends_on("cetmodules", type="build")
    depends_on("cmake", type="build")
