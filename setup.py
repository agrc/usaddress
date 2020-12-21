import os
import subprocess
from distutils.cmd import Command

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py


class TrainModel(Command):
    description = "Training the model before building the package"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        PYTHONPATH = os.environ.get("PYTHONPATH", "")
        subprocess.run(
            ["parserator", "train", "training/labeled.xml", "usaddress"],
            env=dict(os.environ, PYTHONPATH=f".{os.pathsep}{PYTHONPATH}"),
        )


class build_py(_build_py):
    def run(self):
        self.run_command("train_model")  # Run the custom command
        super().run()


# Standard setup configuration
setup(
    version='0.6.0',
    url='https://github.com/agrc/usaddress',
    description='Parse US addresses using conditional random fields',
    name='agrc-usaddress',
    packages=['usaddress'],
    package_data={'usaddress': ['usaddr.crfsuite']},
    license='The MIT License: http://www.opensource.org/licenses/mit-license.php',
    install_requires=['python-crfsuite>=0.7',
                      'future>=0.14',
                      'probableparsing'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis'],
    long_description="""
    usaddress is a python library for parsing unstructured address strings into
    address components, using advanced NLP methods.

    From the python interpreter:

    >>> import usaddress
    >>> usaddress.parse('123 Main St. Suite 100 Chicago, IL')
    [('123', 'AddressNumber'),
     ('Main', 'StreetName'),
     ('St.', 'StreetNamePostType'),
     ('Suite', 'OccupancyType'),
     ('100', 'OccupancyIdentifier'),
     ('Chicago,', 'PlaceName'),
     ('IL', 'StateName')]
    """
)
