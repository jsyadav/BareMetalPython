import oraclebmc

print('Starting')
# Looking for user from config file

# config = oraclebmc.config.from_file("~/.oraclebmc/config","DEFAULT")

config = oraclebmc.config.from_file("bmc_config","DEFAULT")
identity = oraclebmc.identity.IdentityClient(config)
user = identity.get_user(config["user"]).data
print(user)


create_policy = {
    'compartmentId': config['network_compartment'],
    'description': 'test policy from automation',
    'name': 'jit-test-policy',
    'statements':[
        "ALLOW GROUP jit-test-group,  to manage all-resources ON COMPARTMENT cloud_ops"
    ]

}

#response = identity.create_policy(create_policy_details=create_policy)
oraclebmc.identity.models.UpdatePolicyDetails.statements

response = identity.list_policies(compartment_id=config['tenancy'])
print(response.data)