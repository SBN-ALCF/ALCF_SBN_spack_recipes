def undr_to_dot(version):
    return version.replace("_",".").replace("v","",1)

def dot_to_undr(version):
    if not "v" in version:
        return "v"+version.replace(".","_")
    else:
        return version.replace(".","_")

def undr_to_dash(version):
    return version.replace("_","-")

def patch(version):
    splt = version.split("_")
    ret = ""
    for i in range(len(splt)):
        if i != len(splt)-1:
            ret += splt[i]+"_"
        else:
            ret += "p"+splt[i]
    return ret


def all_versioning_styles(v):
        return [dot_to_undr(v), undr_to_dot(v), undr_to_dash(v), "v"+undr_to_dash(v), patch(dot_to_undr(v))]

ignorable_packages = [
        "icarusutil",
        "cigetcert",
        "cigetcertlibs",
        "jobsub_client",
        "jobsub-client",
        "kx509",
        "mrb",
        "sbndutil",
        "ups",
        "upd",
        "gitflow",
        "larbatch",
        "scitokens_cpp",
        "scitokens-cpp", 
        "cetmodules", # spack build and manifest disagree, shouldn't matter  
        "cmake", # spack build and manifest disagree, shouldn't matter  
        "toyExperiment", # https://github.com/drbenmorgan/fnal-toyExperiment/tree/develop
        "fhiclpy", # literally just 4 cmake files, not in official larsoft spack
        "larutils", # scripts only, not in offical larsoft spack
        "golang", # not in official larsoft spack
        "guideline_sl", # not in offifial larsoft spack
        "guideline-sl", # not in offifial larsoft spack
        "studio", # not in offifial larsoft spack
        "inclxx", # putting this here for now... unsure if needed or not.
        # following is a list of packages which are not dependencies for spack build
        "cetpkgsupport",
        "cppunit",
        "gh",
        "g4tendl",
        "gdb",
        "geant4reweight",
        "genie-phyopt",
        "hub",
        "iwyu",
        "py-pycurl",
        "git"# version listed in manifest is deprecated, just grab whatever automatically
        ]

# some packages have slightly different names on ups vs spack
renamed_packages = {
        "g4neutron" : "g4ndl", # G4NDL
        "g4nucleonxs" : "g4saiddata", # G4SAIDDATA
        "g4nuclide" : "g4ensdfstate", # G4ENSDFSTATE
        "g4photon" : "g4photonevaporation", # G4PhotonEvaporation
        "g4radiative" : "g4radioactivedecay", # G4RadioactiveDecay
        "g4surface" : "g4realsurface", # G4RealSurface
        "catch" : "catch2",
        "delaunator" : "delaunator-cpp",
        "fhiclcpp" : "fhicl-cpp",
        "gojsonnet" : "go-jsonnet",
        "libtorch" : "py-torch", # libtorch comes with py-torch
        "pythia" : "pythia6",
        "range" : "range-v3",
        "tbb" : "intel-tbb",
        "TRACE" : "trace",
        }

# this is done in a way that agrees with scisoft spack builds
renamed_versions = {
        "cry" : {"v1_7q" : "1.7"},
        "dk2nudata" : {"v01_10_01h" : "01.10.01"},
        "dk2nugenie" : {"v01_10_01r" : "01.10.01"},
        "eigen" : {"v23_08_01_66e8f" : "3.4.0"},
        "geant4" : {"v4_10_6_p01g" : "10.6.1"},
        "genie" : {"v3_04_02a" : "3.04.02"},
        "grpc" : {"v1_35_0c" : "1.35.0"},
        "hdf5" : {"v1_12_2a" : "1.14.3"}, # match version used in their spack builds
        "jsoncpp" : {"v1_9_5a" : "1.9.5"},
        "py-torch" : {"v2_1_1b" : "2.1.1"}, # also disagrees btwn spack and ups?
        "libwda" : {"v2_30_0a" : "2.30.0"},
        "log4cpp" : {"v1_1_3e" : "1.1.3"},
        "marley" : {"v1_2_1d" : "1.2.1"},
        "pandora" : {"v03_16_00l" : "03.16.00"},
        "protobuf" : {"v3_21_12a" : "3.21.12"},
        "pygccxml" : {"v2_2_1b" : "2.2.1", "2.2.1b" : "2.2.1"},
        "py-pygccxml" : {"2.2.1b" : "2.2.1", "v2_2_1b" : "2.2.1"},
        "pythia8" : {"v8_3_10" : "8.311"},
        "pythia6" : {"v6_4_28x" : "6.4.28"},
        "range-v3" : {"v3_0_12_0" : "0.12.0"},
        "rstartree" : {"v2016_07" : "0.2"},
        "scitokens" : {"v1_0_1a" : "1.1.1"}, # also disagrees btwn spack and ups
        "sqlite" : {"v3_40_01_00" : "3.43.2"}, # also disagrees btwn spack and ups
        "srproxy" : {"v00.44" : "00.44"},
        "torch_scatter" : {"v2_1_2a" : "2.1.2", "v2_1_2" : "2.1.2"},
        "torch-scatter" : {"v2_1_2a" : "2.1.2", "v2_1_2" : "2.1.2"},
        "triton" : {"v2_25_0d" : "23.09"}, # don't understand this naming convention... 
        "xerces_c" : {"v3_2_3e" : "3.2.3"},
        "xerces-c" : {"v3_2_3e" : "3.2.3"},
        "xrootd" : {"v5_5_5a" : "5.6.9"}, # also disagrees btwn spack and ups
        "jemalloc" : {"v5_3_0d" : "5.3.0"}, # diff convention than spack build 
        "cppunit" : {"v1_15_1f" : "1.15.1"}, # diff convention than spack build 
        "tauola" : {"v1_1_8l" : "1.1.8"},
        "h5cpp" : {"v1_10_4_6c" : "1.10.4-6"},
        "go-jsonnet" : {"v0_18_0" : "0.19.1"},
        "py-pybind11" : {"v2_10_4" : "2.11.0"},
        }

