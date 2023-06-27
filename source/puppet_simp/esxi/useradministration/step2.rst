Step 2
=====================

.. code-block:: 
    #!/bin/bash

    set -e

    # variables used
    # firstName: hope you can tell
    # lastName: hope you can tell
    # ctr: is the user a contractor
    # admin: is the user an admin
    # serviceAccount: is this a service account
    # userName: holds the constructed user name

    # SET THIS AS A GLOBAL FOR THE SCRIPT
    domain=$(facter domain | sed 's/^/dc=/;s/[.]/,dc=/g')
    ldapString=$domain
    groupLdapString=",ou=Group$ldapString"
    userLdapString=",ou=People$ldapString"
    adminUser="cn=LDAPAdmin"
    adminUserLogin="$adminUser$userLdapString"
    initialUserPassword='{SSHA}CwTgsd7t5tNlo4U7QZIVG2Ob8kQNFJN0'

    # INITIALIZE VARIABLES
    userName=""
    userId=""
    groupId=""

    rootDir="${LDIF_MANAGEMENT_DIR:-/root/ldifs}"
    settingsFile="${rootDir}/.settings"
    uidDefault=1550
    gidDefault=1550
    svcUidDefault=2550
    svcGidDefault=2550
    standaloneGidDefault=3550


    function readSetting() {
        param="$1"
        defaultValue="$2"

        val=$(grep "^${1}=" $settingsFile | sed 's/^[^=]//')

        if [[ -z "$val" ]]; then
        echo "$param not set. Would you like to use the default of $defaultValue? (y/n)" >> /dev/stderr
        read response
        
        if [[ "$response" == "y" ]]; then
            val="$defaultValue"
        else
            echo "Enter the value to use" >> /dev/stderr
            read val
        fi
        fi

        echo "$val"
    }

    function setSetting() {
        param="$1"
        value="$2"
        #echo "Setting $param to $value"
        sed -i "/${param}/d" $settingsFile
        echo "${param}=${value}" >> $settingsFile
    }

    generateSSHKey() {
        echo "What user do you want to create an SSH key for?"
        read userName
        ssh-keygen -t rsa -f ./tmp_rsa -q -N ""
        echo "*********************************"
        echo "COPY THIS TEXT TO ~/.ssh/id_rsa"
        echo "YOU WILL NEVER SEE THIS AGAIN"
        echo "*********************************"
        cat tmp_rsa
        echo "*********************************"
        echo "COPY THIS TEXT TO ~/.ssh/id_rsa"
        echo "YOU WILL NEVER SEE THIS AGAIN"
        echo "*********************************"
        echo ""
        echo ""
        echo ""
        echo "*********************************"
        echo "COPY THIS TEXT TO ~/.ssh/id_rsa.pub"
        echo "YOU WILL NEVER SEE THIS AGAIN"
        echo "*********************************"
        tmpKey=$(cat tmp_rsa.pub)
        cat tmp_rsa.pub
        echo "*********************************"
        echo "COPY THIS TEXT TO ~/.ssh/id_rsa.pub"
        echo "YOU WILL NEVER SEE THIS AGAIN"
        echo "*********************************"
        echo ""
        echo ""
        echo ""
        # create a log of what you did
        echo "\"date\": \"$(date)\",\"action\": \"generateSSHKey\",\"attributes\": {\"name\":\"$userName\"}" >>ldifScript.log
        dsidm accounts -b "${domain}" user modify $userName add:nsSshPublicKey:"$tmpKey"
        rm -f tmp_rsa
        rm -f tmp_rsa.pub

    }

    createUserInteral() {
    # create the user
    dsidm accounts -b "$domain" user create --uid $userName --cn "$firstName $lastName" --displayName "$userName" --uidNumber $userId --gidNumber $groupId --homeDirectory /home/$userName
    
    # set the initial password
    dsidm accounts -b "$domain" user modify $userName add:userPassword:$initialUserPassword

    # create the user group
    dsidm accounts -b "$domain" posixgroup create --cn $userName --gidNumber $groupId

    # add user to their group
    dsidm accounts -b "$domain" group add_member $userName "cn=$userName$groupLdapString"
    }

    addServiceUser() {
        echo Please enter the name of the service
        echo I will add the .svc to the end
        read firstName
        lastName=".svc"
        userName="$firstName$lastName"
        userId=$(readSetting svcuid ${svcUidDefault})
        groupId=$(readSetting svcgid ${svcGidDefault})
        # create a log of what you did
        echo "\"date\": \"$(date)\",\"action\": \"addServiceUser\",\"attributes\": {\"gid\": $groupId,\"name\":\"$userName\",\"uid\": $userId}" >>ldifScript.log
        createUserInteral
        setSetting svcuid $((userId + 1))
        setSetting svcgid $((groupId + 1))
    }

    addUser() {
        echo Please enter the first name
        read firstName
        echo Please enter the last name
        read lastName
        echo Contractor? y or n
        read ctr
        echo Adminstrator? y or n
        read admin
        userName="$firstName.$lastName"
        if [ "$ctr" = "y" ] || [ "$ctr" = "yes" ]; then
            userName+=".ctr"
        fi
        if [ "$admin" = "y" ] || [ "$admin" = "yes" ]; then
            userName+=".adm"
        fi
        userId=$(readSetting uid ${uidDefault})
        groupId=$(readSetting gid ${gidDefault})
        # create a log of what you did
        echo "\"date\": \"$(date)\",\"action\": \"addUser\",\"attributes\": {\"gid\": \"$groupId\",\"name\":\"$userName\",\"uid\": \"$userId\"}" >>ldifScript.log
        createUserInteral
        setSetting uid $((userId + 1))
        setSetting gid $((groupId + 1))
    }

    # Delete a user
    deleteUser() {
        echo Please enter username to delete
        read userName
        # create a log of what you did
        echo "\"date\": \"$(date)\",\"action\": \"deleteUser\",\"attributes\": {\"gid\": \"$groupId\",\"name\":\"$userName\",\"uid\": \"$userId\"}" >>ldifScript.log
        dsidm accounts -b "$domain" user delete "uid=$userName$userLdapString"
    }

    # script to unlock a user's account
    unlockUserAccount() {
        echo Enter the username to UNLOCK
        read userName
        # create a log of what you did
        echo "\"date\": \"$(date)\",\"action\": \"unlockUserAccount\",\"attributes\": {\"name\":\"$userName\"}" >>ldifScript.log
        dsidm instance account unlock "uid=$userName$userLdapString"
    }

    # Create a standalone group
    createGroup() {
        echo Enter the name of the group you want to CREATE
        read groupName
        standaloneGroupId=$(readSetting standalonegid $standaloneGidDefault)

        # create a log of what you did
        echo "\"date\": \"$(date)\",\"action\": \"createStandaloneGroup\",\"attributes\": {\"gid\": $standaloneGroupId,\"name\":\"$groupName\"}" >>ldifScript.log
        dsidm accounts -b "$domain" posixgroup create --cn $groupName --gidNumber $standaloneGroupId
        
        setSetting standalonegid $((standaloneGroupId + 1))
    }

    # Sets the user password to 1qaz@WSX1qaz@WSX and requires the user to set it to a new password
    resetUserPassword() {
        echo Enter the name of the user
        read userName

        # create a log of what you did
        echo "\"date\": \"$(date)\",\"action\": \"resetUserPassword\",\"attributes\": {\"userName\": $userName}" >>ldifScript.log
        dsidm accounts -b "$domain" user modify $userName add:userPassword:$initialUserPassword
    }

    # Add a user to a group
    addUserToGroup() {
        echo Enter the user name of the user
        read userName
        echo Enter the group name you want to add them to
        read groupName
        
        # create a log of what you did
        echo "\"date\": \"$(date)\",\"action\": \"addUserToGroup\",\"attributes\": {\"userName\": $userName,\"groupName\":\"$groupName\"}" >>ldifScript.log

        dsidm accounts -b "$domain" group add_member $groupName "uid=$userName$userLdapString"
    }

    # Main

    if [[ ! -d "$rootDir" ]]; then
        echo "$rootDir does not exist. Would you like it created? (y/n)"
        read response
        if [[ "$response" == "y" ]]; then
        mkdir $rootDir
        else 
        echo "Please create $rootDir and try again"
        exit 1
        fi
    fi

    if [[ ! -e "$settingsFile" ]]; then
    # Create it to make the UI cleaner. Defaults will be prompted on use
    echo "" > $settingsFile
    fi

    #########################################
    #  START THE RUNNING LOOP
    #########################################

    # keep the loop going until were done
    notDone=1

    while [ $notDone ]; do
        # prompt for action
        echo Press 1 to add a new user
        echo Press 2 to unlock an account
        echo Press 3 to create a group
        echo Press 4 to reset a password
        echo Press 5 to add a user to a group
        echo Press 6 to delete a user
        echo Press 7 to search for user
        echo Press 0 to EXIT


        read -p '[1-7 or 0 to exit]: ' choice1

        case "$choice1" in
        0)
            exit 0
            ;;
        1)
            echo Service Account? y or n
            read serviceAccount
            if [ "$serviceAccount" = "y" ] || [ "$serviceAccount" = "yes" ]; then
                addServiceUser
            else
                addUser
            fi
            ;;
        2)
            unlockUserAccount
            ;;
        3)
            createGroup
            ;;
        4)
            resetUserPassword
            ;;
        5)
            addUserToGroup
            ;;
        6)
            deleteUser
            ;;
        7)
            executeLdapSearch
            ;;
        *)
            exit 0
            ;;
        esac
    done

