import os

import setuptools

about = {}
with open("asciiviewer/_version.py") as f:
    exec(f.read(), about)

os.environ["PBR_VERSION"] = about["__version__"]

setuptools.setup(
    setup_requires=["pbr>=5.1.3"],
    pbr=True,
    version=about["__version__"],
)
