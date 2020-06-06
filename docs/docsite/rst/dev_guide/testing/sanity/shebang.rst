shebang
=======

実行ファイルのほとんどは、以下のいずれかの shebang のみを使用する必要があります。

- ``#!/bin/sh``
- ``#!/bin/bash``
- ``#!/usr/bin/make``
- ``#!/usr/bin/env python``
- ``#!/usr/bin/env bash``

注記: ``#!/bin/bash`` の場合は、いずれのオプションの ``eux`` も使用できます (``#!/bin/bash -eux`` など)。

これは Ansible モジュールには適用されません。これは実行可能ではなく、``#!/usr/bin/python`` を常に使用する必要があります。

一部の例外が許可されます。ご質問がある場合はお問い合わせください。
