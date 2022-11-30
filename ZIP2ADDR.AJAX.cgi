#!/bin/sh -u

######################################################################
#
# ZIP2ADDR.AJAX.cgi : 「郵便番号→住所」の検索を実行する
#
# Written by t-matsuura@usp-lab.com on 2022-06-08
#
######################################################################


# === 各種定義 =======================================================

homd=$(d=${0%/*}/; [ "_$d" = "_$0/" ] && d='./'; cd "$d.."; pwd)
datd=$homd/DATA
shld=$homd/SHELL
webd=$homd/public_html

export LC_ALL=C
#PATH="/home/t-matsuura/usp/bin:$PATH" # Tukubaiコマンドを、自分のホームdir等に
                                       # インストールした場合はそこにPATHを通す


# === エラー関数 =====================================================

exit_trap() {
  set -- ${1:-} $?  # $? is set as $1 if no argument given
  trap '' EXIT HUP INT QUIT PIPE ALRM TERM
  [ -d "${tmpd:-}" ] && rm -rf "$tmpd"
  trap -  EXIT HUP INT QUIT PIPE ALRM TERM
  exit $1
}

error500_exit() {
  echo 'Status: 500 Internal Server Error'
  echo 'Content-Type: text/plain'
  echo
  echo '500 Internal Server Error'
  echo "($@)"
  exit 1
}

error400_exit() {
  echo 'Status: 400 Bad Request'
  echo 'Content-Type: text/plain'
  echo
  echo '400 Bad Request'
  echo "($@)"
  exit 1
}


# === 一時ディレクトリ作成 =========================================

trap 'exit_trap' EXIT HUP INT QUIT PIPE ALRM TERM
tmpd=$(mktemp -d -t "_${0##*/}.$$.XXXXXXXXXXX")
[ -d "$tmpd" ] || error500_exit 'Failed to mktemp'


# === 7桁の郵便番号を取得・正当性チェック ============================

printf '%s\n' "${QUERY_STRING:-}" |
cgi-name                          > $tmpd/cgivars

zip=$(nameread zipcode $tmpd/cgivars)
printf '%s\n' "$zip" | grep -qE '^[0-9]{7}$' || error400_exit 'Invalid zipcode'


# === 検索 ===========================================================

echo $homd/DATA/ziptbl* | grep -qF '*' && error500_exit 'No table files exist'

cat $homd/DATA/ziptbl*                 |
awk '$1=="'"$zip"'"{print "pref",$2;
                    print "city",$3;
                    print "town",$4;}' > $tmpd/address123
[ -s $tmpd/address123 ] || error400_exit 'No address found'


# === 結果出力（部分HTMLで） =========================================

echo 'Content-Type: text/html; charset=utf-8'
echo 'Cache-Control: private, no-store, no-cache, must-revalidate'
echo 'Pragma: no-cache'
echo

formhame $webd/ZIP2ADDR.html $tmpd/address123 |
sed -n '/BEGIN ADDRESS123/,/END ADDRESS123/p'


# === 正常終了 =======================================================

[ -d "${tmpd:-}" ] && rm -rf "$tmpd"
exit 0
