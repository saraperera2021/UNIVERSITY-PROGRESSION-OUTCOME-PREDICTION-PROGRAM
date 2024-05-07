# I declare that my work contains no examples of misconduct, such as plagiarism, or collusion.
# Any code taken from other sources is referenced within my code solution.
# Student ID:w1956172
# Date:14/12/2022

# Some coding syntax copied from W3School and StackOverFlow websites

from typing import Dict, List

PROGRESS_TYPE_PROGRESS: str = "Progress"
PROGRESS_TYPE_TRAILER: str = "Trailer"
PROGRESS_TYPE_RETRIEVER: str = "Retriever"
PROGRESS_TYPE_EXCLUDED: str = "Excluded"

CREDIT_TYPE_PASS = "Pass"
CREDIT_TYPE_DEFER = "Defer"
CREDIT_TYPE_FAIL = "Fail"

totalCredits: int = 120
progressOutcome = {PROGRESS_TYPE_PROGRESS: 0, PROGRESS_TYPE_TRAILER: 0, PROGRESS_TYPE_RETRIEVER: 0,
                   PROGRESS_TYPE_EXCLUDED: 0}
listProgressOutcome = {PROGRESS_TYPE_PROGRESS: 0, PROGRESS_TYPE_TRAILER: 0, PROGRESS_TYPE_RETRIEVER: 0,
                       PROGRESS_TYPE_EXCLUDED: 0}
studentCreditList: any = []


def evaluateProgression():
    print("Part 1")
    noOfPass = noOfDefer = noOfFail = 0
    continueProcess = True
    while continueProcess:
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
                        studentCreditList.append({
                            "passCredits": noOfPass,
                            "deferCredits": noOfDefer,
                            "failCredits": noOfFail
                        })
                        evaluateStatus = evaluateProgress(noOfPass, noOfDefer, noOfFail)
                        progressType: str = evaluateStatus['type']
                        progressMessage: str = evaluateStatus['message']
                        print(progressMessage)
                        if progressType in progressOutcome:
                            progressOutcome[progressType] += 1
                        continueProcess = doItRecursively(progressOutcome)
                    noOfPass = noOfDefer = noOfFail = 0
                else:
                    noOfFail = 0
            else:
                noOfDefer = 0
        else:
            noOfPass = 0

    print("Part : 2")
    evaluateListOfStudentCredits(studentCreditList)
    print("Part : 3")
    outputFileName: str = writeFile(studentCreditList)
    readStudentsCreditFile(outputFileName)


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
        print("Total credits incorrect.")
        return False
    return True


def evaluateProgress(passCredits, deferCredits, failCredits):
    result = dict(message="", type="")
    if passCredits == 120:
        result["message"] = "Progress"
        result["type"] = PROGRESS_TYPE_PROGRESS
    elif passCredits >= 100:
        result["message"] = "Progress (Module Trailer)"
        result["type"] = PROGRESS_TYPE_TRAILER
    elif (passCredits <= 40) & (failCredits >= 80):
        result["message"] = "Exclude"
        result["type"] = PROGRESS_TYPE_EXCLUDED
    else:
        result["message"] = "Do not Progress – Module Retriever"
        result["type"] = PROGRESS_TYPE_RETRIEVER
    return result


def drawProgressHistogram(progressResult):
    totalStudents = 0
    print("------------------------------------------------")
    for progressType in progressResult:
        printString = progressType + " \t\t %d | "
        totalStudents += int(progressResult[progressType])
        for i in range(progressResult[progressType]):
            printString += "*"
        print(printString % progressResult[progressType])
    print("\n%d outcomes in total." % totalStudents)
    print("------------------------------------------------")


def doItRecursively(progressResult):
    print("Would you like to enter another set of data?")
    isContinue = input("Enter 'y' for yes or 'q' to quit and view results")
    if isContinue.upper() == "Y":
        print("")
        return True
    elif isContinue.upper() == "Q":
        drawProgressHistogram(progressResult)
        return False
    else:
        print("Please enter valid input: ")
        return doItRecursively(progressResult)


def evaluateListOfStudentCredits(creditList):
    for studentCredits in creditList:
        passCredit = studentCredits['passCredits']
        deferCredit = studentCredits['deferCredits']
        failCredit = studentCredits['failCredits']
        evaluateStatus: Dict[str, str] = evaluateProgress(passCredit, deferCredit, failCredit)
        progressType: str = evaluateStatus['type']
        progressMessage: str = evaluateStatus['message']
        print(progressMessage + " - " + str(passCredit) + ", " + str(deferCredit) + ", " + str(failCredit))


def writeFile(studentCredits):
    outputFileName = "students-progressions.txt"
    if studentCredits:
        f = open(outputFileName, "a")
        if f:
            f.truncate(0)
            for studentCredit in studentCredits:
                passCredit = studentCredit['passCredits']
                deferCredit = studentCredit['deferCredits']
                failCredit = studentCredit['failCredits']
                writeText = "%d,%d,%d\n" % (passCredit, deferCredit, failCredit)
                f.write(writeText)
            f.close()
            return outputFileName
        else:
            print("Failed to open file.")


def readStudentsCreditFile(outputFileName):
    f = open(outputFileName, "r")
    studentsCreditList: List[str] = f.read().split("\n")
    creditList = []
    for studentCredit in studentsCreditList:
        if studentCredit != '':
            progressionCredits = studentCredit.split(',')
            passCredit = int(progressionCredits[0])
            deferCredit = int(progressionCredits[1])
            failCredit = int(progressionCredits[2])
            creditList.append({
                "passCredits": passCredit,
                "deferCredits": deferCredit,
                "failCredits": failCredit
            })
    evaluateListOfStudentCredits(creditList)


evaluateProgression()

