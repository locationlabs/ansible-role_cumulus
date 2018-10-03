from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import errors


def validate_interfaces(configuration):
    """Validate interface configuration

    Checks the following:
    * interface name is 15 characters or less
    * interface name does not start with a number
    """
    for config_section in ("bonds", "interfaces"):
        for interface in config[config_section]:
            if len(interface) > 15 :
                return False
            elif interface[0].isdigit():
                return False
            else:
                return True


class TestModule(object):
    ''' Ansible file jinja2 tests '''

    def tests(self):
        return {
            'validate_interfaces': validate_interfaces,
        }
