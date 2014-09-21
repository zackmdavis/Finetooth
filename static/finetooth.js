function tag(pk, label) {
    $.ajax({
	url: "/tag/" + pk + "/",
	type: "POST",
	data: {
	    label: label
	},
	success: function(data, status, jqxhr) {
	    renderNewTag(label)
	}
    });
}

function renderNewTag(label) {
    var tags_div = $('#tags')
    tags_div.append($('<span/>').text(label).addClass("tag").hide().fadeIn(400));
    tags_div.append($('<span/>').html(' &bull; '));
}

function setTagSubmitHandler() {
    $('#new-tag-submit').on("click", function(event) {
	tag($(this).data('pk'), $('#new-tag-label').val());
    });
}

function vote(kind, pk, selection, value) {
    $.ajax({
	url: "/vote/" + kind + "/" + pk + "/",
	type: "POST",
	data: {
	    value: value,
	    selection: selection
	}
    });
}

function setVotingClickHandlers() {
    $('.upvote').click(function(event) {
	var upvoteElement = $(this);
	vote(upvoteElement.data("kind"), upvoteElement.data("pk"),
	     window.getSelection().toString(), 1);
	return true;
    });
    $('.downvote').click(function(event) {
	var downvoteElement = $(this);
	vote(downvoteElement.data("kind"), downvoteElement.data("pk"),
	     window.getSelection().toString(), -1);
	return true;
    });
}

function setCommentFormShowHandlers() {
    $('#comments').on('click', '.reply-form-link', function(event) {
	var formLink = $(this);
        var formTemplate = _.template(
            '<form action="/add_comment/{{ post_pk }}/" method="post" ' +
            '      class="reply-form" data-parent-pk="{{ parent_pk }}">' +
            '  <p style="font-size: 80%;"><em>Reply to this comment:</em></p>' +
            '  <textarea rows="4" cols="50" name="content"></textarea>' +
            '  <input type="hidden" name="parent" value="{{ parent_pk }}">' +
            '  <br>' +
            '  <input type="submit" value="Submit">' +
            '  <button class="cancel-comment"' +
            '          data-parent-pk="{{ parent_pk }}">' +
            '    Cancel' +
            '  </button>' +
            '</form>'
        )
        var form = formTemplate({
            post_pk: formLink.data("post-pk"),
            parent_pk: formLink.data("comment-pk")
        });
	$('.reply-form-holder[data-parent-pk="' + formLink.data("comment-pk") +
          '"]').append(form);
	formLink.hide();
    });
    $('#comments').on('click', '.cancel-comment', function(event) {
        event.preventDefault();
        var parent_pk = $(this).data("parent-pk");
        $('.reply-form[data-parent-pk="' + parent_pk + '"]').remove();
        $('.reply-form-link[data-comment-pk="' + parent_pk + '"]').show();
    });
}

$(document).ready(function() {
    setCommentFormShowHandlers();
    setVotingClickHandlers();
    setTagSubmitHandler();
});
