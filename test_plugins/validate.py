from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import errors


def validate_interfaces(configuration):
    """Validate interface configuration

    Checks the following:
    * interface name is 15 characters or less
    * interface name does not start with a number
    """
    for config_section in [ s for s in ("bonds", "interfaces") if s in configuration.keys() ]:
        for interface in configuration[config_section]:
            if len(interface) > 15 :
                return False
            elif interface[0].isdigit():
                return False
            else:
                return True

def validate_802_1x(configuration):
    """Validate 802.1X parameters

    Checks the following when dot1x hash exists:
    * Both server_ip and shared_secret are defined
    * Only one dot1x option is set per switchport
    * MAB activation delay is between 5 and 30
    """
    if 'dot1x' in configuration:
        if ('server_ip' and 'shared_secret') not in configuration["dot1x"]:
            return False

        if 'mab_activation_delay' in configuration["dot1x"]:
            if configuration["dot1x"]["mab_activation_delay"] < 5 or configuration["dot1x"]["mab_activation_delay"] > 30:
                return False

        dot1x_filter = set(['dot1x', 'dot1x_mab', 'dot1x_parking'])
        for interface in configuration["interfaces"].itervalues():
            iface_params = set(interface.keys())
            if len(dot1x_filter.intersection(iface_params)) > 1:
                return False
    else:
        return True

class TestModule(object):
    ''' Ansible file jinja2 tests '''

    def tests(self):
        return {
            'validate_interfaces': validate_interfaces,
            'validate_802_1x': validate_802_1x,
        }
