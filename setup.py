from setuptools import setup, find_packages
import os
import sys

version = '0'
shortdesc = "Connect vortex to nix' facilities (hydra/store/...)"
#longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

install_requires = [
    'setuptools',
    'requests',
    'tpv',
    'tpv.cli',
]


if sys.version_info < (2, 7):
    install_requires.append('argparse')
    install_requires.append('ordereddict')
    install_requires.append('unittest2')


setup(name='tpv.nix',
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
      url='http://github.com/chaoflow/tpv.nix',
      license='AGPLv3+',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['tpv'],
      include_package_data=True,
      zip_safe=True,
      install_requires=install_requires,
      entry_points={
          'console_scripts': ['xin = tpv.nix.xin:app'],
          'tpv.nix.xin.commands': [
              'install = tpv.nix.xin:Install',
              #'generation = tpv.nix.xin.generation:Generation',
              #'generation/remove = tpv.nix.xin.generation:Remove',
              'profile = tpv.nix.xin.profile:Profile',
              'profile/remove = tpv.nix.xin.profile:Remove',
              'remove = tpv.nix.xin:Remove',
              'search = tpv.nix.xin:Search',
          ],
      },
      )
