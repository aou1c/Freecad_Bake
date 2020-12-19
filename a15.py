# -*- coding: utf-8 -*-
import sys
import os



debugFile = True  # Для отладки в режиме "Текущий файл"
if debugFile:
    sys.path = ['/home/aou/.FreeCAD/Mod/Assembly4', '/home/aou/.FreeCAD/Mod/3DFindIT', '/home/aou/anaconda3/envs/ptn386env/Mod/Web', '/home/aou/anaconda3/envs/ptn386env/Mod/Tux', '/home/aou/anaconda3/envs/ptn386env/Mod/Test', '/home/aou/anaconda3/envs/ptn386env/Mod/TechDraw', '/home/aou/anaconda3/envs/ptn386env/Mod/Surface', '/home/aou/anaconda3/envs/ptn386env/Mod/Start', '/home/aou/anaconda3/envs/ptn386env/Mod/Spreadsheet', '/home/aou/anaconda3/envs/ptn386env/Mod/Sketcher', '/home/aou/anaconda3/envs/ptn386env/Mod/Show', '/home/aou/anaconda3/envs/ptn386env/Mod/Robot', '/home/aou/anaconda3/envs/ptn386env/Mod/ReverseEngineering', '/home/aou/anaconda3/envs/ptn386env/Mod/Raytracing', '/home/aou/anaconda3/envs/ptn386env/Mod/Points', '/home/aou/anaconda3/envs/ptn386env/Mod/Path', '/home/aou/anaconda3/envs/ptn386env/Mod/PartDesign', '/home/aou/anaconda3/envs/ptn386env/Mod/Part', '/home/aou/anaconda3/envs/ptn386env/Mod/OpenSCAD', '/home/aou/anaconda3/envs/ptn386env/Mod/MeshPart', '/home/aou/anaconda3/envs/ptn386env/Mod/Mesh', '/home/aou/anaconda3/envs/ptn386env/Mod/Measure','/home/aou/anaconda3/envs/ptn386env/Mod/Material', '/home/aou/anaconda3/envs/ptn386env/Mod/Inspection', '/home/aou/anaconda3/envs/ptn386env/Mod/Import', '/home/aou/anaconda3/envs/ptn386env/Mod/Image', '/home/aou/anaconda3/envs/ptn386env/Mod/Idf', '/home/aou/anaconda3/envs/ptn386env/Mod/Fem', '/home/aou/anaconda3/envs/ptn386env/Mod/Drawing', '/home/aou/anaconda3/envs/ptn386env/Mod/Draft', '/home/aou/anaconda3/envs/ptn386env/Mod/Complete', '/home/aou/anaconda3/envs/ptn386env/Mod/Arch', '/home/aou/anaconda3/envs/ptn386env/Mod/AddonManager', '/home/aou/anaconda3/envs/ptn386env/Mod', '/home/aou/anaconda3/envs/ptn386env/lib', '/home/aou/anaconda3/envs/ptn386env/Ext', '/home/aou/anaconda3/envs/ptn386env/bin', '/home/aou/anaconda3/envs/ptn386env/lib/python38.zip', '/home/aou/anaconda3/envs/ptn386env/lib/python3.8', '/home/aou/anaconda3/envs/ptn386env/lib/python3.8/lib-dynload', '/home/aou/.local/lib/python3.8/site-packages', '/home/aou/anaconda3/envs/ptn386env/lib/python3.8/site-packages', '/home/aou/.FreeCAD/Macro', '/home/aou/anaconda3/envs/ptn386env/Macro']
    print('__debug__')

from PySide import QtGui, QtCore
import FreeCAD
import FreeCADGui as gui


Length = 250
Width = 120
Height = 65
# Width = 65
# Height = 120
shov = 3

# Целое количество кирпичей по X + половинка(ширина кирпича)
FullHoriz = [5.0, 0]

# Целое количество кирпичей по Y
#  + половинка(ширина кирпича)
#  + половинка(ширина кирпича)
FullVertical = [2.0, 1, 0]

CountRow = 1  # Количество рядов/2


StartFromFreecad = False

class PropertyRow():
    def __init__(self, posX, posY, count, shov, ext = 0):
        self.__posX = posX
        self.__posY = posY
        self.__count = count
        self.__shov = shov
        self.__ext = ext
        

    @property
    def posX(self):
        return self.__posX

    @property
    def posY(self):
        return self.__posY

    @property
    def count(self):
        return self.__count

    @property
    def shov(self):
        return self.__shov

    @property
    def ext(self):
        return self.__ext


class BrowserHandler(QtCore.QObject):
    signalForProgress = QtCore.Signal(int, int)
    
    def MakeBrake(self,par):

        Length = int(par.form.BrikLength.value())
        Width = int(par.form.BrikWidth.value())
        Height = int(par.form.BrikHeight.value())
        shov = int(par.form.Shov.value())

        FullHoriz[0] = int(par.form.BakeLength.value())
        FullVertical[0] = int(par.form.BakeWidth.value())
        CountRow = int(par.form.BakeRow.value())

        if (par.form.checkBox1.checkState() == QtCore.Qt.Checked):
            FullHoriz[1] = 1
        else:
            FullHoriz[1] = 0
        if (par.form.checkBox2.checkState() == QtCore.Qt.Checked):
            FullVertical[1] = 1
        else:
            FullVertical[1] = 0

        if par.form.checkBoxCAlcShov.checkState() == QtCore.Qt.Checked:
            CAlcShov = True
        else:
            CAlcShov = False

        if (par.form.checkBox2.checkState() == QtCore.Qt.Checked):
            FullVertical[2] = 1
        else:
            FullVertical[2] = 0



        NumHoriz = FullHoriz[0]
        numVertical = FullVertical[0]

        AllBloks = NumHoriz + numVertical

        shovH = shov
        shovV = shov

        acord = []


        if (FullHoriz[1] == 1 and FullVertical[1] == 1 and FullVertical[2] == 1):
            ######################################################
            # Размер печи
            # X: целое + полкирпича(ширина кирпича)
            # Y: целое количество кирпичей  + полкирпича(ширина кирпича)
            ######################################################

            DistanseX = NumHoriz*Length+shov*(NumHoriz)
            DistanseY = numVertical*Length+(numVertical)*shov + Width + shov

            ext = (Length + Width*2) + shov - Length
            print('ext' + str(ext))

            difHorizontRow1 = PropertyRow(Width + shov, 0,         NumHoriz, shov)
            difHorizontRow2 = PropertyRow(Width + shov, DistanseY, NumHoriz, shov)
            difVerticalRow1 = PropertyRow(Width, 0,     numVertical, shov, ext)
            difVerticalRow2 = PropertyRow(DistanseX+Width, Width + shov, numVertical, shov)

            difHorizontRow3 = PropertyRow(0, DistanseY,NumHoriz, shov)
            difHorizontRow4 = PropertyRow(0, 0, NumHoriz, shov)
            difVerticalRow3 = PropertyRow(Width, Width + shov,     numVertical, shov)
            difVerticalRow4 = PropertyRow(DistanseX+Width, 0, numVertical, shov, ext)




        else:
            if (FullHoriz[1] == 0 and FullVertical[1]) == 0:
                ######################################################
                # Размер печи
                # X: целое количество кирпичей
                # Y: целое количество кирпичей
                ######################################################

                DistanseX = NumHoriz*Length+shov*(NumHoriz-1)
                DistanseY = numVertical*Length+(numVertical-1)*shov - Width

                if CAlcShov:
                    shovH = ((DistanseX - Width*2) - Length*(NumHoriz-1))/NumHoriz
                    shovV = ((numVertical*Length+(numVertical-1)*shov - Width*2) - Length*(numVertical-1))/numVertical
                    ext = 0
                else:
                    shovH = shov
                    ext = (DistanseX - Width*2) - Length*(NumHoriz-1) - (NumHoriz+1)*shov


                difHorizontRow1 = PropertyRow(0, 0,                     NumHoriz, shov)
                difHorizontRow2 = PropertyRow(0, DistanseY,             NumHoriz, shov)
                difVerticalRow1 = PropertyRow(Width, Width + shovV,     numVertical-1, shovV, ext)
                difVerticalRow2 = PropertyRow(DistanseX, Width + shovV, numVertical-1, shovV, ext)

                difHorizontRow3 = PropertyRow(Width + shovH, 0, NumHoriz-1, shovH, ext)
                difHorizontRow4 = PropertyRow(Width + shovH, DistanseY, NumHoriz-1, shovH, ext)
                difVerticalRow3 = PropertyRow(Width, 0,                 numVertical, shov)
                difVerticalRow4 = PropertyRow(DistanseX, 0,             numVertical, shov)

            if (FullHoriz[1] == 1 and FullVertical[1] == 1):
                ######################################################
                # Размер печи
                # X: целое + полкирпича(ширина кирпича)
                # Y: целое количество кирпичей  + полкирпича(ширина кирпича)
                ######################################################

                DistanseX = NumHoriz*Length+shov*(NumHoriz)
                DistanseY = numVertical*Length+(numVertical)*shov

                difHorizontRow1 = PropertyRow(0, 0,                     NumHoriz, shov)
                difHorizontRow2 = PropertyRow(Width + shov, DistanseY, NumHoriz, shov)
                difVerticalRow1 = PropertyRow(
                    Width, Width + shov,     numVertical, shov)
                difVerticalRow2 = PropertyRow(DistanseX+Width, 0, numVertical, shov)

                difHorizontRow3 = PropertyRow(0, DistanseY,
                                            NumHoriz, shov)
                difHorizontRow4 = PropertyRow(Width + shov, 0, NumHoriz, shov)
                difVerticalRow3 = PropertyRow(Width, 0,     numVertical, shov)
                difVerticalRow4 = PropertyRow(
                    DistanseX+Width, Width + shov, numVertical, shov)

            if (FullHoriz[1] == 0 and FullVertical[1] == 1):
                ######################################################
                # Размер печи
                # X: целое количество кирпичей
                # Y: целое количество кирпичей  + полкирпича(ширина кирпича)
                ######################################################

                DistanseX = NumHoriz*Length+shov*(NumHoriz-1)
                DistanseY = numVertical*Length+(numVertical)*shov

                if CAlcShov:
                    shovH = ((DistanseX - Width*2) - Length*(NumHoriz-1))/NumHoriz
                    ext = 0
                else:
                    shovH = shov
                    ext = (DistanseX - Width*2) - Length*(NumHoriz-1) - (NumHoriz+1)*shov
                    print(ext)

                difHorizontRow1 = PropertyRow(0, 0,   NumHoriz, shov)
                difHorizontRow2 = PropertyRow(Width + shovH, DistanseY, NumHoriz-1, shovH, ext)
                difVerticalRow1 = PropertyRow(Width, Width + shov,     numVertical, shov)
                difVerticalRow2 = PropertyRow(DistanseX, Width + shov, numVertical, shov)

                difHorizontRow3 = PropertyRow(0, DistanseY,  NumHoriz, shov)
                difHorizontRow4 = PropertyRow(Width + shovH, 0, NumHoriz-1, shovH, ext)
                difVerticalRow3 = PropertyRow(Width, 0, numVertical, shov)
                difVerticalRow4 = PropertyRow(DistanseX, 0, numVertical, shov)

        if (FullHoriz[1] == 1 and FullVertical[1] == 0):
            msg = QtGui.QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Не правильный размер печи")
            msg.setInformativeText("Этот вариант размера печи не реализован")
            msg.setDetailedText("Вместо: Длина печи + ширина кирпича с Ширина печи, используйте Ширина печи + ширина кирпича с Длина печи")
            retval = msg.exec_()
            return 0






        HeightFull = Height + shov

        print('DistanseX ' + str(DistanseX))
        print('DistanseY ' + str(DistanseY))
        print('shovH ', str(shovH))
        print('shovV ', str(shovV))

        def Makehorizont(dif, Z):
            coord = []
            startX = dif.posX
            startY = dif.posY
            for n in range(dif.count):
                coord.append([startX, startY, Z*HeightFull, 0, 0])
                startX += Length + dif.shov
            if dif.ext > 0:
                coord.append([startX, startY, Z*HeightFull, 0, dif.ext])

            return coord

        def MakeVertical(dif, Z):
            coord = []
            startX = dif.posX
            startY = dif.posY
            for n in range(dif.count):
                coord.append([startX, startY, Z*HeightFull, 1, 0])
                startY += Length + dif.shov
            if dif.ext > 0:
                coord.append([startX, startY, Z*HeightFull, 1, dif.ext])
            return coord

        numRow = 0
        for n in range(CountRow):
            aRow = []
            aRow.extend(Makehorizont(difHorizontRow1, numRow))
            aRow.extend(Makehorizont(difHorizontRow2, numRow))
            aRow.extend(MakeVertical(difVerticalRow1, numRow))
            aRow.extend(MakeVertical(difVerticalRow2, numRow))
            acord.append(aRow)

            numRow += 1
            aRow = []
            aRow.extend(Makehorizont(difHorizontRow3, numRow))
            aRow.extend(Makehorizont(difHorizontRow4, numRow))
            aRow.extend(MakeVertical(difVerticalRow3, numRow))
            aRow.extend(MakeVertical(difVerticalRow4, numRow))
            acord.append(aRow)
            numRow += 1

        CountBloksRow = difHorizontRow1.count + difHorizontRow2.count + \
            difVerticalRow1.count + difVerticalRow2.count
        print("Кирпичей в ряду: "+str(CountBloksRow))

        Length_Bl = str(Length)+' mm'
        Width_Bl = str(Width)+' mm'
        Height_Bl = str(Height)+' mm'

        Rotation90 = App.Rotation(App.Vector(0, 0, 1), 90)
        Rotation0 = App.Rotation(App.Vector(0, 0, 0), 0)

        AllBlock = len(acord)*len(acord[0])

        countBlocks = 1
        countRows = 0
        for row in acord:
            Compound = App.activeDocument().addObject("Part::Compound", "Compound_"+"row"+str(countRows))
            Links = []
            for par in row:
                Object = App.ActiveDocument.addObject("Part::Box", "Box" + str(countBlocks))
                Object.Label = "Куб" + str(countBlocks)
                if (par[4] == 0):
                    Object.Length = Length_Bl
                else:
                    Object .Length = str(par[4])+' mm'
                Object.Width = Width_Bl
                Object.Height = Height_Bl
                countBlocks += 1

                if (par[3] == 0):
                    Rotation = Rotation0
                else:
                    Rotation = Rotation90
                placeX = par[0]
                placeY = par[1]
                placeZ = par[2]
                Object.Placement = App.Placement(App.Vector(
                    placeX, placeY, placeZ), Rotation, App.Vector(0, 0, 0))

                Links.append(Object)
                # sg.one_line_progress_meter(
                #     'Построение печи!', countBlocks+1, AllBlock, '-key-')

            Compound.Links = Links
            Compound.Links = Links
            countRows += 1
            self.signalForProgress.emit(countRows, len(acord))


        App.ActiveDocument.recompute()


class ParamBake(QtGui.QWidget):
    SignalMyWindow = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__()
        if debugFile:
            self.ui_file = 'forma1_3.ui'
        else:
            self.ui_file = os.path.join(App.getUserMacroDir(True), 'forma1_3.ui')
        f, w = gui.PySideUic.loadUiType(self.ui_file)
        self.form = f()
        self.widget = w()
        self.form.setupUi(self.widget)
        self.widget.show()

        # создадим поток
        self.thread = QtCore.QThread()
        # создадим объект для выполнения кода в другом потоке
        self.browserHandler = BrowserHandler()
        # после чего подключим все сигналы и слоты
        self.browserHandler.signalForProgress.connect(self.UpdateProgress)
        self.SignalMyWindow.connect(self.browserHandler.MakeBrake)
        # # запустим поток
        self.thread.start()
        self._connect_widgets()
        self.set_param_form()
        self.widget.show()

    def UpdateProgress(self, count, maximum):
        if self.form.progressBar.maximum() != maximum:
            self.form.progressBar.setMaximum(maximum)
        self.form.progressBar.setValue(count)

    def set_param_form(self):
        self.widget.setWindowTitle("Построитель печи")

        self.form.label.setText("Длина")
        self.form.label_2.setText("Ширина")
        self.form.label_3.setText("Высота")
        self.form.label_4.setText("Параметры кирпича, мм")
        self.form.label_5.setText("Длина")
        self.form.label_6.setText("Размеры печи в кирпичах")
        self.form.label_7.setText("Ширина")
        self.form.label_8.setText("Кол-во рядов")
        self.form.label_9.setText("Шов")
        self.form.checkBox1.setText(" + ширина кирпича")
        self.form.checkBox2.setText(" + ширина кирпича")
        self.form.checkBox2_2.setText(" + ширина кирпича")
        self.form.checkBoxCAlcShov.setText("Растягивать швы")

        self.form.pushButtonCreate.setText("Создать печь")

    def _connect_widgets(self):
        self.form.label.setText("Длина")
        self.form.BrikLength.setProperty("value", Length)
        self.form.BrikWidth.setProperty("value", Width)
        self.form.BrikHeight.setProperty("value", Height)
        self.form.Shov.setProperty("value", shov)
        self.form.BakeLength.setProperty("value", FullHoriz[0])
        self.form.BakeWidth.setProperty("value", FullVertical[0])
        self.form.BakeRow.setProperty("value", CountRow)

        if (FullHoriz[1] == 0):
            self.form.checkBox1.setCheckState(QtCore.Qt.Unchecked)
        else:
            self.form.checkBox1.setCheckState(QtCore.Qt.Checked)
        if (FullVertical[1] == 0):
            self.form.checkBox2.setCheckState(QtCore.Qt.Unchecked)
        else:
            self.form.checkBox2.setCheckState(QtCore.Qt.Checked)
        self.form.pushButtonCreate.pressed.connect(self.draw)


    def draw(self):
        msgBox = QtGui.QMessageBox()
        self.SignalMyWindow.emit(self)

        # MakeBrake(self)

    def close(self):
        self.form.hide()


if __name__ == '__main__':
    if debugFile:
        gui.showMainWindow()

    if App.ActiveDocument == None:
        App.newDocument()
    d = ParamBake()
    if debugFile:
        gui.exec_loop()
