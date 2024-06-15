# bool型
* hehe

```.cpp
        // @@@ data/src_3.cpp #1:0 begin
```

* hehe3

```.cpp
        // @@@ data/src_4.cpp #0:0 begin
```

```test/data_pu/rectangle_square.pu
@startuml

class Rectangle {
    +SetX()
    +SetY()
    -set_x()
    -set_y()
}

class Square {
    -set_x()
    -set_y()
}

Rectangle <|-down- Square

@enduml
```

* vimファイル
"[vim_config/xxx.vim](---)"


