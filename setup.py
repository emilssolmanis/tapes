import os

from setuptools import setup

setup_pth = os.path.dirname(__file__)
readme_pth = os.path.join(setup_pth, 'README.md')
requirements = os.path.join(setup_pth, 'requirements.txt')
dev_requirements = os.path.join(setup_pth, 'dev-requirements.txt')


setup(
    name='tapes',
    version='0.0.dev0',
    description='Stats for Python processes',
    license='Apache 2',
    author='Emils Solmanis',
    author_email='emils.solmanis@gmail.com',
    url='https://www.github.com/emilssolmanis/tapes',
    long_description=open(readme_pth).read(),
    install_requires=open(requirements).read(),
    packages=['tapes'],
    include_package_data=True,
    zip_safe=True,
)
