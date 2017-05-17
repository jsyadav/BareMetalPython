#!/usr/bin/python
# -------------------------------------------------------------------------------------------------------------------------------#
# Copyright (c) 2017 Oracle and/or its affiliates. All rights reserved.								#
#        NAME            : CreateNetworkLayer.py										#
#        AUTHOR          : CloudOps, Rahul Viswambharan ( rahul.viswambharan@oracle.com)					#
#        DESCRIPTION     : BMaaS Network Service automation to create VCNs, Routing Tables, Security Lists  and Subnets		#
#        EXAMPLE USAGE   : ./CreateNetworkLayer.py -a <action_code> -i <input_file> -c <config_file>				#
#        NOTES           : CreateNetworkLayer.py expects input file in a valid json format as sample give below			#
# -------------------------------------------------------------------------------------------------------------------------------#
import oraclebmc
import sys
import json
import argparse
import logging
from oraclebmc.core.models import CreateVcnDetails, CreateInternetGatewayDetails, CreateSubnetDetails
import Read_NetworkLayer
#import Delete_NetworkLayer


class BMCNetworkTopology():
    # ---------------------------------------------------------------------------------------#
    # Method to accept command line options for the below list of parameters :	 	#
    #	1. Action Code : (create/delete) Note: Delete not available at this point.	#
    #	2. Config File : Fully qualified path to the BMaaS config file.			#
    # 	3. Profile Name: Profile name that needs to be used from the config file	#
    #	4. Input File  : Fully qualified path of the input json file			#
    # ---------------------------------------------------------------------------------------#

    def cmd_line_opt(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-a', action="store", dest='action_code', help='Action code for create/delete')
        parser.add_argument('-c', action="store", dest='config_file', help='Path to configuration file')
        parser.add_argument('-p', action="store", dest='profile_name', help='Profile Name to be used from config file')
        parser.add_argument('-i', action="store", dest='input_file', help='Input json file')
        # parser.add_argument('-o', action="store",dest='output_file',help='Output json file')
        results = parser.parse_args()
        return (results.action_code, results.config_file, results.profile_name, results.input_file)

    # ---------------------------------------------------------------------------------------#
    # Method to create Virtual Cloud Netwrok ( VCN ) in BMaaS                               #
    #    The method needs below parameters to create a new VCN :				#
    #       1. vcn_cidr : VCN CIDR information ( eg: 10.0.0.0/16 )        		        #
    #       2. compartment_id :OCID of the compartment where the VCn is expected te be at.  #
    #       3. vcn_name : Name of the VCN that needs to be created.                         #
    # ---------------------------------------------------------------------------------------#

    def create_vcn(self, config, network_client, vcn_cidr, compartment_id, vcn_name, dns_label):
        vcn_model = {
            'cidrBlock': vcn_cidr,
            'compartmentId': compartment_id,
            'displayName': vcn_name,
            'dnsLabel': dns_label,
        }
        vcn_response = network_client.create_vcn(create_vcn_details=vcn_model).data
        return (vcn_response.id, vcn_response.default_dhcp_options_id, vcn_response.default_route_table_id,
                vcn_response.default_security_list_id)

    # ---------------------------------------------------------------------------------------#
    # Method to create Virtual Cloud Netwrok ( VCN ) in BMaaS                               #
    #    The method needs below parameters to create a new VCN :                            #
    #       1. vcn_cidr : VCN CIDR information ( eg: 10.0.0.0/16 )#                         #
    #       2. compartment_id :OCID of the compartment where the VCN is expected te be at.  #
    #       3. vcn_name : Name of the VCN that needs to be created.                         #
    # ---------------------------------------------------------------------------------------#
    def create_internet_gateway(self, config, network_client, ig_display_name, compartment_id, vcn_id):
        ig_create = CreateInternetGatewayDetails()
        ig_create.display_name = ig_display_name
        ig_create.compartment_id = compartment_id
        ig_create.vcn_id = vcn_id
        ig_create.is_enabled = 'true'
        ig_response = network_client.create_internet_gateway(create_internet_gateway_details=ig_create).data
        # print 'IG Response:\n',ig_response
        # print 'IG ID:',ig_response.id
        return ig_response.id

    # ---------------------------------------------------------------------------------------#
    # Method to get OCID of an internet Gateway                               		#
    #    The method needs below parameters retrieve OCID for a given IG :                   #
    #       1. vcn_id : OCID of VCN                         				#
    #       2. compartment_id :OCID of the compartment where the VCN is expected te be at.  #
    #       3. rt_igw_name : Name of the Intenet Gateway.                                   #
    # ---------------------------------------------------------------------------------------#
    def getIGateID(self, config, network_client, compartment_id, vcn_id, rt_igw_name):
        response = network_client.list_internet_gateways(compartment_id, vcn_id).data
        if rt_igw_name == response[0].display_name:
            return response[0].id
        else:
            print
            '\tIG :', rt_igw_name, 'does not exists'

    def paginate(self, operation, *args, **kwargs):
        while True:
            response = operation(*args, **kwargs)
            for value in response.data:
                yield value
            kwargs["page"] = response.next_page
            if not response.has_next_page:
                break

    def getCompID(self, config, identity, comp_name):
        compartment_id = config["tenancy"]
        for comps in self.paginate(identity.list_compartments, compartment_id):
            if comp_name == comps.name:
                return comps.id
                break
                # ---------------------------------------------------------------------------------------#
                # Method to get OCID of a Routing Tables                                                #
                #    The method needs below parameters retrieve OCID for a given IG :                   #
                #       1. vcn_id : OCID of VCN                                                         #
                #       2. compartment_id :OCID of the compartment where the VCN is created.            #
                #       3. rt_igw_name : Name of the Intenet Gateway.                                   #
                # ---------------------------------------------------------------------------------------#

    def getRouting(self, config, network_client, compartment_id, vcn_id, RTName):
        response = network_client.list_route_tables(compartment_id, vcn_id).data
        len_rt_array = len(response)
        cnt = 0
        while cnt <= len_rt_array:
            len_rt_array = len_rt_array - 1
            if RTName == response[cnt].display_name:
                return response[cnt].id
                break
            else:
                cnt = cnt + 1
                # ---------------------------------------------------------------------------------------#
                # Method to retrieve VCN OCID                                                           #
                #    The method needs below parameters retrieve OCID for a given IG :                   #
                #       1. compartment_id :OCID of the compartment where the VCN is created.            #
                #       2. VCN Name    : Name of the VCN whose OCID needs to be retrieved.              #
                # ---------------------------------------------------------------------------------------#

    def getVCNinfo(self, config, network_client, compartment_id, vcn_name):
        response = network_client.list_vcns(compartment_id).data
        len_vcn_array = len(response)
        cnt = 0
        while cnt < len_vcn_array:
            if vcn_name == response[cnt].display_name:
                return response[cnt].id, response[cnt].default_route_table_id, response[cnt].default_security_list_id, \
                       response[cnt].default_dhcp_options_id
                break
            else:
                cnt = cnt + 1
                # ---------------------------------------------------------------------------------------#
                # Method to retrieve VCN OCID                                                           #
                #    The method needs below parameters retrieve OCID for a given IG :                   #
                #       1. compartment_id :OCID of the compartment where the VCN is created.            #
                #       2. VCN Name    : Name of the VCN whose OCID needs to be retrieved.              #
                # ---------------------------------------------------------------------------------------#

    def getVCNid(self, config, network_client, compartment_id, vcn_name):
        response = network_client.list_vcns(compartment_id).data
        len_vcn_array = len(response)
        cnt = 0
        while cnt < len_vcn_array:
            if vcn_name == response[cnt].display_name:
                return response[cnt].id
                break
            else:
                cnt = cnt + 1
                # ---------------------------------------------------------------------------------------#
                # Method to validate input Json file to decide the what network resources to be created #
                #   - The mmethod takes input JSON file as the input.					#
                # ---------------------------------------------------------------------------------------#

    def ValidateJson(self, jsonData):
        try:
            vcn_cnt = len(jsonData['VCN'])
        except KeyError:
            vcn_cnt = 0
        try:
            rt_cnt = len(jsonData['VCN'][0]['RoutingTables'])
        except KeyError:
            rt_cnt = 0
        try:
            sl_cnt = len(jsonData['VCN'][0]['SecurityLists'])
        except KeyError:
            sl_cnt = 0
        try:
            sn_cnt = len(jsonData['VCN'][0]['Subnets'])
        except KeyError:
            sn_cnt = 0
        return vcn_cnt, rt_cnt, sl_cnt, sn_cnt

    # ---------------------------------------------------------------------------------------#
    # Method to Create Routing Table under a given VCN in BMaaS                             #
    #    The method needs below parameters create Routing table :                           #
    #       1. vcn_id : OCID of VCN                                                         #
    #       2. igw_id : Intergnet gateway ID where the routing table is targetted to.       #
    #       3. rt_name : Name of the Routing Table.                                         #
    # ---------------------------------------------------------------------------------------#

    def create_routingtable(self, config, network_client, compartment_id, rt_name, vcn_id, rt_cidr, igw_id):
        rt_model = {
            'displayName': rt_name,
            'vcnId': vcn_id,
            'routeRules': [{
                'cidrBlock': rt_cidr,
                'networkEntityId': igw_id
            }],
            'compartmentId': compartment_id
        }
        response = network_client.create_route_table(create_route_table_details=rt_model)
        rt_id = response.data.id
        return rt_id

    # ---------------------------------------------------------------------------------------#
    # Method to Create Security list in a given VCN in BMaaS :                              #
    #    Below method takes parameters listed here:						#
    #       1. vcn_id: OCID of the VCN where security list will be created.			#
    #       2. compartment_id: compartment ID where the VCN is created.			#
    # 	3. sl_display_name : Display name of the security list				#
    #	4. egress_security_rules : egress security rules allows outbound IP packets	#
    #	5. ingress_security_rules : ingress security rules allows inbound IP packets	#
    # ---------------------------------------------------------------------------------------#
    def create_securitylist(self, config, network_client, vcn_id, compartment_id, sl_display_name,
                            egress_security_rules, ingress_security_rules):
        sl_model = {
            'vcnId': vcn_id,
            'displayName': sl_display_name,
            'ingressSecurityRules': ingress_security_rules,
            'egressSecurityRules': egress_security_rules,
            'compartmentId': compartment_id
        }
        response = network_client.create_security_list(create_security_list_details=sl_model)

    # ---------------------------------------------------------------------------------------#
    # Method to Create Subnets under a given VCN in BMaaS.                                  #
    #    The method needs below parameters							#
    #       1. vcn_id : OCID of VCN                                                         #
    #       2. igw_id : Intergnet gateway ID where the routing table is targetted to.       #
    #       3. rt_name : Name of the Routing Table.                                         #
    # ---------------------------------------------------------------------------------------#
    def subnet_creation(self, config, network_client, compartment_id, appln_domain, vcn_id, routingID, security_list,
                        vcn_dflt_dhcp_id, subnet_name, subnet_cidr, sn_dns_label):
        subnet_model = {
            'vcnId': vcn_id,
            'dhcpOptionsId': vcn_dflt_dhcp_id,
            'displayName': subnet_name,
            'availabilityDomain': appln_domain,
            'cidrBlock': subnet_cidr,
            'routeTableId': routingID,
            'securityListIds': security_list,
            'compartmentId': compartment_id,
            'dnsLabel': sn_dns_label
        }
        response = network_client.create_subnet(create_subnet_details=subnet_model)
        subnet_id = response.data.id
        return subnet_id

    # ---------------------------------------------------------------------------------------#
    # Method to get security list id                                                        #
    #    Below are the important parameter for the method    				#
    #       1. compartment_id : compartment_id where the VCN is created                     #
    #       2. vcn_id : OCID of the VCN created in the compartment                          #
    #       3. SLname : Name of the security list whose id needs to be retrieved            #
    # ---------------------------------------------------------------------------------------#
    def getSLid(self, config, network_client, compartment_id, vcn_id, SLname):
        response = network_client.list_security_lists(compartment_id, vcn_id).data
        len_vcn_array = len(response)
        cnt = 0
        while cnt < len_vcn_array:
            if SLname == response[cnt].display_name:
                return response[cnt].id
                break
            else:
                cnt += 1
                # ---------------------------------------------------------------------------------------#
                # Method to logically call create subnet method                                         #
                #    Below are the important parameter for the method                                   #
                #       1. compartment_id : compartment_id where the VCN is created                     #
                #       2. vcn_id : OCID of the VCN created in the compartment                          #
                #       3. SLname : Name of the security list whose id needs to be retrieved            #
                # ---------------------------------------------------------------------------------------#

    def subnet_main(self, config, network_client, compartment_id, vcn_name, routingID, subnet_name, appln_domain,
                    subnet_cidr, sn_dns_label, sn_sl_list):
        result = []
        vcn_id, df_rt_id, df_sl_id, vcn_dflt_dhcp_id = self.getVCNinfo(config, network_client, compartment_id, vcn_name)
        sb_array_len = len(sn_sl_list)
        cnt = 0
        while cnt < sb_array_len:
            SLname = sn_sl_list[cnt]
            if SLname == 'DefaultSecurityList':
                result.append(df_sl_id)
            else:
                sl_id = self.getSLid(config, network_client, compartment_id, vcn_id, SLname)
                result.append(sl_id)
            cnt += 1
            if cnt == sb_array_len:
                security_list = result
                try:
                    print
                    '\tCalling subnet create method....'
                    subnet_id = self.subnet_creation(config, network_client, compartment_id, appln_domain, vcn_id,
                                                     routingID, security_list, vcn_dflt_dhcp_id, subnet_name,
                                                     subnet_cidr, sn_dns_label)
                    return subnet_id
                    result[:] = []
                except Exception as e:
                    print
                    '\nException creating subnet' + str(e)
                    raise

                    # ---------------------------------------------------------------------------------------#
                    # Method which orchestrates above defined base methods to setup BMC network layer       #
                    #    The method needs below parameters:							#
                    #      - jsonData: The input Json file where the network topology infromation is given  #
                    # ---------------------------------------------------------------------------------------#

    def bmc_network_core_service(self, config, network_client, jsonData):

        print
        '\n\tReading the input json file.......'
        #
        # Reading input Json file for processing.
        #
        for i in jsonData['VCN']:
            vcn_name = i['name']
            comp_name = i['compartment_name']
            compartment_id = self.getCompID(config, identity, comp_name)
            #
            # Input Json file validation
            #
            try:
                vcn_cnt, rt_cnt, sl_cnt, sn_cnt = self.ValidateJson(jsonData)
            except Exception as e:
                print
                '\nException in Json validate' + str(e)
                raise
            #
            # For input Json file with only VCN create scenario
            #
            if sl_cnt == sn_cnt == rt_cnt == 0 and vcn_cnt > 0:
                print
                '\tOnly VCN block found in the input Json...'
                vcn_cidr = i['CIDR']
                ig_display_name = i['IGW']
                vcn_dns_label = i['dns_label']
                try:
                    print
                    '\tChecking for VCN:', vcn_name
                    vcn_exists = self.getVCNid(config, network_client, compartment_id, vcn_name)
                except Exception as e:
                    print
                    '\nException during retrieving VCN OCID' + str(e)
                    raise
                #
                # Check for given VCN exists already or not
                #
                if vcn_exists is None:
                    # Function Call: create_vcn
                    #
                    # Creating VCN
                    #
                    try:
                        vcn_id, vcn_dflt_dhcp_id, vcn_dflt_rt_id, vcn_dflt_sl_id = self.create_vcn(config,
                                                                                                   network_client,
                                                                                                   vcn_cidr,
                                                                                                   compartment_id,
                                                                                                   vcn_name,
                                                                                                   vcn_dns_label)
                    except Exception as e:
                        print
                        '\nException creating VCN' + str(e)
                        raise
                        # Function call for creating IG under the VCN
                    #
                    # Creatin IG for the VCN
                    #
                    try:
                        print
                        '\tCreating Internet Gateway:', ig_display_name
                        ig_id = self.create_internet_gateway(config, network_client, ig_display_name, compartment_id,
                                                             vcn_id)
                    except Exception as e:
                        print
                        '\nException creating Internet Gateway' + str(e)
                        raise
                elif vcn_exists is not None:
                    raise TypeError('Unable to create VCN:', vcn_name, ' VCN alredy exists with OCID:', vcn_exists)
                    #
                    # For adding Routing table to an existing VCN. VCN has to exists.
                    #
            elif sl_cnt == sn_cnt == 0 and vcn_cnt > 0 and rt_cnt > 0:
                print
                '\tVCN and Routing table will be created if they dont already exists'
                for rt_crt in i['RoutingTables']:
                    rt_rules = rt_crt['Rules']
                    rt_name = rt_crt['name']
                    rt_cidr = rt_crt['Rules'][0]['routing_rule']['CIDR']
                    rt_igw_name = rt_crt['Rules'][0]['routing_rule']['gateway']
                    print
                    '\tRetrieving IG ID: ', rt_igw_name
                    #
                    # Storing VCN info
                    #
                    try:
                        vcn_id, dflt_rt_id, dlft_sl_id, vcn_dflt_dhcp_id = self.getVCNinfo(config, network_client,
                                                                                           compartment_id, vcn_name)
                    except Exception as e:
                        print
                        '\nException retrieving VCN ID' + str(e)
                        raise
                    #
                    # Getting IG OCID for routing table creation
                    #
                    try:
                        igw_id = self.getIGateID(config, network_client, compartment_id, vcn_id, rt_igw_name)
                    except Exception as e:
                        print
                        '\nException retrieving IG ID' + str(e)
                        raise
                    if igw_id is not None and vcn_id is not None:
                        print
                        '\tCreating Routing Table', rt_name
                        #
                        # Creating Routing table under the given VCN
                        #
                        try:
                            rt_id = self.create_routingtable(config, network_client, compartment_id, rt_name, vcn_id,
                                                             rt_cidr, igw_id)
                        except Exception as e:
                            print
                            '\nException creating Routing Table:' + str(e)
                            raise
                    else:
                        print
                        '\tUnable to create RT table with the given information', rt_name

                        #
                        # For adding Security Lists to an existing VCN. VCN has to exist.
                        #
            elif rt_cnt == sn_cnt == 0 and vcn_cnt > 0 and sl_cnt > 0:
                print
                'VCN and Security list block found in the input Json'
                for sl in i['SecurityLists']:
                    sl_display_name = sl['name']
                    egress_security_rules = sl['egressSecurityRules']
                    ingress_security_rules = sl['ingressSecurityRules']
                    try:
                        print
                        '\tGetting VCN OCID'
                        vcn_id, dflt_rt, dflt_sl, vcn_dflt_dhcp_id = self.getVCNinfo(config, network_client,
                                                                                     compartment_id, vcn_name)
                    except Exception as e:
                        print
                        '\nException retrieving VCN information' + str(e)
                        raise
                    if vcn_id is not None:

                        try:
                            print
                            '\tCreating security list:', sl_display_name
                            sl_id = self.create_securitylist(config, network_client, vcn_id, compartment_id,
                                                             sl_display_name, egress_security_rules,
                                                             ingress_security_rules)
                        except Exception as e:
                            print
                            '\nException creating security list' + str(e)
                            raise
                    else:
                        print
                        '\tNo Valid VCN found'
                        #
                        # For adding Subnets to an existing VCN. VCN, Routing table and Security Lists has to exist.
                        #
            elif rt_cnt == sl_cnt == 0 and vcn_cnt > 0 and sn_cnt > 0:
                for sb_net in i['Subnets']:
                    subnet_name = sb_net['name']
                    appln_domain = sb_net['AD']
                    subnet_cidr = sb_net['CIDR']
                    RTName = sb_net['RT']
                    sn_dns_label = sb_net['dns_label']
                    sn_sl_list = sb_net['SL']
                    #
                    # Storing VCN information for further use
                    #
                    try:
                        vcn_id, df_rt_id, df_sl_id, vcn_dflt_dhcp_id = self.getVCNinfo(config, network_client,
                                                                                       compartment_id, vcn_name)
                    except Exception as e:
                        print
                        '\nException retrieving VCN information' + str(e)
                        raise
                    if RTName == 'DefaultRouteTable':
                        routingID = df_rt_id
                        #
                        # Calling subnet main function for Subnet creation using Default routing table
                        #
                        try:
                            subnet_id = self.subnet_main(config, network_client, compartment_id, vcn_name, routingID,
                                                         subnet_name, appln_domain, subnet_cidr, sn_dns_label,
                                                         sn_sl_list)
                            print
                            '\tSubnet', subnet_name, ' created successfully : ', subnet_id
                        except Exception as e:
                            print
                            '\nException while creating subnet' + str(e)
                            raise

                    else:
                        #
                        # Getting routing table OCID for custom routing table
                        #
                        try:
                            routingID = self.getRouting(config, network_client, compartment_id, vcn_id, RTName)
                        except Exception as e:
                            print
                            '\nException while retrieving the routing table ID' + str(e)
                            raise
                        #
                        # Calling subnet main function for Subnet creation using custom routing table
                        #
                        if routingID is not None:
                            try:
                                subnet_id = self.subnet_main(config, network_client, compartment_id, vcn_name,
                                                             routingID, subnet_name, appln_domain, subnet_cidr,
                                                             sn_dns_label, sn_sl_list)
                                print
                                '\tSubnet', subnet_name, ' created successfully : ', subnet_id
                            except Exception as e:
                                print
                                '\nException while creating Subnet' + str(e)
                                raise
                        else:
                            print
                            '\tUnable to create subnet', subnet_name
                            #
                            # For creating Complete network topology from VCN-Subnets in BMC
                            #
            elif vcn_cnt > 0 and rt_cnt > 0 and sl_cnt > 0 and sn_cnt > 0:
                print
                '\tCreating complete network layer.'
                vcn_cidr = i['CIDR']
                ig_display_name = i['IGW']
                vcn_dns_label = i['dns_label']
                #
                # Check to see if given VCN name already exists.
                #
                try:
                    print
                    '\tChecking for VCN:', vcn_name
                    vcn_exists = self.getVCNid(config, network_client, compartment_id, vcn_name)
                except Exception as e:
                    print
                    '\nException during retrieving VCN OCID' + str(e)
                    raise
                if vcn_exists is None:
                    #
                    # Creating VCN if given VCN name doesnt exist.
                    #
                    print
                    '\tCreating VCN:', vcn_name
                    vcn_id, vcn_dflt_dhcp_id, vcn_dflt_rt_id, vcn_dflt_sl_id = self.create_vcn(config, network_client,
                                                                                               vcn_cidr, compartment_id,
                                                                                               vcn_name, vcn_dns_label)
                    print
                    '\tVCN created successfully', vcn_id
                    #
                    # Creating IG for the given VCN
                    #
                    if len(vcn_id) > 0:
                        print
                        '\tCreating Internet Gateway:', ig_display_name
                        ig_id = self.create_internet_gateway(config, network_client, ig_display_name, compartment_id,
                                                             vcn_id)
                        #
                        # Creating Routing table for the given VCN
                        #
                        for rt in i['RoutingTables']:
                            rt_rules = rt['Rules']
                            rt_name = rt['name']
                            rt_cidr = rt['Rules'][0]['routing_rule']['CIDR']
                            rt_igw_name = rt['Rules'][0]['routing_rule']['gateway']
                            print
                            '\tRetrieving IG ID: ', rt_igw_name
                            igw_id = self.getIGateID(config, network_client, compartment_id, vcn_id, rt_igw_name)
                            if len(igw_id) > 0:
                                print
                                '\tCreating Routing Table', rt_name
                                rt_id = self.create_routingtable(config, network_client, compartment_id, rt_name,
                                                                 vcn_id, rt_cidr, igw_id)
                                if len(rt_id) > 0:
                                    print
                                    '\tRouting table', rt_name, ' created successfully:', rt_id
                                else:
                                    print
                                    '\tUnable to create routing table:', rt_name
                                    #
                                    # Reading security list from the input Json block and creating Security lists
                                    #

                        for sl in i['SecurityLists']:
                            sl_display_name = sl['name']
                            egress_security_rules = sl['egressSecurityRules']
                            ingress_security_rules = sl['ingressSecurityRules']

                            try:
                                print
                                '\tCreating custom security list', sl_display_name
                                sl_id = self.create_securitylist(config, network_client, vcn_id, compartment_id,
                                                                 sl_display_name, egress_security_rules,
                                                                 ingress_security_rules)
                                print
                                '\tSecurity list created successfully'
                            except Exception as e:
                                print
                                '\nException creating security list' + str(e)
                                raise
                                #
                                # reading subnet creation block from the input Json file and creating subnet under the VCN
                                #
                        for sb_net in i['Subnets']:
                            subnet_name = sb_net['name']
                            appln_domain = sb_net['AD']
                            subnet_cidr = sb_net['CIDR']
                            RTName = sb_net['RT']
                            sn_dns_label = sb_net['dns_label']
                            sn_sl_list = sb_net['SL']
                            #
                            # Check to see if Default routing table for the subnet
                            #
                            if RTName == 'DefaultRouteTable':
                                routingID = vcn_dflt_rt_id
                                subnet_id = self.subnet_main(config, network_client, compartment_id, vcn_name,
                                                             routingID, subnet_name, appln_domain, subnet_cidr,
                                                             sn_dns_label, sn_sl_list)
                                print(
                                '\tSubnet', subnet_name, ' created successfully : ', subnet_id)
                            else:
                                #
                                # Retrieving custom routing table OCID for the Subnet.
                                #
                                routingID = self.getRouting(config, network_client, compartment_id, vcn_id, RTName)
                                if routingID is not None:

                                    subnet_id = self.subnet_main(config, network_client, compartment_id, vcn_name,
                                                                 routingID, subnet_name, appln_domain, subnet_cidr,
                                                                 sn_dns_label, sn_sl_list)
                                    print(
                                    '\tSubnet', subnet_name, ' created successfully : ', subnet_id)
                                else:
                                    print(
                                    '\tUnable to retrieve RoutingTableID for the given routing table name for the subnet:', subnet_name, 'RoutingTable:', RTName)

                    else:
                        print
                        '\tError:Unable to create VCN', vcn_name

                elif vcn_exists is not None:
                    raise TypeError('Unable to create VCN:', vcn_name, ' VCN alredy exists with OCID:', vcn_exists)


if __name__ == "__main__":

    NetworkTopologyClass = BMCNetworkTopology()
    NetworkInfoClass = Read_NetworkLayer.BMCNetworkInfo()
    #NetworkDeleteClass = Delete_NetworkLayer.BMCDelNetwork()
    action_code, config_path, profile_name, input_file = NetworkTopologyClass.cmd_line_opt()

    print
    '\n\tAction Code: ', action_code
    print
    '\tConfig File Path: ', config_path
    print
    '\tProfile Name: ', profile_name
    print
    '\tInput File Path: ', input_file
    print
    '\n'
    config = oraclebmc.config.from_file(config_path, profile_name)
    network_client = oraclebmc.core.virtual_network_client.VirtualNetworkClient(config)
    identity = oraclebmc.identity.IdentityClient(config)
    # Reading the input json file
    with open(input_file) as data_file:
        jsonData = json.load(data_file)
    if action_code.lower() == 'create':
        try:
            NetworkTopologyClass.bmc_network_core_service(config, network_client, jsonData)
        except Exception as e:
            print
            'Error::: Executing method NetworkTopologyClass.bmc_network_core_service ' + str(e)
    elif action_code.lower() == 'read':
        try:
            NetworkInfoClass.bmc_retrieve_network_info(config, network_client, identity, jsonData)
            pass
        except Exception as e:
            print
            'Error::: Executing method NetworkInfoClass.bmc_retrieve_network_info ' + str(e)
    elif action_code.lower() == 'delete':
        try:
            #NetworkDeleteClass.bmc_delete_network_layer(config, network_client, identity, jsonData)
            pass
        except Exception as e:
            print
            'Error::: Executing method NetworkLayerDelete.bmc_delete_network_layer ' + str(e)