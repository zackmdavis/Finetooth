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
        renderVoteStatus("post", 2, true, "Vote recorded!");
        expect(
            $(voteStatusSelector("post", 2)).hasClass("label-success")
        ).toBe(true);
        renderVoteStatus("post", 2, false, "Error!");
        expect(
            $(voteStatusSelector("post", 2)).hasClass("label-success")
        ).toBe(false);
        expect(
            $(voteStatusSelector("post", 2)).hasClass("label-warning")
        ).toBe(true);
    });

});


describe("concerning computing vote selection indices", function() {

    beforeEach(function() {
        $(document.body).append(
            '<div class="post well" data-pk="5" data-kind="post">' +
                '<p><span data-value="1">I threw myself </span>' +
                '<span data-value="2">into my </span>' +
                '<em><span data-value="2">studies</span></em>' +
                '<span data-value="0">, to have </span>' +
                '<span data-value="-1">the world</span>' +
                '<span data-value="0"> in my control</span></p>' +
            '</div>'
        );
    });

    afterEach(function() {
        $('.post[data-pk="5"]').remove();
    });

    it("we know how to traverse the document object model", function() {
        var content = "";
        domTraversal($('.post[data-pk="5"]')[0], function(ourNode) {
            if (ourNode.nodeType === Node.TEXT_NODE) {
                content += ourNode.data;
            }
        });
        expect(content).toEqual(
            "I threw myself into my studies, to have the world in my control"
        );
    });

});
