#!/usr/bin/env sh

if [[ "$USE_SINGULARITY" == "true" ]]; then
    echo "USE SINGULARTIY "
    echo "$(go version) before gimme stable"
    gimme force 1.14
    eval "$(gimme 1.14)"
    echo "$(go version) after gimme stable"

    sudo apt-get update && sudo apt-get install -y \
      build-essential \
      libssl-dev \
      uuid-dev \
      libgpgme11-dev \
      squashfs-tools \
      libseccomp-dev \
      wget \
      pkg-config \
      git \
      cryptsetup

    export VERSION=3.5.2 && # adjust this as necessary \
      wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
      tar -xzf singularity-${VERSION}.tar.gz && \
      cd singularity

    echo "NOW IN $(pwd)"
    echo "$(ls -l)"
    echo "$PATH"
    echo "$(go version)"
    echo "usr/local $(ls -l /usr/local/go/bin)"

    ./mconfig && \
      make -C builddir && \
      sudo make -C builddir install

    singularity help

    cd ..
    pip install .[xgboost,singularity]

else
    echo "DONT USE SINGULARTIY "
    pip install .[xgboost]
fi

