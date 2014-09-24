describe("concerning the `tag` function:", function() {

    it("it should make an Ajax request", function() {
        spyOn($, "ajax");
        tag(2, "unit testing");
        expect($.ajax).toHaveBeenCalledWith({
            url: "/tag/2/",
            type: "POST",
            data: {
                label: "unit testing"
            },
            success: jasmine.any(Function)
        });
    });

    it("it should call `renderNewTag`", function() {
        spyOn(window, "renderNewTag");
        spyOn($, "ajax").and.callFake(function(settings) {
            settings.success();
        });
        tag(2, "filmography");
        expect(renderNewTag).toHaveBeenCalledWith("filmography");
    });

});

describe("concerning the `renderNewTag` function", function() {

    beforeEach(function() {
        $(document.body).append('<div id="tags"></div>');
    });

    afterEach(function() {
        $('#tags').remove()
    });

    it("it should append two things to the #tags div", function() {
        expect($('#tags').children().length).toEqual(0);
        renderNewTag("JavaScripts");
        expect($('#tags').children().length).toEqual(2);
    });

});

describe("concerning the `setTagSubmitHandler`", function() {

    beforeEach(function() {
        $(document.body).append(
            '<button id="new-tag-submit" data-pk="2"></button>'
        );
        $(document.body).append('<input id="new-tag-label" type="text">');
        $('#new-tag-label').val("America");
    });

    afterEach(function() {
        $('#new-tag-submit').remove();
        $('#new-tag-label').remove();
    });

    it("`tag` should be called appropriately on tag button click", function() {
        spyOn(window, "tag");
        setTagSubmitHandler();
        $('#new-tag-submit').trigger('click');
        expect(tag).toHaveBeenCalledWith(2, "America");
    });

});

describe("concerning voting", function() {

    beforeEach(function() {
        $(document.body).append(
            '<div class="voting-area">' +
            '<a class="btn btn-success upvote" data-pk="2" data-kind="post"' +
            'href="javascript:void(0)"> upvote</a>' +
            '<div class="vote-status" data-pk="2" ' +
            'data-kind="post"></div></div>'
        );
    });

    afterEach(function() {
        $('.voting-area').remove();
    });

    it("`renderVoteStatus` sets CSS classes when called upon", function() {
        renderVoteStatus(2, true, "Vote recorded!");
        expect(
            $(voteStatusSelector(2)).hasClass("vote-status-success")
        ).toBe(true);
        renderVoteStatus(2, false, "Error!");
        expect(
            $(voteStatusSelector(2)).hasClass("vote-status-success")
        ).toBe(false);
        expect(
            $(voteStatusSelector(2)).hasClass("vote-status-fail")
        ).toBe(true);
    });

    it("gives feedback on success", function() {
        spyOn($, "ajax").and.callFake(function(settings) {
            settings.success();
        });
        spyOn(window, "renderVoteStatus");
        vote("post", 2, "selected text", 1);
        expect(renderVoteStatus).toHaveBeenCalledWith(2, true, "Vote recorded!");
    });

    it("gives feedback on failure", function() {
        spyOn($, "ajax").and.callFake(function(settings) {
            settings.error({'responseText': "Error!"});
        });
        spyOn(window, "renderVoteStatus");
        vote("post", 2, "selected text", 1);
        expect(renderVoteStatus).toHaveBeenCalledWith(2, false, "Error!");
    });

});
