"""
NYPR Crowdsourcing
"""
from setuptools import setup

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
        'Django==2.2.24',
        'django-admin-sortable2==1.0',
        'django-cors-headers==3.7.0',
        'django-extensions==3.1.3',
        'django-filter==2.4.0',
        'django-storages==1.11.1',
        'djangorestframework==3.12.4',
        'psycopg2==2.8.6',
        'raven',
        'requests',
        'uwsgi==2.0.19.1',
        'Pillow==8.2.0',
    ],
    tests_require=[
        'flake8<4',
        'pytest==3.7.2',
        'pytest-cov',
        'pytest-django',
        'pytest-env',
        'pytest-flake8==1.0.7',
        'importlib-metadata<5.0',
        'pytest-sugar',
        'coverage',
        'ipdb',
        'mixer',
    ],
    scripts=[
        "scripts/run_dev",
        "scripts/run_prod",
        "scripts/wait-for-it.sh",
        "manage.py"
    ],
    setup_requires=[
        'nyprsetuptools@https://github.com/nypublicradio/nyprsetuptools/tarball/master'
    ],
    entry_points={
        'distutils.commands': [
            'requirements = nyprsetuptools:InstallRequirements',
            'test = nyprsetuptools:PyTest',
            'test_requirements = nyprsetuptools:InstallTestRequirements',
            'deploy = nyprsetuptools:DockerDeploy',
        ],
        'distutils.setup_keywords': [
            'requirements = nyprsetuptools:setup_keywords',
            'test = nyprsetuptools:setup_keywords',
            'test_requirements = nyprsetuptools:setup_keywords',
            'deploy = nyprsetuptools:setup_keywords',
        ],
    },
)
