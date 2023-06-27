Make rhel8 go faster
==============================
1. vi /etc/puppetlabs/code/environments/production/data/hosts/<yourhost>.yaml
  Make this match: 
  .. code-block::ruby
    # Edit this:
    iptables::use_firewalld: false # Edit this one 

  Add this to the bottom: 
  .. code-block::ruby
    ############ TESTING TO SPEED UP RUNS ####################
    stunnel::purge_instance_resources: false
  
    simp_firewalld::enable: false

2. maybe rkhunter?
  yum remove -y rkhunter
  rm -rf /var/lib/rkhunter /usr/share/rkhunter

  
