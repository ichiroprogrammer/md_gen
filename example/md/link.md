# リンク
このファイルではリンクについて説明する。

## markdownファイルへのリンク
一連のmarkdownファイル内の見出しにジャンプするためのリンクを張りたい場合、

        [見出し](---)  

のように書く。例えば、

        [外部ファイルの一部抜粋(インデントの変更なし)](---)

と書けば、「[外部ファイルの一部抜粋(インデントの変更なし)](---)」へジャンプできるようになる。

同じ文字列の見出しXXXが複数個ある場合、

        [SEC1|SEC1.1|XXX](---)  

と書くか、XXXが#一つの見出しであった場合、

        [|XXX](---)  

と書くことで一意のXXXを指定できる。

上記ののリンクを解決するためには、cmd/md_make_db.pyを使用し、
すべてのmdファイルから注した見出しをオブジェクトにしたjsonファイルをを生成する必要がある。

## 外部ファイルの参照
code/example_code.cpp全体を参照したい場合、

        "[code/example_code.cpp](---)"

ように書く。これにより、code/example_code.cppの全体がsample_code.mdに引用され、
見出し「"[code/example_code.cpp](---)"」が作ら、上記にそこへのリンクが張られる。

## pngファイルへのリンク
pngファイルをmarkdownドキュメントに取り込みたい場合、

        ![xxx](plant_uml/example.png)  

のように書く。これにより、以下のようにpngを取り込むことができる。

![xxx](plant_uml/example.png)

これはmarkdownの機能であるが、

* cmd/md_compile.py -Dが、このmdファイルのplant_uml/example.pngへの依存を、
  plant_uml/example.puへの依存とする
* Makefileでpuからpngの生成方法を記述する

ことで自動的にpuファイルからpngファイルの生成できる。
また、cmd/md_compile.pyがpngファイルをbase64にエンコードすることで、
markdownドキュメント内に画像ファイルを埋め込む。

## ファイルの生成

### sample_code.mdの生成
[リンク|外部ファイルの参照](---)で述べたsample_code.mdは、
cmd/md_sample_section.pyにより生成される。

### index.mdの生成
cmd/md_make_db.pyが生成したjsonファイルをcmd/md_join.pyに渡すことで、
mdファイルの見出しのインデックスindex.mdを作ることができる。

index.mdに一部の見出しを載せたくない場合(例えば、同じような見出しの羅列)、
md_make_index.pyに--excludeを指定する。例えば、

        --exclude sample_code.md:2

とすることで、 sample_code.mdファイルの###以上の見出しが削除される。
上記のファイル名の部分はpythonの正規表現を使用することができる。

index.mdに一部の見出しに見出しの次の行の抜粋を載せたい場合、上記と同じ様に、

        --excerpt link.md:2

とすることで、link.mdファイルの###の見出しに、その次の行の抜粋が掲載される。


