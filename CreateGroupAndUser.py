import oraclebmc

print('Starting')
# Looking for user from config file

# config = oraclebmc.config.from_file("~/.oraclebmc/config","DEFAULT")
# config = oraclebmc.config.from_file("~/.oraclebmc/config","integ-beta-profile")
config = oraclebmc.config.from_file("bmc_config","DEFAULT")
identity = oraclebmc.identity.IdentityClient(config)
user = identity.get_user(config["user"]).data
print(user)

#oraclebmc.identity.models.CreateGroupDetails.
group_details = {
    'compartmentId': config['tenancy'],
    'description': 'Sample test user from automation',
    'name': 'jit-test-group'
}
response = identity.create_group(create_group_details=group_details)
group_id = response.data.id

user_details = {
    'compartmentId': config['tenancy'],
    'description': 'Sample test user from automation',
    'name': 'jit-test-user'
}

response = identity.create_user(create_user_details=user_details)
print(response)
user_id = response.data.id

user_group_details ={
    'userId': user_id,
    'groupId': group_id
}
#identity.add_user_to_group(add_user_to_group_details=user_group_details)

api_detail ={
    'key': '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA79uvCPJEC9twynrp/eM7\nLfSHmv0nTreYrxcePG/67UKZ9Nyh9cyZnkkKESs5wJLUEy2C2Q/G2pUNZG5GCoz3\nPE7QcPEUszCbjkfwB/au4wab7+Elruviqh5nkUIFkgXXdgxEx48LtgMkYdv+lX73\ns1LFeaSTtNE9bJmL7bIfrYdPxwIxUQFm5utkdvMV6+uKn9jIy5eikX78T8yfUVQH\n/eQlJwVwiv14P0U1JO3pAcVMQ2HSK+sdlWQprQzOv+ZtYHidipwAPvnCTKm+Wesi\ns0o0I8ZHGB+x+gZllHJKt29vh/Zm4l+ysedTk1PvKJTwT0Yjr9y42o61gcmStsRc\nDQIDAQAB\n-----END PUBLIC KEY-----'}

response = identity.upload_api_key(user_id,create_api_key_details=api_detail)
print(response)