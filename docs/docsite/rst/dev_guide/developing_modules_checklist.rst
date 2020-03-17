.. _developing_modules_checklist:
.. _module_contribution:

***********************************
Contributing your module to Ansible
***********************************

Ansible no longer accepts modules in the core ansible/ansible repository. If you want others to use the modules you are writing, either share copies of your module code for :ref:`local use <developing_locally>` or distribute it as part of a collection.

Whether used locally or distributed in a collection, your modules and collections will be easier to use and maintain if you follow the :ref:`tips for module development <developing_modules_best_practices>`.

Module development: objective guidelines
========================================

We recommend that you:

* write your module in either Python or Powershell for Windows
* use the ``AnsibleModule`` common code
* support Python 2.6 and Python 3.5 - if your module cannot support Python 2.6, explain the required minimum Python version and rationale in the requirements section in ``DOCUMENTATION``
* use proper :ref:`Python 3 syntax <developing_python_3>`
* follow `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ Python style conventions - see :ref:`testing_pep8` for more information
* license your module under the GPL license (GPLv3 or later)
* understand the :ref:`license agreement <contributor_license_agreement>`, which applies to all contributions
* conform to Ansible's :ref:`formatting and documentation <developing_modules_documenting>` standards
* include comprehensive :ref:`tests <developing_testing>` for your module
* minimize module dependencies
* support :ref:`check_mode <check_mode_dry>` if possible
* ensure your code is readable
* if a module is named ``<something>_facts``, it should be because its main purpose is returning ``ansible_facts``. Do not name modules that do not do this with ``_facts``. Only use ``ansible_facts`` for information that is specific to the host machine, for example network interfaces and their configuration, which operating system and which programs are installed.
* Modules that query/return general information (and not ``ansible_facts``) should be named ``_info``. General information is non-host specific information, for example information on online/cloud services (you can access different accounts for the same online service from the same host), or information on VMs and containers accessible from the machine.

If you have questions, reach out via `Ansible's IRC chat channel <http://irc.freenode.net>`_ or the `Ansible development mailing list <https://groups.google.com/group/ansible-devel>`_. Experienced Ansible developers can help you create clear, concise, secure, and maintainable code that provides a good user experience, helpful error messages, and reasonable defaults.

Other checklists
================

* :ref:`Tips for module development <developing_modules_best_practices>`.
* :ref:`Amazon development checklist <AWS_module_development>`.
* :ref:`Windows development checklist <developing_modules_general_windows>`.
