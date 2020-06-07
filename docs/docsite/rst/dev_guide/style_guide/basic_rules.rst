.. _styleguide_basic:

基本ルール
===========
.. contents::
  :local:

標準的なアメリカ英語の使用
-----------------------------
Ansible は標準的なアメリカ英語を使用します。アメリカ英語では綴りが異なる一般的な単語に注意してください (color と colour、organize と organise など)。

世界中の読者に向けて書く
---------------------------
記載される内容は、生い立ちや文化が違っても理解できるものでなければなりません。イディオムや地域主義は使用せず、誤って解釈されない中立的な表現を使用します。ユーモアな表現は使用しないでください。

命名規則に従う
-------------------------
命名規則と商標には常に従ってください。

.. Ansible の用語ページへのリンクを追加するのに適した場所

明確な文構造を使用する
----------------------------
明確な文法構造とは、以下のようになります。

- 重要な情報を最初に示します。
- 文章の理解が難しくなるような単語は使用しないでください。
- 文章は短くします。文章が長くなればなるほど、理解が難しくなります。

たとえば、以下のように改善できます。

問題がある文章: 
    The unwise walking about upon the area near the cliff edge may result in a dangerous fall and therefore it is recommended that one remains a safe distance to maintain personal safety. (崖の端近くを歩き回ると、下に落ちる危険があります。安全を維持するために安全な距離を保つことをお勧めします。)

改善例: 
    Danger! Stay away from the cliff. (危険です。崖から離れてください。)

問題がある文章: 
    Furthermore, large volumes of water are also required for the process of extraction. (また、抜歯のプロセスには、水が大量に必要になります。)

改善例: 
    Extraction also requires large volumes of water. (抜歯には、大量の水が必要です。)

冗長を避ける
---------------
短く簡潔な文章を書きます。以下のような用語は使用しないでください。

- 「...as has been said before」
- 「...each and every」
- 「...point in time」
- 「...in order to」

メニュー項目およびコマンドを強調表示する
---------------------------------
メニューまたはコマンドを文書化する場合は、重要な内容を **太字** にすると役立ちます。

メニュー手順では、メニュー名、ボタン名などを太字にして、GUI でその文字を見つけられるようにします。

1. **ファイル** メニューで、**開く** をクリックします。
2. **ユーザー名** フィールドに名前を入力します。
3. **開く** ダイアログボックスで、**保存** をクリックします。
4. ツールバーで、**ファイルを開く** アイコンをクリックします。

コードまたはコマンドスニペットについては、RST `code-block directive <https://www.sphinx-doc.org/en/1.5/markup/code.html#directive-code-block>`_ を参照してください。::

   .. code-block:: bash

     ssh my_vyos_user@vyos.example.net
     show config
