import os
from functools import lru_cache

import zenpy


class Client(object):

    _api_object_to_plural = {
        "Brand": "brands",
        "Group": "groups",
        "Macro": "macros",
        "TicketField": "ticket_fields",
        "TicketForm": "ticket_forms"
    }

    def __init__(
        self,
        subdomain=None,
        email=None,
        password=None,
        token=None,
        oauth_token=None
    ):
        self.subdomain = subdomain
        self._client = zenpy.Zenpy(
            subdomain=subdomain,
            email=email,
            password=password,
            token=token,
            oauth_token=oauth_token
        )

    def for_api_object(self, cls_name):
        return getattr(self, self._api_object_to_plural[cls_name])

    def create(self, api_object):
        if self.subdomain == os.environ.get("PRODUCTION_SUBDOMAIN"):
            raise Exception("DO NOT WRITE TO PRODUCTION!")

        return getattr(
            self._client,
            self._api_object_to_plural[api_object.__class__.__name__]
        ).create(
            api_object
        )

    @property
    @lru_cache()
    def brands(self):
        return dict((brand.name, brand) for brand in self._client.brands())

    @property
    @lru_cache()
    def groups(self):
        return dict((group.name, group) for group in self._client.groups())

    @property
    @lru_cache()
    def macros(self):
        return dict((macro.title, macro) for macro in self._client.macros())

    @property
    @lru_cache()
    def ticket_fields(self):
        return dict(
            (ticket_field.title, ticket_field)
            for ticket_field in self._client.ticket_fields()
        )

    @property
    @lru_cache()
    def ticket_forms(self):
        return dict(
            (ticket_form.name, ticket_form)
            for ticket_form in self._client.ticket_forms()
        )
