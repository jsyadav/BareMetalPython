import oraclebmc

config = oraclebmc.config.from_file("bmc_config","DEFAULT")
iam_client = oraclebmc.identity.IdentityClient(config)

#print (response.data);
inst_client = oraclebmc.core.ComputeClient(config)
net_client = oraclebmc.core.VirtualNetworkClient(config)

# Compartment Dark_Knight_Sandbox
compartment_id = 'ocid1.compartment.oc1..aaaaaaaa5jdzpzjielqgpee5ehjubkfh3n3gapevwzwcosx53dp3r46zxd3a'
# VCN DK Production Network
vcn_id = 'ocid1.vcn.oc1.phx.aaaaaaaa3syk5gazo2y24wrzyfz2btrxj7wjatcc2fekghqxczubtxn55i6a'

subnets = net_client.list_subnets(compartment_id=compartment_id, vcn_id=vcn_id)
all_subnets = []
for subnet in subnets.data:
    # print (subnet.display_name +' -> '+subnet.id)
    if subnet.id not in all_subnets:
        all_subnets.append(subnet.id)

print('Total number of subnets = ' + str(len(all_subnets)))

print(net_client.get_subnet(subnet_id='ocid1.subnet.oc1.phx.aaaaaaaaiuthmhdchslacrjti4juzzjydpufnoqyvflddxynzfxmjj3rxm3q').data)
vnicAttachements = inst_client.list_vnic_attachments(compartment_id=compartment_id)

for vnicAttach in vnicAttachements.data:
    #print(vnicAttach)
    if vnicAttach.lifecycle_state == 'ATTACHED' and vnicAttach.subnet_id in all_subnets:
        inst_id = vnicAttach.instance_id
        instance = inst_client.get_instance(instance_id=inst_id)
        print(inst_id ," name : ", instance.data.display_name)

all_instances_subnets = []
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
    if subnet in all_instances_subnets:
        print ('vnic subnet '+ subnet + ' is in use')
    else:
        print('vnic subnet ' + subnet +' is NOT in use')
        not_used_cnt +=1

print (not_used_cnt)

