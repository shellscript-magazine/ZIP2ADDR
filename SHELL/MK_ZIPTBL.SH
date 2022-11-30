#!/bin/sh -u

######################################################################
#
# MK_ZIPTBL.SH : 「郵便番号→住所」辞書ファイル生成バッチ
#
# Written by t-matsuura@usp-lab.com on 2022-06-06
#
######################################################################


# === 各種定義 =======================================================

homd=$(d=${0%/*}/; [ "_$d" = "_$0/" ] && d='./'; cd "$d.."; pwd)
datd=$homd/DATA
shld=$homd/SHELL
webd=$homd/public_html

url_ken=https://www.post.japanpost.jp/zipcode/dl/oogaki/zip/ken_all.zip
url_jig=https://www.post.japanpost.jp/zipcode/dl/jigyosyo/zip/jigyosyo.zip

export LC_ALL=C

# === 必要な非標準コマンドの存在確認 =================================

nocmds=''
type wget   >/dev/null 2>&1 || { nocmds="$nocmds,wget"  ; }
type gunzip >/dev/null 2>&1 || { nocmds="$nocmds,gunzip"; }
type iconv  >/dev/null 2>&1 || { nocmds="$nocmds,iconv" ; }
if [ -n "$nocmds" ]; then
  echo "${0##*/}: ${nocmds#,} not found. Install them in advance." 1>&2
  exit 1
fi


# === 一般住所郵便番号辞書ファイル生成 ===============================

wget -q -O - "$url_ken"           |
gunzip                            |
tr -d '\r'                        |
iconv -c -f Shift_JIS -t UTF-8    |
tr -d '"'                         |
awk -F , '{print $3,$7,$8,$9}'    > $datd/ziptbl_ken.txt

if [ ! -s $datd/ziptbl_ken.txt ]; then
  echo "${0##*/}: Failed to make zip_ken.txt" 1>&2; exit 1
fi


# === 事業所用郵便番号辞書ファイル生成 ===============================

wget -q -O - "$url_jig"           |
gunzip                            |
tr -d '\r'                        |
iconv -c -f Shift_JIS -t UTF-8    |
tr -d '"'                         |
awk -F , '{print $8,$4,$5,$6 $7}' > $datd/ziptbl_jig.txt

if [ ! -s $datd/ziptbl_jig.txt ]; then
  echo "${0##*/}: Failed to make zip_ken.txt" 1>&2; exit 1
fi


# === 正常終了 =======================================================

exit 0
