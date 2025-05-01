This is a list of temporary expoloits to get around errors in building sbn packages with spack. It is as much a todo list for me as it is a cheatsheet for others...

Error:
Error in <TInterpreter::TCling::AutoLoad>: failure loading library libicaruscode_IcarusObj_dict.so for icarus::SimEnergyDepositSummary

Solution:
Somehow, reinstalling with -j1 seems to fix this problem... Might be related to "no dictionary for class sim::IDE is available" warning which always appears in icaruscode

Error: 
    >> build error ELF load command address/offset not properly aligned

Solution:
Generally, this has indicated compiler versioning errors. I recommend using gcc-12.3.0. YMMV with other compilers. 


Error: 

    >> 1498    CMake Error at /lus/grand/projects/neutrinoGPU/spack_builds/spack/opt/spack/linux-sles15-zen3/gcc-12.3.0/cetmodules-3.25.00-ublvkzinygsrjc6f7qcxwm4zbfnutphc/Modules/CetMakeLibrary.cmake:456 (target_l 
               ink_libraries):                                                                                                                                                                                         
       1499      Target "larrecodnn_ImagePatternAlgs_Tensorflow_PointIdAlg" links to:                                                                                                                                  
       1500                                                                                                                                                                                                            
       1501        TensorFlow::framework                                                                                                                                                                               
       1502                                                                                                                                                                                                            
       1503      but the target was not found.  Possible reasons include:                                                                                                                                              
       1504                                                                                                                                                                                                                                                                                                                                                                                                                     

Solution:
Locate the py-tensorflow installation being used under spack/opt/spack and go to cp lib/python3.9/site-packages/tensorflow/libtensorflow_framework.so.2 lib/python3.9/site-packages/tensorflow/libtensorflow_framework.so. Similar procedure with libtensorflow_cc.so.2

Error:

    >> 1914    /var/tmp/pbs.3117936.polaris-pbs-01.hsn.cm.polaris.alcf.anl.gov/nathanielerowe/spack-stage/spack-stage-larrecodnn-09.23.10-zv46vjh7tqzkofzhajj3ipaccm4xsgm5/spack-src/larrecodnn/ImagePatternAlgs/Tenso 
               rflow/TF/tf_graph.cc:15:10: fatal error: tensorflow/cc/saved_model/tag_constants.h: No such file or directory                                                                                           
       1915       15 | #include "tensorflow/cc/saved_model/tag_constants.h"

Solution:
cp https://github.com/tensorflow/tensorflow/blob/1700c9f70d0b7b26f096c76b818b64d88de86184/tensorflow/cc/saved_model/tag_constants.h into lib/python3.9/site-packages/tensorflow/include/tensorflow/cc/saved_model/tag_constants.h in your py-tensorflow installation in spack/opt/spack

Error:

    >> 67    CMake Error at /exp/sbnd/data/users/nrowe/spack/opt/spack/linux-almalinux9-zen3/gcc-11.5.0/cetmodules-3.25.00-bshzfsyx4mu4vjbknimbeszmrrbc7m5b/Modules/compat/art/CetCMPCleaner.cmake:68 (_include):
       68      _include called with invalid arguments: OPTIONAL used twice
       69    Call Stack (most recent call first):
       70      /exp/sbnd/data/users/nrowe/spack/opt/spack/linux-almalinux9-zen3/gcc-11.5.0/fftw-3.3.10-u5hi7xuvnxtn6samejzuvimbimtfbhv3/lib/cmake/fftw3/FFTW3Config.cmake:13 (include)
       71      /exp/sbnd/data/users/nrowe/spack/opt/spack/linux-almalinux9-zen3/gcc-11.5.0/cetmodules-3.25.00-bshzfsyx4mu4vjbknimbeszmrrbc7m5b/Modules/private/CetOverrideFindPackage.cmake:177 (_find_package)
       72      /exp/sbnd/data/users/nrowe/spack/opt/spack/linux-almalinux9-zen3/gcc-11.5.0/cetmodules-3.25.00-bshzfsyx4mu4vjbknimbeszmrrbc7m5b/Modules/FindFFTW3.cmake:20 (find_package)
       73      /exp/sbnd/data/users/nrowe/spack/opt/spack/linux-almalinux9-zen3/gcc-11.5.0/cetmodules-3.25.00-bshzfsyx4mu4vjbknimbeszmrrbc7m5b/Modules/private/CetOverrideFindPackage.cmake:177 (_find_package)

Solution:
Manually remove OPTIONAL from the line they are referring to in FFTW3Config.cmake.

Error:

      The text leading up to this was:
      --------------------------
      |diff --git a/source/externals/g4tools/include/tools/wroot/columns.icc b/source/externals/g4tools/include/tools/wroot/columns.icc
      |index 0df2c16620..af9b15e0ab 100644
      |--- a/source/externals/g4tools/include/tools/wroot/columns.icc
      |+++ b/source/externals/g4tools/include/tools/wroot/columns.icc
      --------------------------

Solution:
File to patch: source/analysis/g4tools/include/tools/wroot/columns.icc

Error:
      >> 121    CMake Error at /lus/grand/projects/neutrinoGPU/software/spack_builds/spack/opt/spack/linux-sles15-zen3/gcc-12.3.0/cmake-3.31.0-womzeasnikwb25ak337ttfzlzlvicaqc/share/cmake-3.31/Modules/FindPackageHand 
                leStandardArgs.cmake:233 (message):                                                                                                                                                                      
         122      Could NOT find dk2nugenie (missing: dk2nugenie_FOUND)                                                                                                                                                  

Solution:
Remove <package>_FOUND from the Find<package>.cmake file listed in the error output
