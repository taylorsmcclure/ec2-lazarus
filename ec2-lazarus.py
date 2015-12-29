#!/bin/python

import boto3
import sys, traceback
import time

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

# defining global vars
ins = ''
vol_id = ''
temp_ins = ''

# Listing out all stopped instances along with their name tag
# if applicable
def stp_ins():
    instances = ec2.instances.filter(
Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    for instance in instances:
        l = instance.tags
        out = [instance.id]
        for x in l:
            out.append(x[u'Value'])
        print(out)

stp_ins()

# take user input of what instance id to recover
def ins_select():
    global ins
    ins = input('Please input the stopped instance id ' +
    'you wish to recover: ')

ins_select()

# this will identify the root volume's vol id
def root_id():
    instance = ec2.Instance(ins)
    vols = instance.block_device_mappings
    global vol_id
    if len(vols) >= 1:
        for root in vols:
            if root['DeviceName'] == '/dev/xvda' or root['DeviceName'] == '/dev/sda1' or root['DeviceName'] == '/dev/sda':
                vol_id = (root['Ebs']['VolumeId'])
                #print('not failing')
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

# this will start a temporary instance of Amazon Linux
def tmp_ins():
    global temp_ins
    key = input('Please input the desired keypiar name: ')
    sg = input('Please input a security group ID: ')
    sub = input('Please input a subnet ID: ')
    req = 'ImageId=(ami), KeyName=(key), SecurityGroupIds=[(sg)], InstanceType=\'t2.micro\', SubnetId=(sub)'

    print('Please choose your region to launch a recovery instance: \n' +
    '1) us-west-2 \n' +
    '2) us-east-1 \n')
    for retry in range(5):
        usr_input = int(input('Please input the number of your region: '))
        if usr_input == 1:
            ami = 'ami-f0091d91'
            response = client.run_instances(MinCount=1, MaxCount=1, ImageId=(ami), KeyName=(key), SecurityGroupIds=[(sg)], InstanceType='t2.micro', SubnetId=(sub), DryRun=False)
            temp_ins = response['Instances'][0]['InstanceId']
            print(temp_ins + ' is launching.')
            break
        if usr_input == 2:
            ami = 'ami-60b6c60a'
            response = client.run_instances(MinCount=1, MaxCount=1, ImageId=(ami), KeyName=(key), SecurityGroupIds=[(sg)], InstanceType='t2.micro', SubnetId=(sub))
            temp_ins = response['Instances'][0]['InstanceId']
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
        # response = client.describe_instances(InstanceIds=[temp_ins])
        while client.describe_instances(InstanceIds=[temp_ins])['Reservations'][0]['Instances'][0]['State']['Name'] != 'running':
            print(temp_ins + ' is still in the pending state, please wait until it is running.\n' +
            'Trying again in 5s.')
            time.sleep(5)
        else:
            client.attach_volume(VolumeId=vol_id, InstanceId=temp_ins, Device='/dev/sdf')
            print(vol_id + ' has been attached to ' + temp_ins + ' as /dev/sdf.')
    else:
        print('The recovery instance did not launch, please try again.')
        sys.exit(1)

attach_root()
