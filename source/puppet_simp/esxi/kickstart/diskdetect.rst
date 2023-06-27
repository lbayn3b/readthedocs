Disk Detect Configuration
===========================

1. cd /var/www/ks

2. vi diskdetect.sh

for CENT7:

.. code-block:: bash

    if grep -q "simp_disk_swapvol=" /proc/cmdline; then
      simp_disk_swapvol='awk -F "simp_disk_swapvol=" '{print $2}' /proc/cmdline | cut -fi -d' '`
    else
      simp_disk_swapvol=5120  ###set value per your system requirements### 
    fi 
    if grep -q "simp_disk_rootvol=" /proc/cmdline; then
      simp_disk_rootvol='awk -F "simp_disk_rootvol=" '{print $2}' /proc/cmdline | cut -fl-d' '`
    else
      simo disk rootvol=12288 ###set value per your system requirements###
    fi 
    if grep -q "simp_disk_tmpvol=" /proc/cmdline; then
      simp_disk_tmpvol='awk -F "simp_disk_tmpvol=" '{print $2}' /proc/cmdline | cut -fi -d' '`
    else
      simp_disk_tmpvol=5120 ###set value per your system requirements###
    fi 
    if grep -q "simp_disk_homevol=" /proc/cmdline; then
      simp_disk_homevol='awk -F "simp_disk_homevol=" '{print $2}' /proc/cmdline | cut -fl -d' '`
    else
      simp_disk_homevol=5120 ###set value per your system requirements###
    fi 
    if grep -q "simp_disk_varvol=" /proc/cmdline; then
      simp_disk_varvol='awk -F "simp_disk_varvol=" '{print $2}' /proc/cmdline | cut -fl-d' '`
    else
      simp_disk_varvol=12288 ###set value per your system requirements###
    fi 
    if grep -q "simp_disk_varlogvol=" /proc/cmdline; then
      simp_disk_varlogvol='awk -F "simp_disk_varlogvol=" '{print $2}' /proc/cmdline | cut -fi -d' '`
    else
      simp_disk_varlogvol=5120 ###set value per your system requirements###
    fi 
    if grep -q "simp_disk_varlogauditvol=" /proc/cmdline; then
      simp_disk_varlogauditvol='awk -F "simp_disk_varlogauditvol=" '{print $2}' /proc/cmdline | cut -fl -d' '`
    else
      simp_disk_varlogauditvol=5120 ###set value per your system requirements###
    fi

    # This checks to see which disk should grow to fill the rest of the size if any is left over. This defaults 
    # to grow Varvol.

    if grep -q "simp_grow_vol=" /proc/cmdline; then
      simp_grow_vol='awk -F "simp_grow_vol=" '{print $2}' /proc/cmdline cut -fl-d' '`
    else
      simp_grow_vol='Varvol'  ###set value per your system requirements###

for CENT/RHEL7:
Edit the following portion of the file to match your requirements (size parameter)

.. code-block:: bash

  if [ "$simp_opt" != "prompt" ]; then
    cat << EOF >> /tmp/part-include
  volgroup VolGroup00 pv.01
  logvol swap --fstype=swap --name=SwapVol --vgname=VolGroup00 --size=8192
  logvol / --fstype=ext4 --name=RootVol --vgname=VolGroup00 --size=40960 --fsoptions=iversion
  logvol /tmp --fstype=ext4 --name=TmpVol --vgname=VolGroup00 --size=15360 --fsoptions=nosuid,noexec,nodev
  logvol /home --fstype=ext4 --name=HomeVol --vgname=VolGroup00 --size=15360 --fsoptions=nosuid,noexec,nodev,iversion
  logvol /var --fstype=ext4 --name=VarVol --vgname=VolGroup00 --size=40960 --grow
  logvol /var/log --fstype=ext4 --name=VarLogVol --vgname=VolGroup00 --size=15360 --fsoptions=nosuid,noexec,nodev
  logvol /var/log/audit --fstype=ext4 --name=VarLogAuditVol --vgname=VolGroup00 --size=15360 --fsoptions=nosuid,noexec,nodev
  EOF
  fi

