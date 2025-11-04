"""
Network Filtering in Finance
============================

Python implementation for creating animations of filtered correlation networks 
over time, based on geometric filtering methods developed by Tomaso Aste and colleagues.
"""

from setuptools import setup, find_packages
import os

# Read the long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="network-filtering-finance",
    version="1.0.0",
    author="Network Filtering Contributors",
    description="Animated correlation network filtering for financial time series",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/network-filtering-finance",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "jupyter>=1.0",
            "notebook>=6.4",
        ],
    },
    entry_points={
        "console_scripts": [
            "network-filter=correlation_network_animation:main",
        ],
    },
    keywords=[
        "network",
        "filtering",
        "correlation",
        "finance",
        "MST",
        "PMFG",
        "TMFG",
        "animation",
        "visualization",
        "time-series",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/network-filtering-finance/issues",
        "Source": "https://github.com/yourusername/network-filtering-finance",
        "Documentation": "https://github.com/yourusername/network-filtering-finance/blob/main/README.md",
    },
)
