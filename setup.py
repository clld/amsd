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
    author='EVA DLCE Dev',
    author_email='dlce.rdm@eva.mpg.de',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pyramid>=2.0',
        'clld>=11.2.2',
        'csvw>=3.3.0',
        'clldmpg>=4.3.1',
        'sqlalchemy>=1.4.27',
        'waitress>=1.4.4',
    ],
    extras_require={
        'dev': [
            'flake8',
            'tox',
        ],
        'test': [
            'psycopg2>=2.8.6',
            'mock>=4.0.3',
            'pytest>=7.4.2',
            'pytest-clld>=1.2.0',
            'pytest-mock>=3.10.0',
            'pytest-cov>=4.0.0',
            'coverage>=5.5',
            'selenium>=4.17.2',
            'zope.component>=5.0.1',
        ],
    },
    test_suite="amsd",
    entry_points="""\
    [paste.app_factory]
    main = amsd:main
""")
