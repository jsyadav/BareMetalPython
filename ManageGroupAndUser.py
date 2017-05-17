
import oraclebmc
config = oraclebmc.config.from_file("bmc_config","DEFAULT")
identity = oraclebmc.identity.IdentityClient(config)

# Creating group
from oraclebmc.identity.models import CreateGroupDetails
request = CreateGroupDetails()

request.compartment_id = config['tenancy']
request.name = "my-test-group"
request.description = "Created with the Python SDK"
group = identity.create_group(request)
print(group.data.id)

# Create User
from oraclebmc.identity.models import CreateUserDetails
request = CreateUserDetails()
request.compartment_id = config['tenancy']
request.name = "my-test-user"
request.description = "Created with the Python SDK"
user = identity.create_user(request)
print(user.data.id)

# # Add user to the group
from oraclebmc.identity.models import AddUserToGroupDetails
request = AddUserToGroupDetails()
request.group_id = group.data.id
request.user_id = user.data.id
response = identity.add_user_to_group(request)
print(response.status)


# Delete user and group
memberships = identity.list_user_group_memberships(compartment_id=config['tenancy'],
    user_id=user.data.id, group_id=group.data.id)
# There can never be more than one membership for a unique user/group combination
assert len(memberships.data) == 1
membership_id = memberships.data[0].id

identity.remove_user_from_group(user_group_membership_id=membership_id).status

identity.delete_user(user_id=user.data.id).status

identity.delete_group(group_id=group.data.id).status
