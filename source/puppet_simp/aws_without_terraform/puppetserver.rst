Puppet / SIMP Server
====================

.. note::
   This is typically done if you are not standing up the underlying infrastructure

1. Log into ec2 instance with credentials provided by infrastructure team.


2. Configure .repo file at /etc/yum.repos.d/ (the following is the public repo, point this file to your internal repo if in a disconnected environment)::

    vi /etc/yum.repos.d/simp.repo

.. code-block:: ruby

  [simp-project_6_X]
  name=simp-project_6_X
  baseurl=https://packagecloud.io/simp-project/6_X/el/$releasever/$basearch
  gpgcheck=1
  enabled=1
  gpgkey=https://raw.githubusercontent.com/NationalSecurityAgency/SIMP/master/GPGKEYS/RPM-GPG-KEY-SIMP
         https://download.simp-project.com/simp/GPGKEYS/RPM-GPG-KEY-SIMP-6
  sslverify=1
  sslcacert=/etc/pki/tls/certs/ca-bundle.crt
  metadata_expire=300

  [simp-project_6_X_dependencies]
  name=simp-project_6_X_dependencies
  baseurl=https://packagecloud.io/simp-project/6_X_Dependencies/el/$releasever/$basearch
  gpgcheck=1
  enabled=1
  gpgkey=https://raw.githubusercontent.com/NationalSecurityAgency/SIMP/master/GPGKEYS/RPM-GPG-KEY-SIMP
         https://download.simp-project.com/simp/GPGKEYS/RPM-GPG-KEY-SIMP-6
         https://yum.puppet.com/RPM-GPG-KEY-puppetlabs
         https://yum.puppet.com/RPM-GPG-KEY-puppet
         https://apt.postgresql.org/pub/repos/yum/RPM-GPG-KEY-PGDG-96
         https://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-$releasever
  sslverify=1
  sslcacert=/etc/pki/tls/certs/ca-bundle.crt
  metadata_expire=300

3. Install ``puppetserver``

       yum install -y puppetserver

4. Install ``simp``

       yum install -y simp

5. Install ``simp-extras`` (optional)

       yum install -y simp-extras

6. Type ``simp config``::

     Ready to start questionnaire? yes
     Fill out questionnaire based on your environment

7. Type ``simp bootsrap``
