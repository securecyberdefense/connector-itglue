from .itglueapi import ITGlue

from connectors.core.connector import get_logger, ConnectorError

logger= get_logger('connector_name')

def get_companies(config, params):
    """
    Gets all ITGlue companies and returns them.
    """
    itglue = ITGlue(config['api_key'], config['itglue_host'])
    return itglue.get_companies(params['filters'], params['page_size'], params['page_number'])

def get_locations(config, params):
    """
    Gets all locations for a company and returns them.
    """
    itglue = ITGlue(config['api_key'], config['itglue_host'])
    return itglue.get_locations(params['org'], params['filters'], params['page_size'], params['page_number'])

def get_configurations(config, params):
    """
    Gets all configurations for a company and returns them.
    """
    itglue = ITGlue(config['api_key'], config['itglue_host'])
    return itglue.get_configurations(params['org'], params['filters'], params['page_size'], params['page_number'])

def get_domains(config, params):
    """
    Gets all domains for a company and returns them.
    """
    itglue = ITGlue(config['api_key'], config['itglue_host'])
    return itglue.get_domains(params['org'], params['filters'], )

def get_flexible_asset(config, params):
    """
    Gets specified flexible asset for a company and returns it.
    """
    itglue = ITGlue(config['api_key'], config['itglue_host'])
    return itglue.get_flexible_asset(params['flexible_asset_name'], params['org'], params['filters'], params['page_size'], params['page_number'])

def health_check(config):
    """
    Tests the API to ensure it is working.
    """
    itglue = ITGlue(config['api_key'], config['itglue_host'])
    try:
        itglue._make_request('organizations', {})
        return True
    except: 
        return False