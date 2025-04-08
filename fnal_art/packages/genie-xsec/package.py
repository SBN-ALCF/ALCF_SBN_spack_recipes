# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *
from spack.package import *


class GenieXsec(Package):
    """Data files used by genie."""

    url = "https://scisoft.fnal.gov/scisoft/packages/genie_xsec/v3_04_00/genie_xsec-3.04.00-noarch-G1810a0211a-k250-e1000.tar.bz2"
    version("3_04_00", sha256="fb4dc9badd1771c92fabbf818b33544006e8b60c7fb0f33d5288a66d93bd19ea")

    # xsec_name values are designed to line up with the ups setup command
    # when setting the environment variable, we change to match typical
    # genie tune format
    variant(
        "xsec_name",
        default="AR2320i00000-k250-e1000",
        multi=False,
        values=(
            "AR2320i00000-k250-e1000",
            "G1801a00000-k250-e1000",
            "G1802a00000-k250-e1000",
            "G1810a0211a-k250-e1000",
            "G1810a0211b-k250-e1000",
            "G2111a00000-k250-e1000",
            "GDNu2001a00000-k120-e200",
            "N1810j0211a-k250-e1000"
        ),
        description="Name of genie xsec tune set to install.",
    )
    urlbase = (
         "https://scisoft.fnal.gov/scisoft/packages/genie_xsec/v3_04_00/genie_xsec-3.04.00-noarch-"
    )
    resource(
        name="AR2320i00000-k250-e1000",
        placement="AR2320i00000-k250-e1000",
        when="xsec_name=AR2320i00000-k250-e1000",
        url=urlbase + "AR2320i00000-k250-e1000.tar.bz2",
        sha256="13cc9d740c170af9033623049162eeff0fb0b68156122d380aa3262e92e9f61f",
        )

    resource(
        name="G1801a00000-k250-e1000",
        placement="G1801a00000-k250-e1000",
        when="xsec_name=G1801a00000-k250-e1000",
        url=urlbase + "G1801a00000-k250-e1000.tar.bz2",
        sha256="f222ff56360c9c221e8f793a9c09ddbe6578dbbaa9031b3b3a49cb5ec186595d",
        )

    resource(
        name="G1802a00000-k250-e1000",
        placement="G1802a00000-k250-e1000",
        when="xsec_name=G1802a00000-k250-e1000",
        url=urlbase + "G1802a00000-k250-e1000.tar.bz2",
        sha256="d7189bd6c3933b3017c83fafddb84d57b48414632b577835e49babec8537ab6e",
        )

    resource(
        name="G1810a0211a-k250-e1000",
        placement="G1810a0211a-k250-e1000",
        when="xsec_name=G1810a0211a-k250-e1000",
        url=urlbase + "G1810a0211a-k250-e1000.tar.bz2",
        sha256="fb4dc9badd1771c92fabbf818b33544006e8b60c7fb0f33d5288a66d93bd19ea",
        )

    resource(
        name="G1810a0211b-k250-e1000",
        placement="G1810a0211b-k250-e1000",
        when="xsec_name=G1810a0211b-k250-e1000",
        url=urlbase + "G1810a0211b-k250-e1000.tar.bz2",
        sha256="a1031e49ac8ac426074f247d91b2c886edaf7c4fef13993fe69aad92ad698c34",
        )

    resource(
        name="G2111a00000-k250-e1000",
        placement="G2111a00000-k250-e1000",
        when="xsec_name=G2111a00000-k250-e1000",
        url=urlbase + "G2111a00000-k250-e1000.tar.bz2",
        sha256="ae159887772a54891fc4bddb189ab108d74c4a48db68c13ed7166524e8797590",
        )

    resource(
        name="GDNu2001a00000-k120-e200",
        placement="GDNu2001a00000-k120-e200",
        when="xsec_name=GDNu2001a00000-k120-e200",
        url=urlbase + "GDNu2001a00000-k120-e200.tar.bz2",
        sha256="69146aacc6c55bdc5c519e917e48ea005d160824bf960d17734e9c7c6d85b6cb",
        )

    resource(
        name="N1810j0211a-k250-e1000",
        placement="N1810j0211a-k250-e1000",
        when="xsec_name=N1810j0211a-k250-e1000",
        url=urlbase + "N1810j0211a-k250-e1000.tar.bz2",
        sha256="79e7ecd8d0dc577efb525831b90eb2f650c0cdd7fe5cd17e3ea610a686248e33",
        )

    def install(self, spec, prefix):
        val = spec.variants["xsec_name"].value
        comb_str = val.split(':')[0].split('-')[0]
        tune_str = comb_str[:3]+"_"+comb_str[3:6]+"_"+comb_str[6:8]+"_"+comb_str[8:]

        install_tree(
            "{0}/{2}/v{1}/NULL/{2}".format(self.stage.source_path, self.version.underscored, val),
            "{0}/v{1}/NULL/{2}".format(prefix, self.version.underscored, val),
        )

    def setup_run_environment(self, run_env):
        val = self.spec['genie-xsec'].variants['xsec_name'].value
        data_str = "{0}/v{1}/NULL/{2}/data".format(self.spec['genie-xsec'].prefix, self.version.underscored.string.replace('v', ''), val)
        raw_str = self.spec['genie-xsec'].variants['xsec_name'].value
        comb_str = raw_str.split(':')[0].split('-')[0]
        tune_str = comb_str[:-8]+"_"+comb_str[-8:-5]+"_"+comb_str[-5:-3]+"_"+comb_str[-3:] 
        run_env.unset("GENIEXSECPATH")
        run_env.set("GENIEXSECPATH", data_str)
        run_env.unset("GENIEXSECFILE")
        run_env.set("GENIEXSECFILE", data_str+"/gxspl-NUsmall.xml")
        run_env.unset("GXMLPATH")
        run_env.set("GXMLPATH", data_str)
        run_env.unset("GENIE_XSEC_TUNE")
        run_env.set("GENIE_XSEC_TUNE", tune_str)
        run_env.unset("GENIE_XSEC_GENLIST")
        run_env.set("GENIE_XSEC_GENLIST", "Default")
        run_env.unset("GENIE_XSEC_KNOTS")
        run_env.set("GENIE_XSEC_KNOTS", "250")
        run_env.unset("GENIE_XSEC_EMAX")
        run_env.set("GENIE_XSEC_EMAX", "1000.0")
