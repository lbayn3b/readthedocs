How-To - Various Kubernetes Tips
================================


If Rancher certs have expired run the following to restart the rancher deployment:

.. code-block:: ruby

    kubectl rollout restart deployment rancher -n cattle-system
