from setuptools import setup, find_packages
setup(
    name="Wifi_Conf",
    version="0.1dev",
    packages=find_packages(),
    scripts=['scripts/install_wificonf',
	     'scripts/uninstall_wificonf'],

    install_requires=[],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },
    data_files=[('/etc/gunicorn', ['gunicorn.env']),
                ('/etc/systemd/system', ['gunicorn.service']),
                ],

    # metadata for upload to PyPI
    author="Moritz Bunse",
    author_email="moritz.bunse@gmail.com",
    description="Package for setting up AP for configuration if Wifi on raspberry pi",
    license="MIT",
    keywords="wifi access point raspberry pi raspbian",
    url="https://github.com/mbunse/wifi_conf",   # project home page, if any
    project_urls={
        "Source Code": "https://github.com/mbunse/wifi_conf",
    }

    # could also include long_description, download_url, classifiers, etc.
)
