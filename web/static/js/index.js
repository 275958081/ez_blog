/**
 * Created with PyCharm.
 * User: chenyu
 * Date: 14-8-27
 * Time: 下午1:10
 * To change this template use File | Settings | File Templates.
 */
$(function () {
    $("#article_container").load("/blog/load/article?id=0");
    $("#right_container").load("/blog/right/container");
    $(".zxx_text_overflow_1").val();

})

PAGE = 1
function callback(data) {
    IS_end = 'Flase';
    for (i = 0; i < data.length; i++) {
        item = data[i]
        IS_end = item.is_end

        html = '<div class="panel panel-primary"  onclick="article_click(' + item.id + ');">\
            <div class="panel-heading mousemove">\
                <h3 class="panel-title">' + item.title + '</h3></div>\
            <div class="panel-body">' + item.content + '</div><span class="article_inf">'+item.time+' 评论('+item.comment_num+')</span></div>'
        $('#article_container_more').append(html);
    }
    if (IS_end == 'True') {
        $("#more").html("no more ==!");
    }
}

function more(classfiy_id){
    PAGE += 1;
    $.get("/blog/article/list?page=" + PAGE+'&classfiy_id='+classfiy_id, callback, 'json');
}

function article_click(id) {
    window.location.href = "/blog/article/details?id=" + id;
}

function classfiy_article(classfiy_id)
{
     PAGE = 1;
    $("#article_container").load("/blog/load/article?id="+classfiy_id);
    $(window).scrollTop(0);
}