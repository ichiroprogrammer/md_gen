# 外部ファイルの参照
外部ファイルの参照やその加工について説明する。

## 外部ファイルの一部抜粋(インデントの変更なし)
markdownファイル内に下記のように書くことで

        @@@ code/example_code.cpp #0:0 begin  

下記のように外部ファイルの一部をmarkdownドキュメント内に埋め込むことができる
(ただし、この記述の直前には正規表現で表すと[^@ ]+となる文字列が必要)。

```.cpp
    // @@@ code/example_code.cpp #0:0 begin
```

この作用については、

* md/ref.md(オリジナルのファイル)
* md/o/ref.md(cmd/md_compile.pyにより変更されたファイル)
* o/ref.md(cmd/md_compile.pyにより変更されたファイル)
* code/example_code.cpp(一部を抜粋されたファイル)

上記のファイルを見ることで理解できる。

## 外部ファイルの一部抜粋(インデントを左1シフト)
markdownファイル内に下記のように書くことで

        @@@ code/example_code.cpp #0:1 begin -1

下記のように外部ファイルの一部を左1シフトしてmarkdownドキュメント内に埋め込むことができる。

```.cpp
    // @@@ code/example_code.cpp #0:1 begin -1
```

## 外部ファイルの一部抜粋(不要コードの削除)
markdownファイル内に下記のように書くことで

        @@@ code/example_code.cpp #0:2 begin -1

下記のように外部ファイルの一部を左1シフトしてmarkdownドキュメント内に埋め込むことができる。

```.cpp
    // @@@ code/example_code.cpp #0:2 begin -1
```

抜粋したファイルには、不要コードを削除している。
削除の仕組みは、code/example_code.cppを参照すればわかる。

## 外部ファイルの一部の連続抜粋(不要コードを「...」に変換)
markdownファイル内に外部ファイルを抜粋するための記述を連続して行うことで、

    // @@@ code/example_code.cpp 行数

のような不要な行がコード内に挿入されないようにできる。

```.cpp
    // @@@ code/example_code.cpp #2:0 begin
    // @@@ code/example_code.cpp #2:1 begin
    // @@@ code/example_code.cpp #2:2 begin
```

## 外部ファイルの一部の再抜粋(改行コード1追加)
前機能は、再抜粋のためのものであるが、その場合

    // @@@ code/example_code.cpp 行数

の行の後に改行したい場合がある。これに対処するためには、

        @@@ code/example_code.cpp #2:1 begin 0 1

のように書く。

```.cpp
    // @@@ code/example_code.cpp #2:1 begin 0 1
```

## 外部ファイルの一部の再抜粋(インデントを左1シフト、改行コード1追加)
上記例のように、インデントが不自然になる場合、

        @@@ code/example_code.cpp #2:1 begin -2 1

のように書く。

```.cpp
    // @@@ code/example_code.cpp #2:1 begin -2 1
```


