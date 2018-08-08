from setuptools import setup, find_packages
setup(
    name="wifi_conf",
    version="0.1dev",
    packages=find_packages(),
    scripts=['scripts/install_wifi_conf.sh',
	         'scripts/uninstall_wifi_conf.sh'],

    install_requires=[],

    data_files=[('/etc/gunicorn', ['gunicorn.env']),
                ('/etc/systemd/system', ['gunicorn.service']),
                ],

    # metadata for upload to PyPI
    author="Moritz Bunse",
    author_email="moritz.bunse@gmail.com",
    description="Package for setting up AP for configuration of wifi on raspberry pi",
    license="MIT",
    keywords="wifi access point raspberry pi raspbian",
    url="https://github.com/mbunse/wifi_conf",
    project_urls={
        "Source Code": "https://github.com/mbunse/wifi_conf",
    }

    # could also include long_description, download_url, classifiers, etc.
)
