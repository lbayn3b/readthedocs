reverse
=======

Update the db file for dns reverse lookup.

.. code-block:: bash
  :linenos:
  cd /var/simp/environments/production/rsync/CentOS/8/bind_dns/default/named/var/named/reverse
  cp -p 0.0.10.db <rename as your subnet backwards.db> # (for example 192.168.0.2 would be 0.168.192.db)
  vim <rename as your subnet backwards.db>

.. note::
  The -p flag will preserve the permissions of the original file. The following commands will set the ownership and permissions.
  
  .. code-block:: bash
    :linenos:

    chown root:named <rename as your subnet backwards.db>
    chmod 640 <rename as your subnet backwards.db>

.. code-block:: ruby
  :caption: File: <rename as your subnet backwards.db>.db
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
  :emphasize-lines: 2, 8, 10, 11
    
    $TTL    86400
    @               IN SOA  example.com. puppet.lbdev.net. (
                                            2008072900
                                            1h              ; refresh
                                            15m             ; retry
                                            1w              ; expiry
                                            1d )            ; minimum
                    IN NS   puppet.lbdev.net.
    130     IN      PTR     puppet.lbdev.net.
    131     IN      PTR     lbdev02.lbdev.net.