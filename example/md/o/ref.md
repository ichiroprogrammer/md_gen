<!-- md/ref.md -->
# 外部ファイルの参照 <a id="SS_2"></a>
外部ファイルの参照やその加工について説明する。

## 外部ファイルの一部抜粋(インデントの変更なし) <a id="SS_2_1"></a>
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

## 外部ファイルの一部抜粋(インデントを左1シフト) <a id="SS_2_2"></a>
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

## 外部ファイルの一部抜粋(不要コードの削除) <a id="SS_2_3"></a>
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

## 外部ファイルの一部の連続抜粋(不要コードを「...」に変換) <a id="SS_2_4"></a>
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

## 外部ファイルの一部の再抜粋(改行コード1追加) <a id="SS_2_5"></a>
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

## 外部ファイルの一部の再抜粋(インデントを左1シフト、改行コード1追加) <a id="SS_2_6"></a>
上記例のように、インデントが不自然になる場合、

        @@@ code/example_code.cpp #2:1 begin -2 1

のように書く。

```.cpp
    //  code/example_code.cpp 62

    // f()がill-formedにならず、その戻りがvoidでなければならない
    static_assert(std::is_same<decltype(f()), void>::value, "f() must return void");
```


