#Functions used for the neighbor discovery algorithim and for the formation of wi-fi networks between 2 devices
import parameters as p;
import time
import cmd_functions as c;
import socket;

#Input:
#    Neighbor detailed information (sudo wpa_cli p2p_peer <neighbor MAC>)
#Output:
#    Identifier of the neighbor
def is_Parent(cmdout):
    inde=cmdout.find(bytes('PARENT','utf8')); 
    if inde != -1:
        return True;
    return False;
#Input:
#    Neighbor detailed information (sudo wpa_cli p2p_peer <neighbor MAC>)
#Output:
#    RSSI of the neighbor discovery beacon received from the neighbor
def find_neighbor_RSSI(cmdout):
    bstart=bytes('level=','utf8');
    inde=cmdout.find(bstart); 
    if inde != -1:
        cmdout=cmdout[inde+len(bstart):];
        indd=cmdout.find(bytes('\n','utf8'));
        return int(cmdout[:indd]);
    return None;

def reboot():
    cmdout=c.write_read_cmd(['sudo','wpa_cli','p2p_flush']);
    cmdout=c.write_read_cmd(['sudo','wpa_cli','p2p_find']);

def start_ip():
    cmdout=c.write_read_cmd(['sudo','ifconfig','eth0','192.168.1.11','netmask','255.255.255.0']);
    print (cmdout);
#It starts the neighbor discovery mechanisim
#Input: Wifi interface name
def start_protocol(wifiPort):
    cmdout=c.write_read_cmd(['sudo','ifconfig',wifiPort,'up']);
    cmdout=c.write_read_cmd(['sudo','rm','/var/run/wpa_supplicant/"','wifiPort','-f']);
    cmdout=c.write_read_cmd(['sudo','killall','wpa_supplicant']);
    time.sleep(p.sleepStart);
    cmdout=c.write_read_cmd(['sudo','wpa_supplicant','-i',wifiPort,'-c',p.pathe+'/p2p.conf','-Dnl80211','-B','-u']);
    print(cmdout);
    reboot();

def close_connection(s):
    try:
        s.shutdown(1);
    except:
        pass;
    try:
        s.close();
    except:
        pass;
    try:
        s.close();
    except:
        pass;

def start_client():
    s=None;
    try:
        s = socket.socket();
        s.settimeout(15);
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
        s.connect(('192.168.1.10',7000));
    except Exception as e: 
        print(e);
    close_connection(s);

def check_device():
        cmdout=c.write_read_cmd(['sudo', 'wpa_cli','p2p_peer','fe:c2:de:2a:86:c0']);
        if is_Parent(cmdout):
            rssi=find_neighbor_RSSI(cmdout);
            start_client();
            print ('True');
        else:
            print ('False');