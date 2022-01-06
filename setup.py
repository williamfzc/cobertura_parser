from setuptools import setup, find_packages

__PROJECT_NAME__ = r"cobertura_parser"
__AUTHOR__ = r"williamfzc"
__AUTHOR_EMAIL__ = r"fengzc@vip.qq.com"
__VERSION__ = r"0.3.1"

setup(
    name=__PROJECT_NAME__,
    version=__VERSION__,
    author=__AUTHOR__,
    author_email=__AUTHOR_EMAIL__,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.6",
    install_requires=[
        "xmltodict",
        "planter",
        "pydantic",
        "fire",
        "lxml",
    ],
    entry_points={"console_scripts": ["cobertura_parser = cobertura_parser.cli:main"]},
)
