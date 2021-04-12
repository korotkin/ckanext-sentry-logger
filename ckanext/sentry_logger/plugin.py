import logging
from flask import Blueprint
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

import ckan
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import config, asbool

from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

log = logging.getLogger(__name__)

SENTRY_DSN = 'ckanext.sentry_logger.sentry_dsn'
SENTRY_ENABLE_TEST_URL = 'ckanext.sentry_logger.sentry_enable_test_url'


class SentryLoggerPlugin(plugins.SingletonPlugin):
    '''
    Microsoft Azure auth service connector
    '''

    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IConfigurer)

    def update_config(self, config):
        pass

    def update_config_schema(self, schema):
        not_empty = toolkit.get_validator('not_empty')
        unicode_safe = toolkit.get_validator('unicode_safe')
        schema.update({
            SENTRY_DSN: [not_empty, unicode_safe],
        })
        return schema

    def register_debugger(self):
        sentry_sdk.init(
            dsn=config[SENTRY_DSN],
            integrations=[
                FlaskIntegration(),
                SqlalchemyIntegration(),
                RedisIntegration()
            ],

            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0,

            # By default the SDK will try to use the SENTRY_RELEASE
            # environment variable, or infer a git commit
            # SHA as release, however you may want to set
            # something more human-readable.
            release=ckan.__version__,

            # environment='production',
            max_breadcrumbs=50,
            debug=True,
        )

    def get_blueprint(self):
        '''Register test endpoint'''

        blueprint = Blueprint(self.name, self.__module__)
        if asbool(config[SENTRY_ENABLE_TEST_URL]):
            def test_callback():
                division_by_zero = 1 / 0
            blueprint.add_url_rule(
                rule='/debug-sentry',
                endpoint='debug',
                view_func=test_callback,
            )
        self.register_debugger()
        return blueprint
