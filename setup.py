from setuptools import (
    setup,
    find_packages
)


setup(
    name="zdsync",
    version="0.0.1",
    author="Andrew Tribone",
    author_email="tribone@easypost.com",
    # url="https://github.com/easypost/zendesk-sync",
    description="Command-line tool for syncing Zendesk environments",
    license="ISC",
    install_requires=["zenpy"],
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'zdsync = zdsync.cli:main',
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "Operating System :: MacOS X",
        "Operating System :: Unix",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: ISC License (ISCL)",
    ]
)
