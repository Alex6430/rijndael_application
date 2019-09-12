import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, \
    QLineEdit, QFileDialog, QGroupBox, QRadioButton, QTextEdit, \
    QStatusBar, QLabel, QVBoxLayout, QPushButton, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from polynomial import *
from application import *


# global state, blok, key, mod, flagBlok
# state , blok ,key , mod , flagBlok = 0, 0, 0, 0, True

class help(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("help")
        self.resize(600, 500)
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 600, 500))
        self.textEdit.setText("Программа предназначена для шифрования и расшифровки документов.\n"
                             " Можно шифровать только документы с раширением txt.\n"
                             "Сначала необходимо выбрать размер открытого текста и размер ключа.\n"
                             " Также необходимо выбрать режим сцепления блоков шифротектса и неприводимые\n "
                             "полиномы для умножения в полях Галуа.\n "
                             "При нажатии на кнопку продолжить, нужно ввести ключ, вектор инициализации (IV)\n "
                             "(вектор инициализации используется в режимах спецпления блоков шифротекста CBC, OFB, CFB)\n "
                             " и выбать файл. Дальше выбрать, что нужно сделать с файлом - зашифровать или расшифровать.\n"
                             "Размер вектора инициализации должен совпадать с размером текста. \n")
        # self.label_3 = QLabel(self)
        # self.label_3.setGeometry(QtCore.QRect(0, 0, 600, 500))
        # self.label_3.setObjectName("help")
        # self.label_3.setText("Программа предназначена для шифрования и расшифровки документов.\n"
        #                      " Можно шифровать только документы с раширением txt.\n"
        #                      "Сначала необходимо выбрать размер открытого текста и размер ключа.\n"
        #                      " Также необходимо выбрать режим сцепления блоков шифротектса и неприводимые\n "
        #                      "полиномы для умножения в полях Галуа.\n "
        #                      "При нажатии на кнопку продолжить, нужно ввести ключ, вектор инициализации (IV)\n "
        #                      "(вектор инициализации используется в режимах спецпления блоков шифротекста CBC, OFB, CFB)\n "
        #                      " и выбать файл. Дальше выбрать, что нужно сделать с файлом - зашифровать или расшифровать.\n"
        #                      "Размер вектора инициализации должен совпадать с размером текста. \n")

class about(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("about")
        self.resize(400, 200)
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 400, 200))
        self.textEdit.setText("Студент Таранов Алексей\n"
                              "группа М8О-113М-19")


class file(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Rijndael")
        self.resize(600, 500)
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(50, 50, 281, 87))
        self.textEdit.setObjectName("textEdit")
        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(50, 30, 181, 16))
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Введите ключ")

        if (flagBlok == True):
            self.IVEdit = QTextEdit(self)
            self.IVEdit.setGeometry(QtCore.QRect(50, 250, 281, 87))
            self.IVEdit.setObjectName("IVEdit")
            self.label_4 = QLabel(self)
            self.label_4.setGeometry(QtCore.QRect(50, 230, 181, 16))
            self.label_4.setObjectName("label_4")
            self.label_4.setText("Введите IV")

        self.encript_btn = QPushButton(self)
        self.encript_btn.setGeometry(QtCore.QRect(100, 400, 112, 34))
        self.encript_btn.setObjectName("encript_btn")
        ########### button event
        self.encript_btn.clicked.connect(self.show_encript)
        ############
        self.encript_btn.setText("Зашифровать")

        self.decript_btn = QPushButton(self)
        self.decript_btn.setGeometry(QtCore.QRect(300, 400, 122, 34))
        self.decript_btn.setObjectName("decript_btn")
        ########### button event
        self.decript_btn.clicked.connect(self.show_dicript)
        ############
        self.decript_btn.setText("Расшифровать")

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(200, 150, 181, 50))
        self.lineEdit.setObjectName("lineEdit")

        self.file_btn = QPushButton(self)
        self.file_btn.setGeometry(QtCore.QRect(50, 150, 112, 34))
        self.file_btn.setObjectName("file_btn")
        ########### button event
        self.file_btn.clicked.connect(self.openFileNameDialog)
        ############
        self.file_btn.setText("выбрать файл")

        self.lineEdit.setText(fil)

    def show_encript(self):
        if (flagBlok == False):
            text = self.textEdit.toPlainText()
            filename = self.lineEdit.text()
            print(text)
            print(filename)
            if ((self.textEdit.toPlainText().replace(" ", "") == "")
                    or (self.lineEdit.text().replace(" ", "") == "")
                    or (self.textEdit.toPlainText().replace("\n", "") == "")
                    or (self.lineEdit.text().replace(" ", "") == " ")):
                self.showMessageBox("ошибка", "Введите данные")
            else:
                if (key == 128):
                    if (len(self.textEdit.toPlainText()) == 16):
                        text = self.textEdit.toPlainText()
                        filename = self.lineEdit.text()
                        initialization(state, key, mod)
                        encryptRijndael(filename, blok, text, "")
                        self.showMessageBox("готово", "зашифровалось")
                    else:
                        self.showMessageBox("ошибка", "размер ключа должен быть 16 байт")
                elif (key == 192):
                    if (len(self.textEdit.toPlainText()) == 24):
                        text = self.textEdit.toPlainText()
                        filename = self.lineEdit.text()
                        initialization(state, key, mod)
                        encryptRijndael(filename, blok, text, "")
                        self.showMessageBox("готово", "зашифровалось")
                    else:
                        self.showMessageBox("ошибка", "размер ключа должен быть 24 байта")
                elif (key == 256):
                    if (len(self.textEdit.toPlainText()) == 32):
                        text = self.textEdit.toPlainText()
                        filename = self.lineEdit.text()
                        initialization(state, key, mod)
                        encryptRijndael(filename, blok, text, "")
                        self.showMessageBox("готово", "зашифровалось")
                    else:
                        self.showMessageBox("ошибка", "размер ключа должен быть 32 байта")
        else:
            text = self.textEdit.toPlainText()
            filename = self.lineEdit.text()
            IVtext = self.IVEdit.toPlainText()
            print(text)
            print(filename)
            print(IVtext)
            if (self.textEdit.toPlainText().replace(" ", "") == ""
                    or (self.textEdit.toPlainText().replace("\n", "") == "")
                    or self.lineEdit.text().replace(" ", "") == ""
                    or self.IVEdit.toPlainText().replace("\n", "") == ""
                    or self.IVEdit.toPlainText().replace(" ", "") == ""):
                self.showMessageBox("ошибка", "Введите данные")
            else:
                print(state)
                print(blok)
                print(key)
                if (key == 128):
                    print("зашел в кей")
                    print(len(self.textEdit.toPlainText()))
                    if (len(self.textEdit.toPlainText()) == 16):
                        print("зашел в кей == 16")
                        if (state == 128):
                            if (len(self.IVEdit.toPlainText()) == 16):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                encryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "зашифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 16 байт")
                        elif (state == 192):
                            if (len(self.IVEdit.toPlainText()) == 24):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                encryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "зашифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 24 байт")
                        elif (state == 256):
                            if (len(self.IVEdit.toPlainText()) == 32):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                encryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "зашифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 32 байт")
                    else:
                        print("else")
                        self.showMessageBox("ошибка", "размер ключа должен быть 16 байт")
                elif (key == 192):
                    if (len(self.textEdit.toPlainText()) == 24):
                        if (state == 128):
                            if (len(self.IVEdit.toPlainText()) == 16):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                encryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "зашифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 16 байт")
                        elif (state == 192):
                            if (len(self.IVEdit.toPlainText()) == 24):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                encryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "зашифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 24 байт")
                        elif (state == 256):
                            if (len(self.IVEdit.toPlainText()) == 32):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                encryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "зашифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 32 байт")
                    else:
                        self.showMessageBox("ошибка", "размер ключа должен быть 24 байта")
                elif (key == 256):
                    if (len(self.textEdit.toPlainText()) == 32):
                        if (state == 128):
                            if (len(self.IVEdit.toPlainText()) == 16):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                encryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "зашифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 16 байт")
                        elif (state == 192):
                            if (len(self.IVEdit.toPlainText()) == 24):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                encryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "зашифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 24 байт")
                        elif (state == 256):
                            if (len(self.IVEdit.toPlainText()) == 32):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                encryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "зашифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 32 байт")
                    else:
                        self.showMessageBox("ошибка", "размер ключа должен быть 32 байта")
                else:
                    text = self.textEdit.toPlainText()
                    filename = self.lineEdit.text()
                    IVtext = self.IVEdit.toPlainText()
                    print(text)
                    print(filename)
                    print(IVtext)

    def show_dicript(self):
        if (flagBlok == False):
            text = self.textEdit.toPlainText()
            filename = self.lineEdit.text()
            print(text)
            print(filename)
            if ((self.textEdit.toPlainText().replace(" ", "") == "")
                    or (self.lineEdit.text().replace(" ", "") == "")
                    or (self.textEdit.toPlainText().replace("\n", "") == "")
                    or (self.lineEdit.text().replace(" ", "") == " ")):
                self.showMessageBox("ошибка", "Введите данные")
            else:
                if (key == 128):
                    if (len(self.textEdit.toPlainText()) == 16):
                        text = self.textEdit.toPlainText()
                        filename = self.lineEdit.text()
                        initialization(state, key, mod)
                        decryptRijndael(filename, blok, text, "")
                        self.showMessageBox("готово", "расшифровалось")
                    else:
                        self.showMessageBox("ошибка", "размер ключа должен быть 16 байт")
                elif (key == 192):
                    if (len(self.textEdit.toPlainText()) == 24):
                        text = self.textEdit.toPlainText()
                        filename = self.lineEdit.text()
                        initialization(state, key, mod)
                        decryptRijndael(filename, blok, text, "")
                        self.showMessageBox("готово", "расшифровалось")
                    else:
                        self.showMessageBox("ошибка", "размер ключа должен быть 24 байта")
                elif (key == 256):
                    if (len(self.textEdit.toPlainText()) == 32):
                        text = self.textEdit.toPlainText()
                        filename = self.lineEdit.text()
                        initialization(state, key, mod)
                        decryptRijndael(filename, blok, text, "")
                        self.showMessageBox("готово", "расшифровалось")
                    else:
                        self.showMessageBox("ошибка", "размер ключа должен быть 32 байта")
        else:
            text = self.textEdit.toPlainText()
            filename = self.lineEdit.text()
            IVtext = self.IVEdit.toPlainText()
            print(text)
            print(filename)
            print(IVtext)
            if (self.textEdit.toPlainText().replace(" ", "") == ""
                    or (self.textEdit.toPlainText().replace("\n", "") == "")
                    or self.lineEdit.text().replace(" ", "") == ""
                    or self.IVEdit.toPlainText().replace("\n", "") == ""
                    or self.IVEdit.toPlainText().replace(" ", "") == ""):
                self.showMessageBox("ошибка", "Введите данные")
            else:
                print(state)
                print(blok)
                print(key)
                if (key == 128):
                    print("зашел в кей")
                    print(len(self.textEdit.toPlainText()))
                    if (len(self.textEdit.toPlainText()) == 16):
                        print("зашел в кей == 16")
                        if (state == 128):
                            if (len(self.IVEdit.toPlainText()) == 16):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                decryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "расшифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 16 байт")
                        elif (state == 192):
                            if (len(self.IVEdit.toPlainText()) == 24):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                decryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "расшифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 24 байт")
                        elif (state == 256):
                            if (len(self.IVEdit.toPlainText()) == 32):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                decryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "расшифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 32 байт")
                    else:
                        print("else")
                        self.showMessageBox("ошибка", "размер ключа должен быть 16 байт")
                elif (key == 192):
                    if (len(self.textEdit.toPlainText()) == 24):
                        if (state == 128):
                            if (len(self.IVEdit.toPlainText()) == 16):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                decryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "расшифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 16 байт")
                        elif (state == 192):
                            if (len(self.IVEdit.toPlainText()) == 24):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                decryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "расшифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 24 байт")
                        elif (state == 256):
                            if (len(self.IVEdit.toPlainText()) == 32):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                decryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "расшифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 32 байт")
                    else:
                        self.showMessageBox("ошибка", "размер ключа должен быть 24 байта")
                elif (key == 256):
                    if (len(self.textEdit.toPlainText()) == 32):
                        if (state == 128):
                            if (len(self.IVEdit.toPlainText()) == 16):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                decryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "расшифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 16 байт")
                        elif (state == 192):
                            if (len(self.IVEdit.toPlainText()) == 24):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                decryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "расшифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 24 байт")
                        elif (state == 256):
                            if (len(self.IVEdit.toPlainText()) == 32):
                                text = self.textEdit.toPlainText()
                                filename = self.lineEdit.text()
                                IVtext = self.IVEdit.toPlainText()
                                initialization(state, key, mod)
                                decryptRijndael(filename, blok, text, IVtext)
                                self.showMessageBox("готово", "расшифровалось")
                            else:
                                self.showMessageBox("ошибка", "размер IV должен быть 32 байт")
                    else:
                        self.showMessageBox("ошибка", "размер ключа должен быть 32 байта")
                else:
                    text = self.textEdit.toPlainText()
                    filename = self.lineEdit.text()
                    IVtext = self.IVEdit.toPlainText()
                    print(text)
                    print(filename)
                    print(IVtext)

    def showMessageBox(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        # msgBox.setIcon(QtWidgets.QMessageBox.warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()

    def initUI(self):
        # self.setWindowTitle(self.title)

        # self.setGeometry(self.left, self.top, self.width, self.height)

        self.openFileNameDialog()

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()

        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*.txt);;Python Files (*.txt)", options=options)
        if fileName:
            print(fileName)
            self.lineEdit.setText(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()

        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()

        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)


class App(QWidget):
    def __init__(self):
        super().__init__()
        global fil
        fil = ""
        self.setObjectName("Rijndael")
        self.resize(800, 500)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.size_state = QGroupBox(self.centralwidget)
        self.size_state.setGeometry(QtCore.QRect(200, 30, 121, 121))
        self.size_state.setObjectName("size_state")
        self.state128 = QRadioButton(self.size_state)
        self.state128.setGeometry(QtCore.QRect(20, 30, 95, 20))
        self.state128.setObjectName("state128")
        self.state192 = QRadioButton(self.size_state)
        self.state192.setGeometry(QtCore.QRect(20, 60, 95, 20))
        self.state192.setObjectName("state192")
        self.state256 = QRadioButton(self.size_state)
        self.state256.setGeometry(QtCore.QRect(20, 90, 95, 20))
        self.state256.setObjectName("state256")

        self.blok = QGroupBox(self.centralwidget)
        self.blok.setGeometry(QtCore.QRect(200, 200, 150, 150))
        self.blok.setObjectName("blok")
        self.blok_ECB = QRadioButton(self.blok)
        self.blok_ECB.setGeometry(QtCore.QRect(20, 30, 95, 20))
        self.blok_ECB.setObjectName("blok_ECB")
        self.blok_CBC = QRadioButton(self.blok)
        self.blok_CBC.setGeometry(QtCore.QRect(20, 60, 95, 20))
        self.blok_CBC.setObjectName("blok_CBC")
        self.blok_CFB = QRadioButton(self.blok)
        self.blok_CFB.setGeometry(QtCore.QRect(20, 90, 95, 20))
        self.blok_CFB.setObjectName("blok_CFB")
        self.blok_OFB = QRadioButton(self.blok)
        self.blok_OFB.setGeometry(QtCore.QRect(20, 120, 95, 20))
        self.blok_OFB.setObjectName("blok_OFB")

        self.size_key = QGroupBox(self.centralwidget)
        self.size_key.setGeometry(QtCore.QRect(550, 30, 130, 130))
        self.size_key.setObjectName("size_key")
        self.verticalLayout = QVBoxLayout(self.size_key)
        self.verticalLayout.setObjectName("verticalLayout")
        self.key128 = QRadioButton(self.size_key)
        self.key128.setObjectName("key128")
        self.verticalLayout.addWidget(self.key128)
        self.key192 = QRadioButton(self)
        self.key192.setObjectName("key192")
        self.verticalLayout.addWidget(self.key192)
        self.key256 = QRadioButton(self)
        self.key256.setObjectName("key256")
        self.verticalLayout.addWidget(self.key256)

        self.comboBox = QComboBox(self)
        # self.comboBox.addItem("1")
        # self.comboBox.addItem("2")
        # self.comboBox.addItem("20")
        self.comboBox.addItem(" ")
        self.comboBox.addItems(poly_in_str)
        self.comboBox.activated.connect(self.selectionchange)

        self.helpBox = QComboBox(self)
        self.helpBox.addItems(["help", "about"])
        self.helpBox.activated.connect(self.selectionchangehelp)
        self.helpBox.setGeometry(QtCore.QRect(700, 0, 100, 25))
        self.helpBox.setObjectName("helpBox")

        # self.help_comboBox.addItems(["Java", "C#", "Python"])
        # self.help_comboBox.activated.connect(self.selectionchange)
        self.comboBox.setGeometry(QtCore.QRect(500, 200, 300, 25))
        self.comboBox.setObjectName("comboBox")

        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(50, 30, 100, 16))
        self.label.setObjectName("label")
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(390, 30, 100, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(50, 200, 100, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(390, 200, 100, 16))
        self.label_4.setObjectName("label_4")
        self.press_btn = QPushButton(self)
        self.press_btn.setGeometry(QtCore.QRect(300, 400, 112, 34))
        self.press_btn.setObjectName("press_btn")
        ########### button event
        self.press_btn.clicked.connect(self.show_file)
        ############

        # self.setCentralWidget(self)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        # self.setStatusBar(self)

        self.size_state.setTitle("size state")
        self.state128.setText("128 bits")
        self.state192.setText("192 bits")
        self.state256.setText("256 bits")
        self.blok.setTitle("blok")
        self.blok_CBC.setText("blok_CBC")
        self.blok_CFB.setText("blok_CFB")
        self.blok_ECB.setText("blok_ECB")
        self.blok_OFB.setText("blok_OFB")
        self.size_key.setTitle("size key")
        self.key128.setText("128 bits")
        self.key192.setText("192 bits")
        self.key256.setText("256 bits")
        self.label.setText("Размер текста")
        self.label_2.setText("Размер ключа")
        self.label_3.setText("Режим блока")
        self.label_4.setText("модуль")

        self.press_btn.setText("продолжить")
        # self.initUI()

        self.show()

    def selectionchange(self, i):
        global mod
        # print("Items in the list are :")
        # for count in range(self.help_comboBox.count()):
        #     print(self.help_comboBox.itemText(count))
        # print("Current index", i, "selection changed ", self.help_comboBox.currentText())
        poly = [0x00, 0x11B, 0x11D, 0x12B, 0x12D, 0x139, 0x13F,
                0x14D, 0x15F, 0x163, 0x165, 0x169, 0x171,
                0x177, 0x17B, 0x187, 0x18B, 0x18D, 0x19F,
                0x1BD, 0x1C3, 0x1CD, 0x1D7, 0x1DD, 0x1E7,
                0x1F3, 0x1F5, 0x1F9]
        mod = poly[i]
        return mod

    def selectionchangehelp(self, i):
        if i==0:
            self.h = help()
            self.h.show()
        if i==1:
            self.a = about()
            self.a.show()


    def show_file(self):
        global state, blok, key, flagBlok
        if (self.blok_ECB.isChecked() == True):
            flagBlok = False
        else:
            flagBlok = True

        if (self.state128.isChecked() == False) and (self.state192.isChecked() == False) and (
                self.state256.isChecked() == False):
            self.showMessageBox("ошибка", "выберите размер текста")
        elif (self.key128.isChecked() == False) and (self.key192.isChecked() == False) and (
                self.key256.isChecked() == False):
            self.showMessageBox("ошибка", "выберите размер ключа")
        elif (self.blok_OFB.isChecked() == False) and (self.blok_ECB.isChecked() == False) and \
                (self.blok_CFB.isChecked() == False) and (self.blok_CBC.isChecked() == False):
            self.showMessageBox("ошибка", "выберите режим шифрования")
        elif (self.comboBox.currentText()== " "):
            self.showMessageBox("ошибка", "выберите модуль")
        else:
            if (self.state128.isChecked() == True):
                state = 128
            if (self.state192.isChecked() == True):
                state = 192
            if (self.state256.isChecked() == True):
                state = 256
            if (self.key128.isChecked() == True):
                key = 128
            if (self.key192.isChecked() == True):
                key = 192
            if (self.key256.isChecked() == True):
                key = 256
            if (self.blok_OFB.isChecked() == True):
                blok = 3
            if (self.blok_ECB.isChecked() == True):
                blok = 1
            if (self.blok_CFB.isChecked() == True):
                blok = 4
            if (self.blok_CBC.isChecked() == True):
                blok = 2

            # mod = 0
            print(state)
            print(blok)
            print(key)
            print(mod)
            self.w1 = file()
            self.w1.show()

        # self.close()

    def showMessageBox(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        # msgBox.setIcon(QtWidgets.QMessageBox.warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
