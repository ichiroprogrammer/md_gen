#include <exception>

// @@@ sample begin 0:0

class Polymorphic_Base {  // ポリモーフィックな基底クラス
public:
    virtual ~Polymorphic_Base() = default;
};

class Polymorphic_Derived : public Polymorphic_Base {  // ポリモーフィックな派生クラス
};
// @@@ sample end

namespace {
TEST(TermExplanation, RTTI_polymorphic)
{
    // @@@ sample begin 0:1

    Polymorphic_Base    b;
    Polymorphic_Derived d;

    Polymorphic_Base& b_ref_d = d;
    Polymorphic_Base& b_ref_b = b;

    // std::type_infoの比較
    ASSERT_EQ(typeid(b_ref_d), typeid(d));
    ASSERT_EQ(typeid(b_ref_b), typeid(b));
    // @@@ sample end
    // @@@ sample begin 0:2

    // ポインタへのdynamic_cast
    Polymorphic_Derived* d_ptr = dynamic_cast<Polymorphic_Derived*>(&b_ref_d);
    ASSERT_EQ(d_ptr, &d);

    Polymorphic_Derived* d_ptr2 = dynamic_cast<Polymorphic_Derived*>(&b_ref_b);
    ASSERT_EQ(d_ptr2, nullptr);  // キャストできない場合、nullptrが返る
    // @@@ sample end

    // @@@ sample begin 0:3

    // リファレンスへのdynamic_cast
    Polymorphic_Derived& d_ref = dynamic_cast<Polymorphic_Derived&>(b_ref_d);
    ASSERT_EQ(&d_ref, &d);

    SUPPRESS_WARN_BEGIN;               // @@@ delete
    SUPPRESS_WARN_CLANG_UNUSED_VALUE;  // @@@ delete
    // キャストできない場合、エクセプションのが発生する
    ASSERT_THROW(dynamic_cast<Polymorphic_Derived&>(b_ref_b), std::bad_cast);
    // @@@ sample end
    SUPPRESS_WARN_END;
}
}  // namespace

// @@@ sample begin 2:0

template <typename FUNC>
class ScopedGuard {
public:
    explicit ScopedGuard(FUNC f) : f_(f)
    {
        // @@@ sample end
        // @@@ sample begin 2:1
        // f()がill-formedにならず、その戻りがvoidでなければならない
        static_assert(std::is_same<decltype(f()), void>::value, "f() must return void");
        // @@@ sample end
        // @@@ sample begin 2:2
    }

    ~ScopedGuard() { f_(); }

    // @@@ ignore begin

    ~ScopedGuard() { f_(); }
    ScopedGuard(ScopedGuard const&) = delete;     // copyは禁止
    ScopedGuard(ScopedGuard&&)      = default;    // moveは認める
    void operator=(ScopedGuard const&) = delete;  // copyは禁止
    // @@@ ignore end

private:
    FUNC f_;
};
// @@@ sample end
