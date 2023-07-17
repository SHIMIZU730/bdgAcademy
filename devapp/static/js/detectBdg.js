/*staticがjsファイルで記載しても反映されない場合のみhtmlファイルに直書き*/

$(document).ready(function() {
  
  // CSS適用後表示
  $('img.lazyload').each(function() {
      if(this.complete) {
          $(this).addClass('loaded');
      } else {
          $(this).on('load', function() {
              $(this).addClass('loaded');
          });
      }
  });

  // 戻るクリック時(iPhone以外用)
  window.addEventListener('popstate', function(event) {
      $('#loading').css('display', 'none');
  });
  
  // 戻るクリック時(iPhone用)
  window.addEventListener("pageshow", function(event){
    if (event.persisted) {
      // ここにキャッシュ有効時の処理を書く
      window.location.reload();
    }
  });

  $("#searchBdgByText").on("click", function() {
    if($('#inputText').val() == "") {
      alert('ボードゲームを入力してください。');
      return;
    } else {
      
      $('#loading').css('display','flex');
      
      var span2 = document.querySelector('.loader span:nth-child(2)');
      var span3 = document.querySelector('.loader span:nth-child(3)');
      var span4 = document.querySelector('.loader span:nth-child(4)');
  
      var zindex2 = 100;
      var zindex3 = 100;
      var zindex4 = 100;
  
      setInterval(function() {
          span2.style.zIndex = zindex2++;
          span3.style.zIndex = zindex3++;
          span4.style.zIndex = zindex4++;
      }, 1000);
    }
  });
  
  //カメラ・テキスト選択による切替
  $('.btn-group-toggle label').on('click', function(){
    $(this).addClass('active').siblings().removeClass('active');
  });
  
  //カメラ・テキスト選択による切替
  $('input[name="formChoice"]').change(function(){
    if($(this).is(':checked')) {
      if($(this).attr('id') === 'imageIcon') {
        selectImage();
      } else if($(this).attr('id') === 'textIcon') {
        selectText();
      }
    }
  });
  
  // 画像アイコン選択時
  var selectImage = function() {
    $('#textArea').hide();
    $('#imageArea').show();
    
    createCameraBtnTags();
  };
  
  // テキストアイコン選択時
  var selectText = function() {
    $('#imageArea').hide();
    $('#textArea').show();
    
    removeCameraBtnTags();
  };
  

  // カメラ部分タグ生成(iOSカメラ緑ランプの対応)
  var createCameraBtnTags = function() {
    
    $("<label>")
      .attr("id", "lblInputFileId") 
      .addClass("lblInputFile")
      .append(
          $("<input>")
              .attr({
                  type: "file",
                  name: "inputImg",
                  accept: "image/*",
                  capture: "camera",
                  id: "inputImg"
              })
      )
      .append("カメラ起動")
      .prependTo("#cameraBtnPosision");
    
    $("#inputImg").on("change", function(e) {

      var file = $(this).prop('files')[0];
      
      $('.pTagInputFile').text(file.name);
      
      $('#loading').css('display','flex');
      
      // ChatGPT起動
      $("#searchBdg").click();
    });
  }
   // カメラ部タグ削除(iOSカメラ緑ランプ対応)
  var removeCameraBtnTags = function() {
    $("#lblInputFileId").remove();
    $("#inputImg").remove();
  }
  
  var initialize = function() {
    
    selectText();
      
    $('#loading').css('display','none');
    
    // CSSがすべて読み込まれたと仮定してbodyに'loaded'クラスを追加
    $('body.lazyload').addClass('loaded');
  };
  
  // 初期処理
  initialize();
    
});
