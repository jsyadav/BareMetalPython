import oraclebmc
AD='IiWM:PHX-AD-1'
print('Starting', AD)

# Looking for user from config file
config = oraclebmc.config.from_file("bmc_config", "ORACLE_GBU_PROD")

# Create Virtual Cloud Network
network_client = oraclebmc.core.virtual_network_client.VirtualNetworkClient(config)
vcn_model = {'cidrBlock': config['master_vcn_cidr'],
             'compartmentId': config['network_compartment'],
             'displayName': config['vcn_name'],
             'dnsLabel': config['vcn_dns'],
             }
response = network_client.create_vcn(create_vcn_details=vcn_model)
print(response.data)
vcn_id = response.data.id
vcn_default_dhcp_id = response.data.default_dhcp_options_id
vcn_default_route_table_id = response.data.default_route_table_id
vcn_default_security_list_id = response.data.default_security_list_id

# instance client
inst_client = oraclebmc.core.compute_client.ComputeClient(config)

# # Create Custom DHCP Options
# dhcp_details={
#     'compartmentId' : config['network_compartment'],
#     'displayName' : config['dhcp_name'],
#     'vcnId': vcn_id,
#     'options' : [{
#     'type' : "DomainNameServer",
#     #'customDnsServers' : ["202.44.61.9"],
#     #'serverType' : "CustomDnsServer"
#     'serverType' : "VcnLocalPlusInternet"
#   }],
# }
#
# response = network_client.create_dhcp_options(create_dhcp_details=dhcp_details)
# print (response.data)
# dhcp_id = response.data.id

# #
# # #Create custom Master Security List
# # master_sl_model = {
# #   'vcnId' : vcn_id,
# #   'displayName' : config['master_security_list'],
# #   'ingressSecurityRules' : [],
# #   'egressSecurityRules' : [],
# #   'compartmentId' : config['network_compartment']
# # }
# # response = network_client.create_security_list(create_security_list_details=master_sl_model)
# # print (response.data)
# # master_sl_id = response.data.id
#
# # #################### Per compartment ###########
# # compIngressSecurityRules =  [{
# #     "protocol": "6",
# #     "source": "0.0.0.0/0",
# #     "tcpOptions": {
# #         "destinationPortRange": {
# #             "min": "22",
# #             "max": "22"
# #         }
# #     }
# # }, {
# #     "protocol": "1",
# #     "source": "0.0.0.0/0",
# #     "icmpOptions": {
# #         "code": "4",
# #         "type": "3"
# #     }
# # }, {
# #     "protocol": "1",
# #     "source": "10.0.0.0/16",
# #     "icmpOptions": {
# #         "type": "3" # set 'All' to allow pings
# #     }
# # }]
# # compEgressSLData = [{
# #     "protocol" : "all",
# #     "destination" : "0.0.0.0/0"
# #     }
# # ]
# #
# #
# #
# #
# # # Create security list for each compartment
# # ext_sl_model = {
# #   'vcnId' : vcn_id,
# #   'displayName' : 'EXT-SL-1',
# #   'ingressSecurityRules' : compIngressSecurityRules,
# #   'egressSecurityRules' : compEgressSLData,
# #   'compartmentId' : config['network_compartment']
# #}
# #
# # response = network_client.create_security_list(create_security_list_details=ext_sl_model)
# # ext_sl_id = response.data.id
#
# # Create Internet Gateway
igw_model ={
'displayName': config['gateway_name'],
'compartmentId': config['network_compartment'],
'vcnId': vcn_id,
'isEnabled': 'true'
}
response = network_client.create_internet_gateway(create_internet_gateway_details= igw_model)
print (response.data)
igw_id = response.data.id

# # Create Custom routing Table for EXT subnet
ext_rt_model = {
  'displayName' : 'EXT-RT-1',
  'vcnId' : vcn_id,
  'routeRules' : [{
    'cidrBlock' :'0.0.0.0/0',
    'networkEntityId' : igw_id
  }],
  'compartmentId' : config['network_compartment']
}

response = network_client.create_route_table(create_route_table_details=ext_rt_model)
ext_rt_id = response.data.id

ext_subnet_model = {
    'vcnId' : vcn_id,
    'dhcpOptionsId' : vcn_default_dhcp_id,
    'displayName' :config['ext_subnet_name'],
    'availabilityDomain': AD,
    'cidrBlock': config['ext_cidr'],
    'routeTableId': ext_rt_id,
    'securityListIds': [vcn_default_security_list_id],
    'compartmentId': config['network_compartment'],
    'dnsLabel': config['ext_subnet_dns']
}

print(ext_subnet_model)
response = network_client.create_subnet(create_subnet_details=ext_subnet_model)
print(response.data)
ext_subnet_id = response.data.id


bastion_inst_model = {
    'displayName':config['bastion_name'],
    'imageId':config['inst_image_id'],
    'shape':config['shape_name'],
    'availabilityDomain': AD,
    'compartmentId':config['network_compartment'],
    'subnetId':ext_subnet_id,
    'hostnameLabel':config['bastion_name'],
    'metadata':{
    'ssh_authorized_keys':'ssh-rsa  AAAAB3NzaC1yc2EAAAABJQAAAQEAu9+TJnWVpfqrC3rkgI6Sn7a8MM3RhQ4t9J2TrD4d81Qpyh6QQwjvKVnepzmqc+93g1Y14Mtu4SQBhAklBfR0gSGxePtvX6uYU4eQMg6cFrtPkMypnpEUc2J++we6doT1T5hKWpfm46K/BQ7ttVjj/cJ/l6Vc+1/+AxKRHtv+IW1JMa/wmFKHlp0iNJIaZn/OvH6tg1uxZNBeR5PPXk0GLh1fVnbJLkLiiDBpdQKzz4c8jQQzYYrehYnDCS+DOasD6gGo+RYuSbzAF/tVIyHljq3lyTwHNou+vgwacUyDwYqNbtl1hocBK0uNnkJERufQKBn7652r2xjlduQ3vpZN8w== rsa-key-20170310'
  }
}

response=inst_client.launch_instance(launch_instance_details=bastion_inst_model)
print(response.data)


# # Create routing Table for INT subnet

int_subnet_model = {
    'vcnId' : vcn_id,
    'dhcpOptionsId' : vcn_default_dhcp_id,
    'displayName' : config['int_subnet_name'],
    'availabilityDomain': AD,
    'cidrBlock':config['int_cidr'],
    'routeTableId': vcn_default_route_table_id,
    'securityListIds': [vcn_default_security_list_id],
    'compartmentId': config['network_compartment'],
    'dnsLabel': config['int_subnet_dns']

}

print(int_subnet_model)
response = network_client.create_subnet(create_subnet_details=int_subnet_model)
print(response.data)
int_subnet_id = response.data.id

node_inst_model = {
    'displayName':config['node_name'],
    'imageId': config['inst_image_id'],
    'shape': config['shape_name'],
    'availabilityDomain' : AD,
    'compartmentId': config['network_compartment'],
    'subnetId':int_subnet_id,
    'hostnameLabel': config['node_name'],
    'metadata' : {
        'ssh_authorized_keys': 'ssh-rsa  AAAAB3NzaC1yc2EAAAABJQAAAQEAu9+TJnWVpfqrC3rkgI6Sn7a8MM3RhQ4t9J2TrD4d81Qpyh6QQwjvKVnepzmqc+93g1Y14Mtu4SQBhAklBfR0gSGxePtvX6uYU4eQMg6cFrtPkMypnpEUc2J++we6doT1T5hKWpfm46K/BQ7ttVjj/cJ/l6Vc+1/+AxKRHtv+IW1JMa/wmFKHlp0iNJIaZn/OvH6tg1uxZNBeR5PPXk0GLh1fVnbJLkLiiDBpdQKzz4c8jQQzYYrehYnDCS+DOasD6gGo+RYuSbzAF/tVIyHljq3lyTwHNou+vgwacUyDwYqNbtl1hocBK0uNnkJERufQKBn7652r2xjlduQ3vpZN8w== rsa-key-20170310'

    }
}

response=inst_client.launch_instance(launch_instance_details=node_inst_model)
print(response.data)

if __name__ == "__main__":
    pass