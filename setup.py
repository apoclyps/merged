from setuptools import find_namespace_packages, setup


def _requires_from_file(filename):
    with open(filename, encoding="utf-8") as f:
        return f.read().splitlines()


with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="merged",
    packages=find_namespace_packages(include=["*"]),
    version="0.2.3",
    license="MIT",
    description=("A terminal UI dashboard to view python dependencies across Github repositories."),
    author="Kyle Harrison",
    author_email="kyle.harrison.dev@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://pypi.org/project/merged/",
    project_urls={
        "Funding": "https://ko-fi.com/apoclyps",
        "Say Thanks!": "https://twitter.com/apoclyps",
        "Source": "https://github.com/apoclyps/merged",
        "Tracker": "https://github.com/apoclyps/merged/issues",
    },
    keywords=["Merged"],
    install_requires=_requires_from_file("requirements.txt"),
    entry_points={"console_scripts": ["merged = merged.cli.main:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Terminals",
    ],
)
