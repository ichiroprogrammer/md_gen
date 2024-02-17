<!-- md/sample_code.md -->
# Sample Code <a id="SS_4"></a>
## C++ <a id="SS_4_1"></a>
### code/example_code.cpp <a id="SS_4_1_1"></a>
```c++
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



