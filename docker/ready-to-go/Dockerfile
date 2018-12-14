FROM centos:7

RUN yum install -y epel-release
RUN yum install -y python2-pip
RUN yum install -y gcc libffi-devel python-devel openssl-devel
RUN yum install -y httpd mod_ssl gridsite mod_auth_kerb mod_wsgi
RUN yum install -y voms-clients-java
RUN yum install -y gfal2-all gfal2-util
RUN yum install -y supervisor
RUN yum install -y vim

# Upgrade pip & setuptools
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN rm -rf /usr/lib/python2.7/site-packages/ipaddress*

ADD files/ca.repo /etc/yum.repos.d/ca.repo

# Install Rucio
RUN pip install rucio            # [postgresql]
RUN pip install psycopg2-binary
RUN pip install rucio-webui
RUN pip install sseclient

WORKDIR /opt

RUN mkdir /var/log/rucio
RUN chmod 777 /var/log/rucio
RUN mkdir /var/log/rucio/trace
RUN chmod 777 /var/log/rucio/trace

ADD files/httpd.conf /etc/httpd/conf/httpd.conf
ADD files/rucio.conf /etc/httpd/conf.d/rucio.conf

RUN yum install -y supervisor
ADD files/rucio.ini /etc/supervisord.d/rucio.ini
ADD files/supervisord.conf /etc/supervisord.conf
# RUN systemctl enable supervisord.service
# CMD ["/usr/sbin/init"]

ADD files/pyopenssl.py /usr/lib/python2.7/site-packages/urllib3/contrib/pyopenssl.py
# To enable bash completion for the rucio clients
ADD files/rucio/tools/activate_rucio_global_completion.sh /root/.bashrc
ADD files/rucio-admin /usr/bin/rucio-admin
ADD files/rule.py /usr/lib/python2.7/site-packages/rucio/core/rule.py
RUN chmod 644 /usr/lib/python2.7/site-packages/rucio/core/rule.py

WORKDIR /opt/rucio

RUN rm /etc/httpd/conf.d/ssl.conf /etc/httpd/conf.d/autoindex.conf \
       /etc/httpd/conf.d/userdir.conf /etc/httpd/conf.d/welcome.conf

EXPOSE 443

ENV PATH $PATH:/opt/rucio/bin
