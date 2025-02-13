#!/bin/bash

if [[ $# -eq 0 ]]; then
    echo "Incorrect usage!"
    stopbool=1
    exit 1
fi

while [[ $# -gt 0 ]]; do
  case $1 in
    -b|--BUNDLE)
      BUNDLE="$2"
      shift # past argument
      shift # past argument
      ;;
    -o|--old)
      OLD="$2"
      shift # past argument
      shift # past argument
      ;;
    -n|--new)
      NEW="$2"
      shift # past argument
      shift # past argument
      ;;
    -h|--help)
      echo "USAGE: Script for comparison of MANIFEST files for sbnd/icarus
            -b, --BUNDLE: Name of BUNDLE (icarus/sbnd/sbn/...)
            -o, --old: old version of MANIFEST
            -n, --new: new version of MANIFEST
	    NOTE: versioning here is of form vXX_XX_XX"
      stopbool=1
      exit 0
      ;;
    -*|--*)
      echo "Unknown option $1"
      stopbool=1
      exit 1
      ;;
  esac
done

if ! [ $stopbool ]; then
    echo "Bundle   = ${BUNDLE}"
    echo "Old Version  = ${OLD}"
    echo "New Version  = ${NEW}"

    ./pullProducts.sh -M . slf7 $BUNDLE-$OLD e26 prof > /dev/null
    ./pullProducts.sh -M . slf7 $BUNDLE-$NEW e26 prof > /dev/null


    # Have to switch to periods from underscores...
    if [[ $OLD == *"_"* ]]; then
              OLD="${OLD:1}"
	  OLD="${OLD//\_/\.}"
    fi
    if [[ $NEW == *"_"* ]]; then
              NEW="${NEW:1}"
	  NEW="${NEW//\_/\.}"
    fi
    if [[ $OLD == *"v"* ]]; then
              OLD="${OLD:1}"
    fi
    if [[ $NEW == *"v"* ]]; then
              NEW="${NEW:1}"
    fi
    diff ${BUNDLE}-${OLD}-Linux64bit+3.10-2.17-e26-prof_MANIFEST.txt ${BUNDLE}-${NEW}-Linux64bit+3.10-2.17-e26-prof_MANIFEST.txt
    rm ${BUNDLE}-${OLD}-Linux64bit+3.10-2.17-e26-prof_MANIFEST.txt
    rm ${BUNDLE}-${NEW}-Linux64bit+3.10-2.17-e26-prof_MANIFEST.txt
fi
