import os

from setuptools import setup
import tapes

setup_pth = os.path.dirname(__file__)
readme_pth = os.path.join(setup_pth, 'README.rst')
requirements = os.path.join(setup_pth, 'requirements.txt')
dev_requirements = os.path.join(setup_pth, 'dev-requirements.txt')


setup(
    name='tapes',
    version=tapes.__version__,
    description='Metrics for Python processes',
    keywords='metrics',
    license='Apache License (2.0)',
    author='Emils Solmanis',
    author_email='emils.solmanis@gmail.com',
    url='https://www.github.com/emilssolmanis/tapes',
    long_description=open(readme_pth).read(),
    install_requires=open(requirements).read(),
    packages=['tapes'],
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: System :: Monitoring',
    ]
)
