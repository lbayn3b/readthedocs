Puppet Code for HDP Cluster
===========================

1. Create directory for hdp roles.

``cd /etc/puppetlabs/code/environments/production/site/role/manifests``
  
``mkdir hdp``
  
``chown puppet:puppet hdp/``
  
``chmod 755 hdp/``

2. Create roles for all hosts in HDP cluster.
  
``cd hdp/``

``vi master.pp``

.. code:: ruby
   
   class role::hdp::master {
     include profile::local_user
     include profile::hdp::master
     include profile::hdp::hdpall
     include profile::iptables::internal_iptables
     include profile::base

   }
  
``vi datanode.pp``

.. code:: ruby

   class role::hdp::datanode {
     include profile::local_user
     include profile::base
     include profile::hdp::hdpall
     include profile::hdp::datanode
     include profile::iptables::internal_iptables
     include profile::software::java
   }

``vi zookeeper.pp``

.. code:: ruby

   class role::hdp::zookeeper {
     include profile::local_user
     include profile::base
     include profile::hdp::hdpall
     include profile::hdp::zookeeper
     include profile::iptables::internal_iptables
     include profile::software::java
   }

``chown puppet:puppet *.pp``

``chmod 644 *.pp``

3. Create directory for hdp profiles.

  ``cd /etc/puppetlabs/code/environments/production/site/profile/manifests``
  
  ``mkdir hdp``
  
  ``chown puppet:puppet hdp/``
  
  ``chmod 755 hdp/``

4. Add Puppet code to hdpall.pp.

  ``cd /etc/puppetlabs/code/environments/production/site/profile/manifests/hdp/``

  ``vi hdpall.pp``

.. code:: ruby

   class profile::hdp::hdpall {
   
   ############################################
   # Create AJAX directories
   ############################################
   
     file { '/data01/':
       ensure => 'directory',
       owner  => 'root',
       group  => 'root',
       mode   => '0755'
     }
   
   ####################################
   # HDP Account login and su
   ###################################
   
     sudo::user_specification { hdp_su :
       user_list => ['hive','yarn-ats','storm','infra-solr','zookeeper','atlas','oozie','ams','ranger','tez','zeppelin','kms','accumulo','livy','druid','spark','ambari-qa','kafka','hdfs','sqoop','yarn','hbase','mapred','knox','activity_analyzer','koverse',   'postgres'],
       host_list => ['ALL'],
       runas     => 'ALL',
       cmnd      => ['/usr/bin/su'],
       passwd    => false
     }
   
     pam::access::rule { hdp_user_login :
       users   => ['hive','yarn-ats','storm','infra-solr','zookeeper','atlas','oozie','ams','ranger','tez','zeppelin','kms','accumulo','livy','druid','spark','ambari-qa','kafka','hdfs','sqoop','yarn','hbase','mapred','knox','activity_analyzer','koverse','postgres'],
       origins => ['ALL'],
       comment => 'User Access'
     }
   
     package { 'java-devel':
       ensure => installed
     }
   
     user { 'koverse':
       ensure => 'present',
       uid => 1910,
       home => '/home/koverse',
     }
   
     group { 'koverse':
       ensure => 'present',
       gid => 1910,
       members => 'koverse',
       require => User['koverse']
     }
   
     group { 'sechadoop':
       ensure => 'present',
       gid => 1911,
       members => 'koverse',
       require => User['koverse']
     }
   }


5. Create individual profile modules.

``cd /etc/puppetlabs/code/environments/production/site/profile/manifests/hdp/``

``vi master.pp``

.. code:: ruby

   class profile::hdp::master {

   #########################################
   # Install Ambari Server
   ########################################
   
     package { 'ambari-server':
       ensure => installed
     }
   
   ##########################################
   # Ambari User Login Stuff
   ##########################################
   
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
   
     sudo::user_specification { 'ulimit_sudo':
       user_list => ['hdfs'],
       host_list => ['ALL'],
       runas     => 'root',
       cmnd      => ['/bin/bash', '/usr/hdp/3.1.0.0-78/hadoop/bin/hdfs'],
       passwd    => false
     }
   
     sudo::user_specification { 'accumulo_sudo':
       user_list => ['accumulo'],
       host_list => ['ALL'],
       runas     => 'root',
       cmnd      => ['/usr/hdp/current/accumulo-client/bin/accumulo'],
       passwd    => false
     }
   
   ###########################################
   # ULIMIT Set
   ##########################################
   
     pam::limits::rule { 'limit_core':
       domains => ['*'],
       type    => 'hard',
       item    => 'core',
       value   => unlimited,
       order   => 9999
     }
   
   ###########################################
   # Ambari agent install and configuration
   ###########################################
   
     class { 'profile::software::ambari_agent_hdp': }
   
   ############################################
   # Ambari Server Setup
   ############################################
   
   ####### Ensure https://jdbc.postgresql.org/download/postgresql-42.2.23.jar is placed at /usr/share/java/postgresql-jdbc.jar #########
      
     exec { 'ambari-server setup -j /usr/lib/jvm/java/ -s && touch /storage/.firstAmbariSetupDone.txt':
       creates => '/etc/ambari-server/conf/password.dat',
       onlyif => '/bin/test -f /usr/lib/jvm/java/bin/java'
     }
   
     exec { 'ambari-server setup --jdbc-db=postgres --jdbc-driver=/usr/share/java/postgresql-jdbc.jar && touch /storage/.jdbc.txt':
       creates => '/storage/.jdbc.txt',
       onlyif => '/bin/test -f /storage/.pgHba.conf.inplace.txt'
     }
   
     exec { 'build-hive-db':
       environment => ["PGPASSWORD=bigdata"],
       cwd         => "/var/lib/",
       user        => "postgres",
       logoutput   => true,
       command => 'echo "CREATE DATABASE hive;" | psql -U postgres && echo "CREATE USER hive WITH PASSWORD \'password\';" | psql -U postgres && echo "GRANT ALL PRIVILEGES ON DATABASE hive TO hive;" | psql -U postgres',
       unless => ['psql -lqt | cut -d \| -f 1 | grep -qw hive'],
       onlyif => ['systemctl status postgresql']
     }
   
     exec { 'build-ranger-db':
       environment => ["PGPASSWORD=bigdata"],
       cwd         => "/var/lib/",
       user        => "postgres",
       logoutput   => true,
       command => 'echo "CREATE DATABASE ranger;" | psql -U postgres && echo "CREATE USER rangeradmin WITH PASSWORD \'password\';" | psql -U postgres && echo "GRANT ALL PRIVILEGES ON DATABASE ranger TO rangeradmin;" | psql -U postgres',
       unless => ['psql -lqt | cut -d \| -f 1 | grep -qw ranger'],
       onlyif => ['systemctl status postgresql']
     }
   
     exec { 'build-rangerkms-db':
       environment => ["PGPASSWORD=bigdata"],
       cwd         => "/var/lib/",
       user        => "postgres",
       logoutput   => true,
       command => 'echo "CREATE DATABASE rangerkms;" | psql -U postgres && echo "CREATE USER rangerkms WITH PASSWORD \'password\';" | psql -U postgres && echo "GRANT ALL PRIVILEGES ON DATABASE rangerkms TO rangerkms;" | psql -U postgres',
       unless => ['psql -lqt | cut -d \| -f 1 | grep -qw rangerkms'],
       onlyif => ['systemctl status postgresql']
     }
   
     exec { 'build-oozie-db':
       environment => ["PGPASSWORD=bigdata"],
       cwd         => "/var/lib/",
       user        => "postgres",
       logoutput   => true,
       command => 'echo "CREATE DATABASE oozie;" | psql -U postgres && echo "CREATE USER oozie WITH PASSWORD \'password\';" | psql -U postgres && echo "GRANT ALL PRIVILEGES ON DATABASE oozie TO oozie;" | psql -U postgres',
       unless => ['psql -lqt | cut -d \| -f 1 | grep -qw oozie'],
       onlyif => ['systemctl status postgresql']
     }
   
     exec { 'build-druid-db':
       environment => ["PGPASSWORD=bigdata"],
       cwd         => "/var/lib/",
       user        => "postgres",
       logoutput   => true,
       command => 'echo "CREATE DATABASE druid;" | psql -U postgres && echo "CREATE USER druid WITH PASSWORD \'password\';" | psql -U postgres && echo "GRANT ALL PRIVILEGES ON DATABASE druid TO druid;" | psql -U postgres',
       unless => ['psql -lqt | cut -d \| -f 1 | grep -qw druid'],
       onlyif => ['systemctl status postgresql']
     }
   
     exec { 'build-koverse-db':
       environment => ["PGPASSWORD=bigdata"],
       cwd         => "/var/lib/",
       user        => "postgres",
       logoutput   => true,
       command => 'echo "CREATE DATABASE koverse;" | psql -U postgres && echo "CREATE USER koverse WITH PASSWORD \'secret\';" | psql -U postgres && echo "GRANT ALL PRIVILEGES ON DATABASE koverse TO koverse;" | psql -U postgres',
       unless => ['psql -lqt | cut -d \| -f 1 | grep -qw koverse'],
       onlyif => ['systemctl status postgresql']
     }
   
     file { '/storage/pg_hba.conf':
       ensure => 'file',
       owner => 'postgres',
       group => 'postgres',
       mode => '0644',
       content => template('profile/hdp/psql.conf.erb'),
     }
   
     exec { 'putPgHba.conf':
       command => 'cp -f /storage/pg_hba.conf /var/lib/pgsql/data/ && systemctl restart postgresql && touch /storage/.pgHba.conf.inplace.txt',
       onlyif => '/bin/test -f /storage/.firstAmbariSetupDone.txt',
       unless => 'cmp /storage/pg_hba.conf /var/lib/pgsql/data/pg_hba.conf'
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
       ensure => running,
     }
   
   ###########################################
   # Ambari Accumulo User creation
   ###########################################
      
     file { '/storage/':
       ensure => 'directory',
       owner   => 'root',
       group   => 'root',
       mode    => '0755'
     }
   
     file { '/storage/createKoverseAccumuloUser.txt':
       ensure  => present,
       owner   => 'root',
       group   => 'root',
       mode    => '0644',
       content => template('profile/hdp/createKoverseAccumuloUser.txt.erb')
     }
   
     exec { 'createKoverseAccumuloUser':
       command => 'cat /storage/createKoverseAccumuloUser.txt | accumulo shell -u root -p password && touch /storage/.koverseAccumuloUserCreated.txt',
       creates => '/storage/.koverseAccumuloUserCreated.txt',
       onlyif => '/bin/test -f /storage/.rdyToCreateKoverseAccumuloUser.txt'
     }
   }
   
``vi datanode.pp``

.. code:: ruby

   class profile::hdp::datanode {
   
   ####################################
   # Create AJAX directories
   ####################################
   
     file { '/data01/usr':
       ensure => 'directory',
       owner  => 'root',
       group  => 'root',
       mode   => '0755'
     }

     file { '/data01/usr/hdp':
       ensure => 'directory',
       owner  => 'root',
       group  => 'root',
       mode   => '0755'
     }

     file { '/data01/usr/hdp/current':
       ensure => 'directory',
       owner  => 'root',
       group  => 'root',
       mode   => '0755'
     }
   
   ########################################
   # Install / Configure Ambari Agent
   ########################################

     class { 'profile::software::ambari_agent_hdp': }
   }

``vi zookeeper.pp``

.. code:: ruby

   class profile::hdp::zookeeper {
   
   ####################################
   # Install / Configure Ambari Agent
   ####################################
   
     class { 'profile::software::ambari_agent_hdp': }
   
   ####################################
   # Zookeeper Account login and su
   ###################################
   
     sudo::user_specification { master_su :
       user_list => ['ambari-qa','ams','infra-solr','zookeeper'],
       host_list => ['ALL'],
       runas     => 'ALL',
       cmnd      => ['/usr/bin/su'],
       passwd    => false
     }
   
     pam::access::rule { master_user_login :
       users   => ['ambari-qa','ams','infra-solr','zookeeper'],
       origins => ['ALL'],
       comment => 'User Access'
     }
   }

``chown puppet:puppet *.pp``

``chmod 644 *.pp``

6. Create ambari agent module.

``cd /etc/puppetlabs/code/environments/production/site/profile/manifests/software/``

``vi ambari_agent_hdp.pp``

.. code:: ruby

   class profile::software::ambari_agent_hdp {
   
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
       content => template('profile/software/ambari/ambari-agent-hdp.ini.erb'),
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

7. Create ambari agent hdp template file.

``cd /etc/puppetlabs/code/environments/production/site/profile/templates/software/ambari/``

``vi ambari-agent-hdp.ini.erb``

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
   hostname=<fqdn of hdpmaster>
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

``chown puppet:puppet ambari-agent-hdp.ini.erb``

``chmod 644 ambari-agent-hdp.ini.erb``

8. Create postgres template.

``cd /etc/puppetlabs/code/environments/production/site/profile/templates/``

``mkdir hdp/``

``chown puppet:puppet hdp/``

``chmod 755 hdp/``

``vi psql.conf.erb``

.. code:: ruby

   # PostgreSQL Client Authentication Configuration File
   # ===================================================
   #
   # Refer to the "Client Authentication" section in the PostgreSQL
   # documentation for a complete description of this file.  A short
   # synopsis follows.
   #
   # This file controls: which hosts are allowed to connect, how clients
   # are authenticated, which PostgreSQL user names they can use, which
   # databases they can access.  Records take one of these forms:
   #
   # local      DATABASE  USER  METHOD  [OPTIONS]
   # host       DATABASE  USER  ADDRESS  METHOD  [OPTIONS]
   # hostssl    DATABASE  USER  ADDRESS  METHOD  [OPTIONS]
   # hostnossl  DATABASE  USER  ADDRESS  METHOD  [OPTIONS]
   #
   # (The uppercase items must be replaced by actual values.)
   #
   # The first field is the connection type: "local" is a Unix-domain
   # socket, "host" is either a plain or SSL-encrypted TCP/IP socket,
   # "hostssl" is an SSL-encrypted TCP/IP socket, and "hostnossl" is a
   # plain TCP/IP socket.
   #
   # DATABASE can be "all", "sameuser", "samerole", "replication", a
   # database name, or a comma-separated list thereof. The "all"
   # keyword does not match "replication". Access to replication
   # must be enabled in a separate record (see example below).
   #
   # USER can be "all", a user name, a group name prefixed with "+", or a
   # comma-separated list thereof.  In both the DATABASE and USER fields
   # you can also write a file name prefixed with "@" to include names
   # from a separate file.
   #
   # ADDRESS specifies the set of hosts the record matches.  It can be a
   # host name, or it is made up of an IP address and a CIDR mask that is
   # an integer (between 0 and 32 (IPv4) or 128 (IPv6) inclusive) that
   # specifies the number of significant bits in the mask.  A host name
   # that starts with a dot (.) matches a suffix of the actual host name.
   # Alternatively, you can write an IP address and netmask in separate
   # columns to specify the set of hosts.  Instead of a CIDR-address, you
   # can write "samehost" to match any of the server's own IP addresses,
   # or "samenet" to match any address in any subnet that the server is
   # directly connected to.
   #
   # METHOD can be "trust", "reject", "md5", "password", "gss", "sspi",
   # "krb5", "ident", "peer", "pam", "ldap", "radius" or "cert".  Note that
   # "password" sends passwords in clear text; "md5" is preferred since
   # it sends encrypted passwords.
   #
   # OPTIONS are a set of options for the authentication in the format
   # NAME=VALUE.  The available options depend on the different
   # authentication methods -- refer to the "Client Authentication"
   # section in the documentation for a list of which options are
   # available for which authentication methods.
   #
   # Database and user names containing spaces, commas, quotes and other
   # special characters must be quoted.  Quoting one of the keywords
   # "all", "sameuser", "samerole" or "replication" makes the name lose
   # its special character, and just match a database or username with
   # that name.
   #
   # This file is read on server startup and when the postmaster receives
   # a SIGHUP signal.  If you edit the file on a running system, you have
   # to SIGHUP the postmaster for the changes to take effect.  You can
   # use "pg_ctl reload" to do that.
   
   # Put your actual configuration here
   # ----------------------------------
   #
   # If you want to allow non-local connections, you need to add more
   # "host" records.  In that case you will also need to make PostgreSQL
   # listen on a non-local interface via the listen_addresses
   # configuration parameter, or via the -i or -h command line switches.
   
   
   
   # TYPE  DATABASE        USER            ADDRESS                 METHOD
   
   # "local" is for Unix domain socket connections only
   local   all   postgres                                     peer
   # IPv4 local connections:
   host    all   postgres             127.0.0.1/32            ident
   # IPv6 local connections:
   host    all   postgres             ::1/128                 ident
   # Allow replication connections from localhost, by a user with the
   # replication privilege.
   #local   replication     postgres                                peer
   #host    replication     postgres        127.0.0.1/32            ident
   #host    replication     postgres        ::1/128                 ident
   
   local  all  ambari,mapred,hive,rangeradmin,oozie,druid,koverse md5
   host  all   ambari,mapred 0.0.0.0/0  md5
   host  all   ambari,mapred ::/0 md5
   host  all   hive,rangeradmin,rangerkms,oozie,druid,koverse 0.0.0.0/0 trust
   
9. Create createKoverseAccumuloUser template.

``vi createKoverseAccumuloUser.txt.erb``

.. code:: ruby

   createuser koverse
   secret
   secret
   grant -s System.CREATE_TABLE -u koverse
   grant -s System.DROP_TABLE -u koverse
   grant -s System.ALTER_TABLE -u koverse
   grant -s System.SYSTEM -u koverse
   exit

10. Assign roles to instances.

``cd /etc/puppetlabs/code/environments/production/manifests/``

``vi site.pp`` and add your instances to the bottom to match your environments

.. code:: ruby

   node default {
   }
   node <hostname of hdpmaster> {
     include role::hdp::master
   }
   node <hostname of datanode> {
     include role::hdp::datanode
   }
   node <hostname of zookeeper> {
     include role::hdp::zookeeper
   }

11. Log into hdpmaster instance and run ``puppet agent -t``. Ensure you get a clean puppet run and type ``ambari-server status`` to ensure ambari-server is running.

.. note::
   At this point you can either log into all instances in the hdp cluster and run ``puppet agent -t`` or wait 30 minutes for all instances to auto run puppet

