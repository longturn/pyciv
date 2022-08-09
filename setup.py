import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="freeciv",
    version="0.1.0",
    author="The Longturn team and contributors",
    description="Python tools to work with Freeciv files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/longturn/pyciv",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Games/Entertainment :: Turn Based Strategy",
    ],
    entry_points={
        "console_scripts": ["freeciv-doc = freeciv.ruleset.doc:document_ruleset"],
    },
    python_requires=">=3.6",
    install_requires=["ply"],
)
