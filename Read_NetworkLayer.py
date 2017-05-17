#!/usr/bin/python
# -------------------------------------------------------------------------------------------------------------------------------#
# Copyright (c) 2017 Oracle and/or its affiliates. All rights reserved.								#
#        NAME            : NetworkLayerinfo.py 										        #
#        AUTHOR          : CloudOps, Rahul Viswambharan ( rahul.viswambharan@oracle.com)					#
#        DESCRIPTION     : BMaaS Network Service automation to create VCNs, Routing Tables, Security Lists  and Subnets		#
#        NOTES           : NetworkLayerinfo.py expects input file in a valid json format as sample give below			#
# -------------------------------------------------------------------------------------------------------------------------------#
import oraclebmc
import sys
import json
import argparse
import logging
from oraclebmc.core.models import CreateVcnDetails, CreateInternetGatewayDetails, CreateSubnetDetails
from collections import OrderedDict


class BMCNetworkInfo():
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
            # ---------------------------------------------------------------------------------------------------------------#
            # Paginate Method :												#
            #  List operations use pagination to limit the size of each response. The Python SDK exposes the pagination 	#
            #  values through the has_next_page and next_page attributes on each response					#
            # ---------------------------------------------------------------------------------------------------------------#

    def paginate(self, operation, *args, **kwargs):
        while True:
            response = operation(*args, **kwargs)
            for value in response.data:
                yield value
            kwargs["page"] = response.next_page
            if not response.has_next_page:
                break
                # ---------------------------------------------------------------------------------------------------------------#
                # Method to retrieve compartment id from the compartment name:                                                   #
                #   The method needs mainly one parameters apart from the configuration parameter :				#
                # 	1. comp_name												#
                # ---------------------------------------------------------------------------------------------------------------#

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
                return response[cnt].id, response[cnt].route_rules[0].cidr_block, response[cnt].route_rules[
                    0].network_entity_id
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
                return response[cnt].display_name, response[cnt].id, response[cnt].default_route_table_id, response[
                    cnt].default_security_list_id
                break
            else:
                cnt = cnt + 1

                # ---------------------------------------------------------------------------------------#
                # Method to validate input Json file to decide the what network resources to be created #
                #   - The mmethod takes input JSON file as the input.                                   #
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

    def getSNid(self, config, network_client, compartment_id, vcn_id, SNname):
        response = network_client.list_subnets(compartment_id, vcn_id).data
        len_vcn_array = len(response)
        cnt = 0
        while cnt < len_vcn_array:
            if SNname == response[cnt].display_name:
                return response[cnt].id
                break
            else:
                cnt += 1

    # def subnet_call(self,config,network_client,compartment_id,vcn_name,sn_name):

    def listSN(self, config, network_client, compartment_id, vcn_id, jsonData):
        SL = []
        result_SNname = []
        for i in jsonData['VCN']:
            for sn in i['Subnets']:
                SNname = sn['name']
                result_SNname.append(SNname)
                try:
                    result_SNname.append((self.getSNid(config, network_client, compartment_id, vcn_id, SNname)))
                except Exception as e:
                    print
                    '\tError: Retrieving Subnet information'
                    raise
                sn_details = result_SNname[0] + ' : ' + result_SNname[1]
                SL.append(sn_details)
                result_SNname[:] = []
            return SL
            #
            # Method which invoked base methods to list information based on the input Json file
            #

    def bmc_retrieve_network_info(self, config, network_client, identity, jsonData):
        for i in jsonData['VCN']:
            vcn_name = i['name']
            comp_name = i['compartment_name']
            ig_name = i['IGW']
            compartment_id = self.getCompID(config, identity, comp_name)

            try:
                vcn_cnt, rt_cnt, sl_cnt, sn_cnt = self.ValidateJson(jsonData)
            except Exception as e:
                print
                '\nException in Json validate' + str(e)
                raise
            if vcn_cnt > 0 and rt_cnt > 0 and sl_cnt > 0 and sn_cnt > 0:
                try:
                    vcn_name, vcn_id, vcn_df_rt, vcn_def_sl = self.getVCNinfo(config, network_client, compartment_id,
                                                                              vcn_name)
                except Exception as e:
                    print
                    '\tError: Retrieving VCN information'
                    raise
                try:
                    ig_id = self.getIGateID(config, network_client, compartment_id, vcn_id, ig_name)
                except Exception as e:
                    print
                    '\tError: Retrieving IG information under the VCN'
                    raise
                # Retrieving Routing Table details
                for rt in i['RoutingTables']:
                    RTName = rt['name']
                    try:
                        rt_id, rt_cidr, rt_nw_entty_id = self.getRouting(config, network_client, compartment_id, vcn_id,
                                                                         RTName)
                    except Exception as e:
                        print
                        '\tError: Retrieving RoutingTable information'
                        raise
                        # Retrieving SL details
                for sl in i['SecurityLists']:
                    SLname = sl['name']
                    try:
                        sl_id = self.getSLid(config, network_client, compartment_id, vcn_id, SLname)
                    except Exception as e:
                        print
                        '\tError: Retrieving security list information'
                        raise
                        # Retrieving Subnet details
                SN_Details = self.listSN(config, network_client, compartment_id, vcn_id, jsonData)
                vcnData = {}
                vcnData['VCNDetails'] = []
                vcnData['VCNDetails'].append({
                    'Compartment_Name': comp_name,
                    'Compartment_id': compartment_id,
                    'VCNName': vcn_name,
                    'VCNId': vcn_id,
                    'InternetGateway': ig_name,
                    'InternetGatewayId': ig_id,
                    'VCNdfltRT': vcn_df_rt,
                    'VCNdfltSL': vcn_def_sl,
                    'RoutingTableName': RTName,
                    'RoutingTableId': rt_id,
                    'RoutingCIDR': rt_cidr,
                    'RoutingNwEntty': rt_nw_entty_id,
                    'SecurityListName': SLname,
                    'SecurityListId': sl_id,
                    'SubnetInfo': SN_Details
                })

                print
                json.dumps(vcnData, sort_keys=True, indent=4)
                # if __name__ == "__main__":
                #
                #   NetworkTopologyClass = BMCNetworkInfo()
                #   NetworkTopologyClass.bmc_retrieve_network_info(config,network_client,identity,jsonData)