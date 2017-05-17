import oraclebmc

print('Starting')
# Looking for user from config file

# config = oraclebmc.config.from_file("~/.oraclebmc/config","DEFAULT")
# config = oraclebmc.config.from_file("~/.oraclebmc/config","integ-beta-profile")
config = oraclebmc.config.from_file("bmc_config","ORACLE_GBU_PROD_OPS_API")
identity = oraclebmc.identity.IdentityClient(config)
print (identity.get_compartment(config['tenancy']).data)

users = identity.list_compartments(config['tenancy'])
for user in users.data:
    print (user)
