#!/usr/bin/python
#It perform the epidemic routing protocol on top of WiFi direct and TCP/IP
import routing as r;
import dbus;
from gi.repository import GObject as gobject;
import threading;
from dbus.mainloop.glib import DBusGMainLoop;
import parameters as p;
import time;
#It locks sensitive procesess
mutex=threading.Lock(); 
#It describes the signals and the main functions for the epidemic routing protocol
class P2P_EVENT (threading.Thread):
    # Needed Variables
    global bus
    global wpas_object
    global interface_object
    global p2p_interface
    global interface_name
    global wpas
    global wpas_dbus_interface
    global timeout
    global path
    # Dbus Paths
    global wpas_dbus_opath
    global wpas_dbus_interfaces_opath
    global wpas_dbus_interfaces_interface
    global wpas_dbus_interfaces_p2pdevice   
    # Required Signals
    #It is executed when a Neighbor discovery beacon is received
    def deviceFound(self,devicepath):
        pass;
    #It is executed when a neighbor requests a connection
    def goNegotiationRequest(self,devicepath,password,gointent):
        pass;
    #It is executed when 2 devices agree in a channel and in the roles for Wi-Fi direct
    def GONegotiationSuccess(self,status):
        pass;
    #It is executed when the wi-fi network between the 2 devices is ready
    def GroupStarted(self,properties):
        pass;
    #It is executed when the wi-fi network is removed
    def GroupFinished(self,status):
        pass;
    #It is executed when there was an syncronization error in the formation of a wi-fi network between the 2 devices
    def GONegotiationFailure(self,status):
        pass;
    #It is executed when there was an autentification error in the formation of a wi-fi network between the 2 devices
    def WpsFailure(self,status, etc):
        pass;
    #It is executed when the device deletes a neighbor from its internal neighborlist
    def deviceLost(self,devicepath):
        pass;
    #Main loop for periodic procesess
    def p2p_periodic(self):
        time.sleep(5);
        mutex.acquire();
        try:
            r.check_device();
            r.reboot();
        finally:
            mutex.release();
        
    # Constructor. It starts the epidemic protocol and it registers the wpa_supplicant signals in the D-Bus
    def __init__(self):
        r.start_ip();
        # Initializes variables and threads
        self.interface_name=p.wifiPort;   #Wireless interface
        #Start epidemic protocol    
        r.start_protocol(p.wifiPort); 
        self.wpas_dbus_interface = 'fi.w1.wpa_supplicant1'
        # Initializes thread and daemon allows for ctrl-c kill
        threading.Thread.__init__(self)
        self.daemon = True
        # Generating interface/object paths
        self.wpas_dbus_opath = "/" + \
                        self.wpas_dbus_interface.replace(".","/")
        self.wpas_wpas_dbus_interfaces_opath = self.wpas_dbus_opath + \
                        "/Interfaces"
        self.wpas_dbus_interfaces_interface = \
                        self.wpas_dbus_interface + ".Interface"
        self.wpas_dbus_interfaces_p2pdevice = \
                        self.wpas_dbus_interfaces_interface \
                        + ".P2PDevice"
        # Getting interfaces and objects
        DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()
        self.wpas_object = self.bus.get_object(
                        self.wpas_dbus_interface,
                        self.wpas_dbus_opath)
        self.wpas = dbus.Interface(self.wpas_object,
                        self.wpas_dbus_interface)
        self.path = self.wpas.GetInterface(
                                self.interface_name)
        self.interface_object = self.bus.get_object(
                        self.wpas_dbus_interface, self.path)
        self.p2p_interface = dbus.Interface(self.interface_object,
                        self.wpas_dbus_interfaces_p2pdevice)
        #Adds listeners for find and lost
        self.bus.add_signal_receiver(self.deviceFound,
                dbus_interface=self.wpas_dbus_interfaces_p2pdevice,
                signal_name="DeviceFound");
        self.bus.add_signal_receiver(self.deviceLost,
                dbus_interface=self.wpas_dbus_interfaces_p2pdevice,
                signal_name="DeviceLost");
        self.bus.add_signal_receiver(self.goNegotiationRequest,
                dbus_interface=self.wpas_dbus_interfaces_p2pdevice,
                signal_name="GONegotiationRequest");
        self.bus.add_signal_receiver(self.GONegotiationSuccess,
                dbus_interface=self.wpas_dbus_interfaces_p2pdevice,
                signal_name="GONegotiationSuccess");
        self.bus.add_signal_receiver(self.GONegotiationFailure,
                dbus_interface=self.wpas_dbus_interfaces_p2pdevice,
                signal_name="GONegotiationFailure");
        self.bus.add_signal_receiver(self.GroupStarted,
                dbus_interface=self.wpas_dbus_interfaces_p2pdevice,
                signal_name="GroupStarted");
        self.bus.add_signal_receiver(self.WpsFailure,
                dbus_interface=self.wpas_dbus_interfaces_p2pdevice,
                signal_name="WpsFailed");
        self.bus.add_signal_receiver(self.GroupFinished,
                dbus_interface=self.wpas_dbus_interfaces_p2pdevice,
                signal_name="GroupFinished");   
    # Run P2P_EVENT. It runs the epidemic protocol
    def run(self):
        # Allows other threads to keep working while MainLoop runs (It works poorly with GLib.MainLoop())
        gobject.MainLoop().get_context().iteration(True)
        gobject.threads_init();
        gobject.MainLoop().run();
            
#It calls the epidemic protocol
p2p_catch_event = P2P_EVENT();
p2p_catch_event.start();
while True:
    p2p_catch_event.p2p_periodic();
