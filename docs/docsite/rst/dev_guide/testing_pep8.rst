:orphan:

.. _testing_pep8:

*****
PEP 8
*****

.. contents:: トピック

`PEP 8`_ スタイルのガイドラインは、デフォルトでリポジトリーにあるすべての python ファイルで `pycodestyle`_ によって強制されます。

ローカルでの実行
===============

`PEP 8`_ チェックは、次の方法でローカルに実行できます。


    ansible-test sanity --test pep8 [file-or-directory-path-to-check] ...



.. _PEP 8: https://www.python.org/dev/peps/pep-0008/
.. _pycodestyle: https://pypi.org/project/pycodestyle/
