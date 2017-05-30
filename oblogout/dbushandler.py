#!/usr/bin/env python

# Crunchbang Openbox Logout With Login Daemon Support
#   - GTK/Cairo based logout box styled for Crunchbang
#
#    Andrew Williams <andy@tensixtyone.com>
#    Gyorgy Jerovetz <jerovetz@comlions.net>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import logging
import dbus

class DbusController (object):

    @property
    def _sysbus (self):
        if not hasattr (DbusController, "__sysbus"):
            DbusController.__sysbus = dbus.SystemBus ()
        return DbusController.__sysbus

    @property
    def _logind (self):
        if not hasattr (DbusController, "__logind"):
            login1 = self._sysbus.get_object ("org.freedesktop.login1", "/org/freedesktop/login1")
            DbusController.__logind = dbus.Interface(login1, "org.freedesktop.login1.Manager")
        return DbusController.__logind

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def check_ability(self, action):
        if action == 'suspend':
            return self._logind.CanSuspend() == 'yes'
        elif action == 'hibernate':
            return self._logind.CanHibernate() == 'yes'
        elif action == 'safesuspend':
             if not self._logind.CanHibernate() == 'yes' or not pm.CanSuspend:
                return False

        return True

    def restart(self):
        if not self._logind.CanReboot():
            return False

        self.logger.debug("Rebooting...")
        return self._logind.Reboot(False)

    def shutdown(self):
        if not self._logind.CanPowerOff():
            return False
        else:
            return self._logind.PowerOff(False)

    def suspend(self):
        if not self._logind.CanSuspend():
            return False            
        else:
            return self._logind.Suspend(False)

    def hibernate(self):
        if not self._logind.CanHibernate():
            return False            
        else:
            return self._logind.Hibernate(False)

    def safesuspend(self):
        pass

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    t = DbusController()
    print t.restart()



