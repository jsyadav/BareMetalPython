import oraclebmc

config = oraclebmc.config.from_file("bmc_config","ORACLE_GBU_PROD")

#AD = "kgzP:PHX-AD-1"
AD='IiWM:PHX-AD-1'
# Cloud_ops Compartment
# COMP_ID = config['tenancy']
# SUBNET_ID = 'ocid1.subnet.oc1.phx.aaaaaaaaqjhilzu6w3gqprjryzur32775obhrmitxn62y5stkx5qkpoanp3a'
# IMAGE_ID = 'ocid1.image.oc1.phx.aaaaaaaaifdnkw5d7xvmwfsfw2rpjpxe56viepslmmisuyy64t3q4aiquema'
# SHAPE = 'VM.Standard1.1'
#
# inst_model = {
#     'displayName': "repository-host",
#     'imageId': IMAGE_ID,
#     'shape': SHAPE,
#     'availabilityDomain': AD,
#     'compartmentId':config['network_compartment'],
#     'subnetId':SUBNET_ID,
#     'hostnameLabel': config['node_name'],
#     'metadata':{
#         #'user_data':"I2Nsb3VkLWNvbmZpZw0KZ3JvdXBzOg0KICAgIC0gY2xvdWRvcHMNCg0KdXNlcnM6DQogICAgLSBkZWZhdWx0DQogICAgLSBuYW1lOiBzZGFhcw0KICAgICAgZ2Vjb3M6IFNvZnR3YXJlIERlbGl2ZXIgYXMgYSBTZXJ2aWNlDQogICAgICBwcmltYXJ5LWdyb3VwOiBjbG91ZG9wcw0KICAgICAgI2dyb3VwczogdXNlcnMNCiAgICAgICNzZWxpbnV4LXVzZXI6IDxzZWxpbnV4IHVzZXJuYW1lPg0KICAgICAgI2V4cGlyZWRhdGU6IDxkYXRlPg0KICAgICAgI3NzaC1pbXBvcnQtaWQ6IDxub25lL2lkPg0KICAgICAgbG9ja19wYXNzd2Q6IHRydWUNCiAgICAgICNwYXNzd2Q6IHBhc3N3b3JkDQogICAgICBzdWRvOiBbJ0FMTD0oQUxMKSBOT1BBU1NXRDpBTEwnXQ0KICAgICAgaW5hY3RpdmU6IGZhbHNlDQogICAgICBzeXN0ZW06IGZhbHNlDQogICAgICBzaGVsbDogL2Jpbi9iYXNoDQogICAgICBzc2gtYXV0aG9yaXplZC1rZXlzOg0KICAgICAgICAtIHNzaC1yc2EgIGR1bW15DQogICAgLSBuYW1lOiBvc3QNCiAgICAgIGdlY29zOiBPcGVyYXRpb24gU3RhY2sNCiAgICAgIHByaW1hcnktZ3JvdXA6IGNsb3Vkb3BzDQogICAgICAjZ3JvdXBzOiB1c2Vycw0KICAgICAgI3NlbGludXgtdXNlcjogPHNlbGludXggdXNlcm5hbWU+DQogICAgICAjZXhwaXJlZGF0ZTogPGRhdGU+DQogICAgICAjc3NoLWltcG9ydC1pZDogPG5vbmUvaWQ+DQogICAgICBsb2NrX3Bhc3N3ZDogdHJ1ZQ0KICAgICAgI3Bhc3N3ZDogcGFzc3dvcmQNCiAgICAgIHN1ZG86IFsnQUxMPShBTEwpIE5PUEFTU1dEOkFMTCddDQogICAgICBpbmFjdGl2ZTogZmFsc2UNCiAgICAgIHN5c3RlbTogZmFsc2UNCiAgICAgIHNoZWxsOiAvYmluL2Jhc2gNCiAgICAgIHNzaC1hdXRob3JpemVkLWtleXM6DQogICAgICAgIC0gc3NoLXJzYSAgZHVtbXkNCg0KcnVuY21kOg0KICAgIC0gdG91Y2ggL3RtcC90ZXN0LnR4dA0K",
#         'ssh_authorized_keys':'ssh-rsa  AAAAB3NzaC1yc2EAAAABJQAAAQEAu9+TJnWVpfqrC3rkgI6Sn7a8MM3RhQ4t9J2TrD4d81Qpyh6QQwjvKVnepzmqc+93g1Y14Mtu4SQBhAklBfR0gSGxePtvX6uYU4eQMg6cFrtPkMypnpEUc2J++we6doT1T5hKWpfm46K/BQ7ttVjj/cJ/l6Vc+1/+AxKRHtv+IW1JMa/wmFKHlp0iNJIaZn/OvH6tg1uxZNBeR5PPXk0GLh1fVnbJLkLiiDBpdQKzz4c8jQQzYYrehYnDCS+DOasD6gGo+RYuSbzAF/tVIyHljq3lyTwHNou+vgwacUyDwYqNbtl1hocBK0uNnkJERufQKBn7652r2xjlduQ3vpZN8w== rsa-key-20170310'
#   }
# }
# inst_client = oraclebmc.core.compute_client.ComputeClient(config)

#response = inst_client.launch_instance(launch_instance_details=inst_model)
# print( 'instance created with id ', response.data.id)
# print ( response.data)
# api_key = "{}/{}/{}".format(config['tenancy'],config['user'],config['fingerprint'])
# print (api_key)
# with open('c:/Users/JSYADAV/.oraclebmc/bmcs_priv.pem') as f:
#     private_key = f.read().strip()
# #auth = SignedRequestAuth(api_key, private_key)
# #
# signer = oraclebmc.Signer(tenancy=config["tenancy"],
#     user=config["user"],
#     fingerprint=config["fingerprint"],
#     private_key_file_location='c:/Users/JSYADAV/.oraclebmc/bmcs_priv.pem',#config["key_file"],
#     pass_phrase=config["pass_phrase"]
#     )
#
# print (signer())



#inst_id = 'ocid1.instance.oc1.phx.abyhqljtfecf7tjfszzk2tnx4bpoa76hl35polya2z65kobdl2o4xx7dq7pa'
# response = inst_client.update_instance(instance_id=inst_id,update_instance_details={'displayName':'s3_bastion'})
# print (response.data)

# id = 'ocid1.subnet.oc1.phx.aaaaaaaayzmba54utnb6qs5zlowealtopgba7iiiisu3pg6xuwgumcb4gu5a'
# net_client = oraclebmc.core.VirtualNetworkClient(config)
# response = net_client.update_subnet(subnet_id=id,update_subnet_details={'displayName':'INT3'})
# print (response.data)

# GET instance
#inst_id = response.data.id
# inst_id = 'ocid1.instance.oc1.phx.abyhqljrrim5ici4c4ofx6tnn32okkkw47er527xlogocotyua52ry72hjjq'
# response = inst_client.get_instance(instance_id=inst_id)
# print (response.data)
#
#
# network_client = oraclebmc.core.VirtualNetworkClient(config)
# COMP_ID = 'ocid1.compartment.oc1..aaaaaaaal3fn3guhshymrtoejacyzcy7hhqp4k56ln65upoinut3elbsjsmq'
# response =inst_client.list_vnic_attachments(compartment_id=COMP_ID)
# print (response.data)
#
# for l in response.data:
#     if l.lifecycle_state == "ATTACHED" and l.instance_id == inst_id :
#         res = network_client.get_vnic(vnic_id=l.vnic_id)
#         #print(res.data)
#         print ('public ip is '+ res.data.public_ip);
#         print('private ip is ' + res.data.private_ip);
#
