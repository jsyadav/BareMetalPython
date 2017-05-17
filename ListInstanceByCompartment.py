import oraclebmc

config = oraclebmc.config.from_file("bmc_config","ORACLE_GBU_DEV")
iam_client = oraclebmc.identity.IdentityClient(config)

#print (response.data);
inst_client = oraclebmc.core.ComputeClient(config)
net_client = oraclebmc.core.VirtualNetworkClient(config)

printed = False
def printOnce(data):
    global printed
    if not printed:
        print(data)
    printed = True;
# Get compartments from tenancy
compartments = iam_client.list_compartments(compartment_id=config['tenancy'])
# Get all the subnets

def getInstanceByVCN():
    for comp in compartments.data:
        print ('Compartment name  -> ' + comp.name);
        vnicAttachements = inst_client.list_vnic_attachments(compartment_id=comp.id)
        vcns = net_client.list_vcns(compartment_id=comp.id)
        printOnce (vcns.data)
        for vcn in vcns.data:
            all_subnets = []
            subnets = net_client.list_subnets(compartment_id=comp.id, vcn_id=vcn.id)
            printOnce (subnets.data)
            for subnet in subnets.data:
                printOnce (subnet.display_name +' -> '+subnet.id)
                if subnet.id not in all_subnets:
                    all_subnets.append(subnet.id)

            print ('VCN = '+vcn.display_name +', number of subnets = '+str(len(all_subnets)))

            for vnicAttach in vnicAttachements.data:
                print(vnicAttach)
                if vnicAttach.lifecycle_state == 'ATTACHED' and vnicAttach.subnet_id in all_subnets :
                    inst_id = vnicAttach.instance_id
                    instance = inst_client.get_instance(instance_id=inst_id)
                    print("Instance Name : ", instance.data.display_name)



def getInstanceByCompartment():
    for comp in compartments.data:
        print('\n-----------------')
        print ('Compartment name  -> ' + comp.name);
        vnicAttachements = inst_client.list_vnic_attachments(compartment_id=comp.id)
        for vnicAttach in vnicAttachements.data:
            printOnce(vnicAttach)
            if vnicAttach.lifecycle_state == 'ATTACHED':
                inst_id = vnicAttach.instance_id
                instance = inst_client.get_instance(instance_id=inst_id)
                print(">> Instance Name : ", instance.data.display_name)


if __name__ == "__main__":
    getInstanceByCompartment()