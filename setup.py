from setuptools import setup, find_packages
import sys, os

version = '0'
shortdesc = "Connect vortex to nix' hydra"
#longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

install_requires = [
    'setuptools',
    'tpv',
    'requests',
]


if sys.version_info < (2, 7):
    install_requires.append('unittest2')
    install_requires.append('ordereddict')


setup(name='tpv.nix.hydra',
      version=version,
      description=shortdesc,
      #long_description=longdesc,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        ],
      keywords='',
      author='Florian Friesdorf',
      author_email='flo@chaoflow.net',
      url='http://github.com/chaoflow/tpv.nix.hydra',
      license='AGPLv3+',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['tpv', 'tpv.nix'],
      include_package_data=True,
      zip_safe=True,
      install_requires=install_requires,
      )
