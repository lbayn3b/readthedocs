Module Generate Configuration
==============================

.. code-block:: bash
  :linenos:
  
  cd /etc/puppetlabs/code/environments/production
  mkdir site
  chown puppet:puppet site
  chmod 755 site
  cd site
  yum localinstall /var/www/yum/SIMP/RedHat/8/x86_64/puppet-tools/Packages/p/pdk-2.7.1.0-1.el8.x86_64.rpm
  pdk new module
  #fill out questionnaire to create a module named profile
  #fill out questionnaire to create a module named role
  find . -type d -exec chmod 755 {} \\;
  find . -type f -exec chmod 644 {} \\;
  chown -R puppet: *    



