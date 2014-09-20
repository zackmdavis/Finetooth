describe("tagging", function() {

    it("it should make an Ajax request", function() {
        spyOn($, "ajax");
        tag(2, "unit testing");
        expect($.ajax).toHaveBeenCalled();
    });

});
