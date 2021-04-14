import setuptools

with open('README.md','r') as f:
    long_description = f.read()

with open("dnplab/version.py", "r") as f:
    # Define __version__
    exec(f.read())

setuptools.setup(
    name='pyB12MPS',
    version=__version__,
    author='Bridge12 Technologies, Inc',
    author_email='tkeller@bridge12.com',
    description='A Python Package for Interfacing with the Bridge12 MPS',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://www.bridge12.com/',
    project_urls={
        'Source Code':'https://github.com/Bridge12Technologies/pyB12MPS',
        'Documentation':'http://pyb12mps.bridge12.com',
        },
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['numpy','pyserial'],
)
