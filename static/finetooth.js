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
	var form_link = $(this);
	var form = '<form action="/add_comment/' + form_link.data("post-pk")  + '/" method="post"><textarea rows="4" cols="50" name="comment" form="usrform"></textarea><input type="submit" value="Submit"></form>';
	$('.reply-form-holder[data-parent-pk="' + form_link.data("comment-pk") + '"]').append(form);
	form_link.remove();
    });
}

$(document).ready(function() {
    setCommentFormShowHandlers();
    $('.upvote').click(function(event) {
	vote($(this).data("kind"), $(this).data("pk"),
	     window.getSelection().toString(), 1);
	return true;
    });
    $('.downvote').click(function(event) {
	vote($(this).data("kind"), $(this).data("pk"),
	      window.getSelection().toString(), -1);
	return true;
    });
});
