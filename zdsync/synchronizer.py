import os

from zenpy.lib.api_objects import (
    Brand,
    Group,
    Macro,
    TicketField,
    TicketForm
)

from .client import Client
from .printer import Printer


class Synchronizer(object):

    api_object = None
    attributes_to_compare = None
    attributes_to_sync = None

    def __init__(self):
        self.sandbox_client = Client(
            subdomain=os.environ.get("SANDBOX_SUBDOMAIN"),
            email=os.environ.get("SANDBOX_EMAIL"),
            password=os.environ.get("SANDBOX_PASSWORD"),
            token=os.environ.get("SANDBOX_TOKEN"),
            oauth_token=os.environ.get("SANDBOX_OAUTH_TOKEN")
        )
        self.production_client = Client(
            subdomain=os.environ.get("PRODUCTION_SUBDOMAIN"),
            email=os.environ.get("PRODUCTION_EMAIL"),
            password=os.environ.get("PRODUCTION_PASSWORD"),
            token=os.environ.get("PRODUCTION_TOKEN"),
            oauth_token=os.environ.get("PRODUCTION_OAUTH_TOKEN")
        )

    @property
    def production(self):
        return self.production_client.for_api_object(self.api_object.__name__)

    @property
    def sandbox(self):
        return self.sandbox_client.for_api_object(self.api_object.__name__)

    @property
    def only_in_sandbox(self):
        return list(
            set(self.sandbox.keys()) - set(self.production.keys())
        )

    @property
    def only_in_production(self):
        return list(
            set(self.production.keys()) - set(self.sandbox.keys())
        )

    @property
    def in_both(self):
        return list(
            set(self.production.keys()) & set(self.sandbox.keys())
        )

    @property
    def in_both_but_different(self):
        def _compare(title, attribute):
            this = getattr(self.production[title], attribute)
            that = getattr(self.sandbox[title], attribute)
            return this == that

        return [
            title for title in self.in_both
            if not all(
                [
                    _compare(title, attribute)
                    for attribute in self.attributes_to_compare
                ]
            )
        ]

    def find_production_from_production_id(self, cls_name, production_id):
        try:
            return next(
                api_object for api_object in
                self.production_client.for_api_object(cls_name).values()
                if api_object.id == production_id
            )
        except StopIteration:
            raise Exception(
                "Production {}({}) not found".format(
                    cls_name,
                    production_id
                )
            )

    def find_sandbox_from_production_id(self, cls_name, production_id):
        production_object = self.find_production_from_production_id(
            cls_name,
            production_id
        )

        # Zendesk is not consistent about "title" vs. "name" so try both.
        object_name = getattr(production_object, "title", None) or \
            getattr(production_object, "name", None)

        try:
            return self.sandbox_client.for_api_object(cls_name)[object_name]
        except KeyError:
            raise Exception(
                "Sandbox {}({}) not found".format(cls_name, object_name)
            )

    def _prepare_for_sync(self, old, new):
        pass

    def run(self, execute=False):
        if execute:
            created = []

            for title in self.only_in_production:
                attributes = dict(
                    (attribute, getattr(self.production[title], attribute))
                    for attribute in self.attributes_to_sync
                )

                self._prepare_for_sync(
                    self.production[title].to_dict(),
                    attributes
                )

                created.append(
                    self.sandbox_client.create(self.api_object(**attributes))
                )
        else:
            Printer(self).output()


class BrandSynchronizer(Synchronizer):

    api_object = Brand
    attributes_to_compare = ["name"]
    attributes_to_sync = ["name", "subdomain"]

    def _prepare_for_sync(self, _, new):
        if "subdomain" in new:
            new["subdomain"] = "{}{}".format(
                new["subdomain"],
                self.sandbox_client.subdomain.strip("easypost")
            )


class GroupSynchronizer(Synchronizer):

    api_object = Group
    attributes_to_compare = attributes_to_sync = ["name", "deleted"]


class MacroSynchronizer(Synchronizer):

    api_object = Macro
    attributes_to_compare = attributes_to_sync = ["title", "active"]

    def _prepare_for_sync(self, _, new):
        for action in new["actions"]:
            if "brand_id" == action["field"]:
                action["value"] = self.find_sandbox_from_production_id(
                    "Brand",
                    int(action["value"])
                ).id

            if "group_id" == action["field"] and \
                    action["value"] != "current_groups":
                action["value"] = self.find_sandbox_from_production_id(
                    "Group",
                    int(action["value"])
                ).id

            if "ticket_form_id" == action["field"] and \
                    action["value"] != "default_ticket_form":
                action["value"] = self.find_sandbox_from_production_id(
                    "TicketForm",
                    int(action["value"])
                ).id

            if "custom_fields" in action["field"]:
                production_id = int(action["field"].strip("custom_fields_"))
                sandbox_field = self.find_sandbox_from_production_id(
                    "TicketField",
                    production_id
                )

                action["field"] = "custom_fields_{}".format(sandbox_field.id)

                if action["value"].isdigit():
                    production_field = self.find_production_from_production_id(
                        "TicketField",
                        production_id
                    )
                    try:
                        production_option = next(
                            option
                            for option in production_field.custom_field_options
                            if option.id == int(action["value"])
                        )
                    except StopIteration:
                        # Option is no longer active.
                        action["value"] = None
                    else:
                        try:
                            action["value"] = next(
                                option for option
                                in sandbox_field.custom_field_options
                                if option.name == production_option.name
                            )
                        except StopIteration:
                            raise Exception(
                                "Sandbox {}({}) not found".format(
                                    "CustomFieldOption",
                                    production_option.name
                                )
                            )


class TicketFieldSynchronizer(Synchronizer):

    api_object = TicketField
    # TODO: support comparing against field if they exist.
    attributes_to_compare = attributes_to_sync = [
        "active",
        "description",
        "required",
        "tag",
        "title",
        "type",
        "collapsed_for_agents",
        "editable_in_portal",
        "regexp_for_validation"
    ]

    def _prepare_for_sync(self, old, new):
        if "custom_field_options" in old:
            new["custom_field_options"] = old["custom_field_options"]


class TicketFormSynchronizer(Synchronizer):

    api_object = TicketForm
    attributes_to_compare = [
        "name",
        "display_name",
        "active",
        "end_user_visible"
    ]
    attributes_to_sync = [
        "name",
        "display_name",
        "active",
        "end_user_visible",
        "position"
    ]

    def _prepare_for_sync(self, old, new):
        new["ticket_field_ids"] = [
            self.find_sandbox_from_production_id("TicketField", field_id).id
            for field_id in old["ticket_field_ids"]
        ]
        new["restricted_brand_ids"] = [
            self.find_sandbox_from_production_id("Brand", brand_id).id
            for brand_id in old["restricted_brand_ids"]
        ]
