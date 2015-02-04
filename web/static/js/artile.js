/**
 * Created with PyCharm.
 * User: chenyu
 * Date: 14-8-27
 * Time: 上午11:36
 * To change this template use File | Settings | File Templates.
 */

$(function () {
    $("#right_container").load("/blog/right/container");
})

function classfiy_article(classfiy_id)
{
    $("#article_container").load("/blog/load/article?id="+classfiy_id);
    $(window).scrollTop(0);
}

function Next(id) {
    $.ajax({
        type: "get",
        url: '/blog/article/next',
        data: { id: id},
        success: function (msg) {
            if (msg != 'error') {
                window.location.href = "/blog/article/details?id=" + msg;
            }
            else {
                $("#next_warn").show();
            }
        }
    })
}

function Previous(id) {
    $.ajax({
        type: "get",
        url: '/blog/article/previous',
        data: { id: id},
        success: function (msg) {
            if (msg != 'error') {
                window.location.href = "/blog/article/details?id=" + msg;
            }
            else {
                $("#previous_warn").show();
            }
        }
    })
}

function addmsg(id) {
    $.ajax({
        type: "post",
        url: '/blog/add/comment',
        data: {
            id: id,
            nike_name: $("#nike_name").val(),
            email: $("#email").val(),
            web_url: $("#web_url").val(),
            msg: $("#msg").val()
        },
        success: function (msg) {
            $("#comment").load('/blog/load/comment?id=' + id);
        }
    })
}

function article_click(id) {
    window.location.href = "/blog/article/details?id=" + id;
}