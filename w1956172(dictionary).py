studentsCreditDict = {}

totalCredits: int = 120
PROGRESS_TYPE_PROGRESS: str = "Progress"
PROGRESS_TYPE_TRAILER: str = "Trailer"
PROGRESS_TYPE_RETRIEVER: str = "Retriever"
PROGRESS_TYPE_EXCLUDED: str = "Excluded"

CREDIT_TYPE_PASS = "Pass"
CREDIT_TYPE_DEFER = "Defer"
CREDIT_TYPE_FAIL = "Fail"


progressOutcome = {PROGRESS_TYPE_PROGRESS: 0, PROGRESS_TYPE_TRAILER: 0, PROGRESS_TYPE_RETRIEVER: 0,
                   PROGRESS_TYPE_EXCLUDED: 0}
listProgressOutcome = {PROGRESS_TYPE_PROGRESS: 0, PROGRESS_TYPE_TRAILER: 0, PROGRESS_TYPE_RETRIEVER: 0,
                       PROGRESS_TYPE_EXCLUDED: 0}


def gatherCreditData():
    noOfPass = noOfDefer = noOfFail = 0
    continueProcess = True
    while continueProcess:
        studentId = input("Enter students ID :")
        if noOfPass == 0:
            noOfPass = input("Enter your no of %s credits:" % CREDIT_TYPE_PASS)
        if validateInput(noOfPass, CREDIT_TYPE_PASS):
            noOfPass = int(noOfPass)
            if noOfDefer == 0:
                noOfDefer = input("Enter your no of %s credits:" % CREDIT_TYPE_DEFER)
            if validateInput(noOfDefer, CREDIT_TYPE_DEFER):
                noOfDefer = int(noOfDefer)
                if noOfFail == 0:
                    noOfFail = input("Enter your no of %s credits:" % CREDIT_TYPE_FAIL)
                if validateInput(noOfFail, CREDIT_TYPE_FAIL):
                    noOfFail = int(noOfFail)
                    if checkTotalCredits(noOfPass, noOfDefer, noOfFail):
                        studentsCreditDict[studentId] = {
                            "passCredits": noOfPass,
                            "deferCredits": noOfDefer,
                            "failCredits": noOfFail
                        }
                        continueProcess = doItRecursively(progressOutcome)
                    noOfPass = noOfDefer = noOfFail = 0
                else:
                    noOfFail = 0
            else:
                noOfDefer = 0
        else:
            noOfPass = 0


def validateInput(inputValue, inputType):
    validInputs = [0, 20, 40, 60, 80, 100, 120]
    if isinstance(inputValue, int):
        if inputValue not in validInputs:
            print("%s credits is Out of range." % inputType)
            return False
        else:
            return True
    elif inputValue.isnumeric():
        inputValue = int(inputValue)
        if inputValue not in validInputs:
            print("%s credits is Out of range." % inputType)
            return False
        else:
            return True
    else:
        print("Integer required for %s credits." % inputType)
        return False


def checkTotalCredits(passCredits, deferCredits, failCredits):
    creditSum = int(passCredits) + int(deferCredits) + int(failCredits)
    if creditSum != totalCredits:
        print("Total of credits incorrect.")
        return False
    return True


def evaluateProgress(passCredits, deferCredits, failCredits):
    result = dict(message="", type="")
    if passCredits == 120:
        result["message"] = "Progress"
        result["type"] = PROGRESS_TYPE_PROGRESS
    elif passCredits >= 100:
        result["message"] = "Progress (module trailer)"
        result["type"] = PROGRESS_TYPE_TRAILER
    elif (passCredits <= 40) & (failCredits >= 80):
        result["message"] = "Exclude"
        result["type"] = PROGRESS_TYPE_EXCLUDED
    else:
        result["message"] = "Do not Progress – module retriever"
        result["type"] = PROGRESS_TYPE_RETRIEVER
    return result


def doItRecursively(progressResult):
    print("Would you like to enter another set of data?")
    isContinue = input("Enter 'y' for yes or 'q' to quit and view results")
    if isContinue.upper() == "Y":
        print("")
        return True
    elif isContinue.upper() == "Q":
        return False
    else:
        print("Please enter valid input: ")
        return doItRecursively(progressResult)


def evaluateProgression():
    for studentId in studentsCreditDict:
        studentsCredits = studentsCreditDict[studentId]
        passCredit = studentsCredits['passCredits']
        deferCredit = studentsCredits['deferCredits']
        failCredit = studentsCredits['failCredits']
        evaluateStatus = evaluateProgress(passCredit, deferCredit, failCredit)
        progressType: str = evaluateStatus['type']
        progressMessage: str = evaluateStatus['message']
        print(studentId+": "+progressMessage + " - " + str(passCredit) + ", " + str(deferCredit) + ", " + str(failCredit))


gatherCreditData()
evaluateProgression()
