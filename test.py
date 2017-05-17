# i = 10
# print(i, 'hello')
#
# subnet_count = 0
# def nextSubnetCIDR():
#     global subnet_count;
#     subnet_cidr = '10.0.' + (str(subnet_count)) + '.0/24'
#     subnet_count += 1;
#     return subnet_cidr
#
# for sn in range(0, 2):
#     print(sn)
#     print ('jdjdjd'+str(sn))
#     print (type(nextSubnetCIDR()))
#
#
# import oraclebmc
# config = oraclebmc.config.from_file("bmc_config","DEFAULT")
# print(config)
# print(5+int(config['instance_per_ad']))
# COMPARTMENTS = [{
#    "name":"OPS",
#    "id":'ocid1.compartment.oc1..aaaaaaaatait7mwlgyjr7vgyzxdqb5f7etft2khgkajgbj4ootdetg4zax2a'
# }]
#
# for c in COMPARTMENTS:
#     print(c['name'] + c['id'])

# import crypt
# print(crypt.crypt('password', '\$6\$SALT\$'))

import passlib.hash
import getpass
ctype = "6" #for sha512 (see man crypt)
salt = "qwerty"
insalt = '${}${}$'.format(ctype, salt)
password = "AMOROSO8282"

value1 = passlib.hash.sha512_crypt.encrypt(password)#, salt=salt, rounds=5000)
print (value1)


mypass = getpass.getpass("Please enter password : ")
if passlib.hash.sha512_crypt.verify(mypass, value1):
    print("password matched");
else :
    print("password didn't match")