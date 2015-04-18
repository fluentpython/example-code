def phase1(response1):
    request2 = step1(response1)
    fetch2(request2, phase2)


def phase2(response2):
    request3 = step2(response2)
    fetch3(request3, phase3)


def phase3(response3):
    step3(response3)


fetch1(request1, phase1)
