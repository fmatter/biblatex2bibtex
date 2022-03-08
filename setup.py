from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="biblatex2bibtex",
    version="0.0.1",
    author="Florian Matter",
    author_email="florianmatter@gmail.com",
    description="Convert biblatex to bibtex",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fmatter/biblatex2bibtex",
    project_urls={
        "Bug Tracker": "https://github.com/fmatter/biblatex2bibtex/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pybtex==0.24.0",
        "bibtexparser==1.2.0"
    ],
    entry_points={
        "console_scripts": [
            "biblatex2bibtex=biblatex2bibtex.__main__:main",
        ],
    },
)
