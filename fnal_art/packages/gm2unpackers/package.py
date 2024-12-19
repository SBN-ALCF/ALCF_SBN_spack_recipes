# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Gm2unpackers(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://redmine.fnal.gov/projects/gm2unpackers"
    url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/gm2unpackers.v9_60_00.tbz2"
    git_base = "https://cdcvs.fnal.gov/projects/gm2unpackers"

    version("spack_branch", branch="feature/mengel_spack", git=git_base, get_full_repo=True)
    version("9.60.00", sha256="1efd2e99333d99c8fcbaa6743e5e5b86aa0f6d93f7c2c7db823ff08980feedde")

    def url_for_version(self, version):
        return (
            "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/gm2unpackers.v%s.tbz2"
            % version.underscored
        )

    variant("cxxstd", default="17")

    depends_on("pkgconfig", type="build")
    depends_on("cetpkgsupport", type=("build"))
    depends_on("cetbuildtools", type=("build"))
    depends_on("cetmodules", type=("build"))
    depends_on("gm2midas", type=("build", "run"))
    depends_on("gm2geom", type=("build", "run"))
    depends_on("gm2dataproducts", type=("build", "run"))
    depends_on("gm2util", type=("build", "run"))
    depends_on("gm2trackerdaq", type=("build", "run"))
    depends_on("artg4", type=("build", "run"))
    depends_on("gm2aux", type=("build", "run"))


    def cmake_args(self):
        args = [
            "-DCXX_STANDARD=%s" % self.spec.variants["cxxstd"].value,
            "-DOLD_STYLE_CONFIG_VARS=True", 
            "-DCMAKE_MODULE_PATH={0}".format(
                          self.spec['cetmodules'].prefix.Modules.compat),
            "-DUPS_PRODUCT_VERSION=v{0}".format(self.spec.version.underscored),
        ]
        return args
