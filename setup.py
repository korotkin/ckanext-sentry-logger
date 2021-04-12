from setuptools import find_packages, setup

setup(
    name='ckanext-sentry-logger',
    version='0.0.1',
    description='Enable Sentry\'s Flask logger functionality',
    long_description="""
    """,
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[],
    keywords='',
    author='https://github.com/ckan/ckan/graphs/contributors',
    author_email='info@ckan.org',
    url='http://ckan.org/',
    packages=find_packages(exclude=['ez_setup', 'tests']),
    namespace_packages=['ckanext', 'ckanext.sentry_logger'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        'sentry-sdk',
    ],
    entry_points="""
        [ckan.plugins]
        sentry_logger=ckanext.sentry_logger.plugin:SentryLoggerPlugin
    """,
)
