# インデックス
&emsp; 1 [イントロダクション](#SS_1)  
&emsp; 2 [外部ファイルの参照](#SS_2)  
&emsp;&emsp; 2.1 [外部ファイルの一部抜粋(インデントの変更なし)](#SS_2_1)  
&emsp;&emsp; 2.2 [外部ファイルの一部抜粋(インデントを左1シフト)](#SS_2_2)  
&emsp;&emsp; 2.3 [外部ファイルの一部抜粋(不要コードの削除)](#SS_2_3)  
&emsp;&emsp; 2.4 [外部ファイルの一部の連続抜粋(不要コードを「...」に変換)](#SS_2_4)  
&emsp;&emsp; 2.5 [外部ファイルの一部の再抜粋(改行コード1追加)](#SS_2_5)  
&emsp;&emsp; 2.6 [外部ファイルの一部の再抜粋(インデントを左1シフト、改行コード1追加)](#SS_2_6)  
&emsp; 3 [リンク](#SS_3)  
&emsp;&emsp; 3.1 [markdownファイルへのリンク](#SS_3_1)  
&emsp;&emsp; 3.2 [外部ファイルの参照](#SS_3_2)  
&emsp;&emsp; 3.3 [pngファイルへのリンク](#SS_3_3)  
&emsp;&emsp; 3.4 [ファイルの生成](#SS_3_4)  
&emsp;&emsp;&emsp; 3.4.1 [sample_code.mdの生成](#SS_3_4_1) [リンク|外部ファイルの参照](---)で述べたsample_code.md ...  
&emsp;&emsp;&emsp; 3.4.2 [index.mdの生成](#SS_3_4_2) cmd/md_make_db.pyが生成したjsonファイルをcmd/md_join.py ...  
&emsp; 4 [Sample Code](#SS_4)  
&emsp;&emsp; 4.1 [C++](#SS_4_1)  
  
  
<!-- md/intro.md -->
# 1 イントロダクション <a id="SS_1"></a>
この例ではmd_genの使い方について説明する。

実際にmd_genを使用してドキュメントを生成するのであれば、
このexample/ディレクトリ配下のファイルを元にすればよい。
その場合、md/oやo/の配下にあるファイルはMakefileによるビルド生成物であるため、
バージョン管理システムには登録しない方が良いだろう。


<!-- md/ref.md -->
# 2 外部ファイルの参照 <a id="SS_2"></a>
外部ファイルの参照やその加工について説明する。

## 2.1 外部ファイルの一部抜粋(インデントの変更なし) <a id="SS_2_1"></a>
markdownファイル内に下記のように書くことで

        @@@ code/example_code.cpp #0:0 begin  

下記のように外部ファイルの一部をmarkdownドキュメント内に埋め込むことができる
(ただし、この記述の直前には正規表現で表すと[^@ ]+となる文字列が必要)。

```.cpp
    //  code/example_code.cpp 3

    class Polymorphic_Base {  // ポリモーフィックな基底クラス
    public:
        virtual ~Polymorphic_Base() = default;
    };

    class Polymorphic_Derived : public Polymorphic_Base {  // ポリモーフィックな派生クラス
    };
```

この作用については、

* md/ref.md(オリジナルのファイル)
* md/o/ref.md(cmd/md_compile.pyにより変更されたファイル)
* o/ref.md(cmd/md_compile.pyにより変更されたファイル)
* code/example_code.cpp(一部を抜粋されたファイル)

上記のファイルを見ることで理解できる。

## 2.2 外部ファイルの一部抜粋(インデントを左1シフト) <a id="SS_2_2"></a>
markdownファイル内に下記のように書くことで

        @@@ code/example_code.cpp #0:1 begin -1

下記のように外部ファイルの一部を左1シフトしてmarkdownドキュメント内に埋め込むことができる。

```.cpp
    //  code/example_code.cpp 17

    Polymorphic_Base    b;
    Polymorphic_Derived d;

    Polymorphic_Base& b_ref_d = d;
    Polymorphic_Base& b_ref_b = b;

    // std::type_infoの比較
    ASSERT_EQ(typeid(b_ref_d), typeid(d));
    ASSERT_EQ(typeid(b_ref_b), typeid(b));
```

## 2.3 外部ファイルの一部抜粋(不要コードの削除) <a id="SS_2_3"></a>
markdownファイル内に下記のように書くことで

        @@@ code/example_code.cpp #0:2 begin -1

下記のように外部ファイルの一部を左1シフトしてmarkdownドキュメント内に埋め込むことができる。

```.cpp
    //  code/example_code.cpp 29

    // ポインタへのdynamic_cast
    Polymorphic_Derived* d_ptr = dynamic_cast<Polymorphic_Derived*>(&b_ref_d);
    ASSERT_EQ(d_ptr, &d);

    Polymorphic_Derived* d_ptr2 = dynamic_cast<Polymorphic_Derived*>(&b_ref_b);
    ASSERT_EQ(d_ptr2, nullptr);  // キャストできない場合、nullptrが返る
```

抜粋したファイルには、不要コードを削除している。
削除の仕組みは、code/example_code.cppを参照すればわかる。

## 2.4 外部ファイルの一部の連続抜粋(不要コードを「...」に変換) <a id="SS_2_4"></a>
markdownファイル内に外部ファイルを抜粋するための記述を連続して行うことで、

    // @@@ code/example_code.cpp 行数

のような不要な行がコード内に挿入されないようにできる。

```.cpp
    //  code/example_code.cpp 54

    template <typename FUNC>
    class ScopedGuard {
    public:
        explicit ScopedGuard(FUNC f) : f_(f)
        {
            // f()がill-formedにならず、その戻りがvoidでなければならない
            static_assert(std::is_same<decltype(f()), void>::value, "f() must return void");
        }

        ~ScopedGuard() { f_(); }

        ...

    private:
        FUNC f_;
    };
```

## 2.5 外部ファイルの一部の再抜粋(改行コード1追加) <a id="SS_2_5"></a>
前機能は、再抜粋のためのものであるが、その場合

    // @@@ code/example_code.cpp 行数

の行の後に改行したい場合がある。これに対処するためには、

        @@@ code/example_code.cpp #2:1 begin 0 1

のように書く。

```.cpp
    //  code/example_code.cpp 62

            // f()がill-formedにならず、その戻りがvoidでなければならない
            static_assert(std::is_same<decltype(f()), void>::value, "f() must return void");
```

## 2.6 外部ファイルの一部の再抜粋(インデントを左1シフト、改行コード1追加) <a id="SS_2_6"></a>
上記例のように、インデントが不自然になる場合、

        @@@ code/example_code.cpp #2:1 begin -2 1

のように書く。

```.cpp
    //  code/example_code.cpp 62

    // f()がill-formedにならず、その戻りがvoidでなければならない
    static_assert(std::is_same<decltype(f()), void>::value, "f() must return void");
```


<!-- md/link.md -->
# 3 リンク <a id="SS_3"></a>
このファイルではリンクについて説明する。

## 3.1 markdownファイルへのリンク <a id="SS_3_1"></a>
一連のmarkdownファイル内の見出しにジャンプするためのリンクを張りたい場合、

        [見出し](---)  

のように書く。例えば、

        [外部ファイルの一部抜粋(インデントの変更なし)](---)

と書けば、「[外部ファイルの一部抜粋(インデントの変更なし)](#SS_2_1)」へジャンプできるようになる。

同じ文字列の見出しXXXが複数個ある場合、

        [SEC1|SEC1.1|XXX](---)  

と書くか、XXXが#一つの見出しであった場合、

        [|XXX](---)  

と書くことで一意のXXXを指定できる。

上記ののリンクを解決するためには、cmd/md_make_db.pyを使用し、
すべてのmdファイルから注した見出しをオブジェクトにしたjsonファイルをを生成する必要がある。

## 3.2 外部ファイルの参照 <a id="SS_3_2"></a>
code/example_code.cpp全体を参照したい場合、

        [code/example_code.cpp](---)

ように書く。これにより、code/example_code.cppの全体がsample_code.mdに引用され、
見出し「[code/example_code.cpp](#SS_4_1_1)」が作ら、上記にそこへのリンクが張られる。

## 3.3 pngファイルへのリンク <a id="SS_3_3"></a>
pngファイルをmarkdownドキュメントに取り込みたい場合、

        ![xxx](plant_uml/example.png)  

のように書く。これにより、以下のようにpngを取り込むことができる。

<!-- pu:plant_uml/example.pu--><p><img src="data:image/png;base64,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" /></p>

これはmarkdownの機能であるが、

* cmd/md_compile.py -Dが、このmdファイルのplant_uml/example.pngへの依存を、
  plant_uml/example.puへの依存とする
* Makefileでpuからpngの生成方法を記述する

ことで自動的にpuファイルからpngファイルの生成できる。
また、cmd/md_compile.pyがpngファイルをbase64にエンコードすることで、
markdownドキュメント内に画像ファイルを埋め込む。

## 3.4 ファイルの生成 <a id="SS_3_4"></a>

### 3.4.1 sample_code.mdの生成 <a id="SS_3_4_1"></a>
[外部ファイルの参照](#SS_3_2)で述べたsample_code.mdは、
cmd/md_sample_section.pyにより生成される。

### 3.4.2 index.mdの生成 <a id="SS_3_4_2"></a>
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


<!-- md/sample_code.md -->
# 4 Sample Code <a id="SS_4"></a>
## 4.1 C++ <a id="SS_4_1"></a>
### 4.1.1 code/example_code.cpp <a id="SS_4_1_1"></a>
```cpp
          1 #include <exception>
          2 
          3 // @@@ sample begin 0:0
          4 
          5 class Polymorphic_Base {  // ポリモーフィックな基底クラス
          6 public:
          7     virtual ~Polymorphic_Base() = default;
          8 };
          9 
         10 class Polymorphic_Derived : public Polymorphic_Base {  // ポリモーフィックな派生クラス
         11 };
         12 // @@@ sample end
         13 
         14 namespace {
         15 TEST(TermExplanation, RTTI_polymorphic)
         16 {
         17     // @@@ sample begin 0:1
         18 
         19     Polymorphic_Base    b;
         20     Polymorphic_Derived d;
         21 
         22     Polymorphic_Base& b_ref_d = d;
         23     Polymorphic_Base& b_ref_b = b;
         24 
         25     // std::type_infoの比較
         26     ASSERT_EQ(typeid(b_ref_d), typeid(d));
         27     ASSERT_EQ(typeid(b_ref_b), typeid(b));
         28     // @@@ sample end
         29     // @@@ sample begin 0:2
         30 
         31     // ポインタへのdynamic_cast
         32     Polymorphic_Derived* d_ptr = dynamic_cast<Polymorphic_Derived*>(&b_ref_d);
         33     ASSERT_EQ(d_ptr, &d);
         34 
         35     Polymorphic_Derived* d_ptr2 = dynamic_cast<Polymorphic_Derived*>(&b_ref_b);
         36     ASSERT_EQ(d_ptr2, nullptr);  // キャストできない場合、nullptrが返る
         37     // @@@ sample end
         38 
         39     // @@@ sample begin 0:3
         40 
         41     // リファレンスへのdynamic_cast
         42     Polymorphic_Derived& d_ref = dynamic_cast<Polymorphic_Derived&>(b_ref_d);
         43     ASSERT_EQ(&d_ref, &d);
         44 
         45     SUPPRESS_WARN_BEGIN;               // @@@ delete
         46     SUPPRESS_WARN_CLANG_UNUSED_VALUE;  // @@@ delete
         47     // キャストできない場合、エクセプションのが発生する
         48     ASSERT_THROW(dynamic_cast<Polymorphic_Derived&>(b_ref_b), std::bad_cast);
         49     // @@@ sample end
         50     SUPPRESS_WARN_END;
         51 }
         52 }  // namespace
         53 
         54 // @@@ sample begin 2:0
         55 
         56 template <typename FUNC>
         57 class ScopedGuard {
         58 public:
         59     explicit ScopedGuard(FUNC f) : f_(f)
         60     {
         61         // @@@ sample end
         62         // @@@ sample begin 2:1
         63         // f()がill-formedにならず、その戻りがvoidでなければならない
         64         static_assert(std::is_same<decltype(f()), void>::value, "f() must return void");
         65         // @@@ sample end
         66         // @@@ sample begin 2:2
         67     }
         68 
         69     ~ScopedGuard() { f_(); }
         70 
         71     // @@@ ignore begin
         72 
         73     ~ScopedGuard() { f_(); }
         74     ScopedGuard(ScopedGuard const&) = delete;     // copyは禁止
         75     ScopedGuard(ScopedGuard&&)      = default;    // moveは認める
         76     void operator=(ScopedGuard const&) = delete;  // copyは禁止
         77     // @@@ ignore end
         78 
         79 private:
         80     FUNC f_;
         81 };
         82 // @@@ sample end
```



