FROM centos:7

RUN yum install -y epel-release
RUN yum install -y python2-pip
RUN yum install -y gcc libffi-devel python-devel openssl-devel
RUN yum install -y voms-clients-java
RUN yum install -y gfal2-all gfal2-util
RUN yum install -y vim

# Upgrade pip & setuptools
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN rm -rf /usr/lib/python2.7/site-packages/ipaddress*

ADD files/ca.repo /etc/yum.repos.d/ca.repo
ADD files/wlcg-centos7.repo /etc/yum.repos.d/wlcg-centos7.repo
ADD files/RPM-GPG-KEY-wlcg /etc/pki/rpm-gpg/RPM-GPG-KEY-wlcg


RUN yum install -y ca-policy-egi-core
RUN yum install -y wlcg-voms-atlas

# Install Rucio
RUN pip install rucio-clients

# Install ATLAS files
ADD files/rucio.cfg /opt/rucio/etc/rucio.cfg
ADD files/ca.crt /opt/rucio/etc/ca.crt

ADD files/pyopenssl.py /usr/lib/python2.7/site-packages/urllib3/contrib/pyopenssl.py

# To enable bash completion for the rucio clients
ADD files/activate_rucio_global_completion.sh /root/.bashrc

ENV PATH $PATH:/opt/rucio/bin
