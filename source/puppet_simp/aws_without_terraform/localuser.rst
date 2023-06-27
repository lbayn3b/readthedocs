Local User
==========

.. note::
   This must be done prior to rebooting to ensure you don't get locked out of your ec2 instance

1. ``cd /etc/puppetlabs/code/environments/production/site/profile/manifests/``

2. ``vi local_user.pp``

.. code-block:: ruby

   class profile::local_user {

     sudo::user_specification { 'default_<local_user>':
       user_list => ['<local_user>'],
       runas     => 'root',
       cmnd      => ['/bin/su root', '/bin/su - root', 'ALL'],
       passwd    => false,
     }

     pam::access::rule { 'allow_<local_user>':
       users   => ['<local_user>'],
       origins => ['ALL'],
       comment => 'The local user, used to remotely login to the system in the case of a lockout.'
     }

     file { '/root/scripts':
       ensure => 'directory',
       owner  => 'root',
       group  => 'root',
       mode   => '0755',
     }

     file { '/root/scripts/local_user.sh':
       ensure => file,
       owner  => 'root',
       group  => 'root',
       mode   => '0700',
       content => template('profile/admin/local_user.sh.erb')
     }

     exec { 'local_user':
       require => File["/root/scripts/local_user.sh"],
       unless  => ['test -f /etc/ssh/local_keys/maintuser'],
       command => 'sh /root/scripts/local_user.sh',
       user    => 'root',
       group   => 'root',
     }
   }

3. ``chown puppet:puppet local_user.pp``

4. ``chomd 644 local_user.pp``

5. ``cd /etc/puppetlabs/code/environments/production/site/profile/``

6. ``mkdir templates/``

7. ``chown puppet:puppet templates/``

8. ``chmod 755 templates/``

9. ``cd templates/``

10. ``mkdir admin/``

11. ``chown puppet:puppet admin/``

12. ``chmod 755 admin/``

13. ``cd admin/``

14. ``vi local_user.sh.erb``

.. code-block:: ruby
   
   #!/bin/bash

   mkdir -p /etc/ssh/local_keys
   chmod 755 /etc/ssh/local_keys
   cp /home/<local_user>/.ssh/authorized_keys /etc/ssh/local_keys/maintuser

15. ``chown puppet:puppet local_user.sh.erb``

16. ``chmod 644 local_user.sh.erb``

17. ``puppet agent -t``

.. note::
  You should see puppet change configurations on the puppetserver to allow your local_user to login and run sudo commands

18. Once the puppet run is complate ``su <local_user>``

19. If successful ``reboot``

.. note::
  If you are unable to log in after the reboot, a step was missed in this process and you must re-deploy the ec2 instance and try again.
