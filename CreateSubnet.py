import oraclebmc

config = oraclebmc.config.from_file("bmc_config","ORACLE_GBU_DEV")
network_client = oraclebmc.core.virtual_network_client.VirtualNetworkClient(config)

response = network_client.get_vcn('ocid1.vcn.oc1.phx.aaaaaaaad4v57juuqhpn3q4oal4pvwtgpbw6obuvb7dlrl7brbzfae7eng4q');
print(response.data)
vcn_id = response.data.id
vcn_default_dhcp_id = response.data.default_dhcp_options_id
vcn_default_route_table_id = response.data.default_route_table_id
vcn_default_security_list_id = response.data.default_security_list_id


#AD = "kgzP:PHX-AD-1"
AD = "KVnC:PHX-AD-1"

ext_subnet_model = {
    'vcnId' : vcn_id,
    'dhcpOptionsId' : vcn_default_dhcp_id,
    'displayName' :'ext_subnet_name',
    'availabilityDomain': AD,
    'cidrBlock': '10.0.3.0/24',
    'routeTableId': vcn_default_route_table_id,
    'securityListIds': [vcn_default_security_list_id],
    'compartmentId': config['network_compartment'],
}

print(ext_subnet_model)
response = network_client.create_subnet(create_subnet_details=ext_subnet_model)
print(response.data)
ext_subnet_id = response.data.id