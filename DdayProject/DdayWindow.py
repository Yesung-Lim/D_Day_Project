# Coding: utf-8
#
# Developed by Lim YeaSung on Nov 23, 2020
#
# Final code updated on Nov 23, 2020
#
# Mail Address: sjsk3232@gmail.com
#
# Using Pyqt5

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from DdayProject import Icon_rc, DataClass

form_class = uic.loadUiType("DdayWindow.ui")[0]

# Class about Main Window of D-Day program
class MainWindow(QMainWindow, form_class):

    # Creator
    def __init__(self):
        super().__init__()

        # list of DdayData object
        self.__d_day_list = list()

        self.setupUi(self)
        self.loadData()
        self.signalConnect()
        QTableWidget.setEditTriggers(self.dDayTable, QAbstractItemView.NoEditTriggers)

    # Connect signals and functions
    def signalConnect(self):
        self.btn_AddDay.clicked.connect(self.execAddDayDlg)
        self.actionAddDday.triggered.connect(self.execAddDayDlg)
        self.btn_DelDay.clicked.connect(self.deleteCurrentDay)
        self.actionDelDday.triggered.connect(self.deleteCurrentDay)
        self.btn_EditDay.clicked.connect(self.execEditDayDlg)
        self.btn_AddPlan.clicked.connect(self.execAddPlanDlg)
        self.btn_DelPlan.clicked.connect(self.deleteCurrentPlans)
        self.btn_MemoClr.clicked.connect(self.clearMemo)
        self.btn_MemoSave.clicked.connect(self.saveMemo)
        self.dDayTable.cellClicked.connect(self.syncInfo)
        self.planListWidget.itemDoubleClicked.connect(self.changePlanStatus)
        self.actionSaveData.triggered.connect(self.saveData)
        self.actionLoadData.triggered.connect(self.loadData)

    # Synchronize the information of selected DDay object to the GUI
    def syncInfo(self):
        self.syncDdayInfo()
        self.syncPlanInfo()
        self.syncMemoInfo()

    # Execute AddDayDialog and add DdayData object to list
    def execAddDayDlg(self):
        dlg = AddDayDlg()
        dlg.exec_()
        temp = list()
        for i in dlg.getPlanList():
            temp.append(DataClass.PlanData(i))
        day = DataClass.DdayData(dlg.getName(), dlg.getDate(), temp)
        self.__d_day_list.append(day)
        self.addDayInfoToTable(day)

    # Add D-Day information to QTableWidget
    # type of day parameter = DataClass.DdayData
    def addDayInfoToTable(self, day):
        row = self.dDayTable.rowCount()
        self.dDayTable.setRowCount(row + 1)
        self.dDayTable.setItem(row, 0, QTableWidgetItem(day.getName()))
        d_day = QTableWidgetItem()
        d_day.setData(Qt.DisplayRole, day.getDate().daysTo(QDate.currentDate()))
        self.dDayTable.setItem(row, 1, d_day)
        self.dDayTable.setItem(row, 2, QTableWidgetItem(day.getDate().toString("yyyy-MM-dd")))
        self.dDayTable.setItem(row, 3, QTableWidgetItem(str(day.getProgress()) + "%"))
        self.dDayTable.sortItems(1, Qt.DescendingOrder)

    # Delete selected D-Day information to QTableWidget
    def deleteCurrentDay(self):
        current_row = self.dDayTable.currentRow()
        if (current_row == -1): return

        self.__d_day_list.remove(self.findCurrentDdayData())
        for i in range(0, 4):
            self.dDayTable.takeItem(current_row, i)

        row = self.dDayTable.rowCount()
        self.dDayTable.setRowCount(row - 1)

    # Execute AddPlanDialog and add Item to QListWidget
    def execAddPlanDlg(self):
        if(self.dDayTable.currentRow() == -1): return

        dlg = AddPlanDlg()
        dlg.exec_()
        day_data = self.findCurrentDdayData()
        day_data.appendPlan(dlg.getPlanName())
        self.planListWidget.addItem(dlg.getPlanName())
        self.updateProgress(day_data)

    # Execute AddDayDialog and add DdayData object to list
    def execEditDayDlg(self):
        selected_day = self.findCurrentDdayData()
        dlg = EditDayDlg(selected_day.getName, selected_day.getDate, selected_day.getPlanNameList)
        dlg.exec_()
        temp = list()
        for i in dlg.getPlanList():
            temp.append(DataClass.PlanData(i))
        day = DataClass.DdayData(dlg.getName(), dlg.getDate(), temp)
        self.__d_day_list.append(day)
        self.addDayInfoToTable(day)

    # Delete selected Items to QListWidget
    def deleteCurrentPlans(self):
        if (self.planListWidget.currentRow() == -1): return

        selected = self.planListWidget.selectedItems()
        selected.sort()
        selected.reverse()

        temp = list()
        for i in selected:
            item = self.planListWidget.takeItem(self.planListWidget.row(i))
            temp.append(item.text())

        day_data = self.findCurrentDdayData()
        day_data.deletePlan(temp)
        self.updateProgress(day_data)

    # Change plan complete status and set(or remove) icon from planListWidget
    # type of item parameter = QListWidgetItem
    def changePlanStatus(self, item):
        day_data = self.findCurrentDdayData()
        plan = day_data.getPlan(item.text())
        plan.changeStatus()
        self.updateProgress(day_data)

        if plan.isDone():
            icon = QIcon("./D-Day icon/background_imege/check mark.png")
            item.setIcon(icon)
        else:
            item.setIcon(QIcon())

    # Save Memo to current DdayData object
    def saveMemo(self):
        if (self.dDayTable.currentRow() == -1): return

        current_day = self.findCurrentDdayData()
        current_day.setMemo(self.memoEdit.toPlainText())

    # Clear Memo to current DdayData object
    def clearMemo(self):
        if (self.dDayTable.currentRow() == -1): return

        current_day = self.findCurrentDdayData()
        current_day.setMemo(None)
        self.memoEdit.clear()

    # Update new progress information to dDayTable and two of progress bars
    # type of day_data parameter = DataClass.DdayData
    def updateProgress(self, day_data):
        day_data.calProgress()
        self.dDayTable.setItem(self.dDayTable.currentRow(), 3, QTableWidgetItem(str(day_data.getProgress()) + "%"))
        self.pgBar_FirstPage.setValue(day_data.getProgress())
        self.pgBar_SecondPage.setValue(day_data.getProgress())

    # Synchronize dDayTable and lbl_DdayDisplay's d-day information with DdayData object information
    def syncDdayInfo(self):
        d_day = self.dDayTable.item(self.dDayTable.currentRow(), 1).data(Qt.EditRole)
        lbl_text = "D"
        if d_day >= 0: lbl_text += "+"
        lbl_text += str(d_day)
        self.lbl_DdayDisplay.setText(lbl_text)
        self.lbl_DdayDisplay.setAlignment(Qt.AlignCenter)
        self.regulatePointSize(lbl_text)

    # Synchronize planListWidget and progress bars' plan information with DdayData object information
    def syncPlanInfo(self):
        self.planListWidget.clear()

        day_data = self.findCurrentDdayData()
        plan_list = day_data.getPlanList()

        for i in plan_list:
            item = QListWidgetItem()
            item.setText(i.getContent())
            if i.isDone():
                icon = QIcon("./D-Day icon/background_imege/check mark.png")
                item.setIcon(icon)

            self.planListWidget.addItem(item)

        self.pgBar_FirstPage.setValue(day_data.getProgress())
        self.pgBar_SecondPage.setValue(day_data.getProgress())

    # Synchronize memoEdit's memo information with DdayData object information
    def syncMemoInfo(self):
        memo = self.findCurrentDdayData().getMemo()
        if memo == "":
            self.memoEdit.clear()
            return

        self.memoEdit.setPlainText(memo)

    # Find current selected DdayData object
    def findCurrentDdayData(self):
        d_day_name = self.dDayTable.item(self.dDayTable.currentRow(), 0).text()

        for i in self.__d_day_list:
            if i.getName() == d_day_name:
                return i

    # Regulate lbl_DdayDisplay's point size
    # type of lbl_text parameter = String
    def regulatePointSize(self, lbl_text):
        if len(lbl_text) > 7:
            excess = len(lbl_text) - 7
            font = self.lbl_DdayDisplay.font()
            font.setPointSize(60 - excess * 5)
            self.lbl_DdayDisplay.setFont(font)

    # Save data of __d_day_list in D_Days.dat file
    def saveData(self):
        f = open('D_Days.dat', mode = 'wt', encoding = 'utf-8')
        for i in self.__d_day_list:
            f.write("__day_name__\n")
            f.write(i.getName() + " \n")

            date = i.getDate().toString("yyyyMMdd\n")
            f.write("__day_date__\n")
            f.write(date)

            f.write("__day_plan__\n")
            for j in i.getPlanList():
                f.write(j.getContent())
                if j.isDone(): f.write("&&1\n")
                else: f.write("&&0\n")
            f.write("__end_of_plan__\n")

            f.write("__day_memo__\n")
            f.write(i.getMemo() + "\n")

        f.write("__end_of_data__")

        f.close()

    # Load data of D_Days.dat file
    def loadData(self):
        try:
            f = open('D_Days.dat', mode = 'rt', encoding = 'utf-8')

            line = f.readline()

            while line != "__end_of_data__":
                if line == "__day_name__\n":
                    name = f.readline().split(" ")

                    f.readline()
                    tmp = f.readline()
                    date = QDate.fromString(tmp, "yyyyMMdd\n")

                    plan = list()
                    f.readline()
                    line = f.readline()
                    while line != "__end_of_plan__\n":
                        tmp = line.split("&&")
                        status = True
                        if tmp[1] == "0\n": status = False
                        plan_data = DataClass.PlanData(tmp[0], status)
                        plan.append(plan_data)
                        line = f.readline()

                    f.readline()
                    memo = f.readline()

                    day = DataClass.DdayData(name[0], date, plan, memo)
                    self.__d_day_list.append(day)
                    self.addDayInfoToTable(day)

                line = f.readline()

            f.close()

        except FileNotFoundError:
            print("failed loading d_days data")
            return


# Class about AddDayDialog
class AddDayDlg(QDialog):

    # Creator
    def __init__(self):
        super().__init__()

        self.__name = None  # type = String
        self.__date = None  # type = QDate
        self.__plan_list = list()  # type = list, type of contents = String

        uic.loadUi("AddDayDialog.ui", self)
        self.setCurrentDate()
        self.signalConnect()

    # Connect signals and functions
    def signalConnect(self):
        self.btn_AddPlan_Dlg.clicked.connect(self.execAddPlanDlg)
        self.btn_DelPlan_Dlg.clicked.connect(self.deleteCurrentPlans)
        self.btn_AddDay_Dlg.clicked.connect(self.addDay)
        self.btn_Cancel_Dlg.clicked.connect(self.close)

    # Add informations about day to self variables
    def addDay(self):
        self.__name = self.dayNameEdit_Dlg.text()
        self.__date = self.dayDateEdit_Dlg.date()
        self.planListWidget_Dlg.selectAll()
        temp = self.planListWidget_Dlg.selectedItems()
        for i in range(0, len(temp)):
            self.__plan_list.append(temp[i].text())
        self.close()

    # Delete selected plans from planListWidget_Dlg
    def deleteCurrentPlans(self):
        selected = self.planListWidget_Dlg.selectedItems()
        selected.sort()
        selected.reverse()

        for i in range(0, len(selected)):
            self.planListWidget_Dlg.takeItem(self.planListWidget_Dlg.row(selected[i]))

    # Execute AddPlanDialog and add item to planListWidget_Dlg
    def execAddPlanDlg(self):
        dlg = AddPlanDlg()
        dlg.exec_()
        self.planListWidget_Dlg.addItem(dlg.getPlanName())

    # Set current date to dayDateEdit_Dlg
    def setCurrentDate(self):
        self.dayDateEdit_Dlg.setDate(QDate.currentDate())

    # Return name variable
    def getName(self):
        return self.__name

    # Return date variable
    def getDate(self):
        return self.__date

    # Return plan_list variable
    def getPlanList(self):
        return self.__plan_list


# Class about EditDayDialog
class EditDayDlg(AddDayDlg):

    # Creator
    def __init__(self, name, date, plan_list):
        super().__init__()

        self.__name = name  # type = String
        self.__date = date  # type = QDate
        self.__plan_list = plan_list  # type = list, type of contents = String

        uic.loadUi("EditDayDialog.ui", self)
        self.syncInfo()
        self.signalConnect()

    # Connect signals and functions
    def signalConnect(self):
        self.btn_AddPlan_Dlg.clicked.connect(self.execAddPlanDlg)
        self.btn_DelPlan_Dlg.clicked.connect(self.deleteCurrentPlans)
        self.btn_EditDay_Dlg.clicked.connect(self.addDay)
        self.btn_Cancel_Dlg.clicked.connect(self.close)

    # Synchronize the information of selected DDay object to the GUI
    def syncInfo(self):
        self.dayNameEdit_Dlg.setText(self.__name)
        self.dayDateEdit_Dlg.setDate(self.__date)
        for i in self.__plan_list:
            self.planListWidget_Dlg.addItem(i)





# Class about AddPlanDialog
class AddPlanDlg(QDialog):

    # Creator
    def __init__(self):
        super().__init__()

        self.__plan_name = None # type = String

        uic.loadUi("AddPlanDialog.ui", self)
        self.btn_AddPlan_Dlg2.clicked.connect(self.setPlanName)
        self.planNameEdit_Dlg2.returnPressed.connect(self.setPlanName)
        self.btn_Cancel_Dlg2.clicked.connect(self.close)

    # set name to plan_name variable
    def setPlanName(self):
        self.__plan_name = self.planNameEdit_Dlg2.text()
        self.close()

    # Return plan_name variable
    def getPlanName(self):
        return self.__plan_name


if __name__ == '__main__':
    app = QApplication(sys.argv)

    Window = MainWindow()

    Window.show()

    app.exec_()