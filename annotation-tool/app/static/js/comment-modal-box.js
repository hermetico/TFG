$.fn.comment_modal_box = function() {
    var $buttons = this;

    //$.each($boxes, function(key, value){
    //    $(value).prop('checked', false);
    //})

    $buttons.click(function(evt) {

        var id = $(this).data("id");
        $.getJSON( "/api/picture/" + id, function( data ) {
               var label = $('#modal-picture-label');
               var picture = $('#modal-picture');
               var comment = $('#modal-comment');
               picture.attr('src', picture.data('base-path') + data.path );
               comment.val(data.comment);
               label.attr('class', label.data('base-class') + data.labelid );
               $('#modal-dialog-picture-comment').modal('show');
               $('#modal-comment').focus()
            });
        $('#modal-save').unbind('click')
        $('#modal-save').bind('click', function(){
        var data = {comment: $('#modal-comment').val(), id: id}
            $.post('/api/picture/comment', data, function(){
                $('#modal-dialog-picture-comment').modal('hide');
            });
        })



    });


};