from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from distutils.version import LooseVersion
from six import iteritems, itervalues
from ansible import __version__
from ansible.errors import AnsibleError
from ansible.plugins.vars.host_group_vars import VarsModule as AnsibleVarsModule
from ansible.inventory.host import Host
from ansible.inventory.group import Group
# from ansible.utils.vars import combine_vars

if LooseVersion(__version__) < LooseVersion("2.4"):
    raise AnsibleError('Cumulus vars plugin requires Ansible 2.4 or newer')


class VarsModule(AnsibleVarsModule):
    '''
    Looks for bonds with mstpctl settings and configures the slave interfaces
    with the same settings.
    '''

    def get_vars(self, loader, path, entities, cache=True):
        self._display.debug('in CumulusVarsModule')
        new_data = {}
        for entity in entities:
            if isinstance(entity, Host) or isinstance(entity, Group):
                data = super(VarsModule, self).get_vars(loader, path, entities)
                if isinstance(data, dict):
                    if 'config' in data.keys():
                        self._display.debug('config data found')
                        if 'bonds' in data['config'].keys():
                            interfaces = {}
                            for bond in itervalues(data['config']['bonds']):
                                self._display.debug('bond: %s found' % bond['alias_name'])
                                mstpctl_settings = {
                                    key: value
                                    for key, value in iteritems(bond)
                                    if key.startswith('mstpctl')
                                }
                                if mstpctl_settings:
                                    self._display.debug('Configuring slave interface(s): %s' % ''.join(bond['slaves']))
                                    for slave_iface in bond['slaves']:
                                        interfaces[slave_iface] = mstpctl_settings

                            if interfaces:
                                self._display.debug('slave interfaces configured')
                                new_data = {'config': {'interfaces': interfaces}}

        self._display.debug('done with get_vars()')
        return new_data
