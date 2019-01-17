FROM centos:7

RUN yum install -y epel-release
RUN yum install -y python2-pip
RUN yum install -y voms-clients-java
RUN yum install -y gfal2-all gfal2-util
RUN yum install -y nordugrid-arc-client nordugrid-arc-plugins-gfal \
                   nordugrid-arc-plugins-globus nordugrid-arc-plugins-s3 \
                   nordugrid-arc-plugins-xrootd

# Upgrade pip & setuptools
RUN pip install --upgrade setuptools
RUN pip install --upgrade pip

ADD files/ca.repo /etc/yum.repos.d/ca.repo
ADD files/wlcg-centos7.repo /etc/yum.repos.d/wlcg-centos7.repo
ADD files/RPM-GPG-KEY-wlcg /etc/pki/rpm-gpg/RPM-GPG-KEY-wlcg

# Install Rucio
RUN pip install rucio-clients
RUN pip install jinja2 j2cli pyyaml

# Install VOMS / CAs
RUN yum install -y ca-policy-egi-core
RUN yum install -y wlcg-voms-atlas
COPY vars/rucio.yml /
COPY templates/rucio.cfg.j2 /
# dteam
COPY files/dteam-voms2.hellasgrid.gr /etc/vomses/dteam-voms2.hellasgrid.gr
RUN mkdir -p /etc/grid-security/vomsdir/dteam/
COPY files/dteam-voms2.hellasgrid.gr /etc/vomses/dteam-voms2.hellasgrid.gr
COPY files/dteam /etc/grid-security/vomsdir/dteam/

# To generate the configuration and enable bash completion for the rucio clients
ADD files/bashrc /root/.bashrc

ENV PATH $PATH:/opt/rucio/bin
