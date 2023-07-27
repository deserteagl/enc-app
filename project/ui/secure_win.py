
from constants import File_ERROR,SUCCESS,algorithms,VERIFY_FALSE
from queue import Queue
from os.path import isfile,basename,dirname,join
from threading import Lock
from os import stat,rename,walk,getcwd,remove
from struct import pack
from hashlib import sha256
from Marca_Ciph import File_Marca
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.Password_win import PasswordEdit
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

class Ui_secDialog(QtWidgets.QDialog):
    def __init__(self, Parent,folder,oper):
        super().__init__(Parent)
        self.folder = folder
        self.oper = oper
        self.main = Parent
        self.setObjectName("EncDialog")
        self.resize(487, 165)
        self.setMaximumSize(QtCore.QSize(487, 165))

        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 501, 81))
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
        self.stackedWidget.addWidget(self.page)
        self.verticalLayout.addWidget(self.stackedWidget)
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(140, 120, 88, 34))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(250, 120, 88, 34))
        self.pushButton_4.setObjectName("pushButton_4")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setModal(True)
        self.prepare_actions()

        self.q = Queue()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        if self.oper == 1:              #1 if enc 0 if dec
            self.setWindowTitle(_translate("dialog", "Secure folder "))
        else:
            self.setWindowTitle(_translate("dialog", "Decrypt folder "))

        self.label_2.setText(_translate("Form", "Enter Passphrase"))
        self.pushButton_3.setText(_translate("Form", "Ok"))
        self.pushButton_4.setText(_translate("Form", "Cancel"))

    def prepare_actions(self):

        self.stackedWidget.setCurrentIndex(0)

        self.pushButton_4.clicked.connect(self.close)
        if self.oper:
            self.pushButton_3.clicked.connect(self.enc)
        else:
            self.pushButton_3.clicked.connect(self.dec)

    def check(self,files,password,key_data):
        hash = password + sha256(key_data).digest()
        for i in files:
            fd = open(i,'rb')
            if fd.read(64) != hash:
                fd.close()
                return File_ERROR
            fd.close()
        return SUCCESS
    def enc(self):
        if self.lineEdit.text() == '' or len(self.lineEdit.text()) < 8:
            msg = QtWidgets.QMessageBox(self)
            msg.setText("Password is too short \nmust be at least 8 long")
            msg.setWindowTitle("pass error")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.buttonClicked.connect(msg.close)
            msg.setModal(True)
            msg.show()
            return

        root = dirname(self.folder)
        name = basename(self.folder)
        newname = root + '/.' + name
        rename(self.folder, newname)
        self.files = []
        for rootdir, dirs, file in walk(newname):
            for name in file:
                self.files.append(join(rootdir, name))
        #self.main().treeWidget_3.selectedItems()[0].text(1) = newname
        #self.main().treeWidget_3.selectedItems()[0].text(2) = 'hidden'
        fd = open(getcwd()+'/data/Private_key/private.mkey', 'rb')
        fd_data = fd.read()
        fd.close()
        key = Import_marcakey(getcwd()+'/data/Private_key/private.mkey')

        k1, k2, nonce = generate_init_marca_keys(key)
#        threads = []
        self.count = len(self.files)
        self.count_2 = 0
        self.lock = Lock()

        self.value = 0
        self.pgB_d = Ui_Dia(self)
        self.pgB_d.label_2.setText("0/%d" % self.count)
        self.pgB = self.pgB_d.progressBar
        self.pgB_d.show()

        for file in self.files:
            hdata = sha256(self.lineEdit.text().encode()).digest() + sha256(fd_data).digest() + pack('!Q', stat(
                file).st_size)
            self.q.put_nowait(File_Marca(file, [hdata, [k1, k2, nonce, 40, 0]], oper=1))

        if self.count < 2:

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

    def dec(self):
            if self.lineEdit.text() == '' or len(self.lineEdit.text()) < 8:
                msg = QtWidgets.QMessageBox(self)
                msg.setText("Password is too short \nmust be at least 8 long")
                msg.setWindowTitle("pass error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.buttonClicked.connect(msg.close)
                msg.setModal(True)
                msg.show()
                return
            root = dirname(self.folder)
            name = basename(self.folder)[1:]
            newname = root + '/' + name
            rename(self.folder, newname)
            self.files = []
            for rootdir, dirs, file in walk(newname):
                for name in file:
                    self.append(join(rootdir, name))
            fd = open(getcwd()+'/data/Private_key/private.mkey', 'rb')
            fd_data = fd.read()
            fd.close()
            password = sha256(self.lineEdit.text().encode()).digest()
            if self.check(self.files,password,fd_data) == File_ERROR:
                rename(newname,self.folder)
                msg = QtWidgets.QMessageBox(self)
                msg.setText("Password is invalid")
                msg.setWindowTitle("Input error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.buttonClicked.connect(msg.close)
                msg.setModal(True)
                msg.show()
                return

            key = Import_marcakey(getcwd()+'/data/Private_key/private.mkey')

            k1,k2,nonce = generate_init_marca_keys(key)
#           threads = []
            self.count = len(self.files)
            self.count_2 = 0
            self.lock = Lock()

            self.value = 0
            self.pgB_d = Ui_Dia(self)
            self.pgB_d.label.setText("Decrypting Files")
            self.pgB_d.setWindowTitle('Decrypt File')
            self.pgB_d.label_2.setText("0/%d"%self.count)
            self.pgB = self.pgB_d.progressBar
            self.pgB_d.show()


            for file in self.files:
                    self.q.put_nowait(File_Marca(file, [None, [k1, k2, nonce,40,0]], oper=0))

            if self.count < 2:

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


        if self.value >=100 or self.count_2 == self.count:
            lock.acquire()
            self.pgB_d.label_2.setText('%d/%d'%(self.count,self.count))
            self.pgB.setValue(100)
            self.pgB_d.close()
            lock.release()
            sleep(.001)
            for file in self.files:
                remove(file)

        else :
            lock.acquire()
            self.pgB.setValue(self.value)
            self.pgB_d.label_2.setText('%d/%d'%(self.count_2,self.count))
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



