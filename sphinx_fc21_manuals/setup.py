import setuptools

# "import" __version__
__version__ = "unknown"
for line in open("sphinx_fc21_manuals.py"):
    if line.startswith("__version__"):
        exec(line)
        break

setup(
    name="sphinx_fc21_manuals",
    version=__version__,
    # package_dir={'': 'src'},
    py_modules=["sphinx_fc21_manuals"],
    python_requires=">=3.10",
    install_requires=[
        "sphinx>=1.10",
        "pytypes>=1.0",
        "ply>=3.11",
        "typeguard>=2.13",
        "unidecode>=1.3",
    ],
    author="Freeciv21 Contributors",
    author_email="longturn.net@gmail.com",
    description="Create ReST files of Freeciv21 rulesets",
    long_description=open("README.md").read(),
    license="GPL-3.0",
    keywords="Sphinx Freeciv21".split(),
    url="https://github.com/longturn/pyciv/sphinx_fc21_manuals/",
    platforms="any",
    classifiers=[
        "Framework :: Sphinx",
        "Framework :: Sphinx :: Extension",
        "License :: OSI Approved :: GPL-3.0",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Documentation :: Sphinx",
    ],
    zip_safe=True,
)
