$(document).ready(function () {
    $("input.comment-delete-btn").addClass("fa").val("");
    // ADD COMMENT //
    $('.add-comment-form').submit(function (event) {
        event.preventDefault();
        var form = $(this);
        var data = new FormData(form.get(0));
        $.ajax({
                url: $('.add-comment-form').attr('action'),
                type: "POST",
                data: data,
                cache: false,
                processData: false,
                contentType: false,
                success: function (json) {
                    if (json['success'] == 0) {
                        errors = ""
                        for (var err in json['error']) {
                            errors += "" + err + ": " + json['error'][err] + "\n"
                        }
                    }
                    html = "<div id='comment-div-" + json['id'] + "'>" + json['html'] + "</div>"
                    $('.comments').append(html);
                    $('textarea#id_comment').val(" ");

                }
            }
        );
    });

    // DELETE COMMENT //
    $('.comments-wrapper').on('click', '.comment-delete-btn', function (event) {
        event.preventDefault();
        var id = $(this).attr('data-id');
        $.ajax({
            type: "GET",
            url: $('.comment-delete-form').attr('action'),
            data: {'id': id, 'csrfmiddlewaretoken': $("#csrf").attr('value')},
            success: function (data) {
                if (data['success'] == 1) {
                    $('#comment-div-' + id).remove()
                }
                else {
                    alert("ليس لديك إذن بحذف هذا التعليق")
                }
            }
        });
    });

    // COMMENT EDIT //
    $('.comments-wrapper').on('click', '.comment-edit-class', function (event) {

        var id = $(this).attr('data-id');
        $('#comment-edit-' + id).show();
        $('#comment-' + id).hide();
    });

    $('.comments-wrapper').on('submit', '.edit-form', function (event) {
        event.preventDefault();
        var form = $(this);
        var data = form.serialize();
        var id = $(this).attr('data-id');
        var comment = document.getElementById('comment-' + id);
        var error = document.getElementById('edit-form-errors');
        $.ajax({
            type: "POST",
            url: form.attr('action'),
            data: data,

            success: function (data) {
                json = JSON.parse(data);
                if (json.success == 1) {
                    comment.innerHTML = $('#input-comment-' + id).val();
                    $('#comment-edit-' + id).hide();
                    $('#comment-' + id).show();
                } else if (json.success == 0) {
                    errors = ""
                    for (var err in json.error) {
                        errors += "" + json.error[err] + "\n";
                    }
                    error.innerHTML = errors;
                }
            },
            dataType: 'html'
        });
    });


    // LIKE UNLIKE COMMENT //
    $('.comments-wrapper').on('click', '.like-comment-btn', function () {
        var id = $(this).attr('data-id');
        if ($(this).attr('data-like') == 'like') {
            $.ajax({
                type: "GET",
                url: '/comments/like',
                data: {'comment_id': id},
                success: function (data) {
                    if (data['success'] == 1) {
                        $('#like-btn-' + id).attr('data-like', 'liked');
                        $('#like-btn-' + id + ' i').removeClass("far fa-heart").addClass('fas fa-heart');
                        $('#likes-count-' + id).text("اعجاب: " + data['likes_count']);
                    } else {
                        alert(data['error']);
                    }
                }
            });
        } else {
            $.ajax({
                type: "GET",
                url: '/comments/unlike',
                data: {'comment_id': id},
                success: function (data) {
                    if (data['success'] == 1) {
                        $('#like-btn-' + id).attr('data-like', 'like');
                        $('#like-btn-' + id + ' i').removeClass("fas fa-heart").addClass('far fa-heart');
                        $('#likes-count-' + id).text("اعجاب: " + data['likes_count']);
                    } else {
                        alert(data['error']);
                    }
                }
            });
        }
    });

    $('textarea').each(function () {
        this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
    }).on('input', function () {
        this.style.height = (this.scrollHeight) + 'px';
    });

    $('#id_comment, #comment-form-label').focus(function () {
        $('#comment-form-label').css('top', '-40%');
        $('#comment-form-label').css('color', 'black')

    })

    $('#id_comment, #comment-form-label').focusout(function () {
        $('#comment-form-label').css('top', '10%');
        $('#comment-form-label').css('color', 'gray')
    })


})