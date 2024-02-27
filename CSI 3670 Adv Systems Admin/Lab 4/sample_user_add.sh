#!/bin/bash

users=( "tempuser1" "tempuser2" "tempuser3" )
userpw="temp12345" 

ldif_file="/tmp/bulk_user.ldif"
dn="cn=admin,dc=csi3670,dc=local"
adminpw="password"   ### REPLACE THIS WITH YOUR ADMIN PASSWORD

i=0
for user in "${users[@]}"; do
  touch $ldif_file

  uid=$(( $i + 1000 ))
  gid=$(( $i + 1000 ))

  echo $uid $gid

  echo "Adding $user to LDAP directory with UID [$uid] and GID [$gid]"

  echo "dn: uid=$user,ou=People,dc=csi3670,dc=local" >> $ldif_file
  echo "objectClass: inetOrgPerson" >> $ldif_file
  echo "objectClass: posixAccount" >> $ldif_file
  echo "objectClass: shadowAccount" >> $ldif_file
  echo "uid: $user" >> $ldif_file
  echo "sn: 1" >> $ldif_file
  echo "givenName: User" >> $ldif_file
  echo "cn: User $i" >> $ldif_file
  echo "displayName: User $i" >> $ldif_file
  echo "uidNumber: $uid" >> $ldif_file
  echo "gidNumber: $gid" >> $ldif_file
  echo "userPassword: $userpw" >> $ldif_file
  echo "gecos: User $i" >> $ldif_file
  echo "loginShell: /bin/bash" >> $ldif_file
  echo "homeDirectory: /home/$user" >> $ldif_file

  cat $ldif_file

  # Add user
  ldapadd -x -D $dn -w $adminpw -a -f $ldif_file

  # Clean up
  rm $ldif_file
  i=$(( $i + 1 ))

done

