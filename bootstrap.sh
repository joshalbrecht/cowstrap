#!/bin/bash
set -ex

#required configuration:

HOSTNAME=$1
REPO_URL=$2
REPO=$( python -c "print \"$REPO_URL\".split('/')[-1].split('.')[0]" )
GITHUB_USER=$3
GITHUB_PASSWORD=$4

USERNAME="cow"
SCRIPT_NAME="cow.yml"

#shell provisioning:

#set the hostname:
echo $HOSTNAME > /etc/hostname
hostname $HOSTNAME
grep "127.0.0.1 $HOSTNAME" /etc/hosts || echo "127.0.0.1 $HOSTNAME" >> /etc/hosts

#required to be able to call add-apt-repository:
apt-get install -y python-software-properties

#add the ansible ppa
add-apt-repository -y ppa:rquillo/ansible

#update to the latest packages
apt-get update

#install ansible and requirements
apt-get install -y python-dev python-pip git ansible python-apt python-pycurl curl

#remove the weird default hosts file:
echo " " > /etc/ansible/hosts

#set up hosts temporarily
echo "127.0.0.1" > ~/ansible_hosts
export ANSIBLE_HOSTS=~/ansible_hosts

#set up convenient ssh
/usr/bin/ssh-keygen -t rsa -C "$EMAIL" -N "" -f /root/.ssh/id_rsa
cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
eval $(ssh-agent)
ssh-add ~/.ssh/id_rsa
export ANSIBLE_HOST_KEY_CHECKING=False

#generate a random password
SALT='$6$SomeSalt$'
PASSWORD=$( python -c 'import os; import base64; print base64.b64encode(os.urandom(32))' )
HASHED_PASSWORD=$( python -c "import crypt; print crypt.crypt(\"$PASSWORD\", \"$SALT\")" )

#create a user
ansible all -m user -a "name=$USERNAME generate_ssh_key=yes ssh_key_bits=2048 password=$HASHED_PASSWORD state=present shell=/bin/bash" --sudo

#create the group
ansible all -m group -a "name=$USERNAME state=present" --sudo

#add the user to the groups
usermod -a -G sudo $USERNAME
usermod -a -G $USERNAME $USERNAME

#TODO: actually, really this script should only run once, and it's an error if the key already exists, because we just generated it...
#(that failure condition happens when you name two machines the same thing)

#import the key into github if it doesnt exist
GITHUB_KEY_NAME="$USERNAME on $HOSTNAME"
curl -s -u "$GITHUB_USER:$GITHUB_PASSWORD" https://api.github.com/user/keys | /bin/grep "$GITHUB_KEY_NAME" || curl -s -d "{\"title\": \"$GITHUB_KEY_NAME\", \"key\": \"$( /bin/cat /home/$USERNAME/.ssh/id_rsa.pub )\"}" -u "$GITHUB_USER:$GITHUB_PASSWORD" https://api.github.com/user/keys

#TODO: do this more securely
#tell ubuntu to not prompt for host verification for when we're talking to github
echo "StrictHostKeyChecking no" > /home/$USERNAME/.ssh/config
#root needs to be able to log into cow for ansible to work
cat /root/.ssh/id_rsa.pub >> /home/$USERNAME/.ssh/authorized_keys
#should obviously be able to log into himself:
cat /home/$USERNAME/.ssh/id_rsa.pub >> /home/$USERNAME/.ssh/authorized_keys
#and should obviously own their own files...
chown $USERNAME:$USERNAME -vR /home/$USERNAME/.ssh
#and should be able to ssh into root I guess (otherwise can't run ansible commands)
cat /home/$USERNAME/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys

#NOTE: this is https instead of git because we dont have the right keys as root
#check out cowstrap
ansible all -m git -a "repo=https://github.com/joshalbrecht/cowstrap.git dest=/etc/cowstrap" --sudo

#check out the project repository
ansible all -m git -a "repo=$REPO_URL dest=/home/$USERNAME/$REPO" --user=$USERNAME

#set the ansible cows group up for the user
cat >/home/$USERNAME/ansible_hosts <<EOL
[cows]
127.0.0.1
EOL
sudo chown $USERNAME:$USERNAME /home/$USERNAME/ansible_hosts

#finally, run the cow.yml in the project as the user, with sudo privileges (if it exists
if [ ! -f /home/$USERNAME/$REPO/$SCRIPT_NAME ]; then
  ansible-playbook /home/$USERNAME/$REPO/$SCRIPT_NAME
fi

#TODO: generate a nice message to show the user with "here is how you log into the machine"
#TODO: wrap this entire thing into a nice script that takes sensible arguments and does the entire flow
echo "Here is your password: $PASSWORD"



