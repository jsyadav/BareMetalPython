
import oraclebmc

print('Starting')
# Looking for user from config file

config = oraclebmc.config.from_file("bmc_config","ORACLE_GBU_PROD_OPS_API")
identity = oraclebmc.identity.IdentityClient(config)
user = identity.get_user(config["user"]).data

object_storage = oraclebmc.object_storage.ObjectStorageClient(config)
namespace = object_storage.get_namespace().data
print(namespace)

from oraclebmc.object_storage.models import CreateBucketDetails
request = CreateBucketDetails()
request.compartment_id = config['compartment_id']#config['compartment_iduser = identity.get_user(config["user"]).data']
request.name = "MyTestBucket"
bucket = object_storage.create_bucket(namespace, request)
print(bucket.data.etag)

my_data = b"Hello, World!"
obj = object_storage.put_object(namespace,bucket.data.name,
 "my-object-name",my_data)

same_obj = object_storage.get_object( namespace,
bucket.data.name,"my-object-name")

print(same_obj.data)

print(same_obj.data.content)