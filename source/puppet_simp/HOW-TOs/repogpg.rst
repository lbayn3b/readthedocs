How-To - Enable GPG for local Repo
==========================

1. Log into the repo server and perform the following steps (You can enter default values unless you have a reason to be specific):

``gpg --gen-key``

``gpg --export --armor --output /var/www/html/repos/<name_of_gpgkey>.pub``

``cd /var/www/html/repos/base``

``gpg --detach-sign --armor repodata/repomd.xml``

``chmod 644 repomd.xml.asc``

.. note::
   Perform the last two commands on all repos that you have.

2. Change your .repo files to add both gpgcheck: true and gpgkey: http://url_to_your_pub_key/hosted_on_your_repo/<name_of_gpgkey>.pub

**You may have to run yum clean all and rm -rf /var/cache/yum before the key will be pulled to the system connecting to repo**
