import oraclebmc

print('Starting')
# Looking for user from config file

# config = oraclebmc.config.from_file("~/.oraclebmc/config","DEFAULT")
# config = oraclebmc.config.from_file("~/.oraclebmc/config","integ-beta-profile")
# config = oraclebmc.config.from_file("bmc_config","DEFAULT")
# identity = oraclebmc.identity.IdentityClient(config)
# user = identity.get_user(config["user"]).data
#print(user)
#first_page = identity.list_users(compartment_id=config['tenancy'])
#print (len(first_page.data))

def paginate(operation, *args, **kwargs):
    while True:
        response = operation(*args, **kwargs)
        for value in response.data:
            yield value
        kwargs["page"] = response.next_page
        if not response.has_next_page:
            break
def list_users():
    for user in paginate(identity.list_users,compartment_id=config['tenancy']):
        print(user.name, user.id)


if __name__ == '__main__' :
    # config = oraclebmc.config.from_file("bmc_config", "ORACLE_GBU_PROD_OPS_API")
    config = oraclebmc.config.from_file("bmc_config", "ORACLE_GBU_DEV")
    compartment_id = config["tenancy"]
    identity = oraclebmc.identity.IdentityClient(config)
    user_tmp = identity.list_users(compartment_id).data
    print(len(user_tmp))
    for u in user_tmp:
        print (u.name)
    list_users()

