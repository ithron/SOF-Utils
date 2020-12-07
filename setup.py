import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as fh:
    requirements = fh.readlines()
requirements = [line.strip('\n') for line in requirements]

setuptools.setup(
    name="sof_utils",
    version="0.0.2",
    author="Stefan Reinhold",
    description="Small utilities to aid working with the SOF dataset",
    author_email="stefan@sreinhold.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ithron/SOF-Utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=['bin/sof-dicom-meta'],
    install_requires=requirements
)