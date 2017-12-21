from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import errors


def is_member_of(self, value, membership):
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


class FilterModule(object):
    def filters(self):
        return {
            'is_member_of': is_member_of
        }
