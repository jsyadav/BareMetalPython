import oraclebmc

#COMPARTMENTS = ["OPS", "AMPLIFY", "HSGBU"]
COMPARTMENTS = [{
   "name":"OPS",
   "id":'ocid1.compartment.oc1..aaaaaaaatait7mwlgyjr7vgyzxdqb5f7etft2khgkajgbj4ootdetg4zax2a'
}]
# Availability Domains
#ADS = ["kgzP:PHX-AD-1", "kgzP:PHX-AD-2", "kgzP:PHX-AD-3"]
ADS = ["kgzP:PHX-AD-1"]


print('Starting')
# Looking for user from config file

# config = oraclebmc.config.from_file("~/.oraclebmc/config","DEFAULT")
# config = oraclebmc.config.from_file("~/.oraclebmc/config","integ-beta-profile")
config = oraclebmc.config.from_file("bmc_config","DEFAULT")

# {
#   "cidr_block": "10.0.0.0/16",
#   "compartment_id": "ocid1.compartment.oc1..aaaaaaaatait7mwlgyjr7vgyzxdqb5f7etft2khgkajgbj4ootdetg4zax2a",
#   "default_dhcp_options_id": "ocid1.dhcpoptions.oc1.phx.aaaaaaaabtll5c5i2m3xpoxlnrscj3zshogzr7g6eue7tlfnmvrnxoxkocha",
#   "default_route_table_id": "ocid1.routetable.oc1.phx.aaaaaaaa7tbnhli7abc2vmigteqzgymeypam3teb2nl6kfxrkk3cstv4rf4q",
#   "default_security_list_id": "ocid1.securitylist.oc1.phx.aaaaaaaafazyq63n4ldtdeo66ltxw67tmvl7ohgvwq2trcl7ltqehehehdua",
#   "display_name": "cloudops-kb",
#   "id": "ocid1.vcn.oc1.phx.aaaaaaaauahwxjbadiecto2ain4q2nfcd6glxed4hn4jw246kvud2qbdxc3q",
#   "lifecycle_state": "AVAILABLE",
#   "time_created": "2017-01-11T13:19:30.773000+00:00"
# }
# Create Virtual Cloud Network
network_client = oraclebmc.core.virtual_network_client.VirtualNetworkClient(config)

vcn_model = {'cidrBlock' : config['master_vcn_cidr'] ,
  'compartmentId' : config['network_compartment'],
  'displayName' : config['prefix']+config['vcn_name']
    }
response = network_client.create_vcn(create_vcn_details=vcn_model)
print (response.data)
vcn_id = response.data.id
vcn_default_dhcp_id = response.data.default_dhcp_options_id

# Create Internet Gateway
igw_model ={
"displayName": config['prefix']+config['gateway_name'],
"compartmentId": config['network_compartment'],
"vcnId": vcn_id,
"isEnabled": 'true'
}
response = network_client.create_internet_gateway(create_internet_gateway_details= igw_model)
print (response.data)
igw_id = response.data.id


# Create Master Security List

master_sl_model = {
  "vcnId" : vcn_id,
  "displayName" : config['prefix']+config['master_security_list'],
  "ingressSecurityRules" : [],
  "egressSecurityRules" : [],
  "compartmentId" : config['network_compartment']
}
response = network_client.create_security_list(create_security_list_details=master_sl_model)
print (response.data)
master_sl_id = response.data.id

#################### Per compartment ###########
compIngressSecurityRules =  [{
    "protocol": "6",
    "source": "0.0.0.0/0",
    "tcpOptions": {
        "destinationPortRange": {
            "min": "22",
            "max": "22"
        }
    }
}, {
    "protocol": "1",
    "source": "0.0.0.0/0",
    "icmpOptions": {
        "code": "4",
        "type": "3"
    }
}, {
    "protocol": "1",
    "source": "10.0.0.0/16",
    "icmpOptions": {
        "type": "3"
    }
}]
compEgressSLData = [{
    "protocol" : "all",
    "destination" : "0.0.0.0/0"
    }
]

# Create routing Table for each compartment
rt_model = {
  "displayName" : config['routing_table_name'],
  "vcnId" : vcn_id,
  "routeRules" : [{
    "cidrBlock" : "0.0.0.0/0",
    "networkEntityId" : igw_id
  }],
}
# Create security list for each compartment
sl_model = {
  "vcnId" : vcn_id,
  "displayName" : config['subnet_security_list'],
  "ingressSecurityRules" : compIngressSecurityRules,
  "egressSecurityRules" : compEgressSLData,
}

subnet_model = {
    "vcnId" : vcn_id,
    "dhcpOptionsId" : vcn_default_dhcp_id
}
subnet_count=0
def nextSubnetCIDR():
    global subnet_count;
    subnet_cidr = '10.0.'+(str(subnet_count))+'.0/24'
    subnet_count += 1;
    return subnet_cidr

inst_model = {
    'imageId': config['inst_image_id'],
    'shape': config['shape_name'],
    'metadata' : {
     "quake_bot_level" : 'Severe',
     "ssh_authorized_keys" : 'ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEAk3zBitPgG8JH743NdgsDO1Lg3hcC9zTf3qSU3fT1Gjm5Cruuj9Mid6S43bG56IZcL6HiEglWkbjpMm21/hFToz8HS0EZeICVddlfc+oag16mNp5gWqDQxbtrNMUJLZ2XRj1dNmXqbi1S6QMc7+LorfPIdQQ8m8frQeUIFZjF4RcHaq7QlLiXJjXW2TMRVyHvbDay92HoBGaMwSiIfHc5y2o0jyN+4VuNhFNXFIbWLAUpVcPrYLB6JJHR/OHMTsMQLdkm0+1hDbURYz1beuffSc/4fdYHdkrjPjuRAQbg7U+Gda3XmfQ8OFNXoGSF24XbjWTDqu4TnZlsgCWEyseJdQ== rsa-key-20170210'
  }
}
inst_client = oraclebmc.core.compute_client.ComputeClient(config)

for comp in COMPARTMENTS:
    print ('Crating Routing Table, Security List and subnet for ', comp['name'])
    # Creating Routing table for this compartment
    rt_model["displayName"] = config['prefix']+comp['name']+'_rt'
    rt_model["compartmentId"] = comp['id']
    response = network_client.create_route_table(create_route_table_details=rt_model)
    rt_id = response.data.id
    print('routing id for ', config['prefix']+comp['name'] , 'is ', rt_id )

    # Creating security List for this compartment
    sl_model["compartmentId"] = comp['id']
    sl_model["displayName"] = config['prefix']+comp['name']+'_sl'
    response = network_client.create_security_list(create_security_list_details=sl_model)
    sl_id = response.data.id
    print('security id for ', config['prefix']+comp['name'], 'is ', sl_id)

    # iterate over all ADS
    for ad in ADS:
        for sn in range (1,int(config['subnet_per_ad'])+1):
            print('Creating subnet for #', sn, ' in AD ', ad)
            subnet_model['displayName'] = config['prefix']+comp['name']+'_ad_'+ad+'_subnet_'+str(sn)
            subnet_model['availabilityDomain'] = ad
            subnet_model['cidrBlock'] = nextSubnetCIDR()
            subnet_model['routeTableId'] = rt_id
            subnet_model['securityListIds'] = [master_sl_id,sl_id]
            subnet_model['compartmentId'] = comp['id']
            print(subnet_model)
            response = network_client.create_subnet(create_subnet_details=subnet_model)
            print(response.data)
            subnet_id = response.data.id
            print('Created subnet for #', sn, ' in AD ', ad)
            for i in range(1, int(config['instance_per_subnet'])+1):
                inst_model['availabilityDomain'] = ad
                inst_model['compartmentId'] = comp['id']
                inst_model['displayName'] = config['prefix']+comp['name']+'_ad_'+ad+'_subnet_'+str(sn)+'_inst_'+str(i)
                inst_model['subnetId'] = subnet_id
                inst_client.launch_instance(launch_instance_details=inst_model)
                print('instance created with id ', response.data.id)
                print(response.data)


