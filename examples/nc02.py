#! /usr/bin/env python2.6
#
# Retrieve the running config from the NETCONF server passed on the
# command line using get-config and write the XML configs to files.
#
# $ ./nc02.py broccoli

import sys, os, warnings
warnings.simplefilter("ignore", DeprecationWarning)
from ncclient import manager

def demo(host, user, password):
    with manager.connect(host=host, port=2831, username=user, password=password, , hostkey_verify=False) as m:
        c = m.get_config(source='running').data_xml
        with open("%s.xml" % host, 'w') as f:
            f.write(c)
        print c

if __name__ == '__main__':
    demo(sys.argv[1], sys.argv[2], sys.argv[3])
