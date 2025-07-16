from setuptools import setup, find_packages

setup(
    name="skin_classification",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # List requirements here or use requirements.txt
    ],
)
