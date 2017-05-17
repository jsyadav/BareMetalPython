import oraclebmc
#COMPARTMENTS = ["OPS", "AMPLIFY", "HSGBU"]
COMPARTMENTS = [{
   "name":"OPS",
   "id":'ocid1.compartment.oc1..aaaaaaaatait7mwlgyjr7vgyzxdqb5f7etft2khgkajgbj4ootdetg4zax2a'
}]
# Availability Domains
#ADS = ["kgzP:PHX-AD-1", "kgzP:PHX-AD-2", "kgzP:PHX-AD-3"]
ADS = ["kgzP:PHX-AD-1"]

config = oraclebmc.config.from_file("bmc_config","DEFAULT")
network_client = oraclebmc.core.virtual_network_client.VirtualNetworkClient(config)
inst_client = oraclebmc.core.compute_client.ComputeClient(config)
vcn_id='ocid1.vcn.oc1.phx.aaaaaaaaorixdakcmcgvq3phdlr73yzt3a6rli6ophjn6wcibasmcxxibc4a'


for c in COMPARTMENTS:

    # iterate over all ADS
    for ad in ADS :
        for sn in range (1,int(config['subnet_per_ad'])+1):
            subnets = network_client.list_subnets(compartment_id=c['id'],vcn_id=vcn_id)
            for subnet in subnets.data:
                if subnet.display_name == config['prefix']+c['name']+'_ad_'+ad+'_subnet_'+str(sn):
                    print('found '+subnet.display_name)

                # Now remove the instances under this subnet
                for i in range(1, int(config['instance_per_subnet'])+1):
                    instances = inst_client.list_instances(compartment_id=c['id'])
                    for instance in instances.data:
                        if instance.display_name == \
                                config['prefix']+c['name']+'_ad_'+ad+'_subnet_'+str(sn)+'_inst_'+str(i) and \
                                instance.lifecycle_state != 'TERMINATED':
                            print( 'found '+instance.display_name)
                            inst_client.terminate_instance(instance.id)
                # Now remove the subnet
                network_client.delete_subnet(subnet.id)



    # Delete routing tables (routing rules are automatically deleted)
    rt = network_client.list_route_tables(compartment_id=c['id'], vcn_id=vcn_id)
    for routing_table in rt.data:
        if routing_table.display_name == config['prefix']+c['name']+'_rt':
            print('found '+ routing_table.display_name)
            network_client.delete_route_table(routing_table.id)

    # Delete Security lists (master and for each subnet ones)
    sl = network_client.list_security_lists(compartment_id=c['id'], vcn_id=vcn_id)
    for security_list in sl.data:
        if security_list.display_name == config['prefix']+c['name']+'_sl':
            print('found '+ security_list.display_name)
            network_client.delete_security_list(security_list.id)
        if security_list.display_name == config['prefix']+config['master_security_list']:
            print('found ' + security_list.display_name)
            network_client.delete_security_list(security_list.id)



## Remove the top level VCN
response = network_client.get_vcn(vcn_id).data
print(response)
network_client.delete_route_table(response.default_route_table_id)
network_client.delete_security_list(response.default_security_list_id)

#network_client.delete_internet_gateway()
#network_client.delete_vcn(vcn_id)