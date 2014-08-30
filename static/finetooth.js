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

$(document).ready(function() {
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
