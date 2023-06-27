zones
======

Configure the dns zones file

.. code-block:: bash
  :linenos:

  cd /var/simp/environments/production/rsync/CentOS/7/bind_dns/default/named/etc/zones
  cp -p your.domain <insert.yourdomain>
  vim <insert.yourdomain>

.. note::
  The -p flag will preserve the permissions of the original file. The following commands will set the ownership and permissions.
  
  .. code-block:: bash
    :linenos:

    chown root:named insert.yourdomain
    chmod 640 insert.yourdomain
    
.. code-block:: ruby
  :caption: File: <insert.yourdomain>
  :emphasize-lines: 1, 3, 6, 8
  :linenos:

    zone "your.domain" IN { ###Replace your.domain###
    type master;
    file "forward/your.domain.db"; ###Replace your.domain###
  };

  zone "0.0.10.in-addr.arpa" IN { ###Replace 0.0.10 with octets 3, 2, and 1 of the subnet. ex 192.168.0.1 -> 0.168.192###
    type master;
    file "reverse/0.0.10.db"; { ###Replace 0.0.10 with octets 3, 2, and 1 of the subnet. ex 192.168.0.1 -> 0.168.192###
  };


.. code-block:: ruby
  :caption: Example of an updated file.
  :emphasize-lines: 2, 4, 7, 9
  :linenos:

  ## your.domain = dev.net ip = 10.10.60.130
  zone "dev.net" IN { ###Replace your.domain###
    type master;
    file "forward/dev.net.db"; ###Replace your.domain###
  };

  zone "60.10.10.in-addr.arpa" IN { ###Replace 0.0.10 with octets 3, 2, and 1 of the subnet. ex 192.168.0.1 -> 0.168.192###
    type master;
    file "reverse/60.10.10.db"; { ###Replace 0.0.10 with octets 3, 2, and 1 of the subnet. ex 192.168.0.1 -> 0.168.192###
  };