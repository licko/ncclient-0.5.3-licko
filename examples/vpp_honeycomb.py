# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 Cisco Systems, Inc.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# @author: Hareesh Puthalath, Cisco Systems, Inc.

import sys
import logging
from ncclient import manager

log = logging.getLogger(__name__)

# Various IOS Snippets




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
GET_CONFIURE = """
<get-config>
        <source>
            <running/>
        </source>
</get-config>
"""
GET_DATA = """
<get/>
"""

def csr_connect(host, port, user, password):
    return manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           device_params={'name': "csr"},
                           timeout=10
            )

def get_configure(conn):
    try:
        confstr = GET_CONFIURE
        rpc_obj = conn.edit_config(target='running', config=confstr)
        _check_response(rpc_obj, 'GET_CONFIURE')
    except Exception:
        log.exception("Exception in get confiure ")

def get_data(conn):
    try:
        confstr = GET_DATA
        rpc_obj = conn.edit_config(target='running', config=confstr)
        _check_response(rpc_obj, 'GET_DATA')
    except Exception:
        log.exception("Exception in get confiure data")
            
def create_subinterface(conn, subinterface, vlan_id, ip, mask):
    try:
        confstr = CREATE_SUBINTERFACE % (subinterface,
                                         subinterface, vlan_id,
                                         subinterface, vlan_id, ip, mask,
                                         subinterface, vlan_id)
        rpc_obj = conn.edit_config(target='running', config=confstr)
        _check_response(rpc_obj, 'CREATE_SUBINTERFACE')
    except Exception:
        log.exception("Exception in creating subinterface %s" % subinterface)

def _check_response(rpc_obj, snippet_name):
    log.debug("RPCReply for %s is %s" % (snippet_name, rpc_obj.xml))
    xml_str = rpc_obj.xml
    if "<ok />" in xml_str:
        log.info("%s successful" % snippet_name)
    else:
        log.error("Cannot successfully execute: %s" % snippet_name)


def test_csr(host, user, password):
    with csr_connect(host, port=2831, user=user, password=password) as m:
        #create_vrf(m, "test_vrf")
        print "##############1###############"
        #for c in m.server_capabilities:
        #    print "@@@@@@@@@@"+c


        #print "##############2###############"
        c = m.get_config(source='running').data_xml

        print c
        print "##############3###############"
        #with open("%s.xml" % host, 'w') as f:
        #    f.write(c)

        print "##############4###############"
        #get_data(m)
        #create_subinterface(m, "TenGigabitEthernet81/0/1",
         #                   '500',
         #                   '192.168.0.1', '255.255.255.0')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_csr(sys.argv[1], sys.argv[2], sys.argv[3])
