#!/usr/bin/env python3

from pathlib import Path

import setuptools

project_dir = Path(__file__).parent

setuptools.setup(
    name="impfbot",
    version=project_dir.joinpath(
        "version.txt").read_text().split("\n")[0],
    description="Notification bot for the lower saxony vaccination portal",
    long_description=project_dir.joinpath(
        "README.md").read_text(encoding="utf-8"),
    keywords=["python"],
    author="sibalzer",
    url="https://github.com/sibalzer/impfbot",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=project_dir.joinpath(
        "requirements.txt").read_text().split("\n"),
    zip_safe=False,
    license="GPL v3",
)
