import oraclebmc


config = oraclebmc.config.from_file("bmc_config","DEFAULT")
iam_client = oraclebmc.identity.IdentityClient(config)
inst_client = oraclebmc.core.ComputeClient(config)
# response = iam_client.list_compartments(compartment_id=config['tenancy'])
# for compartment in response.data:
#     response = inst_client.list_instances(compartment_id=compartment.id)
#     print (response.data)
#
# {
#   "availability_domain": "kgzP:PHX-AD-1",
#   "compartment_id": "ocid1.compartment.oc1..aaaaaaaatait7mwlgyjr7vgyzxdqb5f7etft2khgkajgbj4ootdetg4zax2a",
#   "display_name": "cloudops-registry-kb",
#   "id": "ocid1.instance.oc1.phx.abyhqljr7eb6f5ih6rxtn4dujvxjepmks23d777lncd2f6fpr5saqo6cd6sq",
#   "image_id": "ocid1.image.oc1.phx.aaaaaaaavyrt4az6ruewole6itmd6vfuuvtkrettbtw6v5gzssn23wyozy2a",
#   "ipxe_script": null,
#   "lifecycle_state": "RUNNING",
#   "metadata": {
#     "ssh_authorized_keys": "ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEAq3tV2u6Gc3fq/JTgFwxW0HFRtd56p28LyIgmS8Gcn3lKTRc6g9f/2RVfXccy0z/387yzZVHEqItGnuTLCdPf/xrbPG2kstag6+w3oGLinQpRbYvONEnIte/jRXvvf46/n7AFwqtb4EB+AEVJjbk1gwoPW63AKIqtbuoPwNWkIY1xLfrPx9skpjCA368GhZSK/zlePuc5T0oC6ez9Q8abfDtUbvSsA9yNxpVu39HSBbAdxVVN7iQs3rGamCHc9j+M2rDVgdQYPV5oGs73oMI986TTCzkQvtrl1E/AnpuHi+SUAhsyIwOn1ZX5fc6JnePy7m1ClnZuqSBkxsY3kf7jXQ== rsa-key-20170111"
#   },
#   "region": "phx",
#   "shape": "BM.Standard1.36",
#   "time_created": "2017-02-03T18:51:54.187000+00:00"
# },
inst_id = 'ocid1.instance.oc1.phx.abyhqljr7eb6f5ih6rxtn4dujvxjepmks23d777lncd2f6fpr5saqo6cd6sq'
# response = inst_client.list_console_histories(compartment_id="ocid1.compartment.oc1..aaaaaaaatait7mwlgyjr7vgyzxdqb5f7etft2khgkajgbj4ootdetg4zax2a")
# oraclebmc.core.models.CaptureConsoleHistoryDetails.

ch = {
    # "availabilityDomain": "kgzP:PHX-AD-1",
    # "compartmentId": "ocid1.compartment.oc1..aaaaaaaatait7mwlgyjr7vgyzxdqb5f7etft2khgkajgbj4ootdetg4zax2a",
    # "display_name": "cloudops-registry-kb",
    "instanceId": "ocid1.instance.oc1.phx.abyhqljr7eb6f5ih6rxtn4dujvxjepmks23d777lncd2f6fpr5saqo6cd6sq",
}
response = inst_client.capture_console_history(capture_console_history_details=ch)
print (response.data)
response = inst_client.capture_console_history(instance_console_history_id=ch)
print (response.data)
oraclebmc.identity.IdentityClient.create_or_reset_ui_password()