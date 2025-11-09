from setuptools import setup, find_packages

setup(
    name="queuectl",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "tabulate>=0.8.0",
    ],
    entry_points={
        "console_scripts": [
            "queuectl=queuectl.cli:cli",
        ],
    },
)
