from setuptools import setup, find_packages

setup(
    name="fbref_scraper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "pandas"
        ],
    author="Cesc Blanco Arnau",
    author_email="cesc.blanco98@gmail.com",
    description="Una librería para scrapear datos necesarios de la pagina FBREF",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/CescBlanco/proyecto_libreria_Evolve/fbref_scraper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 