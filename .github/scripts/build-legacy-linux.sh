#!/usr/bin/env bash
set -eux

if command -v yum >/dev/null 2>&1; then
  # CentOS 7 is EOL; mirrorlist.centos.org / mirror.centos.org are gone, repoint at the vault
  sed -i 's/mirrorlist/#mirrorlist/g; s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/*.repo
  yum install -y bzip2 curl ca-certificates gtk3 mesa-libGL libSM libXext libXrender libXi libXtst
else
  apt-get update
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    bzip2 curl ca-certificates binutils libgtk-3-0 libsm6 libxext6 libxrender1 libxi6 libxtst6
fi

# Anaconda's own Miniconda installer now requires GLIBC >=2.28 (newer than CentOS 7's 2.17),
# defeating the point of building here. Miniforge is conda-forge's own installer, built against
# conda-forge's glibc 2.17 floor (the same floor wxpython itself is built against), so use that.
curl -fsSL -o /tmp/miniforge.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash /tmp/miniforge.sh -b -p /opt/conda
source /opt/conda/etc/profile.d/conda.sh

conda env create -f environment.yml
conda activate asciiviewer

pyinstaller --clean -y --dist ./dist/linux ./asciiviewer.spec
