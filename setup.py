from setuptools import setup, find_packages
from pyrtkgps import __version__ as VERSION

LONG_DESCRIPTION = """\
PyRTKGPS is a library for managing and configuring GPS and other
GNSS chips. The main focus of this library is to provide support
for Real-Time Kinematic (RTK) positioning. Currently, GPS modules 
made by u-blox are supported."""

setup(
    name="pyrtkgps",
    version=VERSION,
    description="Manage Real-Time Kinematic GPS (RTK-GPS) with Python",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="alkeldi",
    author_email="ali.alkeldi@gmail.com",
    url="https://github.com/alkeldi/pyrtkgps",
    packages=find_packages(),

    install_requires=[
        "pyubx2>=1.2.7",
        "jsonschema>=4.4.0",
        "pyyaml>=6.0"
    ],
    license="License",
    keywords="RTK RTK-GPS ublox u-blox GPS-RTK GLONASS GNSS GPS UBX RTCM NMEA",
    platforms="Any",
    project_urls={
        "Bug Tracker": "https://github.com/alkeldi/pyrtkgps/issues",
        "Documentation": "https://github.com/alkeldi/pyrtkgps/wiki",
        "Source Code": "https://github.com/alkeldi/pyrtkgps",
    },
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    python_requires=">=3.6",
)
