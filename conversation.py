from config import API_TOKEN
from roadmap import Roadmap
from utils import WebhookResult


class Conversation:
    def __init__(self):
        self.action_map = {
            'organization.select': self._select_organization,
            'roadmap.select': self._select_roadmap
        }

    def process_request(self, req):
        results = req.get('result')
        action = results.get('action')
        parameters = results.get('parameters')
        contexts = self._map_contexts(results.get('contexts', []))

        action_function = self.action_map.get(action)

        if not action_function:
            return {}

        webhook_response = action_function(parameters, contexts)

        return webhook_response.to_dict()

    def _map_contexts(self, contexts_list):
        return {
            context['name']:
                {'parameters': context['parameters'], 'lifespan': context['lifespan']}
            for context in contexts_list
        }

    def _select_roadmap(self, params, contexts):
        roadmap_name = params['roadmap_name']
        organization_name = params['organization_name']

        roadmap = self._roadmap_client().get_roadmap_by_name(roadmap_name, organization_name)
        speech = 'Ok. {roadmap_name} in {organization_name} selected'.format(
            roadmap_name=roadmap['name'],
            organization_name=organization_name,
        )

        result = WebhookResult(speech)
        result.add_context('roadmap', 5, {
            'roadmap_name': roadmap['name'],
            'rodmap_id': roadmap['id']
        })

        return result

    def _select_organization(self, params, contexts):
        organization_name = params['organization_name']
        organization = self._roadmap_client().get_organization_by_name(organization_name)

        speech = 'Ok. {organization_name} selected'.format(organization_name=organization['name'])
        result = WebhookResult(speech)
        result.add_context(
            'organization',
            5,
            {
                'organization_name': organization['name'],
                'organization_id': organization['id']
            }
        )
        return result

    def _roadmap_client(self):
        return Roadmap(API_TOKEN)
