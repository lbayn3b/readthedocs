User Setup
==========

1. ``mkdir /ldifs``

2. ``cp /usr/share/simp/ldisf/* /ldifs/``

3. ``cd /ldifs``

4. ``sed -i 's/dc=your,dc=domain/<your actual DN information>/g' *.ldif``

5. Use the ``slappasswd`` command to generate a password hash for a user.

6. ``vi /ldifs/add_user_with_password.ldif``

.. code:: ruby

    dn: cn=<username>,ou=Group,dc=your,dc=domain
    objectClass: posixGroup
    objectClass: top
    cn: <username>
    gidNumber: <Unique GID Number>
    description: "<Group Description>"

    dn: uid=<username>,ou=People,dc=your,dc=domain
    uid: <username>
    cn: <username>
    givenName: <First Name>
    sn: <Last Name>
    mail: <e-mail address>
    objectClass: inetOrgPerson
    objectClass: posixAccount
    objectClass: top
    objectClass: shadowAccount
    objectClass: ldapPublicKey
    shadowMax: 180
    shadowMin: 1
    shadowWarning: 7
    shadowLastChange: 10701
    sshPublicKey: <some SSH public key>
    loginShell: /bin/bash
    uidNumber: <some UID number above 1000>
    gidNumber: <GID number from above>
    homeDirectory: /home/<username>
    userPassword: <slappasswd generated SSHA hash>
    pwdReset: TRUE

7. Type the following, ensuring to change the DN information ``dc=your,dc=domain`` to your environment domain information::
     
  # ldapadd -Z -x -W -D "cn=LDAPAdmin,ou=People,dc=your,dc=domain" -f /ldifs/add_user_with_password.ldif

8. Add user to administrators group ``vi /ldifs/add_to_group.ldif``::

  dn: cn=administrators,ou=Group,dc=your,dc=domain
  changetype: modify
  delete: memberUid
  memberUid: <UID1>
  memberUid: <UID2>

9. Type the following, ensuring to change the DN information ``dc=your,dc=domain`` to your environment domain information::
     
  # ldapmodify -Z -x -W -D "cn=LDAPAdmin,ou=People,dc=your,dc=domain" -f /root/ldifs/del_from_group.ldif