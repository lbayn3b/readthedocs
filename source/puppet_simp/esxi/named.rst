DNS Configuration
=====================

1. cd /var/simp/environments/production/rsync/CentOS/8/bind_dns/default/named/etc
2. vi named.conf ``ensure the following fields are correct``

.. code-block:: ruby

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

3. cd /var/simp/environments/production/rsync/CentOS/7/bind_dns/default/named/etc/zones

4. cp your.domain <insert.yourdomain>

5. chown root:named insert.yourdomain

6. chmod 640 insert.yourdomain   

7. vi insert.yourdomain

.. code-block:: ruby

    zone "us-gov-west-1.compute.internal" IN {
        type master;
        file "forward/us-gov-west-1.compute.internal.db";
    };

    zone "0.10.10.in-addr.arpa" IN {
        type master;
        file "reverse/0.10.10.db";
    };

    zone "10.10.10.in-addr.arpa" IN {
        type master;
        file "reverse/10.10.10.db";
    };


8. cd /var/simp/environments/production/rsync/CentOS/8/bind_dns/default/named/var/named/forward

9. cp your.domain.db <insert.yourdomain.db>

10. chown root:named insert.yourdomain.db

11. chmod 640 insert.yourdomain.db

12. vi insert.yourdomain.db


.. code-block:: ruby
    
    $TTL    86400
    your.domain                   IN SOA <ns>.your.domain. root.your.domain. (   ###set value per your system requirements###
                                                 2008072900
                                                 3H              ; refresh
                                                 15M             ; retry
                                                 1W              ; expiry
                                                 1D )            ; minimum
                     IN NS               <ns>.your.domain. ###set value per your system requirements###
    <ns>           IN  A      10.10.0.1  ###set value per your system requirements###


13. cd /var/simp/environments/production/rsync/CentOS/8/bind_dns/default/named/var/named/reverse

14. cp 0.0.10.db <rename as your subnet backwards.db> (for example 192.168.0.2 would be 0.168.192.db)

15. chown root:named insert.subnet.db

16. chmod 640 insert.subnet.db

17. vi insert.subnet.db


.. code-block:: bash
    
    $TTL    86400
    @                     IN SOA your.domain. ns.your.domain. (  ###set value per your system requirements###
                                                 2008072900
                                                 1h              ; refresh
                                                 15m             ; retry
                                                 1w              ; expiry
                                                 1d )            ; minimum
                     IN NS   <ns>.your.domain.  ###set value per your system requirements###
    1        IN      PTR     <ns>.your.domain.  ###set value per your system requirements### (1 meaning IP)

18. save insert.subnet.db

19. run puppet agent -t \-\-tagged named
