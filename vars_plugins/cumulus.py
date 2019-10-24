from __future__ import absolute_import, division, print_function
__metaclass__ = type

from distutils.version import LooseVersion
from six import iteritems, itervalues, iterkeys
from ansible import __version__
from ansible.errors import AnsibleError
from ansible.inventory.group import Group
from ansible.inventory.host import Host
from ansible.plugins.vars.host_group_vars import VarsModule as AnsibleVarsModule
from ansible.utils.display import Display
from ansible.utils.vars import combine_vars

display = Display()
if LooseVersion(__version__) < LooseVersion("2.4"):
    raise AnsibleError('Cumulus vars plugin requires Ansible 2.4 or newer')


class VarsModule(AnsibleVarsModule):
    '''
    Adds configuration to slave interfaces of a bond:
      * Sets alias_name of interface to Master:<bond_name>
      * Copies mstpctl settings from bond to slave interfaces if they exist
    '''

    def get_vars(self, loader, path, entities, cache=True):
        display.debug('in cumulus get_vars()')
        new_data = {}
        for entity in entities:
            if isinstance(entity, Host) or isinstance(entity, Group):
                host_group_vars_data = super(VarsModule, self).get_vars(loader, path, entities)
                if isinstance(host_group_vars_data, dict):
                    if 'config' in host_group_vars_data.keys():
                        display.debug('config data found')
                        if 'bonds' in host_group_vars_data['config'].keys():
                            interfaces = {}
                            # This works because of explaination at
                            # https://docs.python.org/2/library/stdtypes.html#dict.items and six
                            # is just a wrapper around them
                            for bond, bond_name in zip(itervalues(host_group_vars_data['config']['bonds']),
                                                       iterkeys(host_group_vars_data['config']['bonds'])):
                                display.debug('bond: %s found' % bond_name)
                                mstpctl_settings = {
                                    key: value
                                    for key, value in iteritems(bond)
                                    if key.startswith('mstpctl')
                                }

                                if 'slaves' in bond:
                                    for slave_iface in bond['slaves']:
                                        if mstpctl_settings:
                                            display.debug(
                                                'Configuring slave interface(s): %s' % ' '.join(
                                                    bond['slaves']
                                                )
                                            )
                                            interfaces[slave_iface] = combine_vars(mstpctl_settings, {'alias_name': 'Master:%s' % bond_name})
                                        else:
                                            interfaces[slave_iface] = {'alias_name': 'Master:%s' % bond_name}

                            if interfaces:
                                display.debug('slave interfaces configured')
                                new_data = {'config': {'interfaces': interfaces}}

        display.debug('done with get_vars()')
        return new_data
