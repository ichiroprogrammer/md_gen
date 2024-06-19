# md_gen

## md_genの目的
md_genはコンピュータ言語の解説や使用法等についてのドキュメントを効率的に作成するためのツールである。

## md_genの機能

md_genは、

* [markdownドキュメント内に外部ファイルの抜粋を挿入する](#md_compile)
* [markdownドキュメントが依存する外部ファイのリストを作る](#md_compile_d)
* [markdownドキュメントのインデックスを挿入する](#md_index_inject)
* [markdownドキュメントの見出しからデータベースを作る](#md_make_db)
* [markdownドキュメント内のリンクを解決する](#md_link)
* [markdownドキュメントのインデックスを作る](#md_make_index)
* [markdownドキュメントが参照する外部ファイルをmarkdownドキュメントにまとめる](#md_sample_section)
* [markdownドキュメントを一つのmarkdownファイルにまとめる](#md_join)
* [plant umlドキュメントをpngにレンダリングする](#plant_uml_encode)
* [pngのサイズをチェックする](#png_checker)
* [markdownドキュメントをhtmlに変換する](#md_to_html)

のような機能を持っている。

より詳細な記述方法については[example/o/example.md](example/o/example.md)を参照せよ。


### markdownドキュメント内に外部ファイルの抜粋を挿入する <a id="md_compile"></a>
md_compile.pyは、markdownドキュメント内に外部ファイルの抜粋を挿入する。

	    > cmd/md_compile.py -o OUT in --mds MDS ...

外部ファイルの抜粋を挿入するためには、下記のような記述をmarkdownドキュメント内に書く必要がある。

        // @@@ example/example.mk #0:0 begin

通常、上記のような行はマークダウンのコードブロック記号(```)で囲まれる。
コードブロック開始を表す```の次の行に

        @@@ lineno

と書くことで、このコードブロックに行番号が付加される。

コードの挿入に合わせて、各見出しへのアンカリングも行う。

### markdownドキュメントが依存する外部ファイのリストを作る <a id="md_compile_d"></a>
md_compile.pyは、-Dにより、markdownドキュメントが依存するファイルのリストを作る。

	    > cmd/md_compile.py -D o/MD -o MD_D MD

md_genはmakeから使われることを想定しているため、
この依存関係リストにより効率の良いドキュメント生成ができる。

### markdownドキュメントのインデックスを挿入する <a id="md_index_inject"></a>
md_link.pyは[markdownドキュメント内のリンクを解決する](#md_link)際に、

    <!-- index 3 -->

のようなマークダウンコメントを発見すると、その場所にその章のインデックスを埋め込む。
indexの後の数字はインデックスを生成するレベルを表す。

md_make_db.pyは、
md_compile.pyで処理された複数個のmarkdownドキュメントの見出しからデータベースを生成する。
このデータベースは、インデックスの生成やリンクの解決に使用される。

	    > cmd/md_make_db.py OUT --mds MDS ...

### markdownドキュメント内のリンクを解決する <a id="md_link"></a>
md_link.pyは、データベースから、
md_compile.pyで処理されたのmarkdownドキュメント内のリンクを解決する。

	    > cmd/md_link.py --sec_num -o OUT --db MDS_DB MD

また、これに合わせて各見出しにナンバリングを行う。
これにより生成されたOUT(markdownドキュメント)は、最終生成ドキュメントの一部となる。

### markdownドキュメントのインデックスを作る <a id="md_make_index"></a>
md_make_index.pyは、
md_make_dbで作られたデータベースからインデックス用のmarkdownドキュメントを生成する。

	    > cmd/md_make_index.py --sec_num -o OUT MDS_DB

### markdownドキュメントが参照する外部ファイルをmarkdownドキュメントにまとめる <a id="md_sample_section"></a>
md_sample_section.pyは、引数で渡された全markdownドキュメントが全体を参照する外部ファイルを、
一つの参照用markdownドキュメントとしてまとめる。

        > cmd/md_sample_section.py -o OUT MDS

MDSのmarkdownドキュメントに下記のような記述がある場合、

        "[xxx/yyy/zzz.cpp](---)"

参照用markdownドキュメントにxxx/yyy/zzz.cppの見出しが作られ、その全体がそこに挿入される。

### markdownドキュメントを一つのmarkdownファイルにまとめる <a id="md_join"></a>
md_join.pyは、複数個のmarkdownドキュメントを一つのファイルにまとめる。

        > cmd/md_join.py -o OUT MDS ...

### plant umlドキュメントをpngにレンダリングする <a id="plant_uml_encode"></a>
md_genは、

        http://www.plantuml.com/plantuml/img/

を利用して、 plant umlドキュメントをpngにレンダリングする。
plant_uml_encode.pyは、plant umlドキュメントを、
このレンダリングサーバが受け付ける形式にエンコードし、URLとして出力する。
このURLをwgetに渡すことでpngファイルが得られる。

	    > wget -q $(cmd/plant_uml_encode.py PU) -O PNG

また、下記のようにすることで上記コマンドと同様の結果が得られる。

	    > cmd/plant_uml_encode.py PU -o PNG

### pngのサイズをチェックする <a id="png_checker"></a>
pngの画像が大きすぎると最終生成物であるmarkdownドキュメントやhtmlドキュメントの見栄えが悪くなる。
png_checker.pyは、横幅が700ピクセルを超えるpngファイルが引数として渡されると非0で終了する。

	    > cmd/png_checker.py PNG

### markdownドキュメントをhtmlに変換する <a id="md_to_html"></a>
md_to_html.pyは、pandocを使用し、markdownドキュメントをhtmlドキュメントに変換する。

        > cmd/md_to_html.py --title TITLE -o OUT MD

pandocのバージョン情報は以下の通り。

        > pandoc --version
        pandoc 3.1.2
        Features: +server +lua
        Scripting engine: Lua 5.4
        User data directory: /home/ichiro/.local/share/pandoc
        Copyright (C) 2006-2023 John MacFarlane. Web:  https://pandoc.org
        This is free software; see the source for copying conditions. There is no
        warranty, not even for merchantability or fitness for a particular purpose.

## md_genの動作環境
md_genはpython3で書かれており、下記に示すパッケージを使用している。

### pip
pipはpythonのパッケージ管理ツールである。
これをインストールすることで、パッケージ管理ができるようになる。

        > curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        > sudo python3 get-pip.py

### markdown
下記パッケージは、markdownドキュメント内のソースコードの抜粋にカラーリングを行う。


        > sudo python3 -m pip install markdown      # markdown to html
        > sudo pip install markdown py-gfm Pygments # codeのハイライト

### plantuml
下記パッケージは、plant umlドキュメントをplant umlレンダリングサーバーへ送るためのエンコードを行う。

        > sudo pip install plantuml

### pillow
下記パッケージは、pngファイルの扱うためのものである。

        > sudo pip install pillow

### unicodedata
下記パッケージは、utf-8文字列を扱うためのものである。

        > sudo pip install unicodedata2

### black
下記のパッケージは、pythonの標準コーディングスタイルであるpep8へのフォーマッターである。

        > sudo pip install black        # PEP8フォーマッター

このパッケージのコマンドであるblackは、./tools/format.shから使える。
