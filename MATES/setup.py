from setuptools import setup, find_packages
setup(
    name="MATES",
    version="0.1",
    packages=find_packages(),
    install_requires=["matplotlib==3.7.2",
        "numpy==1.24.3",
        "numpy==1.23.5",
        "pandas==2.0.3",
        "pybedtools==0.9.1",
        "pysam==0.21.0",
        "scipy==1.10.1",
        "torch==2.0.1",
        "tqdm==4.65.0"],
)