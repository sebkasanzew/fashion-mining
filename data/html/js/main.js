$().ready(function () {
    var $tagged = $(".found");

    $tagged.each(function(index) {
        var $this = $(this);
        var taggedWord = $this.html();
        var foundIndex = $.inArray(taggedWord, dictionary);
        if (foundIndex != -1) {
            console.log(taggedWord, "found at", foundIndex);
            $this.addClass("exists-in-dict")
        } else {
            $this.addClass("new-for-dict")
        }
    });

    $tagged.on("mouseenter", function () {
        // console.log($(this));
    });
});
