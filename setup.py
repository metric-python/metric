import os
import setuptools

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Metric",
    version="1.0rc1",
    description="Metric python framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={
        'scripts': 'metric/scripts'
    },
    python_requires='>=3.7'
)
