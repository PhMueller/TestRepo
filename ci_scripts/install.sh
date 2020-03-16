#!/usr/bin/env sh

if [[ "$USE_SINGULARITY" == "true" ]]; then
    echo "USE SINGULARTIY "
    echo "$(PATH)"

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

    export VERSION=1.13 OS=linux ARCH=amd64 && \  # Replace the values as needed
      wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz && \ # Downloads the required Go package
      sudo tar -C /usr/local -xzvf go$VERSION.$OS-$ARCH.tar.gz && \ # Extracts the archive
      rm go$VERSION.$OS-$ARCH.tar.gz    # Deletes the ``tar`` file

    echo 'export PATH=/usr/local/go/bin:$PATH' >> ~/.bashrc && \
      source ~/.bashrc

    export VERSION=3.5.2 && # adjust this as necessary \
      wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
      tar -xzf singularity-${VERSION}.tar.gz && \
      cd singularity

    echo "NOW IN $(pwd)"

    ./mconfig && \
      make -C builddir && \
      sudo make -C builddir install

    singularity help

    pip install .[xgboost,singularity]
else
    echo "DONT USE SINGULARTIY "
    pip install .[xgboost]
fi

