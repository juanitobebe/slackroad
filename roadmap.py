import requests
import requests_toolbelt.adapters.appengine # Patch it
from models import Organization

DEFAULT_ORG = 'plat'


class Roadmap:
    def __init__(self, api_token):
        requests_toolbelt.adapters.appengine.monkeypatch()
        self.api_token = api_token

    def get_roadmap_by_id(self, roadmap_id, organization_id):
        url = self._build_base_url(organization_id) + '/roadmaps/{roadmap_id}'.format(roadmap_id=roadmap_id)
        response = requests.get(url, headers=self._buld_headers())
        return response.json()['value']

    def get_roadmap_by_name(self, roadmap_name, organization_id):
        url = self._build_base_url(organization_id) + '/roadmaps/{roadmap_id}'.format(roadmap_id=roadmap_id)
        response = requests.get(url, headers=self._buld_headers())
        roadmaps = response.json()['values']

        for roadmap in roadmaps:
            if roadmap['name'].lower() == roadmap_name.lower():
                return roadmap

    def get_organization_by_name(self, organization_name):
        url = self._build_base_url() + '/organizations'
        response = requests.get(url, params={'page_size': 1000}, headers=self._buld_headers())
        values = response.json()['values']
        for organization in values:
            self._cache_organization(organization)
            if organization['name'].lower() == organization_name.lower():
                return organization

    def get_organization_by_id(self, organization_id):
        organization = self._get_organization_from_cache(organization_id)
        if organization:
            return organization

        url = self._build_base_url() + '/organizations'
        response = requests.get(url, params={'page_size': 1000}, headers=self._buld_headers())
        values = response.json()['values']
        for organization in values:
            self._cache_organization(organization)
            if organization['id'] == organization_id:
                return organization

    def create_roadmap(self, data):
        pass

    def create_item(self, data):
        pass

    def _buld_headers(self):
        return {
            'Authorization': self.api_token
        }

    def _build_base_url(self, organization_id=None):
        domain = self._fetch_organization_domain(organization_id) if organization_id else DEFAULT_ORG
        return 'https://{domain}.wizelineroadmap.com/api/v1'.format(domain=domain)

    def _fetch_organization_domain(self, organization_id):
        # Fetch from cache
        organization = self._get_organization_from_cache(organization_id)

        if organization:
            return organization.domain

        # Query if not there
        if not organization:
            roadmap_organization = self.get_organization_by_id(organization_id)
            return roadmap_organization['domain']

    def _get_organization_from_cache(self, organization_id):
        return Organization.get_by_id(organization_id)

    def _cache_organization(self, organization):
        Organization(id=organization['id'], domain=organization['domain']).put_async()
