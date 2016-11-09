from setuptools import setup, find_packages

setup(
    name='taxcli',
    author='Arne Beer',
    author_email='arne@twobeer.de',
    version='0.6.4',
    description='Ein commandline interface zur erfassung von Ausgaben, Rechnungen und AfA — Edit',
    keywords='commandline tax germany',
    url='http://github.com/nukesor/taxcli',
    license='MIT',
    install_requires=[
        'sqlalchemy>=1.1.3',
        'terminaltables>=2.1.0'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Environment :: Console'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'taxcli=taxcli:main'
        ]
    })
