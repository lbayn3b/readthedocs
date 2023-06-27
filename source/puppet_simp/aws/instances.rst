Terraform Instance Base
========================

Define the parameters for the instance

Building instances with the base module, you can set and override the following variables:
.. code-block:: ruby 
# Define the image to use
"base_ami"
"availability_zone_names"
"security_group_id"
"subnet_id"
"aws_region"
"key_id" 
"base_size" = "r5.2xlarge"
"number_servers" = 1
"ip_addresses" = [""]
"name_list" = [""]
"assign_public_ip" = false
"ebs_volume_size" = 0
"ebs_volume_count" = 0
"ebs_volume_mountpoint" = ["sdb","sdc","sdd","sde","sdf"]
"root_block_volume_size" = 100
"iam_profile" = ""

Set the parameters for the ssh bastion host
.. code-block:: ruby
"bastion_user" = "ec2-user"
"ssh_user" = "maintuser"
"bastion_host_ip"
"bastion_private_key"
"host_private_key"



Building instances with the base module, you can use the following variables to run commands and send files:
.. code-block:: ruby 
"command_to_pass" = [""]
"file_to_pass" = ""
"user_data" = "hostname -f"

