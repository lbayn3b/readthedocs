Ambari HDF Install
==================

.. note::
   The Ambari UI should now be accessible. You will have to access it in whatever way your environment is setup to access internal sites.

.. note::   
   ssh tunnel using the following: ssh -i 'C:\path\to\user.pem' <user>@<public ip> -L 8080:<hostname of hdfmaster>:8080) Then you should be able to access the Ambari UI using http://localhost:8080 from your browser. 

.. note::   

   Some sites have AWS workspaces stood up and you can access the Ambari UI in the workspaces browser using http://<ip of hdfmaster>:8080

1. There is a bug in Ambari and the following will show how to get around this bug (this should be performed on the hdfmaster server):

``cd /usr/lib/ambari-server/web/javascripts/``

``cp app.js app.js_backup``

``vi app.js``

**Find line (39892)**

**Change**

.. code:: guess

   /**
    * Use Local Repo if some network issues exist
    */
   onNetworkIssuesExist: function () {
     if (this.get('networkIssuesExist')) {
       this.get('content.stacks').forEach(function (stack) {
           stack.setProperties({
             usePublicRepo: false,
             useLocalRepo: true
           });
           stack.cleanReposBaseUrls();
       });
     }
   }.observes('networkIssuesExist'),

**To**

.. code:: guess

   /**
    * Use Local Repo if some network issues exist
    */
   onNetworkIssuesExist: function () {
     if (this.get('networkIssuesExist')) {
       this.get('content.stacks').forEach(function (stack) {
         if(stack.get('useLocalRepo') != true){
           stack.setProperties({
             usePublicRepo: false,
             useLocalRepo: true
           });
           stack.cleanReposBaseUrls();
         } 
       });
     }
   }.observes('networkIssuesExist'),

``ambari-server reset``   

2. Navigate to http://<your.ambari.server>:8080, where <your.ambari.server> is the name of your Ambari server host.

3. Log in to the Ambari server by using the default user name and password: admin and admin. You can change these credentials later.


4. In the **Ambari Welcome** page, choose **Launch Install Wizard**.

.. figure:: photos/welcome.JPG
    :width: 800px
    :align: center
    :height: 600px
    :alt: alternate text
    :figclass: align-center


5. In the **Get Started** step, specify a name for your cluster.

.. figure:: photos/GetStarted.JPG
    :width: 800px
    :align: center
    :height: 600px
    :alt: alternate text
    :figclass: align-center


6. In the **Select Version** page, select the correct HDF version and remove all repositories except the one appropriate for your operating system. Change the Base URL for HDF and HDP-UTILS to the base URL appropriate for your operating system.

.. figure:: photos/versionrepo.JPG
    :width: 800px
    :align: center
    :height: 600px
    :alt: alternate text
    :figclass: align-center


7. In the **Install Options** page, under **Target Hosts** enter the fqdn's of all the hosts in your HDF cluster. Also check the **Perform manual registration on hosts and do not use SSH** option as we have set that up with Puppet code.

.. figure:: photos/targethosts.JPG
    :width: 800px
    :align: center
    :height: 600px
    :alt: alternate text
    :figclass: align-center


8. If registration is successful you should see the following screen. Check the warnings to ensure there is nothing that will impact the install.

.. figure:: photos/installerSuccess.JPG
    :width: 800px
    :align: center
    :height: 600px
    :alt: alternate text
    :figclass: align-center


9. In the **Choose Services** page, select all services that you want to install to your HDF cluster.

.. figure:: photos/chooseservices.JPG
    :width: 800px
    :align: center
    :height: 600px
    :alt: alternate text
    :figclass: align-center


10. In the **Assign Masters** page, choose which hosts to deploy the master services to.

.. figure:: photos/assign_masters.JPG
    :width: 800px
    :align: center
    :height: 600px
    :alt: alternate text
    :figclass: align-center


11. In the **Assign Slaves and Clients** page, choose which hosts to deploy slave and client services to.

.. figure:: photos/assignslaves.JPG
    :width: 800px
    :align: center
    :height: 600px
    :alt: alternate text
    :figclass: align-center


12. In the **Credentials** page, set passwords for the different services listed.

.. figure:: photos/credentials.JPG
    :width: 800px
    :align: center
    :height: 600px
    :alt: alternate text
    :figclass: align-center


13. In the **Data Dirs** page, configure the directories for the different services.

.. note::
   This is an important step. Most of these services attempt to execute from the /tmp directory and on a STIG system /tmp has noexec. You must change these values to another location.

.. figure:: photos/datadirs.JPG
    :width: 800px
    :align: center
    :height: 600px
    :alt: alternate text
    :figclass: align-center


14. In the **Accounts** page, verify all accounts to be created. If you have created accounts manually on the system input those accounts here instead of having Ambari create accounts.

.. figure:: photos/accounts.JPG
    :width: 800px
    :align: center
    :height: 600px
    :alt: alternate text
    :figclass: align-center


15. In the **All Configurations** page, go through and make any customizations to the services you may want.

.. note::
   In a STIG environment you will need to go to NIFI, expand Advanced nifi-bootstrap-env, scroll down to java.arg.18=-Djavax.security.auth.useSubjectCredsOnly=true, add the following to the line beneath this: javva.arg.snappy=-Dorg.xerial.snappy.tempdir=/data01/nifi/tmp/ **This will be a path that you have created on each NiFi host and placed the snappy file into

.. figure:: photos/snappy.JPG
    :width: 800px
    :align: center
    :height: 400px
    :alt: alternate text
    :figclass: align-center


16. You will notice a Red bell on the screen with a number 2 next to it. Click this to set the nifi db password.

.. figure:: photos/nifipass.JPG
    :width: 800px
    :align: center
    :height: 600px
    :alt: alternate text
    :figclass: align-center


17. In the **Review** page, ensure everything looks good before clicking Deploy. In this picture, you can tell the bug fix has not been applied as the Repositories show blank.

.. figure:: photos/deploy.JPG
    :width: 800px
    :align: center
    :height: 600px
    :alt: alternate text
    :figclass: align-center


18. Once you click deploy you should see the services begin to install on each host.

.. figure:: photos/installing.JPG
    :width: 800px
    :align: center
    :height: 600px
    :alt: alternate text
    :figclass: align-center


19. Once this is complete, click next and you should see a functioning HDF cluster.

.. figure:: photos/functioning.JPG
    :width: 800px
    :align: center
    :height: 400px
    :alt: alternate text
    :figclass: align-center
