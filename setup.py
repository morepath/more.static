from setuptools import setup, find_packages

long_description = "\n".join(
    (
        open("README.rst", encoding="utf-8").read(),
        open("CHANGES.txt", encoding="utf-8").read(),
    )
)

setup(
    name="more.static",
    version="0.11.dev0",
    description="BowerStatic integration for Morepath",
    long_description=long_description,
    author="Martijn Faassen",
    author_email="faassen@startifact.com",
    keywords="morepath bowerstatic bower",
    license="BSD",
    url="https://github.com/morepath/more.static",
    namespace_packages=["more"],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    install_requires=[
        "setuptools",
        "morepath >= 0.16",
        "bowerstatic >= 0.8",
    ],
    extras_require=dict(
        test=[
            "pytest >= 2.9.0",
            "WebTest >= 2.0.14",
            "pytest-remove-stale-bytecode",
        ],
        coverage=["pytest-cov"],
    ),
)
