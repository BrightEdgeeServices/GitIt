#!/bin/bash

## Called from Docker script
## Set root password from environment variable
#echo "root:${LINUX_ROOT_PWD}" | chpasswd
#
## Create user account from environment variables
#useradd -rm -d /home/${INSTALLER_USERID} -s /bin/bash -g root -G sudo ${INSTALLER_USERID}
#echo "${INSTALLER_USERID}:${INSTALLER_PWD}" | chpasswd

# Start the SSH server
/usr/sbin/sshd -D
