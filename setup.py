from setuptools import setup, find_packages

setup(
    name="ensemble-uq-ase",
    version="0.1.0",
    description="Uncertainty quantification with ensembles of interatomic potentials in ASE",
    author="Cuauhtemocnv",
    packages=find_packages(),
    install_requires=[
        "ase",
        "numpy"
    ],
    python_requires=">=3.8",
)
