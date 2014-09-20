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
    $('.reply-form-link').on("click", function(event) {
	var formLink = $(this);
	var form = '<form action="/add_comment/' + formLink.data("post-pk")  + '/" method="post"><textarea rows="4" cols="50" name="content"></textarea><input type="hidden" name="parent" value="' + formLink.data("comment-pk") + '"><br><input type="submit" value="Submit"></form>';
	$('.reply-form-holder[data-parent-pk="' + formLink.data("comment-pk") + '"]').append(form);
	formLink.remove();
    });
}

$(document).ready(function() {
    setCommentFormShowHandlers();
    setVotingClickHandlers();
    setTagSubmitHandler();
});
