.. _playbooks_lookups:

*******
Lookups
*******

Lookup plugins retrieve data from outside sources such as files, databases, key/value stores, APIs, and other services. Like all templating, lookups execute and are evaluated on the Ansible control machine. Ansible makes the data returned by a lookup plugin available using the standard templating system. Before Ansible 2.5, lookups were mostly used indirectly in ``with_<lookup>`` constructs for looping. Starting with Ansible 2.5, lookups are used more explicitly as part of Jinja2 expressions fed into the ``loop`` keyword.

.. note::
    - Lookups are executed within the directory containing the role or play, as opposed to local tasks which are executed with the directory of the executed script.
    - You can pass wantlist=True to lookups to use in jinja2 template "for" loops.
    - Lookups are an advanced feature. You should have a good working knowledge of Ansible plays before incorporating them.

.. warning:: Some lookups pass arguments to a shell. When using variables from a remote/untrusted source, use the `|quote` filter to ensure safe usage.

.. _lookups_and_variables:

Using lookups in variables
==========================

You can populate variables using lookups. Ansible evaluates the value each time it is executed in a task (or template)::

    vars:
      motd_value: "{{ lookup('file', '/etc/motd') }}"
    tasks:
      - debug:
          msg: "motd value is {{ motd_value }}"

For more details and a complete list of lookup plugins available, please see :ref:`plugins_lookup`.

.. seealso::

   :ref:`working_with_playbooks`
       An introduction to playbooks
   :ref:`playbooks_conditionals`
       Conditional statements in playbooks
   :ref:`playbooks_variables`
       All about variables
   :ref:`playbooks_loops`
       Looping in playbooks
   `User Mailing List <https://groups.google.com/group/ansible-devel>`_
       Have a question?  Stop by the google group!
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
