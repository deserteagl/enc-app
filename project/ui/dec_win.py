
from constants import File_ERROR,SUCCESS,algorithms,VERIFY_FALSE
from queue import Queue
from os.path import isfile
from threading import Lock
from multiprocessing import Pool
from os import stat
from struct import pack
from hashlib import sha256
from OEAP_enc import *
from AES_CTR import File_KDF_AES
from BlowFish_CTR import File_KDF_BlowFish
from Marca_Ciph import File_Marca
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.Password_win import PasswordEdit
from KDF import KDF
from time import sleep
from ui.progress import Ui_Dia
from Key_gen import Import_marcakey,generate_init_marca_keys
from _queue import Empty

lock = Lock()
class ThreadPool(QtCore.QThread):
    signal = QtCore.pyqtSignal(int)
    value = 0
    working_thread = 0
    threads_running = []
    counter = 0
    q = Queue()
    def __init__(self,threads):
        super(ThreadPool, self).__init__()
        self.threads = threads

    def change_state(self):
            self.value += (1/len(self.threads))*100
            self.working_thread -= 1
            try:
                lock.release()
            except:
                pass
            if self.working_thread < 2:
                    try:
                        thread = self.q.get_nowait()

                        #lock.acquire()
                        self.signal.emit(self.value)
                        #lock.release()
                        thread.update.connect(self.change_state)
                        thread.start()
                        sleep(.001)
                        self.working_thread += 1
                    except Empty:
                        #lock.acquire()
                        self.signal.emit(100)
                        #lock.release()
                        self.quit()
                        self.wait()
            '''            
            else:
                try:
                    for th in self.threads_running:
                        th.quit()
                    raise ValueError('Too much threading are running')
                except:
                    self.quit()
                    self.wait()
                    raise ValueError('no threads are running')
            '''

    def run(self):

        if len(self.threads) > 2:
            for t in self.threads:
                self.q.put_nowait(t)

            t1 =self.q.get_nowait()
            t2 = self.q.get_nowait()
            t1.update.connect(self.change_state)
            t2.update.connect(self.change_state)
            t1.start()
            sleep(.01)
            t2.start()
            sleep(.01)
            self.working_thread = 2
        else:
            for t in self.threads:
                t.update.connect(self.change_state)
                t.start()
                sleep(0.001)
                self.working_thread = 2

class Ui_decDialog(QtWidgets.QDialog):
    def __init__(self, Parent,files):
        super().__init__(Parent)
        self.files = files
        self.setObjectName("EncDialog")
        self.resize(487, 286)
        self.setMaximumSize(QtCore.QSize(487, 234))

        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 40, 501, 131))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.verticalLayoutWidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.label_2 = QtWidgets.QLabel(self.page)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 111, 18))
        self.label_2.setObjectName("label_2")
        self.lineEdit = PasswordEdit(self.page)
        self.lineEdit.setGeometry(QtCore.QRect(10, 30, 441, 32))
        self.lineEdit.setObjectName("passwordEdit")
        self.label_3 = QtWidgets.QLabel(self.page)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 58, 18))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.page)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 90, 401, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.page)
        self.pushButton.setGeometry(QtCore.QRect(420, 90, 33, 31))
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/folde.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.page_2)
        self.lineEdit_3.setGeometry(QtCore.QRect(10, 90, 401, 32))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_4 = QtWidgets.QLabel(self.page_2)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 58, 18))
        self.label_4.setObjectName("label_4")
        self.lineEdit_4 = PasswordEdit(self.page_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(10, 30, 441, 32))
        self.lineEdit_4.setObjectName("passwordEdit_2")
        self.label_5 = QtWidgets.QLabel(self.page_2)
        self.label_5.setGeometry(QtCore.QRect(10, 10, 111, 18))
        self.label_5.setObjectName("label_5")
        self.pushButton_2 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_2.setGeometry(QtCore.QRect(420, 90, 33, 31))
        self.pushButton_2.setText("")
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setObjectName("pushButton_2")
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout.addWidget(self.stackedWidget)
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(140, 180, 88, 34))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(250, 180, 88, 34))
        self.pushButton_4.setObjectName("pushButton_4")

        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setModal(True)
        self.prepare_actions()
        self.len_f = len(self.files)

        self.q = Queue()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("dialog", "Decrypt File"))

        self.label_2.setText(_translate("Form", "Enter Passphrase"))
        self.label_3.setText(_translate("Form", "Key-File"))
        self.label_4.setText(_translate("Form", "Key-File"))
        self.label_5.setText(_translate("Form", "Enter Passphrase"))
        self.pushButton_3.setText(_translate("Form", "Ok"))
        self.pushButton_4.setText(_translate("Form", "Cancel"))

    def prepare_actions(self):
        if self.files[0].endswith('mfai'):
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(0)

        self.pushButton_4.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.dec)
        self.pushButton.clicked.connect(self.behav_btn)
        self.pushButton_2.clicked.connect(self.behav_btn)

    def behav_btn(self):
        if self.stackedWidget.currentIndex() == 0:
            fileMode = QtWidgets.QFileDialog(self)
            #fileMode.setFilter(QtWidgets.QFileDialog.DirectoryOnly)

            file = fileMode.getOpenFileName(caption='get key file',filter='key files (*.key)')
            if file[0]:
                self.lineEdit_2.setText(file[0])
        elif self.stackedWidget.currentIndex() == 1:
            fileMode = QtWidgets.QFileDialog(self)
            file = fileMode.getOpenFileName(caption='get key file', filter='key files (*.mkey)')
            if file[0]:
                self.lineEdit_3.setText(file[0])
    def check(self,files,password,key_data):
        hash = password + sha256(key_data).digest()
        for i in files:
            fd = open(i,'rb')
            if fd.read(64) != hash:
                fd.close()
                return File_ERROR
            fd.close()
        return SUCCESS

    def dec(self):
        if self.stackedWidget.currentIndex() == 1:
            if self.lineEdit_4.text() == '' or len(self.lineEdit_4.text()) < 8:
                msg = QtWidgets.QMessageBox(self)
                msg.setText("Password is too short \nmust be at least 8 long")
                msg.setWindowTitle("pass error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.buttonClicked.connect(msg.close)
                msg.setModal(True)
                msg.show()
                return

            if self.lineEdit_3.text() == '' or not isfile(self.lineEdit_3.text()):
                msg = QtWidgets.QMessageBox(self)
                msg.setText("key file path is invalid or empty ")
                msg.setWindowTitle("key path error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.buttonClicked.connect(msg.close)
                msg.setModal(True)
                msg.show()
                return
            files = self.files
            fd = open(self.lineEdit_3.text(), 'rb')
            fd_data = fd.read()
            fd.close()
            password = sha256(self.lineEdit_4.text().encode()).digest()
            if self.check(self.files,password,fd_data) == File_ERROR:
                msg = QtWidgets.QMessageBox(self)
                msg.setText("The key or Password is invalid")
                msg.setWindowTitle("Input error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.buttonClicked.connect(msg.close)
                msg.setModal(True)
                msg.show()
                return

            key = Import_marcakey(self.lineEdit_3.text())

            if key == File_ERROR:
                msg = QtWidgets.QMessageBox(self)
                msg.setText("key file is invalid")
                msg.setWindowTitle("key file error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.buttonClicked.connect(msg.close)
                msg.setModal(True)
                msg.show()
                return
            k1,k2,nonce = generate_init_marca_keys(key)
            #k1 = k1;k2=str(k2);nonce=str(nonce)
            threads = []
            self.count = len(self.files)
            self.count_2 = 0
            self.lock = Lock()

            self.value = 0
            self.pgB_d = Ui_Dia(self)
            self.pgB_d.label.setText("Decrypting Files")
            self.pgB_d.setWindowTitle('Decrypt File')
            self.pgB_d.label_2.setText("0/%d"%len(self.files))
            self.pgB = self.pgB_d.progressBar
            self.pgB_d.show()


            for file in self.files:
                    self.q.put_nowait(File_Marca(file, [None, [k1, k2, nonce,40,0]], oper=0))

            if self.len_f < 2:

                self.working_threads = 2
                t = self.q.get_nowait()
                t.update.connect(self.change_value)
                print('inside')
                t.start()
                sleep(.001)
            else:

                self.working_threads = 2
                t1 = self.q.get_nowait()
                t2 = self.q.get_nowait()
                t1.update.connect(self.change_value)
                t2.update.connect(self.change_value)
                print('inside')
                t1.start()
                sleep(.001)
                t2.start()
                sleep(.001)
            '''pool = ThreadPool(threads)
            pool.signal.connect(self.change_value)
            pool.start()
            
            for thread in threads:
                if self.working_thread < 2:
                    self.working_thread += 1
                    thread.update.connect(self.change_value)
                    print('inside')
                    thread.start()
                    sleep(0.001)
            '''

        else:
            if self.lineEdit.text() == '' or len(self.lineEdit.text()) < 8:
                msg = QtWidgets.QMessageBox(self)
                msg.setText("Password is too short \nmust be at least 8 long")
                msg.setWindowTitle("pass error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.buttonClicked.connect(msg.close)
                msg.setModal(True)
                msg.show()
                return
            elif self.lineEdit_2.text() =='' or not isfile(self.lineEdit_2.text()):
                msg = QtWidgets.QMessageBox(self)
                msg.setText("key file path is invalid or empty ")
                msg.setWindowTitle("key path error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.buttonClicked.connect(msg.close)
                msg.setModal(True)
                msg.show()
                return
            keysize = check_key_valid(self.lineEdit_2.text())

            if keysize == File_ERROR:
                msg = QtWidgets.QMessageBox(self)
                msg.setText("key file is invalid")
                msg.setWindowTitle("key file error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.buttonClicked.connect(msg.close)
                msg.setModal(True)
                msg.show()
                return
            keysize = int(keysize/8)
            files = self.files
            rsa_wrapper = Signature
            hash_pass = sha256(self.lineEdit.text().encode()).digest()
            files_data = dict()
            for i in self.files:
                fd = open(i,'rb')
                data = fd.read(keysize)
                is_inValid,data = Signature.Verify(data,self.lineEdit_2.text())
                fd.close()
                if is_inValid == SUCCESS:
                    if data[:32] !=  hash_pass:
                        msg = QtWidgets.QMessageBox(self)
                        msg.setText("key or Password is incorrect")
                        msg.setWindowTitle("Input error")
                        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        msg.buttonClicked.connect(msg.close)
                        msg.setModal(True)
                        msg.show()
                        return
                    files_data[i] = [data[32:40],data[40:44]]
                    continue

                msg = QtWidgets.QMessageBox(self)
                msg.setText("key or Password is incorrect")
                msg.setWindowTitle("Input error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.buttonClicked.connect(msg.close)
                msg.setModal(True)
                msg.show()
                return

            password = KDF(self.lineEdit.text()).generate_key_from_pass()
            threads = []
            self.count = len(self.files)
            self.count_2 = 0
            self.lock = Lock()
            self.value = 0
            self.pgB_d = Ui_Dia(self)
            self.pgB_d.label.setText("Decrypting Files")
            self.pgB_d.setWindowTitle('Decrypt File')
            self.pgB_d.label_2.setText("0/%d" % len(self.files))
            self.pgB = self.pgB_d.progressBar
            self.pgB_d.show()
            for file in self.files:
                k1 = password[:32];k2=password[32:48]
                if files_data[file][1] == algorithms['AES']:

                    self.q.put_nowait(File_KDF_AES(file,[0,[k1,k2,keysize,files_data[file][0]]],0))
                else:
                    self.q.put_nowait(File_KDF_BlowFish(file,[0,[k1,k2,keysize,files_data[file][0]]],oper=0))
            if self.len_f < 2:

                self.working_threads = 2
                t = self.q.get_nowait()
                t.update.connect(self.change_value)
                print('inside')
                t.start()
                sleep(.001)
            else:

                self.working_threads = 2
                t1 = self.q.get_nowait()
                t2 = self.q.get_nowait()
                t1.update.connect(self.change_value)
                t2.update.connect(self.change_value)
                print('inside')
                t1.start()
                sleep(.001)
                t2.start()
                sleep(.001)


        self.close()


    def change_value(self,val):
        self.value += (1 / self.count) * 100
        print(self.value)
        self.count_2 +=1
        self.working_threads -= 1


        if self.value >=100 or self.count_2 == self.len_f:
            lock.acquire()
            self.pgB_d.label_2.setText('%d/%d'%(len(self.files),len(self.files)))
            self.pgB.setValue(100)
            self.pgB_d.close()
            lock.release()
            sleep(.001)
        else :
            lock.acquire()
            self.pgB.setValue(self.value)
            self.pgB_d.label_2.setText('%d/%d'%(self.count_2,len(self.files)))
            lock.release()
            sleep(.001)

        if self.working_threads < 2:
            try:
                thread = self.q.get_nowait()
                thread.update.connect(self.change_value)
                self.working_threads += 1
                thread.start()
                sleep(.001)

            except Empty:
                pass



    def change_page(self):
        if self.comboBox.currentIndex() == 3:
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(0)

