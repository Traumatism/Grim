from setuptools import setup, find_namespace_packages

# The version of this tool is based on the following steps:
# https://packaging.python.org/guides/single-sourcing-package-version/

setup(
    name="grim",
    author="toast",
    author_email="toast@mailfence.com",
    url="https://github.com/traumatism/grim",
    description="Create discord bots",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src", exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "setuptools>=45.0",
        "pydantic>=1.0.0",
        "requests>=2.22.0",
        ""
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.0",
        "Topic :: Utilities",
    ],
)
