import netsnmp
class S:
    def conv(vars):
        res = ()
        integ = ('INTEGER32', 'INTEGER', 'UNSIGNED32', 'COUNTER', 'GAUGE', 'COUNTER64', 'UINTEGER')
        strin = ('IPADDR', 'OCTETSTR', 'TICKS', 'OPAQUE', 'OBJECTID', 'NETADDR', 'NULL', 'BITS', 'ENDOFMIBVIEW', 'NOSUCHINSTANCE')
        for var in vars:
            if var.type in integ:
                res = res + (int(var.val),)
            elif var.type in strin:
                res = res + (var.val.decode(encoding='utf-8'),)
            elif var.type == 'NOSUCHOBJECT':
                res = res + ('No Such Object',)
            else:
                res = res + ('None',)
        return res
    def snmp_v1_v2_get(*vs: str, ver_snmp:int, dest_host:str, community:str):
        sess = netsnmp.Session( Version = ver_snmp,
                                DestHost=dest_host,
                                Community=community)
        vars = netsnmp.VarList(*tuple(netsnmp.Varbind(i) for i in vs))
        vals = sess.get(vars)
        print(S.conv(vars=vars))

        # res = netsnmp.snmpget(*tuple(netsnmp.Varbind(i) for i in vs),
        #                         Version = ver_snmp,
        #                         DestHost=dest_host,
        #                         Community=community)
        # print(S.conv(res))
        # print(f"  v{ver_snmp} snmpget result: ", res, )

    def snmp_v3_get(*vs: str, dest_host:str, sec_level:str,
                sec_name:str, priv_pass:str, auth_pass:str,
                auth_proto:str, priv_proto:str):
        
        sess = netsnmp.Session(Version = 3, 
                            DestHost = dest_host,
                            SecLevel = sec_level,
                            SecName = sec_name,
                            PrivPass = priv_pass,
                            AuthPass = auth_pass,
                            AuthProto = auth_proto,
                            PrivProto = priv_proto)
        sess.UseSprintValue = 1
        vars = netsnmp.VarList(*tuple(netsnmp.Varbind(i) for i in vs))
        vals = sess.get(vars)
        print(S.conv(vars=vars))


S.snmp_v1_v2_get('.1.3.6.1.2.1.25.6.3.1.2.1229', ver_snmp=2, dest_host='localhost', community='public')
S.snmp_v3_get('.1.3.6.1.2.1.25.6.3.1.2.1229', '.1.3.6.1.2.1.4.22.1.2.2.192.168.116.2', dest_host='127.0.0.1', sec_level='authPriv', sec_name='gohan', 
        priv_pass='0987654321', auth_pass='1234567890',auth_proto='SHA', priv_proto='AES')
# '.1.3.6.1.2.1.25.1.1.0','.1.3.6.1.2.1.6.4.0', '.1.3.6.1.2.1.25.4.2.1.1.88', '.1.3.6.1.2.1.25.4.2.1.1.90', '.1.3.6.1.2.1.4.22.1.3.2.192.168.116.254'