$().ready(function () {
    var $tagged = $(".found");
    var $edit = $("#edit");
    var $inputCosine = $('#inputCosine');
    var $modalCosineThresholdSet = $("#modalCosineThresholdSet");
    var $currentThreshold = $("#currentThreshold");

    $tagged.each(function() {
        var $this = $(this);
        var taggedWord = $this.html();
        var foundIndex = $.inArray(taggedWord, dictionary);
        if (foundIndex != -1) {
            // console.log(taggedWord, "found at", foundIndex);
            $this.addClass("exists-in-dict")
        } else {
            $this.addClass("new-for-dict")
        }
    });

    $edit.on('click', function() {
        $('#modalCosineThreshold').openModal();
    });

    $modalCosineThresholdSet.on('click', function() {
        var chosenCosineThreshold = $inputCosine.val();

        filterWords(chosenCosineThreshold);
        $currentThreshold.text(chosenCosineThreshold)
    });

    var filterWords = function(cosine) {
        cosine = parseFloat(cosine);

        $('.found').each(function() {
            var thisCosine = parseFloat($(this).data("cosine"));
            if (!thisCosine) {
                thisCosine = 0;
            }

            if (thisCosine < cosine) {
                $(this).addClass("filtered");
            } else {
                $(this).removeClass("filtered");
            }
        })
    }
});
