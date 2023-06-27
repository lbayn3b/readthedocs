Pupclient Configuration
===========================

Encode BOOTPASS

.. code-block:: bash
  
  grub2-mkpasswd-pbkdf2

Encode ROOTPASS

.. code-block:: bash
    
  # Replace "password" with the password to be encoded
  /opt/puppetlabs/pdk/private/ruby/2.7.7/bin/ruby -r 'digest/sha2' -e 'puts "password".crypt("$6$" + rand(36**8).to_s(36))'


.. code-block:: bash

  cd /var/www/ks
  vim pupclient_x86_64.cfg

| Replace all #BOOTPASS# with value encoded above
| Replace all #ROOTPASS# with value encoded above
| Replace all #KSSERVER# with ip of kickstart server
| Replace all #YUMSERVER# with IP of puppet server
| Replace all #LINUXDIST# with RedHat   

.. code-block:: ruby
  :linenos:
  :emphasize-lines: 36, 51, 60, 61, 69, 81
  
  #
  # Use the following Ruby code to generate your rootpw hash:
  #   ruby -r 'digest/sha2' -e 'puts "password".crypt("$6$" + rand(36**8).to_s(36))'
  #
  # Use the following command to generate your grub password hash:
  #   grub2-mkpasswd-pbkdf2
  #
  # Replace the following strings in this file:
  #
  #     #BOOTPASS#  - Your hashed bootloader password
  #     #ROOTPASS#  - Your hashed root password
  #     #KSSERVER#  - The IP address of your Kickstart server
  #     #YUMSERVER# - The IP address of your YUM server
  #     #LINUXDIST# - The LINUX Distribution you are kickstarting
  #                 - Current CASE SENSITIVE options: RedHat CentOS
  #
  # This kickstart file was tested with a CentOS 8.4 iso.
  #
  # On some EL versions (notably 7.0-7.4), anaconda had a known issue, where
  # installation images did not support FIPS mode (fips=1) when the kickstart file
  # (this file) is loaded from an HTTPS source.
  #
  # Details:
  #
  #   - https://access.redhat.com/errata/RHBA-2018:0947
  #   - https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/7.5_release_notes
  #   - https://bugzilla.redhat.com/show_bug.cgi?id=1341280
  #   - https://groups.google.com/forum/?fromgroups#!topic/simp-announce/3pBQDZl1OVc
  #
  # If this affects your OS, remove the `fips=1 ` string from the bootloader
  # line's `--append` argument below (this will not affect the FIPS Mode of the
  # final system):
  bootloader --location=mbr --append="fips=1 console=ttyS1,57600 console=tty1" --iscrypted --password=#BOOTPASS#
  ## Remove the `--location=mbr` option from the above bootloader line if booting UEFI
  
  rootpw --iscrypted #ROOTPASS#
  firewall --enabled --ssh
  firstboot --disable
  logging --level=info
  selinux --enforcing
  
  text
  zerombr
  clearpart --none --initlabel
  %include /tmp/part-include
  skipx
  %include /tmp/repo-include
  
  keyboard us
  lang en_US
  url --noverifyssl --url=https://#YUMSERVER#/yum/#LINUXDIST#/8/x86_64
  
  module --name=python36 --stream=3.6
  module --name=perl --stream=5.26
  module --name=perl-IO-Socket-SSL --stream=2.066
  module --name=perl-libwww-perl --stream=6.34
  
  ...

  ksserver="#KSSERVER#"
  yumserver="#YUMSERVER#"
  
  # Fetch disk and repo detection scripts from kickstart server and run them
  # to create the files used by the'%include /tmp/*-include' above.
  wget --no-check-certificate -O /tmp/diskdetect.sh https://$ksserver/ks/diskdetect.sh
  /bin/sh /tmp/diskdetect.sh
  
  wget --no-check-certificate -O /tmp/repodetect.sh https://$ksserver/ks/repodetect.sh
  /bin/sh /tmp/repodetect.sh '8' "$yumserver" '#LINUXDIST#'
  
  %end
  
  ...

  if $FIPS; then
    /usr/bin/fips-mode-setup --enable
  else
    /usr/bin/fips-mode-setup --disable
  fi
  
  ksserver="#KSSERVER#"
  
  echo "Welcome to SIMP!  If this is firstboot, SIMP bootstrap is scheduled to run.
  If this host is not autosigned by Puppet, sign your Puppet certs to begin bootstrap.
  Otherwise, it should already be running! Tail /root/puppet.bootstrap.log for details.
  Wait for completion and reboot.
  
  To remove this message, delete /root/.bootstrap_msg" > /root/.bootstrap_msg
  sed -i "2i if [ -f /root/.bootstrap_msg ]\nthen\n  cat /root/.bootstrap_msg\nfi" /root/.bashrc
  source /root/.bashrc
  
  # Enable wait-online
  systemctl enable NetworkManager-wait-online
  
  # Enable the firstboot bootstrapping script.
  wget --no-check-certificate \
    -O /etc/systemd/system/simp_client_bootstrap.service \
    https://$ksserver/ks/simp_client_bootstrap.service
  chmod 644 /etc/systemd/system/simp_client_bootstrap.service
  wget --no-check-certificate \
    -O /usr/local/sbin/bootstrap_simp_client \
    https://$ksserver/ks/bootstrap_simp_client
  chmod 700  /usr/local/sbin/bootstrap_simp_client
  
  systemctl enable simp_client_bootstrap.service
  %end
  