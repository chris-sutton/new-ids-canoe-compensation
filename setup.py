from setuptools import setup, find_packages

setup(
    name="new_ids_canoe_compensation",
    version="0.1.0",
    description="Fetches new IDs from CANOE_2_General and CANOE_VU03_Principal and creates new records in CANOE_Compensation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Christopher Sutton",
    author_email="csuttonmajor@gmail.com",
    url="https://github.com/chris-sutton/new-ids-canoe-compensation",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        # List your project's dependencies here
        "pandas",
        "pytest",
        "python-dotenv",
        "Requests",
        "requests_mock",
        "setuptools",
        # Add other dependencies
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
)
