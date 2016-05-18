Disk Resource Allocation REST API
=================================

Purpose
-------
The objective of this module is to provide a REST API to perform
Resource Allocation of the physical disks of a given node.

REST API
--------
Endpoint: resources/disks/v1/<node>/disks/<diskX>

::
    GET <node>/disks
    {
        'disk0': 'free',
        'disk1': 'jenes/mpi/cluster01/master0',
        'disk2': 'free',
        'disk3': 'free',
    }

    GET <node>/disks?free
    {
        'number': 3,
        'disks': ['disk0', disk2', 'disk3']
    }


    GET <node>/disks?used
    {
        'number': 1,
        'disks': ['disk1']
    }

    GET <node>/disks/<diskX>
    {
        'status': 'free'
    }

    PUT <node>/disks/<diskX>
    {
        'status': 'jenes/mpi/cluster01/master0'
    }

KV Store
--------
/resources/<node>/disks/<disk>/status

Deployment
----------

Installation::

    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt
    pip install gunicorn

Running the application in production using screen::

    su - restuser
    cd <install_dir>
    . venv/bin/activate
    FLASK_CONFIG=production gunicorn --workers=2 --bind=:5000 wsgi:application

