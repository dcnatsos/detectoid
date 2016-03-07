from setuptools import setup


required = [
    'setuptools',
    'waitress',
    'sqlalchemy',
    'requests',
]

extras = {
    'test': [
        'setuptools',
        'mock',
        'webtest',
    ]
}


setup(
    name='destructoid',
    version='0.0.1.dev0',
    description="Destructoid, a simple website to guess whether a Twitch stream has viewbots",
    author="Benjamin Maisonnas",
    author_email="ben@wainei.net",
    url="https://github.com/Benzhaomin/destructoid.git",
    license = 'GPLv3',
    packages=[
        'destructoid',
    ],
    include_package_data=True,
    zip_safe = False,
    install_requires=required,
    extras_require=extras,
    test_suite="destructoid.tests",
    entry_points="""\
    [paste.app_factory]
    main = destructoid:main
    """,
      )
