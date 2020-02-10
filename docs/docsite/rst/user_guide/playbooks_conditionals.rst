.. _playbooks_conditionals:

Conditionals
============

You may want to execute different tasks, or have different goals, depending on the value of a variable, a fact (something learned about the remote system), or the result of a previous task. You may want the value of some variables to depend on the value of other variables. Or you may want to create additional groups of hosts based on whether the hosts match other criteria. You can do all of these things with conditionals.

.. note::

  There are many options to control execution flow in Ansible. More examples of supported conditionals can be located here: https://jinja.palletsprojects.com/en/master/templates/#comparisons.

.. contents::
   :local:

.. _the_when_statement:

Basic conditionals with ``when``
--------------------------------

Sometimes you want to skip a particular step on a particular host. For example, you may not want to install a certain package if the operating system is a particular version. Or you may want to perform some cleanup steps only if a filesystem is getting full.

This is easy to do in Ansible with the ``when`` clause, which contains a raw `Jinja2 expression <https://jinja.palletsprojects.com/en/master/templates/#expressions>`_ without double curly braces (see :ref:`group_by_module`). The ``when`` statement is simple::

    tasks:
      - name: "shut down Debian flavored systems"
        command: /sbin/shutdown -t now
        when: ansible_facts['os_family'] == "Debian"
        # note that all variables can be used directly in conditionals without double curly braces

You can apply multiple conditions, using parentheses to group them::

    tasks:
      - name: "shut down CentOS 6 and Debian 7 systems"
        command: /sbin/shutdown -t now
        when: (ansible_facts['distribution'] == "CentOS" and ansible_facts['distribution_major_version'] == "6") or
              (ansible_facts['distribution'] == "Debian" and ansible_facts['distribution_major_version'] == "7")

You can use logical operators <https://jinja.palletsprojects.com/en/master/templates/#logic>`_ to combine conditions. When you have multiple conditions that all need to be true (that is, a logical ``and``), you can specify them as a list::

    tasks:
      - name: "shut down CentOS 6 systems"
        command: /sbin/shutdown -t now
        when:
          - ansible_facts['distribution'] == "CentOS"
          - ansible_facts['distribution_major_version'] == "6"

.. note:: Jinja2 expressions are built up from comparisons, filters, tests, and logical combinations thereof. These examples show some basic uses. For a more complete overview over all operators to use, please refer to the official `Jinja2 documentation <https://jinja.palletsprojects.com/en/master/templates/#expressions>`_ .

You can use Jinja2 :ref:`tests <playbooks_tests>` and :ref:`filters <playbooks_filters>` in when statements. Ansible supports all the `standard tests and filters <https://jinja.palletsprojects.com/en/master/templates/#other-operators>`_, and adds some unique ones as well. Suppose you want to ignore the error of one statement and then decide to do something conditionally based on success or failure::

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


To see what facts are available on a particular system, you can do the following in a playbook::

    - debug: var=ansible_facts


Tip: Sometimes you'll get back a variable that's a string and you'll want to do a math operation comparison on it.
You can do this like so::

    tasks:
      - shell: echo "only on Red Hat 6, derivatives, and later"
        when: ansible_facts['os_family'] == "RedHat" and ansible_facts['lsb']['major_release']|int >= 6

.. note:: the above example requires the lsb_release package on the target host in order to return the `lsb major_release` fact.

Variables defined in the playbooks or inventory can also be used, just make sure to apply the ``|bool`` filter to non-boolean variables (e.g., `string` variables with content like ``yes``, ``on``, ``1``, ``true``).
An example may be the execution of a task based on a variable's boolean value::

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

Applying 'when' to roles, imports, and includes
-----------------------------------------------

Note that if you have several tasks that all share the same conditional statement, you can place those tasks in a tasks file, playbook, or role and apply the conditional when you incorporate them with ``roles``, imports, or includes. Ansible will return a 'skipped' message when you use this approach on systems that do not match the criteria. In many cases the :ref:`group_by module <group_by_module>` can be a more streamlined way to accomplish the same thing; see :ref:`os_variance`.


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

When a conditional is used with ``include_*`` tasks instead of imports, it is applied `only` to the include task itself and not to any other tasks within the included file(s). A common situation where this distinction is important is as follows::

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

Thus if ``x`` is initially undefined, the ``debug`` task will be skipped.  By using ``include_tasks`` instead of ``import_tasks``,
both tasks from ``other_tasks.yml`` will be executed as expected.

For more information on the differences between ``include`` v ``import`` see :ref:`playbooks_reuse`.

.. _conditional_imports:

Conditional variable values
---------------------------

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

Selecting files and templates based on variables
------------------------------------------------

.. note:: This is an advanced topic that is infrequently used.  You can probably skip this section.

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

Registering variables
---------------------

Often in a playbook it may be useful to store the result of a given command in a variable and access
it later.  Use of the command module in this way can in many ways eliminate the need to write site specific facts, for instance, you could test for the existence of a particular program.

.. note:: Registration happens even when a task is skipped due to the conditional. This way you can query the variable for `` is skipped`` to know if task was attempted or not.

The ``register`` keyword decides what variable to save a result in.  The resulting variables can be used in templates, action lines, or *when* statements.  It looks like this (in an obviously trivial example)::

    - name: test play
      hosts: all

      tasks:
          - shell: cat /etc/motd
            register: motd_contents

          - shell: echo "motd contains the word hi"
            when: motd_contents.stdout.find('hi') != -1

As shown previously, the registered variable's string contents are accessible with the ``stdout`` value.
The registered result can be used in the loop of a task if it is converted into
a list (or already is a list) as shown below.  ``stdout_lines`` is already available on the object as
well though you could also call ``home_dirs.stdout.split()`` if you wanted, and could split by other
fields::

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


As shown previously, the registered variable's string contents are accessible with the ``stdout`` value.
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
