class WebhookResult:
    def __init__(self, speech):
        self.speech = speech
        self.contexts = []

    def to_dict(self):
        result = {
            'speech': self.speech,
            'displayText': self.speech,
            'source': 'slackroad-webhook-filler',
        }

        if self.contexts:
            result['contextOut'] = self.contexts

        return result

    def add_context(self, name, lifespan, params):
        self.contexts.append(
            {
                'name': name,
                'lifespan': lifespan,
                'parameters': params
            }
        )

    def _add_slack_data(self, slack_data):
        pass

    def _add_display_text(self, display_text):
        pass

    def _add_follow_up_event(self, name, param_value):
        pass
