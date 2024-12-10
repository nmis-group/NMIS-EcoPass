from setuptools import setup, find_packages

setup(
    name='NMIS_Ecopass', 
    version='0.1.7',
    packages=find_packages(),
    package_data={'dpp_framework': ['py.typed']},
    install_requires=[
        'pydantic>=1.7',
        'pydantic[email]'
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.5',
            'flake8>=3.8.4',
            'black>=22.3.0'
        ]
    },
    description='A package for creating and managing digital product passports',
    author='Syed Awais Hassan Munawar',
    author_email='syed.munawar@strath.ac.uk',
    url='https://github.com/yourusername/NMIS_Ecopass',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
