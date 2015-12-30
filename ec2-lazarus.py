#!/bin/python

###################################################################################
## Created by: Taylor McClure #####################################################
## GNU License ####################################################################
###################################################################################
## I am not liable for any issues that may be caused by this script. ##############
## USE AT YOUR OWN RISK. ALWAYS TAKE BACKUPS. #####################################
###################################################################################
## Feel free to contribute at https://github.com/taylorsmcclure/ec2-lazarus #######
###################################################################################

import boto3
import sys, traceback
import time

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

# defining global vars
ins = ''
vol_id = ''
temp_ins = ''

# take user input of what instance id to recover
def ins_select():
    global ins
    ins = input('Please input the unreachable instance\'s id ' +
    'you wish to recover: ')

ins_select()

# This will perform a check to make sure the instance
# input is in the stopped state, if not it was ask the user to stop
def stp_chk():
    response = client.describe_instances(InstanceIds=[ins])
    if response['Reservations'][0]['Instances'][0]['State']['Name'] == 'stopped':
        print('\n')
    elif response['Reservations'][0]['Instances'][0]['State']['Name'] == 'running':
        print('\n' + ins + ' has to be in the stopped state.\n' +
        '\n**WARNING** **WARNING**\nIf your instance has any data stored on ephemeral or instance' +
        '-store devices they will be erased upon a stop!!\n' +
        '**WARNING** **WARNING**\n' +
        '\nI am not responsible for any lost data.\n')
        for retry in range(5):
            usr_response = input('Do you wish to stop ' + ins + '? [Y/N] ')
            if usr_response == 'y' or usr_response == 'Y':
                # do the instance stop
                for i in range(10):
                    stp_response = client.stop_instances(InstanceIds=[ins])
                    if stp_response['StoppingInstances'][0]['CurrentState']['Name'] == 'shutting-down' or stp_response['StoppingInstances'][0]['CurrentState']['Name'] == 'stopping':
                        print(ins + ' is still in the ' + stp_response['StoppingInstances'][0]['CurrentState']['Name'] + ' state.')
                        print('Waiting 10 seconds...\n')
                        time.sleep(10)
                    elif stp_response['StoppingInstances'][0]['CurrentState']['Name'] != 'stopped':
                        print(ins + ' is either stuck in a stopping state or is in a state other than \'stopping\' or \'stopped\'.')
                        print('Please try again later.')
                        sys.exit(0)
                else:
                    print(ins + ' is now stopped.')
                break
            elif usr_response == 'n' or usr_response == 'N':
                print('Please attempt to migrate data off and try again later.')
                sys.exit(1)
            else:
                print('Please input \'y\', \'n\', \'Y\', or \'N\'.')
        else:
            print('Too many attempts, please try again.')
            sys.exit(0)
    else:
        print('Your instance is neither in the \'stopped\' or ' +
        '\'running\' state.\nPlease try again later.')
        sys.exit(0)

stp_chk()

# this will identify the root volume's vol id
def root_id():
    instance = ec2.Instance(ins)
    vols = instance.block_device_mappings
    global vol_id
    if len(vols) >= 1:
        for root in vols:
            if root['DeviceName'] == '/dev/xvda' or root['DeviceName'] == '/dev/sda1' or root['DeviceName'] == '/dev/sda':
                vol_id = (root['Ebs']['VolumeId'])
            else:
                print('no root attached.')
                break
                sys.exit(0)
    else:
        print('no root attached.')
        sys.exit(0)

root_id()

# this will detach the root volume from the instance
def detach_root():
    instance = ec2.Instance(ins)
    instance.detach_volume(VolumeId=(vol_id))
    print(vol_id + ' was detached successfully from ' +
    ins)

detach_root()

# this will start a temporary instance of Amazon Linux in the same subnet as the unreachable one
def tmp_ins():
    global temp_ins
    key = input('Please input the desired keypiar name: ')
    sg = input('Please input a security group ID: ')
    # Automatically obtains subnetId from stopped instance
    sub_response = client.describe_instances(InstanceIds=[ins])
    sub = sub_response['Reservations'][0]['Instances'][0]['SubnetId']

    print('\n**NOTE** **NOTE** \n' +
    'This will launch a t2.nano instance in the region you choose.\n' +
    'You will be charged at minimum one hour of on-demand t2.nano\n')

    print('Please choose your region to launch a recovery instance: \n' +
    '1) us-west-2 \n' +
    '2) us-west-1 \n' +
    '3) us-east-1 \n' +
    '4) eu-central-1 \n' +
    '5) eu-west-1 \n' +
    '6) ap-southeast-1 \n')
    for retry in range(5):
        usr_input = int(input('Please input the number of your region: '))
        #us-west-2
        if usr_input == 1:
            ami = 'ami-f0091d91'
            response = client.run_instances(MinCount=1, MaxCount=1, ImageId=(ami), KeyName=(key), SecurityGroupIds=[(sg)], InstanceType='t2.nano', SubnetId=(sub))
            temp_ins = response['Instances'][0]['InstanceId']
            tag = client.create_tags(Resources=[temp_ins], Tags=[{'Key': 'Name', 'Value': 'ec2-lazarus recovery instance'}])
            print(temp_ins + ' is launching.')
            break
        #us-west-1
        if usr_input == 2:
            ami = 'ami-d5ea86b5'
            response = client.run_instances(MinCount=1, MaxCount=1, ImageId=(ami), KeyName=(key), SecurityGroupIds=[(sg)], InstanceType='t2.nano', SubnetId=(sub))
            temp_ins = response['Instances'][0]['InstanceId']
            tag = client.create_tags(Resources=[temp_ins], Tags=[{'Key': 'Name', 'Value': 'ec2-lazarus recovery instance'}])
            print(temp_ins + ' is launching.')
            break
        #us-east-1
        if usr_input == 3:
            ami = 'ami-60b6c60a'
            response = client.run_instances(MinCount=1, MaxCount=1, ImageId=(ami), KeyName=(key), SecurityGroupIds=[(sg)], InstanceType='t2.nano', SubnetId=(sub))
            temp_ins = response['Instances'][0]['InstanceId']
            tag = client.create_tags(Resources=[temp_ins], Tags=[{'Key': 'Name', 'Value': 'ec2-lazarus recovery instance'}])
            print(temp_ins + ' is launching.')
            break
        #eu-central-1
        if usr_input == 4:
            ami = 'ami-bc5b48d0'
            response = client.run_instances(MinCount=1, MaxCount=1, ImageId=(ami), KeyName=(key), SecurityGroupIds=[(sg)], InstanceType='t2.nano', SubnetId=(sub))
            temp_ins = response['Instances'][0]['InstanceId']
            tag = client.create_tags(Resources=[temp_ins], Tags=[{'Key': 'Name', 'Value': 'ec2-lazarus recovery instance'}])
            print(temp_ins + ' is launching.')
            break
        #eu-west-1
        if usr_input == 5:
            ami = 'ami-bff32ccc'
            response = client.run_instances(MinCount=1, MaxCount=1, ImageId=(ami), KeyName=(key), SecurityGroupIds=[(sg)], InstanceType='t2.nano', SubnetId=(sub))
            temp_ins = response['Instances'][0]['InstanceId']
            tag = client.create_tags(Resources=[temp_ins], Tags=[{'Key': 'Name', 'Value': 'ec2-lazarus recovery instance'}])
            print(temp_ins + ' is launching.')
            break
        #ap-southeast-1
        if usr_input == 6:
            ami = 'ami-c9b572aa'
            response = client.run_instances(MinCount=1, MaxCount=1, ImageId=(ami), KeyName=(key), SecurityGroupIds=[(sg)], InstanceType='t2.nano', SubnetId=(sub))
            temp_ins = response['Instances'][0]['InstanceId']
            tag = client.create_tags(Resources=[temp_ins], Tags=[{'Key': 'Name', 'Value': 'ec2-lazarus recovery instance'}])
            print(temp_ins + ' is launching.')
            break
        print('Please try again: \n')
    else:
        print('Too many tries, please run again.')
        sys.exit(1)

tmp_ins()

# this will attach the root of the unreachable instance to the new recovery instance
def attach_root():
    global temp_ins
    global vol_id
    # loop to wait to see if the recovery instance is in the running state
    if len(temp_ins) > 0:
        for i in range(10):
            if client.describe_instances(InstanceIds=[temp_ins])['Reservations'][0]['Instances'][0]['State']['Name'] != 'running':
                print(temp_ins + ' is still in the pending state, please wait until it is running.\n' +
                'Trying again in 10s.\n')
                time.sleep(10)
            else:
                client.attach_volume(VolumeId=vol_id, InstanceId=temp_ins, Device='/dev/sdf')
                print(vol_id + ' has been attached to ' + temp_ins + ' as /dev/sdf.')
                sys.exit(0)
    else:
        print('The recovery instance did not launch, please try again.')
        sys.exit(1)

attach_root()
