TFTPBOOT Configuration
========================

.. code-block:: bash
  :linenos:
  
  cd /etc/puppetlabs/code/environments/production/site/profile/manifests
  vim tftpboot.pp

.. code-block:: ruby   
  :linenos:
  :emphasize-lines: 8,9,10,11,25,26,27,28,38,39,47,48 

  class profile::tftpboot {
    include '::tftpboot'
    
    #--------
    # BIOS MODE MODEL EXAMPLES
    
    # for CentOS/RedHat 7 Legacy/BIOS boot
    tftpboot::linux_model { 'el8_x86_64':
      kernel => 'redhat-8.7-x86_64/vmlinuz',
      initrd => 'redhat-8.7-x86_64/initrd.img',
      ks => "https://10.10.60.130/ks/pupclient_x86_64.cfg",
      extra => "inst.noverifyssl ksdevice=bootif simp_disk_crypt\nipappend 2"
    }
    
    #------
    # UEFI MODE MODEL EXAMPLES
    
    # NOTE UEFI boot uses the linux_model_efi module and has different
    # 'extra' arguments. You also would use a different kickstart file
    # because the bootloader command within the kickstart file is
    # different. Read the instructions in the default pupclient_x86_64.cfg
    # file and make sure you have the correct bootloader line.
    #
    # For CentOS/RedHat 7 UEFI boot
    tftpboot::linux_model_efi { 'el8_x86_64_efi':
      kernel => 'redhat-8.7-x86_64/vmlinuz',
      initrd => 'redhat-8.7-x86_64/initrd.img',
      ks => "https://10.10.60.130/ks/pupclient_x86_64_efi_el8.cfg",
      extra => "inst.noverifyssl simp_disk_crypt"
    }
    
    #--------
    # DEFAULT HOST BOOT CONFIGURATION EXAMPLES
    
    # If desired, create defaults boot configuration for BIOS and UEFI.
    # Note that the name of the default UEFI configuration file needs
    # to be 'grub.cfg'.
    tftpboot::assign_host { 'default': model => 'el8_x86_64' }
    tftpboot::assign_host_efi { 'grub.cfg': model => 'el8_x86_64_efi' }
    
    #--------
    # HOST BOOT CONFIGURATION ASSIGNMENT EXAMPLES
    
    # For each system define what module you want to use by pointing
    # its MAC address to the appropriate model. Note that the MAC
    # address is preceded by '01-''.
    tftpboot::assign_host { '01-aa-ab-ac-1d-05-11': model => 'el8_x86_64' }
    tftpboot::assign_host_efi { '01-aa-bb-cc-dd-00-11': model => 'el8_x86_64_efi' }
    }

.. code-block:: bash
  :linenos:

  chown puppet:puppet tftpboot.pp
  chmod 644 tftpboot.pp   
  cd /etc/puppetlabs/code/environments/production/data/hosts
  vim puppet.yaml

.. code-block:: ruby
  :linenos:
  :emphasize-lines: 6,7

  classes:
    - 'simp::server::yum'
    - 'simp::server'
    - 'simp::puppetdb'
    - 'dhcp' 
    - 'simp::server::kickstart'  ###add this line###
    - 'profile::tftpboot'  ###add this line###  

.. code-block:: bash

  puppet agent -t --tags tftpboot
