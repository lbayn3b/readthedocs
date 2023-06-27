Step 1
=====================

1. mkdir /root/ldifs

2. cp -R /usr/share/simp/ldifs/* /root/ldifs/

3. cd /root/ldifs

4. sed -i 's/dc=your,dc=domain/<dc=your,dc=domain>/g' \*.ldif   ###set value per your system requirements###

5. vi addUser.sh

6. enter script on next page 

7. after creating the script run sh addUser.sh