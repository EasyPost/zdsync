from setuptools import (
    setup,
    find_packages
)


setup(
    name="zdsync",
    version="0.0.2",
    author="Andrew Tribone",
    author_email="oss@easypost.com",
    url="https://github.com/easypost/zdsync",
    description="Command-line tool for syncing Zendesk environments",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="ISC",
    install_requires=["zenpy"],
    packages=find_packages(exclude=["tests"]),
    python_requires=">3.5",
    entry_points={
        "console_scripts": [
            "zdsync = zdsync.cli:main",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: ISC License (ISCL)",
    ]
)
