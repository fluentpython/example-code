fetch1(request1, function (response1) {
    // phase 1
    var request2 = step1(response1);

    fetch2(request2, function (response2) {
        // phase 2
        var request3 = step2(response2);

        fetch3(request3, function (response3) {
            // phase 3
            step3(response3);
        });
    });
});
