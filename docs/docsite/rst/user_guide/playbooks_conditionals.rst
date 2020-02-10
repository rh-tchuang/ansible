.. _playbooks_conditionals:

************
Conditionals
************

You may want to execute different tasks, or have different goals, depending on the value of a fact (something learned about the remote system), a variable, or the result of a previous task. You may want the value of some variables to depend on the value of other variables. Or you may want to create additional groups of hosts based on whether the hosts match other criteria. You can do all of these things with conditionals, also known as ``when`` statements.

Ansible uses Jinja2 :ref:`tests <playbooks_tests>` and :ref:`filters <playbooks_filters>` in when statements. Ansible supports all the standard tests and filters, and adds some unique ones as well.

.. note::

  There are many options to control execution flow in Ansible. More examples of supported conditionals can be located here: https://jinja.palletsprojects.com/en/master/templates/#comparisons.

.. contents::
   :local:

.. _the_when_statement:

Basic conditionals with ``when``
================================

The simplest conditional statement applies to a single task. Create the task, then add a ``when`` statement that applies a test. When you run the task or playbook, Ansible evaluates the test for all hosts. On any host where the test passes (returns a value of True), Ansible runs that task. For example, if you are installing mysql on multiple machines, some of which have SELinux enabled, you might have a task to configure SELinux to allow mysql to run. You would only want that task to run on machines that have SELinux enabled. This is easy to do in Ansible with a conditional, or ``when`` clause, which contains a raw Jinja2 expression without double curly braces (see :ref:`group_by_module`):

.. code-block:: yaml

    tasks:
      - name: Configure SELinux to start mysql on any port
        seboolean: name=mysql_connect_any state=true persistent=yes
        when: ansible_selinux.status == "enabled"
        # note that all variables can be used directly in conditionals without double curly braces

Conditionals based on ansible_facts
-----------------------------------

Facts are data about hosts, and they are frequently the basis for conditionals. Facts include things like the IP address or operating system of a remote host, or the status of a filesystem. Many conditionals evaluate Ansible facts. Here are some use cases for conditionals based on facts:

  - Install a certain package only if the operating system is a particular version.
  - Skip configuring a firewall on hosts with internal IP addresses.
  - Perform some cleanup steps only if a filesystem is getting full.

Here is a sample conditional based on a fact:

.. code-block:: yaml

    tasks:
      - name: shut down Debian flavored systems
        command: /sbin/shutdown -t now
        when: ansible_facts['os_family'] == "Debian"

If you have multiple conditions, you can group them with parentheses:

.. code-block:: yaml

    tasks:
      - name: shut down CentOS 6 and Debian 7 systems
        command: /sbin/shutdown -t now
        when: (ansible_facts['distribution'] == "CentOS" and ansible_facts['distribution_major_version'] == "6") or
              (ansible_facts['distribution'] == "Debian" and ansible_facts['distribution_major_version'] == "7")

You can use logical operators <https://jinja.palletsprojects.com/en/master/templates/#logic>`_ to combine conditions. When you have multiple conditions that all need to be true (that is, a logical ``and``), you can specify them as a list::

    tasks:
      - name: shut down CentOS 6 systems
        command: /sbin/shutdown -t now
        when:
          - ansible_facts['distribution'] == "CentOS"
          - ansible_facts['distribution_major_version'] == "6"

To see what facts are available on a particular system, add a debug task to your playbook::

    - debug: var=ansible_facts

Tip: If a fact or variable is a string, and you need to run a mathematical comparison on it, use a filter to case the value to an integer::

    tasks:
      - shell: echo "only on Red Hat 6, derivatives, and later"
        when: ansible_facts['os_family'] == "RedHat" and ansible_facts['lsb']['major_release']|int >= 6

.. note:: the above example requires the lsb_release package on the target host in order to return the 'lsb major_release' fact.

Conditions based on registered variables
----------------------------------------

Often in a playbook you want to execute or skip a task based on the outcome of an earlier task. For example, you might want to configure a package only if it was upgraded by an earlier task. To create a conditional based on a registered variable:

  # register the outcome of the earlier task as a variable
  # create a conditional test based on the registered variable

You create the name of the registered variable using the ``register`` keyword. You can use registered variables in templates and action lines as well as in conditional ``when`` statements.  It looks like this (in an obviously trivial example)::

    - name: test play
      hosts: all

      tasks:

          - shell: cat /etc/motd
            register: motd_contents

          - shell: echo "motd contains the word hi"
            when: motd_contents.stdout.find('hi') != -1

You can access the string contents of the registered variable using the 'stdout' value. You can us registered results in the loop of a task if the variable is a list or is converted into a list. You can either use "stdout_lines" or call "home_dirs.stdout.split()". You can also split the lines by other fields::

    - name: registered variable usage as a loop list
      hosts: all
      tasks:

        - name: retrieve the list of home directories
          command: ls /home
          register: home_dirs

        - name: add home dirs to the backup spooler
          file:
            path: /mnt/bkspool/{{ item }}
            src: /home/{{ item }}
            state: link
          loop: "{{ home_dirs.stdout_lines }}"
          # same as loop: "{{ home_dirs.stdout.split() }}"

.. note:: Registration happens even when a task is skipped due to the conditional. This way you can query the variable for `` is skipped`` to know if task was attempted or not.

As shown previously, the registered variable's string contents are accessible with the 'stdout' value.
You may check the registered variable's string contents for emptiness::

    - name: check registered variable for emptiness
      hosts: all

      tasks:

          - name: list contents of directory
            command: ls mydir
            register: contents

          - name: check contents for emptiness
            debug:
              msg: "Directory is empty"
            when: contents.stdout == ""

A registered variable also contains the status of the task that created it. You can create conditionals based on the success or failure of a task. Remember to ignore errors if you want Ansible to continue executing when a failure occurs::

    tasks:
      - command: /bin/false
        register: result
        ignore_errors: True

      - command: /bin/something
        when: result is failed

      - command: /bin/something_else
        when: result is succeeded

      - command: /bin/still/something_else
        when: result is skipped


.. note:: Older versions of Ansible used ``success`` and ``fail``, but ``succeeded`` and ``failed`` use the correct tense. All of these options are now valid.

.. warning:: You might expect a variable of a skipped task to be undefined and use `defined` or `default` to check that. **This is incorrect**! Even when a task is failed or skipped the variable is still registered with a failed or skipped status. See :ref:`registered_variables`.




Conditionals based on variables
-------------------------------

You can also create conditionals based on variables defined in the playbooks or inventory, just make sure to apply the `|bool` filter to non boolean variables (ex: string variables with content like 'yes', 'on', '1', 'true').  An example may be the execution of a task based on a variable's boolean value::

    vars:
      epic: true
      monumental: "yes"

Then a conditional execution might look like::

    tasks:
        - shell: echo "This certainly is epic!"
          when: epic or monumental|bool

or::

    tasks:
        - shell: echo "This certainly isn't epic!"
          when: not epic

If a required variable has not been set, you can skip or fail using Jinja2's ``defined`` test.
For example::

    tasks:
        - shell: echo "I've got '{{ foo }}' and am not afraid to use it!"
          when: foo is defined

        - fail: msg="Bailing out. this play requires 'bar'"
          when: bar is undefined

This is especially useful in combination with the conditional import of vars files (see below).
As the examples show, you don't need to use ``{{ }}`` to use variables inside conditionals, as these are already implied.

.. _loops_and_conditionals:

Using conditionals in loops
---------------------------

If you combine a ``when`` statement with a :ref:`loop <playbooks_loops>`, Ansible processes the `when` statement separately for each item. This is by design, so you can execute the task on some items in the loop and skip it on other items. For example::

    tasks:
        - command: echo {{ item }}
          loop: [ 0, 2, 4, 6, 8, 10 ]
          when: item > 5

If you need to skip the whole task when the loop variable is undefined, use the `|default` filter to provide an empty iterator. For example, when looping over a list::

        - command: echo {{ item }}
          loop: "{{ mylist|default([]) }}"
          when: item > 5


You can do the same thing when looping over a dict::

        - command: echo {{ item.key }}
          loop: "{{ query('dict', mydict|default({})) }}"
          when: item.value > 5

.. _loading_in_custom_facts:

Loading custom facts
--------------------

You can provide provide your own facts if you want, which is covered in :ref:`developing_modules`.  To run them, just make a call to your own custom fact gathering module at the top of your list of tasks, and variables returned there will be accessible to future tasks::

    tasks:
        - name: gather site specific fact data
          action: site_facts
        - command: /usr/bin/thingy
          when: my_custom_fact_just_retrieved_from_the_remote_system == '1234'

.. _when_roles_and_includes:

Conditionals with re-use
------------------------

You can apply the same condition to multiple tasks by placing those tasks in a re-usable tasks file, playbook, or role, then applying the condition to the ``roles`` entry, import, or include. See :ref:`playbooks_reuse` for more information on re-use in Ansible.

When you use this approach, Ansible returns a 'skipped' message for every host that does not match the criteria. In many cases the :ref:`group_by module <group_by_module>` can be a more streamlined way to accomplish the same thing; see :ref:`os_variance`.

Conditionals with imports
^^^^^^^^^^^^^^^^^^^^^^^^^

When you use a conditional on an import statement, all the tasks get evaluated, but the conditional is applied to each and every task::

    - import_tasks: tasks/sometasks.yml
      when: "'reticulating splines' in output"

Starting with Ansible 2.0, you can apply conditions to ``import_tasks`` and to ``import_playbook``.

Conditionals with roles
^^^^^^^^^^^^^^^^^^^^^^^

You can apply a conditional to a role::

    - hosts: webservers
      roles:
         - role: debian_stock_config
           when: ansible_facts['os_family'] == 'Debian'

You will note a lot of ``skipped`` output by default in Ansible when using this approach on systems that don't match the criteria. In many cases the :ref:`group_by module <group_by_module>` can be a more streamlined way to accomplish the same thing; see :ref:`os_variance`.

Conditionals with includes
^^^^^^^^^^^^^^^^^^^^^^^^^^

When you use a conditional on an ``include_*`` statement, the condition is applied only to the include task itself and not to any other tasks within the included file(s). A common situation where this distinction is important is as follows::

    # We wish to include a file to define a variable when it is not
    # already defined

    # main.yml
    - import_tasks: other_tasks.yml # note "import"
      when: x is not defined

    # other_tasks.yml
    - set_fact:
        x: foo
    - debug:
        var: x

This expands at include time to the equivalent of::

    - set_fact:
        x: foo
      when: x is not defined
    - debug:
        var: x
      when: x is not defined

Thus if ``x`` is initially undefined, the ``debug`` task will be skipped.  By using ``include_tasks`` instead of ``import_tasks``, both tasks from ``other_tasks.yml`` will be executed as expected.

For more information on the differences between ``include`` v ``import`` see :ref:`playbooks_reuse`.

.. _conditional_imports:

Variable values based on facts
------------------------------

Sometimes you want to set the value of a variable differently in a playbook based on certain criteria.
For example, the names of many packages are different on CentOS and on Debian. You can create a playbook that works on multiple platforms and OS versions with a minimum of syntax by placing your variable values in vars files and conditionally importing them. If you want to install Apache on some CentOS and some Debian servers, create variables files with YAML keys and values. For example::

    ---
    # for vars/RedHat.yml
    apache: httpd
    somethingelse: 42

Then import those variables files based on the facts you gather on the hosts in your playbook::

    ---
    - hosts: webservers
      remote_user: root
      vars_files:
        - "vars/common.yml"
        - [ "vars/{{ ansible_facts['os_family'] }}.yml", "vars/os_defaults.yml" ]
      tasks:
      - name: make sure apache is started
        service: name={{ apache }} state=started

Ansible gathers facts on the hosts in the webservers group, then interpolates the variable "ansible_facts['os_family']" into a list of filenames. If you have hosts with Red Hat operating systems ('CentOS', for example), Ansible looks for 'vars/RedHat.yml'. If that file does not exist, Ansible attempts to load 'vars/os_defaults.yml'. For Debian hosts, Ansible first looks for 'vars/Debian.yml', before falling back on 'vars/os_defaults.yml'. If no files in the list are found, Ansible raises an error.

Ansible separates variables from tasks, keeping your playbooks from turning into arbitrary code with nested conditionals. This approach results in more streamlined and auditable configuration rules because there are fewer decision points to track.

Files and templates based on facts
----------------------------------

Sometimes a configuration file you want to copy, or a template you will use may depend on a variable.
The following construct selects the first available file appropriate for the variables of a given host, which is often much cleaner than putting a lot of if conditionals in a template.

The following example shows how to template out a configuration file that was very different between, say, CentOS and Debian::

    - name: template a file
      template:
          src: "{{ item }}"
          dest: /etc/myapp/foo.conf
      loop: "{{ query('first_found', { 'files': myfiles, 'paths': mypaths}) }}"
      vars:
        myfiles:
          - "{{ansible_facts['distribution']}}.conf"
          -  default.conf
        mypaths: ['search_location_one/somedir/', '/opt/other_location/somedir/']

Commonly-used facts
===================

The following Facts are frequently used in Conditionals - see above for examples.

.. _ansible_distribution:

ansible_facts['distribution']
-----------------------------

Possible values (sample, not complete list)::

    Alpine
    Altlinux
    Amazon
    Archlinux
    ClearLinux
    Coreos
    CentOS
    Debian
    Fedora
    Gentoo
    Mandriva
    NA
    OpenWrt
    OracleLinux
    RedHat
    Slackware
    SMGL
    SUSE
    Ubuntu
    VMwareESX

.. See `OSDIST_LIST`

.. _ansible_distribution_major_version:

ansible_facts['distribution_major_version']
-------------------------------------------

The major version of the operating system. For example, the value is `16` for Ubuntu 16.04.

.. _ansible_os_family:

ansible_facts['os_family']
--------------------------

Possible values (sample, not complete list)::

    AIX
    Alpine
    Altlinux
    Archlinux
    Darwin
    Debian
    FreeBSD
    Gentoo
    HP-UX
    Mandrake
    RedHat
    SGML
    Slackware
    Solaris
    Suse
    Windows

.. Ansible checks `OS_FAMILY_MAP`; if there's no match, it returns the value of `platform.system()`.

.. seealso::

   :ref:`working_with_playbooks`
       An introduction to playbooks
   :ref:`playbooks_reuse_roles`
       Playbook organization by roles
   :ref:`playbooks_best_practices`
       Best practices in playbooks
   :ref:`playbooks_variables`
       All about variables
   `User Mailing List <https://groups.google.com/group/ansible-devel>`_
       Have a question?  Stop by the google group!
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
