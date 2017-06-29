import oraclebmc

config = oraclebmc.config.from_file("bmc_config","ORACLE_GBU_PROD_OPS_API")
iam_client = oraclebmc.identity.IdentityClient(config)

#print (response.data);
inst_client = oraclebmc.core.ComputeClient(config)
net_client = oraclebmc.core.VirtualNetworkClient(config)

# Get compartments from tenancy
compartments = iam_client.list_compartments(compartment_id=config['tenancy'])

def getInstanceByCompartment():
    # Get all the subnets
    all_subnets = []
    for comp in compartments.data:
        print ('Compartment name  -> ' + comp.name);
        vcns = net_client.list_vcns(compartment_id=comp.id)
        #print (vcns.data)
        for vcn in vcns.data:
            subnets = net_client.list_subnets(compartment_id=comp.id, vcn_id=vcn.id)
            #print (subnets.data)
            for subnet in subnets.data:
                #print (subnet.display_name +' -> '+subnet.id)
                if subnet.id not in all_subnets:
                    all_subnets.append(subnet.id)

        print ('Total number of subnets = '+str(len(all_subnets)))

    print('-------------------------------------')
    # Get all the instances
    all_instances_subnets = []
    for comp in compartments.data:
        print('Compartment name  -> ' + comp.name);
        vnicAttachements = inst_client.list_vnic_attachments(compartment_id=comp.id)

        # iterate over all the VNIC
        for vnicAttach in vnicAttachements.data:
            #print(vnicAttach)
            if vnicAttach.lifecycle_state == 'ATTACHED':
                vnic = net_client.get_vnic(vnicAttach.vnic_id)
                #print (vnic.data)
                if vnic.data.subnet_id not in all_instances_subnets:
                    all_instances_subnets.append(vnic.data.subnet_id)
            else:
                print (vnicAttach.id + ' is not in ATTACHED state ,state = '+ vnicAttach.lifecycle_state)

    print('-------------------------------------')
    print('Total compartments subnets '+ (str(len(all_subnets))))
    print('Total instances subnets '+ (str(len(all_instances_subnets))))
    # Iterate over subnets to find which one is not used
    not_used_cnt=0
    for subnet in all_subnets:
        s_name = net_client.get_subnet(subnet_id=subnet);
        if subnet in all_instances_subnets:
            print ('vnic subnet '+ s_name.data.display_name + ' is in use')
        else:
            print('vnic subnet ' + s_name.data.display_name +' is NOT in use')
            not_used_cnt +=1

    print (not_used_cnt)


def listInstanceBySubnet(comp_id, subnet_id):
    s_name = net_client.get_subnet(subnet_id=subnet_id).data.display_name;
    vnicAttachements = inst_client.list_vnic_attachments(compartment_id=comp_id)
    # iterate over all the VNIC
    for vnicAttach in vnicAttachements.data:
        #print(vnicAttach)
        if vnicAttach.lifecycle_state == 'ATTACHED':
            vnic = net_client.get_vnic(vnicAttach.vnic_id)
            #print (vnic.data)
            inst_id = vnicAttach.instance_id
            inst_name = inst_client.get_instance(instance_id=inst_id).data.display_name
            if vnic.data.subnet_id == subnet_id:
                print ('Instance ',inst_name,' using subnet ', s_name);


if __name__ == "__main__":
    #getInstanceByCompartment()

    c_id = 'ocid1.compartment.oc1..aaaaaaaaqwbrp3el7z3npjnixfqr4ca77tevwum55oojido4twdp7nzyt37q'
    s_id = 'ocid1.subnet.oc1.phx.aaaaaaaabm2hesa7fomvscbavhchio5msubtfhnq644bff7invd2uiu37bia' #EXT10
    #s_id = 'ocid1.subnet.oc1.phx.aaaaaaaai3hnhxtv4bh6tsmuvyy46v4ix5p6s7nylprmthnjytt2jklhpeda' #EXT20
    listInstanceBySubnet(c_id, s_id)