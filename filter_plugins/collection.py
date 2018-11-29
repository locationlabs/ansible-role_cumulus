from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import errors


def is_member_of(value, membership):
    """
    Return value if value is in given list, else raise error

    This form was inspired from http://www.dasblinkenlichten.com/creating-ansible-filter-plugins/
    and https://projectme10.wordpress.com/2016/01/17/how-to-write-an-ansible-filter-dynamically-configuring-interface-descriptions-in-a-multivendor-environment/
    """
    if isinstance(membership, list):
        if value in membership:
            return value
        else:
            raise errors.AnsibleFilterError("Variable value is invalid!")
    else:
        raise errors.AnsibleFilterError("Provided membership list is not a list!")

def dot1x_interfaces(configuration, type='dot1x'):
    """
    Return list of dot1x enabled interfaces.

    Default will return all dot1x interfaces, use type to get a subset.
    """
    ## Redo this!
    dot1x_filter = set(['dot1x', 'dot1x_mab', 'dot1x_parking'])
    if type not in dot1x_filter:
        raise errors.AnsibleFilterError("Invalid type provided. Valid types: dot1x, dot1x_mab, dot1x_parking")

    interface_list = []
    for iface, iface_config in configuration['interfaces'].iteritems():
        if type == 'dot1x':
            if len(dot1x_filter.intersection(set(iface_config))) > 0:
                interface_list.append(iface)
        else:
            if type in iface_config:
                interface_list.append(iface)

    return interface_list


class FilterModule(object):
    def filters(self):
        return {
            'is_member_of': is_member_of,
            'dot1x_interfaces': dot1x_interfaces
        }
