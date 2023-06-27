named.conf
=====================

Update named.conf.

.. code-block:: bash
  :linenos:

  cd /var/simp/environments/production/rsync/RedHat/8/bind_dns/default/named/etc
  vim named.conf

.. code-block:: ruby
    :linenos:
    :emphasize-lines: 1, 4, 18, 19, 21, 24

    FIX_YOUR_NAMED_CONFIG_PRIOR_TO_RUNNING ###remove this line###

    acl trusted_hosts {
      10.10.0.0/16;  ###set value per your system requirements###
    };

    options
    {
      version " ";
      query-source    port 53;
      query-source-v6 port 53;

      directory "/var/named";
      dump-file     "data/cache_dump.db";
      statistics-file   "data/named_stats.txt";
      memstatistics-file  "data/named_mem_stats.txt";

      allow-query { 10.10.0.0/16; }; ###set value per your system requirements###
      allow-recursion { 10.10.0.0/16; }; ###set value per your system requirements###
      allow-transfer { "none"; };
      forwarders { 10.10.0.2; }; ###set value per your system requirements###
    };

    include "/etc/zones/us-gov-west-1.compute.internal"; ###set value per your system requirements###

    #zone "higher.domain" IN {               
    #  type forward;                        
    #  forwarders { 10.0.1.4; 10.0.1.6; };   
    #};                                      

    #zone "." IN {                          
    #  type forward;                        
    #  forward only;                        
    #  forwarders { 10.0.1.4; 10.0.1.6; };  
    #};                                     

.. code-block:: ruby
    :linenos:
    :caption: Updated sections of an named.conf file
    :emphasize-lines: 2, 20, 21, 23, 26

    acl trusted_hosts {
      10.10.60.0/16;
    };
    
    options
    {
      version " ";
      query-source    port 53;
      query-source-v6 port 53;
      # The following option mitigates CVE-2019-6477
      # This issue was introduced in bind-9.11.4-9.P2
      # Comment out the line if an earlier version of bind is in use 
      keep-response-order { any; };
    
      directory "/var/named";
      dump-file     "data/cache_dump.db";
      statistics-file   "data/named_stats.txt";
      memstatistics-file  "data/named_mem_stats.txt";
    
      allow-query { 10.10.60.0/24; };
      allow-recursion { 10.10.60.0/24; };
      allow-transfer { "none"; };
      forwarders { 10.10.60.130; };
    };

    include "/etc/zones/dev.net";

    #zone "higher.domain" IN {               
    #  type forward;                        
    #  forwarders { 10.0.1.4; 10.0.1.6; };   
    #};                                      

    #zone "." IN {                          
    #  type forward;                        
    #  forward only;                        
    #  forwarders { 10.0.1.4; 10.0.1.6; };  
    #};     