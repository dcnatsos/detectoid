from setuptools import setup


required = [
    'setuptools',
    'waitress',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
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
    name='detectoid',
    version='0.0.1.dev0',
    description="Detectoid, a simple website to guess whether a Twitch stream has viewbots",
    author="Benjamin Maisonnas",
    author_email="ben@wainei.net",
    url="https://github.com/Benzhaomin/detectoid.git",
    license = 'GPLv3',
    packages=[
        'detectoid',
    ],
    include_package_data=True,
    zip_safe = False,
    install_requires=required,
    extras_require=extras,
    test_suite="detectoid.tests",
    entry_points="""\
    [paste.app_factory]
    main = detectoid:main
    """,
      )
