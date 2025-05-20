#!/bin/bash

while [[ $# -gt 0 ]]; do
  case $1 in
    -e|--env)
      ENV="$2"
      echo "Environment  = ${ENV}"
      shift # past argument
      shift # past argument
      ;;
    -i|--input)
      INPUT="$*"
      # Have to do some cleaning to handle multiple word argument
      INPUT=$(sed -e 's/-i //g;s/--input //g;s/[[:space:]]*$//;s/^[[:space:]]*//' <<< "$INPUT")
      INPUT=$(cat $INPUT)
      # Erases invisible encoding character that ruins the spack spec if present 
      INPUT=$(sed -e $'1s/^\uFEFF//' <<< "$INPUT")
      echo "Input        = ${INPUT}"
      shift # past argument
      shift # past argument
      ;;
    -h|--help)
      echo "USAGE: Script for creation, acivation, and adding spec
            -e, --env: Name of spack environment to be created
	    -i, --input: input spec (can be piped from file using cat)"
      exit 1
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      shift
      ;;
  esac
done

. /lus/grand/projects/neutrinoGPU/software/spack_builds/spack/share/spack/setup-env.sh
#spack env create "${ENV}"
spack env activate "${ENV}"
#INPUT=${INPUT%-spec*}
#echo Adding "${INPUT}"
spack add "${INPUT}"
spack concretize -f
spack install
