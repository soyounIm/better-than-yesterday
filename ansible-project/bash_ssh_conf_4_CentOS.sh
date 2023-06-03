#! /usr/bin/env bash

sudo echo 'root:dlathdus' | sudo chpasswd
sudo sed -i -e 's/PermitRootLogin no/PermitRootLogin yes/g' /etc/ssh/sshd_config
sudo sed -i -e 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sudo systemctl restart sshd