from setuptools import setup

version="1.0.0"

with open("README.md", "r") as fd:
    long_description = fd.read()

setup(
    name="zheight",
    version=version,
    description="command-line tool to draw a picture of z-height",
    long_description=long_description,
    author="Kwanghun Chung Lab",
    packages=["zheight"],
    url="https://github.com/chunglabmit/zheight",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Programming Language :: Python :: 3.5'
    ],
    entry_points=dict(
        console_scripts = [
            "zheight=zheight.main:main"
        ]
    ),
    install_requires=[
        "numpy",
        "scipy",
        "tifffile",
        "scikit-image",
        "matplotlib"
    ]
)