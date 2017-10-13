"""
NYPR Crowdsourcing
"""
from setuptools import setup
try:
    import nyprsetuptools
except ImportError:
    import pip
    pip.main(['install', '-U', 'git+https://github.com/nypublicradio/nyprsetuptools.git'])
    import nyprsetuptools


setup(
    name='crowdsourcing',
    version='0.0.1',
    author='NYPR Digital',
    author_email='digitalops@nypublicradio.org',
    url='https://github.com/nypublicradio/crowdsourcing',
    description=__doc__,
    long_description=__doc__,
    packages=[
        'crowdsourcing',
        'surveys',
        'surveys.migrations',
    ],
    package_dir={
        'crowdsourcing': 'crowdsourcing',
        'surveys': 'surveys',
    },
    zip_safe=True,
    license='BSD',
    include_package_data=True,
    install_requires=[
        'boto3',
        'Django>=1.8,<2.0',
        'django-admin-sortable2',
        'django-cors-headers',
        'django-extensions',
        'django-filter',
        'django-storages',
        'djangorestframework>=3.7.0',
        'djangorestframework-jsonapi',
        'psycopg2',
        'raven',
        'requests',
        'uwsgi',
    ],
    tests_require=[
        'coverage',
        'ipdb',
        'mixer',
    ],
    scripts=[
        "scripts/run_dev",
        "scripts/run_prod",
        "manage.py"
    ],
    cmdclass={
        'deploy': nyprsetuptools.DockerDeploy,
        'requirements': nyprsetuptools.InstallRequirements,
        'test': nyprsetuptools.DjangoTest,
    }
)
