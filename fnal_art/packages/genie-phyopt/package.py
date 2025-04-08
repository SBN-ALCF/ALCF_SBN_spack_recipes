# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack import *
from spack.package import *


class GeniePhyopt(Package):
    """Phyopt files used by genie."""

    #url = "file://" + os.path.dirname(__file__) + "/../../config/junk.xml"
    url = "https://scisoft.fnal.gov/scisoft/packages/genie_phyopt/v2_12_0/genie_phyopt-2.12.0-noarch-dkcharm.tar.bz2" 
    version("3.04.00", sha256="c4a5360e379d371df2b2e845aee673b984a2f0f6ba62dae682f8cb0223e84a0f") # FIXME
    version(
        "2.12.10", "2cae8b754a9f824ddd27964d11732941fd88f52f0880d7f685017caba7fea6b7", expand=False
    )

    variant(
        "phyopt_name",
        default="dkcharm",
        multi=False,
        values=("dkcharm", "dkcharmtau"),
        description="Name of genie phyopt to use.",
    )

    baseurl = "https://scisoft.fnal.gov/scisoft/packages/genie_phyopt/v2_12_10/genie_phyopt-2.12.10-noarch-"
    def install(self, spec, prefix):
        val = spec.variants["phyopt_name"].value
        install_tree(
            "{0}/genie_phyopt/v{1}/NULL/{2}".format(
                self.stage.source_path, self.version.underscored, val
            ),
            "{0}/{1}".format(prefix, val),
        )

    def url_for_version(self, version):
        url = "https://scisoft.fnal.gov/scisoft/packages/genie_phyopt/v{0}/genie_phyopt-{1}-noarch-{2}.tar.bz2"
        try:
            return url.format(version.underscored, version.dotted, self.spec.variants["phyopt_name"].value)
        except:
            return url.format(version.underscored, version.dotted, "dkcharm")
