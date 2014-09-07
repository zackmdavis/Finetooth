function vote(kind, pk, selection, value) {
    console.log(kind, pk, selection, value);
    $.ajax({
	url: "/vote/" + kind + "/" + pk + "/",
	type: "POST",
	data: {
	    value: value,
	    selection: selection
	}
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


$(document).ready(function() {
    setCommentFormShowHandlers();
    setVotingClickHandlers()
});
