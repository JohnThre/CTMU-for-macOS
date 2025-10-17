from setuptools import setup, find_packages

setup(
    name="ctmu",
    version="2.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "qrcode[pil]>=7.4.2",
        "Pillow>=10.0.0", 
        "requests>=2.31.0",
        "click>=8.1.0"
    ],
    entry_points={
        "console_scripts": [
            "ctmu=ctmu.cli:main",
        ],
    },
    python_requires=">=3.8",
    author="CTMU Development Team",
    description="Swiss Army Knife CLI tool for macOS - QR codes, hashing, networking, file ops, and more",
    license="GPL-3.0",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: MacOS",
        "Environment :: Console",
        "Topic :: Utilities",
        "Topic :: System :: Systems Administration",
    ],
)