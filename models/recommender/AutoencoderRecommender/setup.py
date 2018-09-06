from setuptools import find_packages, setup

setup(
    name="autorecommender",
    description="Autoencoder-based recommender system",
    install_requires=[
        "Keras >= 2.1.3",
        "pandas >= 0.23.0",
        "numpy >= 1.14.2",
        "tensorflow >= 1.4.0",
        "scipy >= 1.1.0"
    ],
    packages=find_packages()
)