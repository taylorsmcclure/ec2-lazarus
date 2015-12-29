# ec2-lazarus
<p>Python based script to stop your unreachable instance and mount its root volume on a temporary recovery instance</p>

<h2>Prerequisites</h2>
<ul>
<li>AWS CLI</li>
<code>$ sudo pip install awscli</code>
<li>boto3</li>
<code>$ sudo pip install boto3</code>
<li>Python</li>
<li><b>NOT</b> tested on Windows at the moment, only OS X and Linux</li>
</ul>

<h2>Usage</h2>
1) Ensure your AWS CLI credentials are set. Verify with <code>$ aws configure</code> or <code>$ cat ~/.aws/credentials</code>

2) Execute the python script <code>python ec2-lazarus.py</code>

3) Follow the instructions

4) You will see a temporary instance with your instance's root volume mounted as /dev/sdf. SSH to the instance and perform diagnostics/troubleshooting there.

5) Detach the root volume once done

6) Reattach the root volume back on the original instance
