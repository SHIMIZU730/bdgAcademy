$(document).ready(function() {
    
    // $(window).on('load', function() {
        
    // });
    // 初期処理
    var initialize = function() {
        // 初期表示でローディングを消しておく
        $('#loading').css('display','none');
        
        // CSSがすべて読み込まれたと仮定してbodyに'loaded'クラスを追加
        $('body.lazyload').addClass('loaded');
    };
    
    // 初期処理
    initialize();
});