from requests import request
from urllib import parse

class ITGlue:
    
    def __init__(self, api_key:str, host:str='https://api.itglue.com/'):
        self.host = self._fix_host(host)
        self.api_key = api_key

    def _fix_host(self, host):
        """
        Adds https:// to the beginning and / to the end of
        a given host name (if needed).
        """
        # Add 'https://' prefix
        if not host.startswith('https://'):
            host = f'https://{host}'
        
        # Add '/' suffix
        if not host.endswith('/'):
            host += '/'

        # Return host
        return host
        
    def _make_request(self, endpoint:str, filters:dict, page_size:int=50, page_number:int=1):
        """
        Generic function to handle making a request to ITGlue API. 
        Builds parameters, headers and URL and checks for a valid 
        response. 
        """
        # Build parameters
        params = {}
        for key, value in filters.items():
            if isinstance(value, (str, int)):
                params[f'filter[{key}]'] = value.replace(',', '\\,')
            elif isinstance(value, list):
                params[f'filter[{key}]'] = ','.join(value)
            else:
                raise TypeError(f'Invalid type. Must be str, list or int, got {type(value)}')
        params['page[size]'] = page_size
            
        # Build Headers
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }

        # Build URL
        url = self.host + endpoint

        # Make request
        response = request(method='get', url=url, params=params, headers=headers)

        # Verify response
        if not response.ok:
            raise Exception(f'Request failed for {endpoint} with status code {response.status_code} and message: {response.text}')

        return response.json()

    def _get_org_id_from_name(self, name):
        # Get organization
        org = self._make_request('organizations', {'name': name})

        # Return ID
        return org['data'][0]['id']

    def get_companies(self, filters:dict, page_size:int=None, page_number:int=None):
        """
        Gets all ITGlue companies and returns them.
        """
        return self._make_request('organizations', filters, page_size, page_number)

    def get_locations(self, org_name:int, filters:dict, page_size:int=None, page_number:int=None):
        """
        Gets all locations for a company and returns them.
        """
        # Get Org ID
        org_id = self._get_org_id_from_name(org_name)
        return self._make_request(f'organizations/{org_id}/relationships/locations', filters, page_size, page_number)

    def get_configurations(self, org_name:int, filters:dict, page_size:int=None, page_number:int=None):
        """
        Gets all configurations for a company and returns them.
        """
        # Get Org ID
        org_id = self._get_org_id_from_name(org_name)
        return self._make_request(f'organizations/{org_id}/relationships/configurations', filters, page_size, page_number)

    def get_domains(self, org_name:int, filters:dict, page_size:int=None, page_number:int=None):
        """
        Gets all domains for a company and returns them.
        """
        # Get Org ID
        org_id = self._get_org_id_from_name(org_name)
        return self._make_request(f'organizations/{org_id}/relationships/domains', filters, page_size, page_number)

    def get_flexible_asset(self, asset_name:str, org_name:int, filters:dict, page_size:int=None, page_number:int=None):
        """
        Gets specified flexible asset for a company and returns it.
        """
        # Get Org ID
        org_id = self._get_org_id_from_name(org_name)

        # Get flexible asset type ID
        asset_type_filters = {'name': asset_name}
        flexible_asset_obj = self._make_request('flexible_asset_types', asset_type_filters)
        asset_type_id = flexible_asset_obj['data'][0]['id']

        # Get flexible asset
        filters['flexible-asset-type-id'] = asset_type_id
        filters['organization-id'] = org_id
        return self._make_request(f'flexible_assets', filters, page_size, page_number)
