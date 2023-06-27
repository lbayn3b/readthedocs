DHCP Configuration
========================

.. code-block:: bash
  :linenos:
  
  cd /var/simp/environments/production/rsync/RedHat/Global/dhcpd
  vim dhcpd.conf

.. code-block:: ruby   
  :linenos:
  :emphasize-lines: 14, 30, 32, 33, 35, 36, 45, 46, 47

  allow booting;
  allow bootp;
  ddns-update-style interim;

  option space pxelinux;
  option pxelinux.magic code 208 = string;
  option pxelinux.configfile code 209 = text;
  option pxelinux.pathprefix code 210 = text;
  option pxelinux.reboottime code 211 = unsigned integer 32;
  option architecture-type code 93 = unsigned integer 16;

  class "pxeclients" {
    match if substring(option vendor-class-identifier, 0, 9) = "PXEClient";
    next-server                           10.0.0.2;  ###set value per your system requirements###

    # The appropriate value to use for the default UEFI PXEboot file
    # below depends upon the OS and whether secure boot is enabled:
    #   CentOS 7 (grub2) normal UEFI boot       -->  "linux-install/efi/grubx64.efi";
    #   CentOS 7 (grub2) secure UEFI boot       -->  "linux-install/efi/shim.efi";
    #   CentOS 6 (legacy grub) normal UEFI boot -->  "linux-install/efi/grub.efi";
    #   (There is no CentOS 6 support for secure boot)
    #
    if option architecture-type = 00:07 {
      filename    "linux-install/efi/grubx64.efi";
    } else {
      filename    "linux-install/pxelinux.0";
    }
  }

  subnet 10.0.0.0 netmask 255.255.255.0 {    ###set value per your system requirements###

    option routers                        10.0.0.254;  ###set value per your system requirements###
    option subnet-mask                    255.255.255.0;  ###set value per your system requirements###

    option domain-name                    "your.domain";  ###set value per your system requirements###
    option domain-name-servers            10.0.0.1;  ###set value per your system requirements###

    option time-offset                    -0;

    default-lease-time                    21600;
    max-lease-time                        43200;

    # We explicitly list our hosts to restrict the hosts that can access our
    # network.
    host ns { ###set value per your system requirements###
      hardware ethernet 00:AA:BB:CC:DD:EE; ###set value per your system requirements###
      fixed-address 10.0.0.1;  ###set value per your system requirements###
    }
  }


.. code-block:: ruby
  :linenos:
  :caption: Updated sections of the dhcp.conf file
  :emphasize-lines: 14, 30, 32, 33, 35, 36, 45, 46, 47, 50, 51, 52

  allow booting;
  allow bootp;
  ddns-update-style interim;

  option space pxelinux;
  option pxelinux.magic code 208 = string;
  option pxelinux.configfile code 209 = text;
  option pxelinux.pathprefix code 210 = text;
  option pxelinux.reboottime code 211 = unsigned integer 32;
  option architecture-type code 93 = unsigned integer 16;

  class "pxeclients" {
    match if substring(option vendor-class-identifier, 0, 9) = "PXEClient";
    next-server                           10.10.60.130;

    if option architecture-type = 00:07 {
      # UEFI boot
      # The appropriate value to use for the default UEFI PXEboot file
      # below depends upon the OS and whether secure boot is enabled:
      #   Normal UEFI boot --> "linux-install/efi/grubx64.efi"
      #   Secure UEFI boot --> "linux-install/efi/shim.efi"
      #
      filename    "linux-install/efi/grubx64.efi";
    } else {
      # Legacy BIOS boot
      filename    "linux-install/pxelinux.0";
    }
  }

  subnet 10.10.60.0 netmask 255.255.255.0 {

    option routers                        10.10.60.254;
    option subnet-mask                    255.255.255.0;

    option domain-name                    "dev.net";
    option domain-name-servers            10.10.60.130;

    option time-offset                    -0;

    default-lease-time                    21600;
    max-lease-time                        43200;

    # We explicitly list our hosts to restrict the hosts that can access our
    # network.
    host puppet {
      hardware ethernet 52:54:00:38:bc:7c;
      fixed-address 10.10.60.130;
    }

    host dev02 {  ###set value per your system requirements###
      hardware ethernet 52:54:00:5f:63:38;  ###set value per your system requirements###
      fixed-address 10.10.60.131;  ###set value per your system requirements###
   }
  }

1. cd /etc/puppetlabs/code/environments/production/data/hosts

2. vi #puppet server host name#.yaml

.. code-block:: ruby

    classes:
      - 'simp::server::yum'
      - 'simp::server'
      - 'simp::puppetdb'
      - 'dhcp'  ###add this line###
    
    # Add these lines
    ds389::install::dnf_module: 389-ds
    ds389::install::dnf_stream: '1.4'
    ds389::install::dnf_enable_only: true
5. puppet agent -t
