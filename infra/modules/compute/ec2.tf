resource "aws_launch_template" "ansible_instance_launch_template" {
  name_prefix = "instances_launch_template-"
#   image_id = "ami-0b59bfac6be064b78" 
  instance_type = "${var.instance_type}"
  instance_initiated_shutdown_behavior = "stop"
  key_name = "${var.key_name}" 
  block_device_mappings {
    device_name = "/dev/xvda"
    ebs {
      volume_size = 40
      volume_type = "gp2"
      delete_on_termination = true
    }
  }
  ebs_optimized = true
  monitoring {
    enabled = true
  }
  user_data = "${base64encode(file("${path.module}/compute_startup_scripts/ansible_asg_startup_script.sh"))}"
}


# Our master instance with everything we need to use ansible
resource "aws_instance" "master" {
    launch_template {
      id = aws_launch_template.ansible_instance_launch_template.id
      name = "AnsibleComputeNode"
    }
    # ami = "ami-0b59bfac6be064b78"
    instance_type = "${var.instance_type}"
    # vpc_security_group_ids = ["${aws_security_group.public.id}"]
    # key_name = "Default SSH"
    # subnet_id = "${aws_subnet.default.id}"
    # associate_public_ip_address = true
    # # Use our local ssh key to connect to the master
    # connection {
    #     host = ""
    #     type = "ssh"
    #     user = "ec2-user"
    #     # private_key = "${file("~/.ssh/id_rsa")}"
    # }
  
    provisioner "remote-exec" {
        inline = [
            # Install ansible on master
            "sudo yum-config-manager --enable epel",
            "sudo yum -y install ansible",
          
            "ansible-playbook setup_hadoop.yml", 
        ]
    }
}
