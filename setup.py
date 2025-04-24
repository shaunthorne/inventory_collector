from setuptools import setup, find_packages

setup(
    name="inventory_collector",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "scrapli",
        "easysnmp",
        "pydantic",
        "python-dotenv",
    ],
    python_requires=">=3.8",
    description="Modular tool for collecting inventory from network devices via CLI and SNMP.",
    author="showunthorne",
    author_email="a.mu@ro.ru",
    url="https://github.com/shaunthorne/inventory_collector",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
    "console_scripts": [
        "inventory-collector = inventory_collector.main:main"
    ]
},
)
