import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyelfwrapper", # Replace with your own username
    version="0.0.5",
    author="Sgnes",
    author_email="sgnes0514@gmai.com",
    description="A wrapper for dwarf format elf file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sgnes/elf_dwarf_wrapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'pyelftools',
      ],
    packages=[
        'elfwrapper'
        ],

    python_requires='>=3.8',
)