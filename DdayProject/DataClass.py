# Coding: utf-8
#
# Developed by Lim YeaSung on Nov 22, 2020
#
# Final code updated on Nov 23, 2020
#
# Address: sjsk3232@gmail.com


# Class about D-day Data
class DdayData:

    # Creator
    def __init__(self, name, date, plan_list = list(), memo = ""):
        self.__name = name
        self.__date = date
        self.__plan_list = plan_list
        self.__memo = memo
        self.__progress = None
        self.calProgress()

    def getName(self):
        return self.__name

    # type of name parameter = String
    def setName(self, name):
        self.__name = name

    def getDate(self):
        return self.__date

    # type of date parameter = PyQt5.QtCore.QDate
    def setDate(self, date):
        self.__date = date

    def getPlanNameList(self) -> list:
        temp = list()

        for i in self.__plan_list:
            temp.append(i.getContent)

        return temp

    def getPlanList(self):
        return self.__plan_list

    # type of plan_list parameter = list, type of component = DataClass.PlanData
    def setPlanList(self, plan_list):
        self.__plan_list = plan_list

    # type of plan parameter = String or list(type of component = String)
    def appendPlan(self, plan):
        if str(type(plan)) == "<class 'str'>":
            temp = PlanData(plan)
            self.__plan_list.append(temp)

        elif str(type(plan)) == "<class 'list'>":
            for i in plan:
                temp = PlanData(i)
                self.__plan_list.append(temp)

    # type of plan parameter = String or list(type of component = String)
    def deletePlan(self, plan):
        if str(type(plan)) == "<class 'str'>":
            idx = 0

            for i in range(len(self.__plan_list)):
                if self.__plan_list[i].getContent() == plan:
                    idx = i
                    break

            self.__plan_list.pop(idx)

        elif str(type(plan)) == "<class 'list'>":
            idx_list = list()

            for i in range(len(self.__plan_list)):
                for j in plan:
                    if self.__plan_list[i].getContent() == j:
                        idx_list.append(i)
                        plan.remove(j)
                        break

            idx_list.reverse()
            for i in idx_list:
                self.__plan_list.pop(i)

    # type of content parameter = String
    def getPlan(self, content):
        for i in self.__plan_list:
            if i.getContent() == content:
                return i

    def getMemo(self):
        return self.__memo

    # type of memo parameter = String
    def setMemo(self, memo):
        self.__memo = memo

    def getProgress(self):
        return self.__progress

    def calProgress(self):
        if len(self.__plan_list) == 0:
            self.__progress = 0
            return

        done = 0
        for i in self.__plan_list:
            if i.isDone():
                done += 1
        self.__progress = int(done / len(self.__plan_list) * 100)


# Class about Plan Data
class PlanData:

    # Creator
    def __init__(self, content, status = False):
        self.__content = content
        self.__complete_status = status

    def isDone(self):
        return self.__complete_status

    def Done(self):
        self.__complete_status = True

    def changeStatus(self):
        if self.isDone(): self.__complete_status = False
        else: self.Done()

    def getContent(self):
        return self.__content

    # type of revise parameter = String
    def setContent(self, revise):
        self.__content = revise