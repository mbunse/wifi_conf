from setuptools import setup, find_packages
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="wifi_conf",
    version="0.1dev",
    packages=find_packages(),
    scripts=['scripts/install_wifi_conf',
	         'scripts/uninstall_wifi_conf'],

    entry_points = {
        "console_scripts": [
            "wifi_conf_daemon = wifi_conf.wifi_conf_daemon:run_daemon"
        ]
    },

    install_requires=[
        'python_version>="3.5"',
        'socket-client-server>="0.5.dev3"',
    ],
    package_data={"wifi_conf": [
        "data/hostapd", 
        "data/hostapd.conf",
        "data/dnsmasq.conf", 
        "data/wifi_conf.service",
    ]},

    # metadata for upload to PyPI
    author="Moritz Bunse",
    author_email="moritz.bunse@gmail.com",
    description="Package for setting up AP for configuration of wifi on raspberry pi",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    keywords="wifi access point raspberry pi raspbian",
    url="https://github.com/mbunse/wifi_conf",
    project_urls={
        "Source Code": "https://github.com/mbunse/wifi_conf",
    }

    # could also include long_description, download_url, classifiers, etc.
)
