Deploying SIMP / Puppet Server
=========================================

.. note::
   | SIMP Server requirements
   | 4 CPU's
   | 8 GB RAM
   | 150 GB HDD

.. note:: 
  Parameters
  * Local domain
  * Server IP Address
  * Server Hostname
  * Agent IP Address
  * Agent Hostname
  * Gateway
  * Subnet mask
  * OS Distribution
  * OS Version
  * SIMP User Password
  * Root User Password
 
** ISO Location: `<https://download.simp-project.com/simp/ISO/>`_


1. Once you have the VM created and the SIMP ISO is in your datastore, right click the VM and select edit settings 

2. Under CD/DVD Drive click the dropdown and select Datastore ISO file

3. Under CD/DVD Media select the Browse button and browse to where you uploaded the SIMP ISO file

4. Ensure you check the box to Connect

5. Boot VM from CDROM

6. At boot screen type ``simp``

7. Let run until you get to puppet login

8. Puppet login::
  
     username: simp 
     password: UserPassword

9. Set new password

10. Type ``exit``

11. Puppet root login::

     username: root
     password: RootPassword

12. Set new password

13. Type ``simp config``::

     Ready to start questionnaire? yes
     Fill out questionnaire based on your environment

14. Type ``simp bootstrap``

15. Reboot
