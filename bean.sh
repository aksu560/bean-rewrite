#!/bin/bash

if [ -z "$1" ]
then
      export BEAN_ENV="prod"
else
      export BEAN_ENV=$1
fi

vagrant status | grep 'running' &> /dev/null
if [ $? == 0 ];
then
   echo "Vagrant running, provisioning"
   vagrant provision
else
   echo "Vagrant not running, upping box"
   vagrant up
fi