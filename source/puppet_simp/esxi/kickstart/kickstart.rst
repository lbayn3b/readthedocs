Kickstart Configuration
========================

1. Stand up a new VM or bare metal server

2. Pause on boot to get the MAC address

3. Go back into puppet server

4. cd /var/simp/environments/production/rsync/RedHat/Global/dhcpd

5. vi dhcpd.conf

6. Add mac address to the end of the file    

.. code-block:: ruby   
  
    # We explicitly list our hosts to restrict the hosts that can access our
    # network.
     host ns {  ###set value per your system requirements###
       hardware ethernet 00:AA:BB:CC:DD:EE;  ###set value per your system requirements###
       fixed-address 10.0.0.1;  ###set value per your system requirements###
     }
    host host {  ###set value per your system requirements###
      hardware ethernet 00:AA:BB:CC:DD:EE;  ###set value per your system requirements###
      fixed-address 10.0.0.1;  ###set value per your system requirements###
     } 
    }

7. cd /var/simp/environments/production/rsync/RedHat/8/bind_dns/default/named/var/named/forward

8. vi yourdomain.db 

9. Add your new system to the file

10. cd /var/simp/environments/production/rsync/RedHat/8/bind_dns/default/named/var/named/reverse

11. vi yoursubnet.db

12. Add your new system

13. Run puppet agent -t

14. Go back to your new system and resume boot

15. Go back into puppet server   

16. cd /var/simp/environments/production/FakeCA

17. vi togen

18. Add FQDN

19. run ./gencerts_nopass.sh

20. On Rhel8 - had to also do puppetserver ca sign --certname <client> on the host after 1 failed run from client
