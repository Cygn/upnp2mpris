#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Sinan Haliyo <sinan@haliyo.net>
#


import gobject

import logging

import dbus
import dbus.service
import dbus.proxies
import dbus.mainloop.glib

from time import sleep

global manager
manager = None

global Renderers
Renderers=dict()

import json
import xml.etree.ElementTree as ET

ROOT_OBJECT_PATH = '/com/intel/dLeynaRenderer'
RENDERER_BUS = 'com.intel.dleyna-renderer'

PROPS_IF_NAME = 'org.freedesktop.DBus.Properties'
INTROSPECTABLE_IF_NAME = 'org.freedesktop.DBus.Introspectable'

DEVICE_IF_NAME = 'com.intel.dLeynaRenderer.RendererDevice'
PUSH_HOST_IF_NAME = 'com.intel.dLeynaRenderer.PushHost'
MANAGER_INTERFACE = 'com.intel.dLeynaRenderer.Manager'

MEDIAPLAYER2_IF_NAME = 'org.mpris.MediaPlayer2'
PLAYER_IF_NAME = 'org.mpris.MediaPlayer2.Player'



def print_json(props):
    print json.dumps(props, indent=4, sort_keys=True)

def get_interface(path, if_name):
    return dbus.Interface(bus.get_object(RENDERER_BUS, path), if_name)


class RenderObject(dbus.service.Object):

    def __init__(self,object_path):
        self.__path = object_path
        self.__propsIF = get_interface(object_path, PROPS_IF_NAME)
        self.__playerIF = get_interface(object_path, PLAYER_IF_NAME)
        self.__pushhostIF = get_interface(object_path, PUSH_HOST_IF_NAME)
        self.__deviceIF = get_interface(object_path, DEVICE_IF_NAME)
        self.rendererName = self.__propsIF.Get('com.intel.dLeynaRenderer.RendererDevice','ModelName')
        dbus_Name = "org.mpris.MediaPlayer2."+self.rendererName       
        bus_name = dbus.service.BusName(dbus_Name,bus)
        dbus.service.Object.__init__(self, bus_name, '/org/mpris/MediaPlayer2')
        
        bus.add_signal_receiver(self.emitPropertiesChanged, path = self.__path, signal_name = "PropertiesChanged")



    def get_interfaces(self):
        try:
            introspectable_IF = get_interface(self.__path,
                                              INTROSPECTABLE_IF_NAME)
        except:
            print(u"Failed to retrieve introspectable interface")

        introspection = introspectable_IF.Introspect()
        tree = ET.fromstring(introspection)

        return [i.attrib['name'] for i in tree if i.tag == "interface"]

    def interfaces(self):
        for i in self.get_interfaces():
            print i



    def print_props(self, inner_if_name = ""):
        print_json(self.get_props(inner_if_name))
 
    @dbus.service.signal(PROPS_IF_NAME, signature="sa{sv}as")
    def PropertiesChanged(self, interface, changed_properties,
                          invalidated_properties):
        pass
 
    @dbus.service.method(PROPS_IF_NAME, signature="sa{sv}as")
    def emitPropertiesChanged(self, interface, changed_properties,
                          invalidated_properties):
        self.PropertiesChanged(interface, changed_properties,
                          invalidated_properties)

         
 
       
    @dbus.service.method(INTROSPECTABLE_IF_NAME)
    def Introspect(self):
        introspectable_IF = get_interface(self.__path, INTROSPECTABLE_IF_NAME)
        return introspectable_IF.Introspect()


    @dbus.service.method(PROPS_IF_NAME)
    def GetAll(self, inner_if_name = ""):
        return self.__propsIF.GetAll(inner_if_name)

    @dbus.service.method(PROPS_IF_NAME,in_signature="ss", out_signature="v")
    def Get(self, inner_if_name = "", prop_name = ""):
        return self.__propsIF.Get(inner_if_name, prop_name)


    @dbus.service.method(PROPS_IF_NAME,in_signature="ssv", out_signature="")
    def Set(self, if_name, prop_name, val):
        return self.__propsIF.Set(if_name, prop_name, val)

# Control methods
    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def Play(self):
        return self.__playerIF.Play()

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def Pause(self):
        return self.__playerIF.Pause()

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def PlayPause(self):
        return self.__playerIF.PlayPause()

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def Next(self):
        self.__playerIF.Next()

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def OpenUri(self, uri):
        self.__playerIF.OpenUri(uri)

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def OpenUriEx(self, uri, metadata):
        self.__playerIF.OpenUriEx(uri, metadata)

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def OpenNextUri(self, uri, metadata):
        self.__playerIF.OpenNextUri(uri, metadata)

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def SetUri(self, uri, metadata):
        self.__playerIF.SetUri(uri, metadata)

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def Previous(self):
        self.__playerIF.Previous()

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def Seek(self, offset):
        self.__playerIF.Seek(offset)

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def ByteSeek(self, offset):
        self.__playerIF.ByteSeek(offset)

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def GotoTrack(self, trackID):
        self.__playerIF.GotoTrack(trackID)

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def SetPosition(self, trackID, position):
        self.__playerIF.SetPosition(trackID, position)

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def SetBytePosition(self, trackID, position):
        self.__playerIF.SetBytePosition(trackID, position)

    @dbus.service.method('org.mpris.MediaPlayer2.Player')
    def Stop(self):
        self.__playerIF.Stop()

    @dbus.service.method('org.mpris.MediaPlayer2')
    def print_icon(self, mime_type, resolution):
        bytes, mime = self.__deviceIF.GetIcon(mime_type, resolution)
        print "Icon mime type: " + mime

# Push Host methods
    @dbus.service.method('org.mpris.MediaPlayer2')
    def host_file(self, path):
        return self.__pushhostIF.HostFile(path)

    @dbus.service.method('org.mpris.MediaPlayer2')
    def remove_file(self, path):
        self.__pushhostIF.RemoveFile(path)


def init_dleyna(bus):
    
    bus.start_service_by_name('com.intel.dleyna-renderer')
   
    sleep(3)

   
    dleyna_object = bus.get_object('com.intel.dleyna-renderer','/com/intel/dLeynaRenderer')
    global manager
    manager = dbus.Interface(dleyna_object,dbus_interface='com.intel.dLeynaRenderer.Manager')
    logger.info("dleyna initialized")
    try:
        makeRenderers()
    except:
        pass
                        

def makeRenderers(*args, **kwargs):
    obj = manager.GetRenderers()
    for i in obj:
        if i not in Renderers.keys():
            Renderers[i]=createMprisObject(i)

def checkRenderers(*args, **kwargs):
    obj = manager.GetRenderers()
    for i in Renderers.keys():
        if i not in obj:
            Renderers[i].remove_from_connection()
            logger.info("Lost renderer %s at %s",Renderers[i].rendererName,i)
            del Renderers[i]
        

def createMprisObject(path):
    renderer = RenderObject(path)
    logger.info("New renderer %s at %s", renderer.rendererName, path)
    
    return renderer



if __name__ == '__main__':
    
    log_format = '%(asctime)s %(module)s %(levelname)s: %(message)s'
    log_level = logging.INFO
    logging.basicConfig(format=log_format, level=log_level)
    logger = logging.getLogger('upnp2mpris')


    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    global bus
    bus = dbus.SessionBus()

    init_dleyna(bus)

    bus.add_signal_receiver(makeRenderers, dbus_interface = 'com.intel.dLeynaRenderer.Manager', signal_name = "FoundRenderer")
    bus.add_signal_receiver(checkRenderers, dbus_interface = 'com.intel.dLeynaRenderer.Manager', signal_name = "LostRenderer")

    loop = gobject.MainLoop()
    loop.run()
