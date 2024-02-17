# md_genの使い方の例を書く
* REF_BEGINの拡張 \d+:\d+: -> \d+:\d+(:\d+)?の単体テストがない
  REF_BEGINと下記のコードが被っている
        after_index = re.compile(" *#\d+:\d+(:\d+)? begin *(-?\d)? *(\d)?")  # REF_BEGIN参照
