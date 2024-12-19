# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
#     spack install sbnd-data
#
# You can edit this file again by typing:
#
#     spack edit sbnd-data
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *
import glob

class SbndData(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    # homepage = "https://scisoft.fnal.gov/scisoft/packages/sbnd_data/v01_24_00"
    url_base = "https://scisoft.fnal.gov/scisoft/packages/sbnd_data/"
    # url = "https://scisoft.fnal.gov/scisoft/packages/sbnd_data/v01_24_00/sbnd_data-01.24.00-noarch.tar.bz2"

    version("01_25_00", sha256="84bc68f77366c38beb1695e0c635d7ec2c8b1ff02548c03b9f79a5b9b188c4b0", url=url_base+"v01_25_00/sbnd_data-01.25.00-noarch.tar.bz2")
    version("01_24_00", sha256="36659fd880d34f7a987fc395b20abdcbc9a39a8b318ba8e47312a0d3e7893ddb", url=url_base+"v01_24_00/sbnd_data-01.24.00-noarch.tar.bz2")

    def install(self, spec, prefix):
        src = glob.glob("%s/v*[0-9]" % self.stage.source_path)[0]
        install_tree(src, prefix)

    def setup_run_environment(self, env):
        env.set("SBND_DATA_VERSION", "v%s" % self.version.underscored)
        env.prepend_path("WIRECELL_PATH", "%s/WireCell" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/sbnd-data" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/sbnd-data/CNNHitClassification" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/sbnd-data/CRUMBS" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/sbnd-data/FlashMatch" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/sbnd-data/GENIE" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/sbnd-data/OpDetReco" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/sbnd-data/OpDetSim" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/sbnd-data/OpticalLibrary" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/sbnd-data/PandoraMVAs" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/sbnd-data/ParticleGunHists" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/sbnd-data/PhysicsBook" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/sbnd-data/PID" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/sbnd-data/Response" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/sbnd-data/SCEoffsets" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/sbnd-data/ShowerEnergyReco" % self.prefix)
        env.prepend_path("FW_SEARCH_PATH", "%s/sbnd-data/WireCell" % self.prefix)
        env.prepend_path("CMAKE_PREFIX_PATH", "%s" % self.prefix)
        env.prepend_path("PKG_CONFIG_PATH", "%s" % self.prefix)

