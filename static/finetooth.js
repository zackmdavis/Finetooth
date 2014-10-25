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

function classKindPkSelector(theClass, kind, pk) {
    return _.template(
        '.{{ theClass }}[data-kind="{{ kind }}"][data-pk={{ pk }}]'
    )({ theClass: theClass, kind: kind, pk: pk });
}

function kindSelector(kind, pk) {
    return classKindPkSelector(kind, kind, pk);
}

function domTraversal(node, callback) {
    callback(node);
    var node = node.firstChild;
    while (node) {
        domTraversal(node, callback);
        node = node.nextSibling;
    }
}

function instarender(range, value) {
    var $hotscored = $('<span>').addClass('hotscored');
    $hotscored[0].appendChild(range.extractContents());
    range.insertNode($hotscored[0]);
    $hotscored.contents().each(function(_index, node) {
        $node = $(node);
        if (node.nodeType === Node.TEXT_NODE) {
            var oldValue = $node.parents('[data-value]').data('value');
            $node.wrap($('<span>').attr('data-value', oldValue + value));
        } else {
            $node.attr('data-value', $node.data('value') + value);
        }
    });
    window.getSelection().collapse($('body')[0],0);
}

function getVoteSelectionIndices(kind, pk) {
    var range = window.getSelection().getRangeAt(0);
    var ourIndex = 0;
    var startIndex, endIndex;
    domTraversal($(kindSelector(kind, pk))[0], function(node) {
        if (node.nodeType === Node.TEXT_NODE) {
            if (node === range.startContainer) {
                startIndex = ourIndex + range.startOffset;
            }
            if (node === range.endContainer) {
                endIndex = ourIndex + range.endOffset;
            }
            ourIndex += node.data.length;
        }
    });
    if (typeof startIndex != 'undefined' && typeof endIndex != 'undefined') {
        return { startIndex: startIndex, endIndex: endIndex }
    } else {
        return false;
    }
}

function vote(kind, pk, ballot, range) {
    $.ajax({
	url: "/vote/" + kind + "/" + pk + "/",
	type: "POST",
	data: ballot,
        success: function(data, status, jqxhr) {
            renderVoteStatus(
                pk, true,
                '<i class="glyphicon glyphicon-ok"></i> Vote recorded!'
            );
            instarender(range, ballot.value);
        },
        error: function(jqxhr, status, error) {
            renderVoteStatus(
                pk, false,
                '<i class="glyphicon glyphicon-remove"></i> ' + jqxhr.responseText
            );
        }
    });
}

function voteStatusSelector(pk) {
    // XXX TODO we're going to want to vote on comments, too
    return classKindPkSelector('vote-status', "post", pk)
}

function renderVoteStatus(pk, success, message) {
    var statusClass = success ? "label-success" : "label-danger";
    var notStatusClass = success ? "label-danger" : "label-success";
    var statusSelector = voteStatusSelector(pk);
    var $statusDiv = $(statusSelector)
    $statusDiv.addClass(statusClass).removeClass(notStatusClass);
    $statusDiv.html(message);
    setTimeout(function() {
        $statusDiv.removeClass(statusClass).removeClass(notStatusClass)
            .text(' ... ');
    }, 1000);
}

function setVotingClickHandlers() {
    _.each(
        [['.upvote', 1], ['.downvote', -1]],
        function(valenceDescriptor, index) {
            var classSelector = valenceDescriptor[0];
            $(classSelector).click(function(event) {
	        var votingElement = $(this);
                var kind = votingElement.data("kind");
                var pk = votingElement.data("pk");
                var ballot = getVoteSelectionIndices(kind, pk);
                if (ballot) {
                    ballot.value = valenceDescriptor[1];
                    vote(kind, pk, ballot, window.getSelection().getRangeAt(0));
                } else {
                    renderVoteStatus(
                        pk, false,
                        '<i class="glyphicon glyphicon-remove"></i> ' +
                        'Invalid vote not recorded!'
                    );
                }
            });
        }
    );
}

function setCommentFormShowHandlers() {
    $('#comments').on('click', '.reply-form-link', function(event) {
	var formLink = $(this);
        var formTemplate = _.template(
            '<form action="/add_comment/{{ post_pk }}/" method="post" ' +
            '      class="reply-form" data-parent-pk="{{ parent_pk }}">' +
            '  <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">' +
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
            parent_pk: formLink.data("comment-pk"),
            csrf_token: getCsrfToken()
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

function convertToSlug(text) {
    // courtesy http://stackoverflow.com/q/1053902
    return text.toLowerCase().replace(/ /g,'-').replace(/[^\w-]+/g,'');
}

function verifySlug(slug) {
    $.ajax({
        url: '/check_slug/',
        data: {
            slug: slug
        },
        success: function(data, status, jqxhr) {
            renderVerifiedSlug(slug, data.alreadyExists);
        }
    });
}

function renderVerifiedSlug(slug, alreadyExists) {
    if (alreadyExists) {
        $('#new-post-slug').val(slug+"-2");
    } else {
        $('#new-post-slug').val(slug);
    }
}

function setSlugVerificationHandler() {
    $('#new-post-title').on('input', function(event) {
        verifySlug(convertToSlug($(this).val()));
    });
}

$(document).ready(function() {
    setCommentFormShowHandlers();
    setVotingClickHandlers();
    setTagSubmitHandler();
    setSlugVerificationHandler();
});
