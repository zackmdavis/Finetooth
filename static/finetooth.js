// Django-style template delimiters for Underscore; thanks to
// https://gist.github.com/thurloat/5355714
_.templateSettings = {
    'interpolate':/\{\{(.+?)\}\}/g,
    'evaluate':/\{%(.+?)%\}/g
};

function getCsrfToken() {
    return /csrftoken=(\w+)/g.exec(document.cookie)[1];
}

$.ajaxSetup({
    beforeSend: function(jqxhr, settings) {
        if (settings.type == "POST" && !this.crossDomain) {
            jqxhr.setRequestHeader("X-CSRFToken", getCsrfToken());
        }
    }
});

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
	},
        success: function(data, status, jqxhr) {
            renderVoteStatus(pk, true, "Vote recorded!");
        },
        error: function(jqxhr, status, error) {
            renderVoteStatus(pk, false, jqxhr.responseText);
        }
    });
}

function voteStatusSelector(pk) {
    return _.template(
        // XXX TODO we're going to want to vote on comments, too
        '.vote-status[data-pk={{ pk }}][data-kind="post"]'
    )({ pk: pk })
}

function renderVoteStatus(pk, success, message) {
    var statusClass = success ? "vote-status-success" : "vote-status-fail";
    var notStatusClass = success ? "vote-status-fail" : "vote-status-success";
    var statusSelector = voteStatusSelector(pk);
    var $statusDiv = $(statusSelector)
    $statusDiv.addClass(statusClass).removeClass(notStatusClass);
    $statusDiv.text(message);
    setTimeout(function() {
        $statusDiv.removeClass(statusClass).removeClass(notStatusClass).text('');
    }, 1000);
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
