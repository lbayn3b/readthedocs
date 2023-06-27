Client Administration
=======================

1. boot your VM and pause on boot to grab MAC address

2. vi /var/simp/environments//production/rsync/CentOS/Global/dhcpd/dhcpd.conf

3. add the following to file

  .. code-block:: ruby
  
    host <your host here> {  ###set value per your system requirements###
    hardware ethernet AA:BB:CC:DD:EE:FF;  ###set value per your system requirements###
    fixed-address 0.0.0.0;  ###set value per your system requirements###
   } 


4. vi /var/simp/environments//production/rsync/CentOS/7/bind_dns/default/named/var/named/forward/<your.domain.db>

5. add forward entry for your new host

6. vi /var/simp/environments//production/rsync/CentOS/7/bind_dns/default/named/var/named/reverse/<your.domain.db>

7. add reverse entry for you new host

8. puppet agent -t 

9. continue pxe boot of VM

10. cd /var/simp/environments/production/FakeCA/

11. vi togen

12. input fqdn (one per line)

13. save file  

14. run ./gencerts_nopass.sh