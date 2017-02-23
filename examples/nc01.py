#! /usr/bin/env python2.6
#
# Connect to the NETCONF server passed on the command line and
# display their capabilities. This script and the following scripts
# all assume that the user calling the script is known by the server
# and that suitable SSH keys are in place. For brevity and clarity
# of the examples, we omit proper exception handling.
#
# $ ./nc01.py broccoli


import sys, os, warnings
import logging
from ncclient import manager
warnings.simplefilter("ignore", DeprecationWarning)
log = logging.getLogger(__name__)

CREATE_SUBINTERFACE = """
<config>
        <cli-config-data>
            <cmd>set interface state  %s up</cmd>
            <cmd>create sub %s %s</cmd>
            <cmd>set interface ip address %s.%s %s/%s</cmd>
            <cmd>set interface state  %s.%s up</cmd>
        </cli-config-data>
</config>
"""
HEELO = """
#<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <capabilities>
        <capability>urn:ietf:params:netconf:base:1.0</capability>
    </capabilities>
#</hello>
"""

def _check_response(rpc_obj, snippet_name):
    log.debug("RPCReply for %s is %s" % (snippet_name, rpc_obj.xml))
    xml_str = rpc_obj.xml
    if "<ok />" in xml_str:
        log.info("%s successful" % snippet_name)
    else:
        log.error("Cannot successfully execute: %s" % snippet_name)


def hello(conn):
    try:
        confstr = HEELO
        rpc_obj = conn.edit_config(target='running', config=confstr)
        _check_response(rpc_obj, 'HELLO')
    except Exception:
        log.exception("Exception in creating subinterface @@@")

def create_subinterface(conn):
    try:
        confstr = CREATE_SUBINTERFACE % (subinterface,
                                         subinterface, vlan_id,
                                         subinterface, vlan_id, ip, mask,
                                         subinterface, vlan_id)
        rpc_obj = conn.edit_config(target='running', config=confstr)
        _check_response(rpc_obj, 'CREATE_SUBINTERFACE')
    except Exception:
        log.exception("Exception in creating subinterface %s" % subinterface)
            
def csr_connect(host, port, user, password):
    return manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           device_params={'name': "csr"},
                           timeout=10
            )
            
def demo(host, user, password):
    with csr_connect(host=host, port=2831, user=user, password=password) as m:
        print "##############1###############"
        c = m.get_config(source='running').data_xml
        print c
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    demo(sys.argv[1], sys.argv[2], sys.argv[3])
