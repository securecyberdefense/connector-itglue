from .operations import get_companies, get_locations, get_configurations, get_domains, get_flexible_asset, health_check
from connectors.core.connector import get_logger, Connector

logger = get_logger('ITGlue')


class Itglue(Connector):

    def execute(self, config, operation, params, **kwargs):
        supported_operations = {
            'get_companies': get_companies, 
            'get_locations': get_locations, 
            'get_configurations': get_configurations,
            'get_domains': get_domains,
            'get_flexible_asset': get_flexible_asset
        }
        return supported_operations[operation](config, params)

    def check_health(self, config):
        return health_check(config)
