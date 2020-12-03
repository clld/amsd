from setuptools import setup, find_packages


setup(
    name='amsd',
    version='0.0',
    description='amsd',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='SHH DLCE Dev',
    author_email='lingweb@shh.mpg.de',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'clld>=7.4',
        'pyramid>=1.10',
        'csvw>=1.8',
        'clldmpg>=4.0.0',
        'sqlalchemy>=1.3',
        'waitress>=1.4.4',
    ],
    extras_require={
        'dev': [
            'flake8',
            'tox',
        ],
        'test': [
            'psycopg2>=2.8.6',
            'mock',
            'pytest>=6.0',
            'pytest-clld>=1.0.2',
            'pytest-mock>=3.3.1',
            'pytest-cov>=2.10.1',
            'coverage>=5.3',
            'selenium>=3.141',
            'zope.component>=4.6.2',
        ],
    },
    test_suite="amsd",
    entry_points="""\
    [paste.app_factory]
    main = amsd:main
""")
