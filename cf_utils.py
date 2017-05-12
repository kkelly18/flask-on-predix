import json
import os

from custom__exceptions import ServiceBindingError

from app import logger


def get_postgres_bindings():
    """ Interrogate Cloud Foundry environment for bindings to Postgres service 
    
    $cf env <app name> shows the current form of the json for VCAP_SERVICES
    
    :return tuple 
    """

    # todo: consider returning named tuple

    binding_uri = None
    binding_name = None
    binding_label = None

    vcap_services = os.getenv("VCAP_SERVICES")
    if vcap_services:
        decoded_config = json.loads(vcap_services)

        try:
            postgres = decoded_config['postgres'][0]  # todo: handle more than one postgres service bound to app
            if postgres:
                binding_uri = postgres['credentials']['uri']
                binding_name = postgres['name']
                binding_label = postgres['label']

        except (KeyError, IndexError):
            logger.exception("Postgres config is missing or mangled ")
            raise ServiceBindingError(vcap_services, "Missing or mangled postgres config")

    else:
        logger.debug("Missing VCAP_SERVICES")
        raise ServiceBindingError(vcap_services, "VCAP_SERVICES not found")

    logger.info("Postgres binding: {}".format(binding_uri))

    return binding_uri, binding_name, binding_label


