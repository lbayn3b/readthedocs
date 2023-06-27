Profile / Role Puppet Modules
=============================

1. ``cd /etc/puppetlabs/code/environments/production/``

2. ``mkdir site``

3. ``chown puppet:puppet site/``

4. ``chmod 755 site/``

5. ``cd site/``

6. ``puppet module generate <author>:profile``::

    answer questions to fit your environment

7. ``puppet module generate <author>:role``::
    
    answer questions to fit your environment

8. ``find . -type d -exec chmod 755 {} \;``

9. ``find . -type f -exec chmod 644 {} \;``
