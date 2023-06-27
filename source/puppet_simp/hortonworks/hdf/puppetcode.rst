Puppet Code for HDF Cluster
===========================

1. Create directory for hdf roles.

``cd /etc/puppetlabs/code/environments/production/site/role/manifests``
  
``mkdir hdf``
  
``chown puppet:puppet hdf/``
  
``chmod 755 hdf/``

2. Create roles for all hosts in HDF cluster.
  
``cd hdf/``

``vi master.pp``

.. code:: ruby
   
   class role::hdf::master {
     include profile::local_user
     include profile::hdf::hdfall
     include profile::hdf::master
     include profile::software::java
     include profile::iptables::internal_iptables
     include profile::base

   }
  
``vi kafka.pp``

.. code:: ruby

   class role::hdf::kafka {
     include profile::local_user
     include profile::base
     include profile::hdf::hdfall
     include profile::hdf::kafka
     include profile::iptables::internal_iptables
     include profile::software::java
   }

``vi nifi.pp``

.. code:: ruby

   class role::hdf::nifi {
     include profile::local_user
     include profile::base
     include profile::hdf::hdfall
     include profile::hdf::nifi
     include profile::iptables::internal_iptables
     include profile::software::java
   }

``vi zookeeper.pp``

.. code:: ruby

   class role::hdf::zookeeper {
     include profile::local_user
     include profile::base
     include profile::hdf::hdfall
     include profile::hdf::zookeeper
     include profile::iptables::internal_iptables
     include profile::software::java
   }

``chown puppet:puppet *.pp``

``chmod 644 *.pp``

3. Create directory for hdf profiles.

  ``cd /etc/puppetlabs/code/environments/production/site/profile/manifests``
  
  ``mkdir hdf``
  
  ``chown puppet:puppet hdf/``
  
  ``chmod 755 hdf/``

4. Create directory for iptables.

  ``cd /etc/puppetlabs/code/environments/production/site/profile/manifests``
  
  ``mkdir iptables``
  
  ``chown puppet:puppet iptables/``
  
  ``chmod 755 iptables/``

5. Create directory for software.

  ``cd /etc/puppetlabs/code/environments/production/site/profile/manifests``
  
  ``mkdir software``
  
  ``chown puppet:puppet software/``
  
  ``chmod 755 software/``

6. Add Puppet code to hdfall.pp.

  ``cd /etc/puppetlabs/code/environments/production/site/profile/manifests/hdf/``

  ``vi hdfall.pp``

.. code:: ruby

   class profile::hdf::hdfall {
     
      file { '/storage' :
        ensure => 'directory',
        owner  => 'root',
        group  => 'root',
        mode   => '0755'
      }

   }

7. Create java puppet module.

  ``cd /etc/puppetlabs/code/environments/production/site/profile/manifests/software/``

  ``vi java.pp``

.. code:: ruby

   class profile::software::java {

     package { 'java' :
       ensure => installed
     }

   }

8. Create individual profile modules.

``cd /etc/puppetlabs/code/environments/production/site/profile/manifests/hdf/``

``vi master.pp``

.. code:: ruby

   class profile::hdf::master {

   #########################################
   # Install Ambari Server
   ########################################
   
     package { 'ambari-server':
       ensure => installed
     }
   
   #####################################################################
   # Ambari User Login (Allows created users to login to systems and su)
   #####################################################################
   
     sudo::user_specification { master_su :
       user_list => ['ambari-qa','ams','postgres','infra-solr'],
       host_list => ['ALL'],
       runas     => 'ALL',
       cmnd      => ['/usr/bin/su'],
       passwd    => false
     }
   
     pam::access::rule { master_user_login :
       users   => ['ambari-qa','ams','postgres','infra-solr'],
       origins => ['ALL'],
       comment => 'User Access'
     }
   
   ###########################################
   # Ambari agent install and configuration
   ###########################################
   
     class { 'profile::software::ambari_agent': }
   
   ############################################
   # Ambari Server Setup
   ############################################
   
     exec { 'ambari-server setup -j /usr/lib/jvm/jre/ -s':
       creates => '/etc/ambari-server/conf/password.dat',
     }
   
   ###########################################
   # Ambari Server Service
   ###########################################
   
     service { 'ambari-server':
       ensure  => running,
       start   => '/usr/sbin/ambari-server start',
       stop    => '/usr/sbin/ambari-server stop',
       status  => '/usr/sbin/ambari-server status',
       restart => '/usr/sbin/ambari-server restart',
     }
   
     service { 'postgresql':
       ensure => running
     }
   
   ###########################################
   # Ambari HDF Mpack Installation
   ###########################################
   
     file { '/storage/':
       ensure => 'directory',
       owner   => 'root',
       group   => 'root',
       mode    => '0755'
     }
   
     archive { '/storage/mpack.tar.gz':
       ensure => present,
       source => 'http://<repo_server_where_mpack_is_hosted/hdf-ambari-mpack-3.4.1.1-4.tar.gz',
       user   => 0,
       group  => 0
     }
   
     exec { 'cp -r /var/lib/ambari-server/resources /var/lib/ambari-server/resources.backup && ambari-server install-mpack --mpack=/storage/mpack.tar.gz':
       creates => '/var/lib/ambari-server/resources.backup',
       notify  => Service['ambari-server']
     }
   }
   
``vi kafka.pp``

.. code:: ruby

   class profile::hdf::kafka {
   
   ####################################
   # Install / Configure Ambari Agent
   ####################################
   
     class { 'profile::software::ambari_agent': }
   
   ####################################
   # Kafka Account login and su
   ###################################
   
     sudo::user_specification { master_su :
       user_list => ['ambari-qa','ams','nifi','infra-solr','kafka','nifiregistry','zookeeper'],
       host_list => ['ALL'],
       runas     => 'ALL',
       cmnd      => ['/usr/bin/su'],
       passwd    => false
     }
   
     pam::access::rule { master_user_login :
       users   => ['ambari-qa','ams','nifi','infra-solr','kafka','nifiregistry','zookeeper'],
       origins => ['ALL'],
       comment => 'User Access'
     }
   }

``vi nifi.pp``

.. note::
   Ensure you place snappy-1.0.5-libsnappyjava.so at /tmp on all nifi hosts prior to putting this code in puppet

.. code:: ruby

   class profile::hdf::nifi {
         
          
   ############################################
   # Create data01 directories
   ############################################
   
     file { '/data01/usr':
       ensure => 'directory',
       owner  => 'root',
       group  => 'root',
       mode   => '0755'
     }
     
     file { '/data01/usr/hdf':
       ensure => 'directory',
       owner  => 'root',
       group  => 'root',
       mode   => '0755'
     }
  
     file { '/data01/usr/hdf/current':
       ensure => 'directory',
       owner  => 'root',
       group  => 'root',
       mode   => '0755'
     }
     
     file { '/data01/usr/hdf/current/nifi':
       ensure => 'directory',
       owner  => 'root',
       group  => 'root',
       mode   => '0755'
     }
     
     file { '/data01/usr/hdf/current/nifi/tmp':
       ensure => 'directory',
       owner  => 'root',
       group  => 'root',
       mode   => '0755'
     }
   
     file { '/data01/nifi':
       ensure => 'directory',
       owner  => 'root',
       group  => 'root',
       mode   => '0755'
     }
   
     file { '/data01/nifi/tmp':
       ensure => 'directory',
       owner  => 'root',
       group  => 'root',
       mode   => '0755'
     }
   
     file { '/data01/nifi/tmp/snappy-1.0.5-libsnappyjava.so':
       ensure => 'file',
       owner  => 'root',
       group  => 'root',
       mode   => '0755',
       source => '/tmp/snappy-1.0.5-libsnappyjava.so',
     }
   
    ####################################
    # Install / Configure Ambari Agent
    ####################################
     
     class { 'profile::software::ambari_agent': }
   
   ####################################
   # Nifi Account login and su
   ###################################
   
     sudo::user_specification { master_su :
       user_list => ['ambari-qa','ams','nifi','infra-solr','kafka','nifiregistry','zookeeper'],
       host_list => ['ALL'],
       runas     => 'ALL',
       cmnd      => ['/usr/bin/su'],
       passwd    => false
     }

  pam::access::rule { master_user_login :
    users   => ['ambari-qa','ams','nifi','infra-solr','kafka','nifiregistry','zookeeper'],
    origins => ['ALL'],
    comment => 'User Access'
  }
   }

``vi zookeeper.pp``

.. code:: ruby

   class profile::hdf::zookeeper {
   
   ####################################
   # Install / Configure Ambari Agent
   ####################################
   
     class { 'profile::software::ambari_agent': }
   
   ####################################
   # Zookeeper Account login and su
   ###################################
   
     sudo::user_specification { master_su :
       user_list => ['ambari-qa','ams','nifi','infra-solr','kafka','nifiregistry','zookeeper'],
       host_list => ['ALL'],
       runas     => 'ALL',
       cmnd      => ['/usr/bin/su'],
       passwd    => false
     }
   
     pam::access::rule { master_user_login :
       users   => ['ambari-qa','ams','nifi','infra-solr','kafka','nifiregistry','zookeeper'],
       origins => ['ALL'],
       comment => 'User Access'
     }
   }

``chown puppet:puppet *.pp``

``chmod 644 *.pp``

9. Create ambari agent module.

``cd /etc/puppetlabs/code/environments/production/site/profile/manifests/software/``

``vi ambari_agent.pp``

.. code:: ruby

   class profile::software::ambari_agent {
   
   ###########################################
   # Ambari agent install and configuration
   ###########################################
   
     package { 'ambari-agent':
       ensure => installed
     }
   
     file { '/etc/ambari-agent/conf/ambari-agent.ini':
       ensure  => 'file',
       owner   => 'root',
       group   => 'root',
       mode    => '0640',
       content => template('profile/software/ambari/ambari-agent.ini.erb'),
       require => Package['ambari-agent'],
       notify  => Service['ambari-agent']
     }
   
     service { 'ambari-agent':
       ensure => running,
       enable => true
     }
   }

``chown puppet:puppet ambari_agent.pp``

``chmod 644 ambari_agent.pp``

10. Create ambari agent template file.

``cd /etc/puppetlabs/code/environments/production/site/profile/templates/``

``mkdir -p software/ambari/``

``chown -R puppet:puppet *``

``find . -type d -exec chmod 755 {} \;``

``cd software/ambari/``

``vi ambari-agent.ini.erb``

.. code:: ruby

   # Licensed to the Apache Software Foundation (ASF) under one or more
   # contributor license agreements.  See the NOTICE file distributed with
   # this work for additional information regarding copyright ownership.
   # The ASF licenses this file to You under the Apache License, Version 2.0
   # (the "License"); you may not use this file except in compliance with
   # the License.  You may obtain a copy of the License at
   #
   #     http://www.apache.org/licenses/LICENSE-2.0
   #
   # Unless required by applicable law or agreed to in writing, software
   # distributed under the License is distributed on an "AS IS" BASIS,
   # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   # See the License for the specific
 
   [server]
   hostname=<fqdn of hdfmaster>
   url_port=8440
   secured_url_port=8441 
 
   [agent]
   logdir=/var/log/ambari-agent
   piddir=/var/run/ambari-agent
   prefix=/var/lib/ambari-agent/data
   tmp_dir=/var/lib/ambari-agent/tmp
   ;loglevel=(DEBUG/INFO)
   loglevel=INFO
   data_cleanup_interval=86400
   data_cleanup_max_age=2592000
   data_cleanup_max_size_MB = 100
   ping_port=8670
   cache_dir=/var/lib/ambari-agent/cache
   tolerate_download_failures=true
   run_as_user=root
   parallel_execution=0
   alert_grace_period=5
   alert_kinit_timeout=14400000
   system_resource_overrides=/etc/resource_overrides
 
   [security]
   keysdir=/var/lib/ambari-agent/keys
   server_crt=ca.crt
   passphrase_env_var_name=AMBARI_PASSPHRASE
 
   [services]
   pidLookupPath=/var/run/
 
   [heartbeat]
   state_interval_seconds=60
   dirs=/etc/hadoop,/etc/hadoop/conf,/etc/hbase,/etc/hcatalog,/etc/hive,/etc/oozie,
     /etc/sqoop,/etc/ganglia,
     /var/run/hadoop,/var/run/zookeeper,/var/run/hbase,/var/run/templeton,/var/run/oozie,
     /var/log/hadoop,/var/log/zookeeper,/var/log/hbase,/var/run/templeton,/var/log/hive
   ; 0 - unlimited
   log_lines_count=300
   idle_interval_min=1
   idle_interval_max=10
 
   [logging]
   syslog_enabled=0

``chown puppet:puppet ambari-agent.ini.erb``

``chmod 644 ambari-agent.ini.erb``

11. Configure iptables modules (This allows open communication between hosts of the cluster).

``cd /etc/puppetlabs/code/environments/production/site/profiles/manifests/iptables/``

``vi internal_iptables.pp``

.. code:: ruby

   class profile::iptables::internal_iptables {
   
     iptables::listen::all { 'internal_internal_all':
       trusted_nets => [ 'xxx.xxx.xxx.xxx/xx'],
     }
   }

12. Assign roles to instances.

``cd /etc/puppetlabs/code/environments/production/manifests/``

``vi site.pp`` and add your instances to the bottom to match your environments

.. code:: ruby

   node default {
   }
   node <hostname of hdfmaster> {
     include role::hdf::master
   }
   node <hostname of nifi> {
     include role::hdf::nifi
   }
   node <hostname of kafka> {
     include role::hdf::kafka
   }
   node <hostname of zookeeper> {
     include role::hdf::zookeeper
   }

13. Log into hdfmaster instance and run ``puppet agent -t``. Ensure you get a clean puppet run and type ``ambari-server status`` to ensure ambari-server is running.

.. note::
   At this point you can either log into all instances in the hdf cluster and run ``puppet agent -t`` or wait 30 minutes for all instances to auto run puppet
