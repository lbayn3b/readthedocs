Client Administration
=====================

.. note::
    Follow these steps to add an instance to be managed by the Puppet Server


1. ``vi /var/simp/environments//production/rsync/CentOS/7/bind_dns/default/named/var/named/forward/<your.domain.db>``

2. add forward entry for your new host

3. ``vi /var/simp/environments//production/rsync/CentOS/7/bind_dns/default/named/var/named/reverse/<your.domain.db>``

4. add reverse entry for you new host

5. ``puppet agent -t --tags named``

6.  ``cd /var/simp/environments/production/FakeCA/``

7.  ``vi togen``

8.  input fqdn (one per line)

9.  save file  

10. run ``./gencerts_nopass.sh``

11. ``cd /etc/puppetlabs/code/environments/production/site/profile/manifests``

12. ``vi base.pp``

.. code:: ruby

    class profile::base {

      class { 'profile::local_user': }
    }

13. ``cd /etc/puppetlabs/code/environments/production/manifests/``

14. ``vi site/pp``

15. Add the following lines to the end of the file. In this example it will be hostname repo and be given the role::admin::repo role

.. code:: ruby

  node default {
  }

  node repo {
    include role::admin::repo
  }

16. ``cd /etc/puppetlabs/code/environments/production/site/role/manifests``

17. ``mkdir admin/``

18. ``chown puppet:puppet admin/``

19. ``chmod 755 admin/``

20. ``vi repo.pp`` (This will add the profile base we previously created to the repo role)

.. code:: ruby
    
    class role::admin::repo {

      include profile::base
    }

.. note::
    Your system is now ready to be taken over by the Puppet Server

21. Log into the new instance with the credentials provided by the infrastructure team.

22. ``vi addToPuppet.sh``

23. Copy the following contents into addToPuppet.sh

.. code:: ruby

    #! /bin/bash

    nameserver="<ip.of.dns.server"
    domain="<domain.of.environment"
    puppetserver="<puppet-server-hostname>.${domain}"
    puppetip="<ip.of.puppet.server"
    repo="<ip.of.repo.server"
    prefix="<prefixOfHostname>-"

    echo "Enter the Server's Hostname"

    read hostname

    echo "The fqdn will be $prefix$hostname.$domain"

    echo "Enter y to continue or Ctrl-C to quit"

    read doigonow

    hostnamectl set-hostname $prefix$hostname.$domain

    ################################################################################################################################
    #  PUT IN REPOS
    ################################################################################################################################

    echo "[epel]" >> /etc/yum.repos.d/epel.repo
    echo "name=epel" >> /etc/yum.repos.d/epel.repo
    echo "baseurl=http://$repo/mc-release/7/x86_64/epel" >> /etc/yum.repos.d/epel.repo
    echo "enabled=1" >> /etc/yum.repos.d/epel.repo
    echo "gpgcheck=0" >> /etc/yum.repos.d/epel.repo

    echo "[rhel-79-server-rpms]" >> /etc/yum.repos.d/redhat_local.repo
    echo "name=rhel-79-server-rpms" >> /etc/yum.repos.d/redhat_local.repo
    echo "baseurl=http://$repo/rhel7/rhel-79-server-rpms" >> /etc/yum.repos.d/redhat_local.repo
    echo "enabled=1" >> /etc/yum.repos.d/redhat_local.repo
    echo "gpgcheck=0" >> /etc/yum.repos.d/redhat_local.repo

    echo "[simp]" >> /etc/yum.repos.d/simp.repo
    echo "name=simp" >> /etc/yum.repos.d/simp.repo
    echo "baseurl=http://$repo/mc-release/7/x86_64/ajax/simp-project_6_X" >> /etc/yum.repos.d/simp.repo
    echo "enabled=1" >> /etc/yum.repos.d/simp.repo
    echo "gpgcheck=0" >> /etc/yum.repos.d/simp.repo

    echo "[simp-dependencies]" >> /etc/yum.repos.d/simp_dependencies.repo
    echo "name=simp-dependencies" >> /etc/yum.repos.d/simp_dependencies.repo
    echo "baseurl=http://$repo/mc-release/7/x86_64/ajax/simp-project_6_X_dependencies" >> /etc/yum.repos.d/simp_dependencies.repo
    echo "enabled=1" >> /etc/yum.repos.d/simp_dependencies.repo
    echo "gpgcheck=0" >> /etc/yum.repos.d/simp_dependencies.repo


    # Stop NetworkManager
    systemctl stop NetworkManager

    # Disable NetworkManager
    systemctl disable NetworkManager

    # Unmanage NetworkManager in network-scripts
    echo 'NM_CONTROLLED="no"' >> /etc/sysconfig/network-scripts/ifcfg-ens<value_of_active_interface>

    # Modify /etc/resolve.conf

    cat > /etc/resolve.conf <<EOL
    # This file is managed by Puppet (module 'resolv')
    nameserver ${nameserver}
    domain ${domain}
    search ${domain}
    EOL

    # Disable gpgcheck in yum.conf

    sed -i 's/repo_gpgcheck=1/repo_gpgcheck=0/g' /etc/yum.conf
    sed -i 's/localpkg_gpgcheck=1/localpkg_gpgcheck=0/g' /etc/yum.conf
    sed -i 's/gpgcheck=1/gpgcheck=0/g' /etc/yum.conf
        
    # Clean yum cache
    yum clean all
    rm -rf /var/cache/yum

    # Install puppet-agent
    yum install puppet-agent

    # Create puppet.conf

    cat > /etc/puppetlabs/puppet/puppet.conf <<EOL
    [main]
    vardir            = /opt/puppetlabs/puppet/cache
    classfile         = $vardir/classes.txt
    localconfig       = $vardir/localconfig
    logdir            = /var/log/puppetlabs/puppet
    report            = false
    rundir            = /var/run/puppetlabs
    server            = ${puppetserver}
    ssldir            = /etc/puppetlabs/puppet/ssl
    trusted_node_data = true
    stringify_facts   = false
    digest_algorithm  = sha256
    keylength         = 2048
    ca_server         = ${puppetserver}
    ca_port           = 8141
    splay = false
    syslogfacility = local6
    srv_domain = ${domain}
    certname = ${hostname}
    confdir = /etc/puppetlabs/puppet
    runinterval = 1800
    masterport = 8140

    [agent]
    daemonize = false
    environment = production
    report = false
    EOL

    # RUN PUPPET
    /opt/puppetlabs/puppet/bin/puppet agent -t

24. ``chmod +x addToPuppet.sh``

25. ``./addToPuppet.sh``

26. Log back in to PuppetServer and ``puppet sign cert <fqdn of new instance>``

27. You should now be able to run ``puppet agent -t`` on new instance and it will now be managed by the Puppet Server.