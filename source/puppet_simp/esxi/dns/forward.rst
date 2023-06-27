forward
=======

Update the db file for dns forwarding.

.. code-block:: bash
  :linenos:

  cd /var/simp/environments/production/rsync/CentOS/8/bind_dns/default/named/var/named/forward
  cp -p your.domain.db <insert.yourdomain.db>
  vim <insert.yourdomain.db>

.. note::
  The -p flag will preserve the permissions of the original file. The following commands will set the ownership and permissions.
  
  .. code-block:: bash
    :linenos:

    chown root:named insert.yourdomain.db
    chmod 640 insert.yourdomain.db

.. code-block:: ruby
  :caption: File: <insert.yourdomain>.db
  :emphasize-lines: 2, 8, 9
    
    $TTL    86400
    your.domain                   IN SOA <ns>.your.domain. root.your.domain. (   ###set value per your system requirements###
                                                 2008072900
                                                 3H              ; refresh
                                                 15M             ; retry
                                                 1W              ; expiry
                                                 1D )            ; minimum
                     IN NS               <ns>.your.domain. ###set value per your system requirements###
    <ns>           IN  A      10.10.0.1  ###set value per your system requirements###

.. code-block:: ruby
  :caption: Example of an updated file.
  :emphasize-lines: 2, 8, 10,11
    
    $TTL    86400
    lbdev.net.            IN SOA  puppet.lbdev.net. root.lbdev.net. (
                                            2008072900
                                            3H              ; refresh
                                            15M             ; retry
                                            1W              ; expiry
                                            1D )            ; minimum
                    IN NS           puppet.lbdev.net.

    puppet       IN  A       10.10.60.130
    lbdev02      IN  A       10.10.60.131