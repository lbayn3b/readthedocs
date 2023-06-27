Update the Puppet Profile
========================

.. code-block:: bash
  :linenos:
  
  cd /etc/puppetlabs/code/environments/production/data/hosts
  vim #puppet server host name#.yaml
  
.. code-block:: ruby
  :linenos:
  :emphasize-lines: 6,8,9,10
  
  simp::classes:
  - simp_ds389::instances::accounts
  - simp::server::yum
  - simp_grub
  - simp::server
  - dhcp

  ds389::install::dnf_module: 389-ds
  ds389::install::dnf_stream: '1.4'
  ds389::install::dnf_enable_only: true

.. code-block:: bash
  
  puppet agent -t
