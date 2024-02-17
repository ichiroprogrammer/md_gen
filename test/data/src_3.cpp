#include <list>
#include "header_1.h"
#include "header_2.h"

void f()
{
    // @@@ sample begin 0:0

    int32_t* a = 0;        // NG   オールドスタイル
    int32_t* b = NULL;     // NG   C90の書き方
    int32_t* c = nullptr;  // OK   C++11

    // @@@ sample end

    // @@@ sample begin 0:1

    IGNORE_UNUSED_VAR(a);
    // @@@ ignore begin
    IGNORE_UNUSED_VAR(b);
    IGNORE_UNUSED_VAR(c);
    // @@@ ignore end
    // @@@ sample end
}


void g()
{
    // @@@ sample begin 1:0
    // clang-format off

    bool b = false;

    ASSERT_EQ(1, ++b);  // @@@ delete

    // clang-format on
    bool c;
    // @@@ sample end
}

