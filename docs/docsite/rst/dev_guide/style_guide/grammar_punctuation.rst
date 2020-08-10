
文法および句読点
``````````````````````````````````````

一般的なスタイルおよび使用方法、ならびに一般的な間違い
----------------------------------------------------

Ansible
~~~~~~~~~
* 「Ansible」と書きます。 「Ansible, Inc.」または「AnsibleWorks」にはしないでください。このルールの唯一の例外は、法的文書または財務諸表を作成する場合です。

* ロゴマークは、本文で使用しないでください。その他の文章で使用しているフォントを常に使用します。

* 米国では、会社は単数形で使用します。つまり、Ansible は、「they」ではなく「it」になります。


大文字
~~~~~~~~~~~~~~
Ansible の実際の製品、サービス、または部門ではない場合には、大文字にしないでください。重要に思えてもです。見出しの最初の単語の最初の文字だけを大文字にします。

コロン
~~~~~~~~~~~~~~~~~
通常、コロンは、リストまたは一連の要素の前に使用されます。
The Triangle Area consists of three cities: Raleigh, Durham, and Chapel Hill.

ただし、リストが、文内の要素の補語または目的語の場合は、以下のようにします。
Before going on vacation, be sure to (1) set the alarm, (2) cancel the newspaper, and (3) ask a neighbor to collect your mail.

直後に関連するリストを追加する場合は、「as follows」および「the following」(次のとおり) の後にコロンを使用します。
The steps for changing directories are as follows:

    1.Open a terminal.
    2.Type cd...

コロンを使用して、箇条書きリスト (ダッシュ、アイコンまたは記号を使用) 追加します。

    In the Properties dialog box, you'll find the following entries:
    
    - Connection name
    - Count
    - Cost per item


コンマ
~~~~~~~~~~~
3 つ以上の項目が続く場合は、「and」の前にコンマを使用します。 

- Item 1, item 2, and item 3.

   
これにより読みやすくなり、混乱を避けることができます。これに対する主な例外は PR です。PR では、多くの場合ジャーナリスト向けのスタイルにより、このようなコンマは使用しません。

次の 2 つの文章の意味が大きく異なることを考えると、コンマは常に重要です。

- Let's eat, Grandma
- Let's eat Grandma.

正しい句読点により、おばあさんの命を救うことができます。

もしくは、以下の例をご覧ください。

.. image:: images/commas-matter.jpg


縮約
~~~~~~~~~~~~~
Ansible ドキュメントでは、縮約は使用しないでください。

エムダッシュ (－)
~~~~~~~~~~
可能な場合は、両側にスペースを入れずにエムダッシュ (－) を使用します。エムダッシュ (－) が利用できない場合は、両側に空白を入れずに二重ダッシュを使用します。

読みやすくするために、コンマの代わりにエムダッシュをペアにして使用できます。ただし、ダッシュはコンマよりも常に強調されることに注意してください。

エムダッシュのペアは、括弧のペアの代わりに使用することもできます。ダッシュは括弧よりも形式的ではないと見なされ、押しつけがましく感じることもあります。括弧内のコンテンツに注意を引きたい場合は、ダッシュを使用します。括弧内のコンテンツにあまり注意を引きたくない場合は、括弧を使用します。

.. note::
    括弧の代わりにダッシュを使用する場合は、前後の句読点を省略してください。次の例を比較してください。

::

    Upon discovering the errors (all 124 of them), the publisher immediately recalled the books.

    Upon discovering the errors—all 124 of them—the publisher immediately recalled the books.


文末に括弧の代わりに使用する場合は、ダッシュを 1 つだけに使用します。

::

    After three weeks on set, the cast was fed up with his direction (or, rather, lack of direction).

    After three weeks on set, the cast was fed up with his direction—or, rather, lack of direction.


感嘆符 (!)
~~~~~~~~~~~~~~~~~~~~~~~
文末には使用しないでください。感嘆符は、bang (!) などのコマンドを参照する場合に使用できます。

性別の参照
~~~~~~~~~~~~~~~~~~
ドキュメンテーションでは、性別固有の代名詞は使用しないでください。「he/she」や「his/hers」ではなく「they」および「their」を使用する方が適切です。 

指示を示す場合は「you」と使用し、より一般的な説明では「the user」、「new users」などを使用すると良いでしょう。 

テクニカルドキュメントを作成する際は、「You」 の意味で「one」を使用しないでください。「one」を使用すると堅苦しくなります。

ドキュメントの作成時に「we」は使用しないでください。「we」はユーザーの動作を示しません。Ansible の製品は、ユーザーの要求に応じて作業を行っています。


ハイフン
~~~~~~~~~~~~~~
このハイフンの主な機能は、特定の複合用語の特徴です。目的が満たされない限り、ハイフンは使用しないでください。複合形容詞が間違って解釈されない場合、または多くの心理学用語と同じ様に、その意味が確立されている場合は、ハイフンが必要ありません。

ハイフンは、あいまいさや混乱を避けるためにを使用します。

::

    a little-used car
    a little used-car

    cross complaint
    cross-complaint

    high-school girl
    high schoolgirl

    fine-tooth comb (most people do not comb their teeth)

    third-world war
    third world war

.. image:: images/hyphen-funny.jpg

適切な編集が必要な出版物 (特に本、雑誌、新聞) では、単語が行をまたがる場合にハイフンを使用します。これにより、単語の間隔が大きく変わる (そして気が散る) ことなく、右マージンを均等に揃えることができます。


リスト
~~~~~~~
箇条書きリストの構造を同等で一貫性のあるものにします。1 つの箇条書きを動詞句にした場合は、残りもすべて動詞句にする必要があります。1 つの箇条書きを文にした場合は、残りもすべて文にする必要があります。

箇条書きでは、それぞれ最初の単語を大文字にします。次のような項目のリストなど、単に項目のリストであることが明らかである場合は除きます。
* computer
* monitor
* keyboard
* mouse

箇条書きに他の文章が含まれる場合は、(上の例のような単純なリストでない限り) 箇条書きが完全な文になっていなくてもピリオドを追加します。この理由の 1 つは、各箇条書きが元の文を完了すると言われているためです。

箇条書きがポスターやホームページのプロモーションなどのように独立して示される場合は、ピリオドは必要ありません。

手順を説明するときは、箇条書きの代わりに番号付きリストを使用してください。


月および州
~~~~~~~~~~~~~~~~~~~~
AP スタイルブックに従って、月と州の名前を省略します。月は、日付と組み合わせて使用される場合に限り省略されます。たとえば、「The President visited in January 1999.」または「The President visited Jan. 12.」です。

月: Jan.、Feb.、March、April、May、June、July、Aug.、Sept.、Nov.、Dec.

州: Ala.、Ariz.、Ark.、Calif.、Colo.、Conn.、Del.、Fla.、Ga.、Ill.、Ind.、Kan.、Ky.、La.、Md.、Mass.、Mich.、Minn.、Miss.、Mo.、Mont.、Neb.、Nev.、NH、NJ、NM、NY、NC、ND、Okla.、Ore.、Pa.、RI、SC、SD、Tenn.、Vt.、Va.、Wash.、W.Va.、Wis.、Wyo.

数字
~~~~~~~~~
1 から 9 までの数字が使用されます。10 以上の値は数字を使用します。「4 million」または「4 GB」などは例外となります。 また、表やチャートでは数値を使用することもできます。

電話番号
+++++++++++++++

電話番号の形式: 1 (919) 555-0123 x002 および 1 888-GOTTEXT


引用 (引用符の使用と引用の記述)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     "Place the punctuation inside the quotes," the editor said.

ほとんどの場合は、「said」または「say」だけを使用してください。それ以外は、引用の邪魔になり、編集される傾向があるためです。

引用の直後に名前を追加します。
     "I like to write first-person because I like to become the character I'm writing," Wally Lamb said. 

以下のようにはしないでください。
       "I like to write first-person because I like to become the character I'm writing," said Wally Lamb. 


セミコロン
~~~~~~~~~~~~~~~
項目にコンマが含まれている場合は、セミコロンを使用して項目を区切ります。

- Everyday I have coffee, toast, and fruit for breakfast; a salad for lunch; and a peanut butter sandwich, cookies, ice cream, and chocolate cake for dinner.

接続詞副詞 (however、therefore、otherwise、namely、for example) の前にセミコロンを使用します。
「I think; therefore, I am.」のようにします。

文の後のスペース
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
文の後には、シングルスペースのみを使用してください。

時間
~~~~~~~~
* 時刻は「4 p.m」とします。
