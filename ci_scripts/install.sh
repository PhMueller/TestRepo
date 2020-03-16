#!/usr/bin/env sh

if [[ "$USE_SINGULARITY" == "true" ]]; then
    echo "USE SINGULARTIY "
    gimme force 1.14
    eval "$(gimme 1.14)"

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

    ./mconfig && \
      make -C builddir && \
      sudo make -C builddir install

    cd ..
    pip install .[xgboost,singularity]

else
    echo "DONT USE SINGULARTIY "
    pip install .[xgboost]
fi

