#!/bin/bash
useradd -m {username}
echo '{username}:{password}' | chpasswd
apt update -y && apt install -y gdebi-core r-base 
wget https://download2.rstudio.org/rstudio-server-1.1.383-amd64.deb
gdebi --non-interactive rstudio-server-1.1.383-amd64.deb
rm rstudio-server-1.1.383-amd64.deb
