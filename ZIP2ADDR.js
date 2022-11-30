//////////////////////////////////////////////////////////////////////
//
// ZIP2ADDR.js : 郵便番号検索用 クライアントサイドプログラム
//
// Written by t-matsuura@usp-lab.com on 2022-06-08
//
//////////////////////////////////////////////////////////////////////


// ===== XHRオブジェクト作成 =========================================

function createXMLHttpRequest(){
  if(window.XMLHttpRequest){return new XMLHttpRequest()}
  if(window.ActiveXObject){
    try{return new ActiveXObject("Msxml2.XMLHTTP.6.0")}catch(e){}
    try{return new ActiveXObject("Msxml2.XMLHTTP.3.0")}catch(e){}
    try{return new ActiveXObject("Microsoft.XMLHTTP")}catch(e){}
  }
  return false;
}


// ===== 検索リクエスト ==============================================

function zip2addr() {
  var url;
  var zipcode;      // フォームから取得した郵便番号文字列の格納用
  var xhr;          // XML HTTP Requestオブジェクト格納用

  // --- 1)郵便番号欄チェック ----------------------------------------
  if (! document.getElementById('zipcode1').value.match(/^([0-9]{3})$/)) {
    alert('郵便番号(前の3桁)が正しくありません');
    return;
  }
  zipcode  = RegExp.$1;
  if (! document.getElementById('zipcode2').value.match(/^([0-9]{4})$/)) {
    alert('郵便番号(後の4桁)が正しくありません');
    return;
  }
  zipcode += RegExp.$1;

  // --- 3)Ajaxコール ------------------------------------------------
  xhr = createXMLHttpRequest();
  if (xhr) {
    url  = 'ZIP2ADDR.AJAX.cgi?zipcode='+zipcode;
    url += '&dummy='+parseInt((new Date)/1); // ブラウザcache対策

    xhr.open('GET', url, true);
    xhr.onreadystatechange = function(){zip2addr_callback(xhr)};
    xhr.send(null);
  }

  // --- 4)正常終了 --------------------------------------------------
  return;
}


// ===== 検索結果ハメ込み ============================================

function zip2addr_callback(xhr) {

  var e;            // 汎用変数(エレメント用)

  // --- 1)アクセス成功で呼び出されたのでないなら即終了 --------------
  if (xhr.readyState != 4) {return;}
  if (xhr.status == 0    ) {return;} // ステータスが0の場合は部座ウザによる
  if      (xhr.status == 400) {      // 中断の可能性があるので無視
    alert('郵便番号が正しくありません');
    return;
  }
  else if (xhr.status != 200) {
    alert('アクセスエラー(' + xhr.status + ')');
    return;
  }

  // --- 2)サーバーから返された部分HTMLで差し替える ----------------------
  e = document.getElementById('adress123');
  if (!e) {alert('エラー: 住所欄が存在しない!'); return;}
  e.innerHTML = xhr.responseText;

  // --- 3)正常終了 --------------------------------------------------
  return;
}
