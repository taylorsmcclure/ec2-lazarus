# ec2-lazarus
<p>Have you ever been unable to reach your EC2 Linux instance through SSH? Even after multiple restarts?</p>
<p>I know this feeling all too well. One of the major drawbacks with AWS EC2 is no access to the physical console. This means there is no way to internally troubleshoot or access an instance's root filesystem without mounting it on another EC2 Linux instance.</p>

<h2>Diclaimer</h2>
<p>Always, always take a snapshot or AMI (image) of an unreachable instance. I am not responsible for any data loss, downtime, or unforeseen circumstances resulting from running this script.</p>
<p>This script will launch a t2.nano as a recovery instance. At a minimum you will be paying for one hour of on-demand usage for a t2.nano in your region.</p>

<h2>What does ec2-lazarus do?</h2>
<p>ec2-lazarus eliminates the tediousness of the detaching the root volume from your unreachable instance and spinning up a recovery one to mount it on. It is all done through this interactive script.<p>

<h2>What is the workflow?</h2>
<ol>
<li>Based on user input the script locates the unreachable instance on your account.</li>
<li>It will check if the instance is stopped.</li>
<li>It will launch a recovery instance (t2.micro using Amazon Linux AMI) in the region you choose. In the same subnet as your unreachable instance.</li>
<li>Once the recovery instance is running it will detach the root volume from the unreachable instance and mount it as /dev/sdf on the recovery instance.</li>
<li>Now it is up to the user to SSH to the recovery instance and troubleshoot the issue.</li>
</ol>

<h2>Requirements</h2>
<ul>
<li>AWS CLI</li>
<code>$ sudo pip install awscli</code>
<li>AWS CLI configured to use credentials that allow EC2 access and in the region your unreachable instance is in.</li>
<code>$ aws configure</code>
<li>boto3</li>
<code>$ sudo pip install boto3</code>
<li>Python</li>
<li><b>NOT</b> tested on Windows at the moment, only OS X and Linux</li>
<li>Current supported regions:</li>
<ul>
<li>us-west-2</li>
<li>us-west-1</li>
<li>us-east-1</li>
<li>eu-central-1</li>
<li>eu-west-1</li>
<li>ap-southeast-1</li>
</ul>
</ul>

<h2>Usage</h2>
1) Ensure your AWS CLI credentials are set. Verify with <code>$ aws configure</code> or <code>$ cat ~/.aws/credentials</code>

2) Execute the python script <code>python ec2-lazarus.py</code>

3) Input your unreachable instance ID.

4) Your unreachable instance must be in the "stopped" state. If not the script will notify you.

5) Input a keypair name stored in AWS. This will be the keypair you will use to login to the recovery instance.

6) Associate an existing security group ID with this (ex: sg-412cdef1). At a minimum you will need TCP 22 accessible from your IP to SSH to your recovery instance.

7) Choose which region your unreachable instance is in and where the recovery instance will be launched
(<strong>NOTE:</strong> you will need to have <code>aws configure</code> set to the region you specify.)

8) You will see a temporary instance with a name tag of "ec2-lazarus recovery instance" with your instance's root volume mounted as /dev/sdf. SSH to the instance and perform diagnostics/troubleshooting there.

9) Once finished detach the root volume and place and mount it back on your original instance.
<strong>Note:</strong> Depending on your AMI or OS your mount point for the root volume may be /dev/sda1 || /dev/sda || /dev/xvda || something else entirely.

<h2>FAQ</h2>
<ol>
<li>Nothing yet. Ask me some questions.</li>
</ol>
