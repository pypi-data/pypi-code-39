#!/usr/bin/python3

from file_handler.filer import make_file, read_file
from PyQt5 import QtCore, QtGui, QtWidgets
from mainApp.serial_execution import SerialThread
import sys


class Ui_My_Form(object):
    """ """

    def __init__(self):
        """Initialize  storage"""
        self.loaded_inventory_storage = set()
        self.available_commands = []
        self.username = ""
        self.password = ""

        # MultiThread Communications
        self.new_thread = SerialThread(self.username, self.password,
                                       commands=self.available_commands,
                                       hosts_file=self.loaded_inventory_storage)

        self.new_thread.current_outputs_signal.connect(self.update_current_outputs)
        self.new_thread.unreachable_hots_signal.connect(self.update_unreachable_hosts)
        self.new_thread.configured_hosts_signal.connect(self.update_configured_hosts)

    def update_current_outputs(self, data):
        """ """
        self.textBrowser_current_outputs.append(data)

    def update_unreachable_hosts(self, data):
        """ """
        self.textBrowser_unreachable_hosts.append(data)

    def update_configured_hosts(self, data):
        """ """
        self.textBrowser_configured_hosts.append(data)

    def setupUi(self, My_Form):
        """ """
        My_Form.setObjectName("My_Form")
        My_Form.resize(1500, 847)
        My_Form.setMaximumWidth(1500)
        My_Form.setMinimumWidth(1500)
        My_Form.setMinimumHeight(847)
        My_Form.setMaximumHeight(847)

        self.user_infoGroupBox = QtWidgets.QGroupBox(My_Form)
        self.user_infoGroupBox.setGeometry(QtCore.QRect(10, 10, 450, 161))
        self.user_infoGroupBox.setTitle("USER INFO")
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(30)
        self.user_infoGroupBox.setFont(font)

        self.username_Label = QtWidgets.QLabel(self.user_infoGroupBox)
        self.username_Label.setGeometry(QtCore.QRect(10, 40, 111, 16))
        self.username_Label.setText("User Name")

        self.password_Label = QtWidgets.QLabel(self.user_infoGroupBox)
        self.password_Label.setGeometry(QtCore.QRect(10, 80, 111, 16))
        self.password_Label.setText("Password")

        self.username_LineEdit = QtWidgets.QLineEdit(self.user_infoGroupBox)
        self.username_LineEdit.setGeometry(QtCore.QRect(140, 30, 300, 31))

        self.password_LineEdit = QtWidgets.QLineEdit(self.user_infoGroupBox)
        self.password_LineEdit.setGeometry(QtCore.QRect(140, 70, 300, 31))
        self.password_LineEdit.setAutoFillBackground(False)
        self.password_LineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.deactivate_PushButton = QtWidgets.QPushButton(self.user_infoGroupBox)
        self.deactivate_PushButton.setGeometry(QtCore.QRect(260, 110, 111, 41))
        self.deactivate_PushButton.setText("DEACTIVATE")

        self.activate_PushButton = QtWidgets.QPushButton(self.user_infoGroupBox)
        self.activate_PushButton.setGeometry(QtCore.QRect(140, 110, 111, 41))
        self.activate_PushButton.setText("ACTIVATE")

        self.ssh_options_GroupBox = QtWidgets.QGroupBox(My_Form)
        self.ssh_options_GroupBox.setGeometry(QtCore.QRect(10, 180, 450, 151))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(30)
        self.ssh_options_GroupBox.setFont(font)
        self.ssh_options_GroupBox.setTitle("SSH OPTIONS")

        self.ssh_port_Label = QtWidgets.QLabel(self.ssh_options_GroupBox)
        self.ssh_port_Label.setGeometry(QtCore.QRect(10, 30, 61, 20))
        self.ssh_port_Label.setText("SSH Port:")

        self.ssh_port_lineEdit = QtWidgets.QLineEdit(self.ssh_options_GroupBox)
        self.ssh_port_lineEdit.setGeometry(QtCore.QRect(80, 30, 81, 21))

        self.serial_processing_RadioButton = QtWidgets.QRadioButton(self.ssh_options_GroupBox)
        self.serial_processing_RadioButton.setGeometry(QtCore.QRect(10, 60, 141, 20))
        self.serial_processing_RadioButton.setText("Serial Processing")
        self.serial_processing_RadioButton.setChecked(True)

        self.parallel_processing_RadioButton = QtWidgets.QRadioButton(self.ssh_options_GroupBox)
        self.parallel_processing_RadioButton.setGeometry(QtCore.QRect(10, 90, 141, 20))
        self.parallel_processing_RadioButton.setText("Parallel Processing")

        self.allowed_cores_LineEdit = QtWidgets.QLineEdit(self.ssh_options_GroupBox)
        self.allowed_cores_LineEdit.setGeometry(QtCore.QRect(390, 90, 51, 21))

        self.allowed_cores_Label = QtWidgets.QLabel(self.ssh_options_GroupBox)
        self.allowed_cores_Label.setGeometry(QtCore.QRect(250, 90, 91, 20))
        self.allowed_cores_Label.setText("Allowed Cores")

        self.connection_timeout_Label = QtWidgets.QLabel(self.ssh_options_GroupBox)
        self.connection_timeout_Label.setGeometry(QtCore.QRect(10, 120, 131, 20))
        self.connection_timeout_Label.setText("Connection Timeout")

        self.connection_timeout_lineEdit = QtWidgets.QLineEdit(self.ssh_options_GroupBox)
        self.connection_timeout_lineEdit.setGeometry(QtCore.QRect(170, 120, 31, 21))
        self.connection_timeout_lineEdit.setText("")


        self.command_delay_Label = QtWidgets.QLabel(self.ssh_options_GroupBox)
        self.command_delay_Label.setGeometry(QtCore.QRect(250, 120, 101, 20))
        self.command_delay_Label.setText("Command Delay")

        self.command_delay_LineEdit = QtWidgets.QLineEdit(self.ssh_options_GroupBox)
        self.command_delay_LineEdit.setGeometry(QtCore.QRect(390, 120, 51, 21))

        self.hosts_inventory_options_GroupBox = QtWidgets.QGroupBox(My_Form)
        self.hosts_inventory_options_GroupBox.setGeometry(QtCore.QRect(10, 500, 450, 161))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(30)
        self.hosts_inventory_options_GroupBox.setFont(font)
        self.hosts_inventory_options_GroupBox.setTitle("HOSTS INVENTORY OPTIONS")

        self.hosts_inventory_Label = QtWidgets.QLabel(self.hosts_inventory_options_GroupBox)
        self.hosts_inventory_Label.setGeometry(QtCore.QRect(10, 40, 351, 15))
        self.hosts_inventory_Label.setText("Please paste the file path of your hosts inventory")

        self.inventory_file_path_LineEdit = QtWidgets.QLineEdit(self.hosts_inventory_options_GroupBox)
        self.inventory_file_path_LineEdit.setGeometry(QtCore.QRect(10, 60, 430, 30))

        self.load_inventory_PushButton = QtWidgets.QPushButton(self.hosts_inventory_options_GroupBox)
        self.load_inventory_PushButton.setGeometry(QtCore.QRect(10, 100, 151, 51))
        self.load_inventory_PushButton.setText("LOAD INVENTORY")

        self.list_of_commands_GroupBox = QtWidgets.QGroupBox(My_Form)
        self.list_of_commands_GroupBox.setGeometry(QtCore.QRect(10, 670, 450, 171))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(30)
        self.list_of_commands_GroupBox.setFont(font)
        self.list_of_commands_GroupBox.setTitle("LIST OF COMMANDS")

        self.list_of_commands_TextEdit = QtWidgets.QTextEdit(self.list_of_commands_GroupBox)
        self.list_of_commands_TextEdit.setGeometry(QtCore.QRect(10, 30, 430, 131))

        self.start_execution_PushButton = QtWidgets.QPushButton(My_Form)
        self.start_execution_PushButton.setGeometry(QtCore.QRect(500, 790, 241, 51))
        self.start_execution_PushButton.setText("START EXECUTION")
        self.start_execution_PushButton.clicked.connect(self.control_executions)  # Handles Serial/Parallel functions

        self.stop_execution_PushButton = QtWidgets.QPushButton(My_Form)
        self.stop_execution_PushButton.setGeometry(QtCore.QRect(750, 790, 241, 51))
        self.stop_execution_PushButton.setText("STOP EXECUTION")

        self.outputs_options_GroupBox = QtWidgets.QGroupBox(My_Form)
        self.outputs_options_GroupBox.setGeometry(QtCore.QRect(10, 350, 450, 131))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(30)
        self.outputs_options_GroupBox.setFont(font)
        self.outputs_options_GroupBox.setTitle("OUTPUTS OPTIONS")

        self.donot_save_outputs_to_file_RadioButton = QtWidgets.QRadioButton(self.outputs_options_GroupBox)
        self.donot_save_outputs_to_file_RadioButton.setGeometry(QtCore.QRect(210, 30, 201, 20))
        self.donot_save_outputs_to_file_RadioButton.setText("Do Not Save Outputs To File")

        self.save_outputs_to_file_RadioButton = QtWidgets.QRadioButton(self.outputs_options_GroupBox)
        self.save_outputs_to_file_RadioButton.setGeometry(QtCore.QRect(10, 30, 151, 20))
        self.save_outputs_to_file_RadioButton.setText("Save Outputs To File")

        self.output_redirection_Label = QtWidgets.QLabel(self.outputs_options_GroupBox)
        self.output_redirection_Label.setGeometry(QtCore.QRect(10, 70, 351, 16))
        self.output_redirection_Label.setText("Please paste the file path for outputs redirection")

        self.outputs_redirectionLineEdit = QtWidgets.QLineEdit(self.outputs_options_GroupBox)
        self.outputs_redirectionLineEdit.setGeometry(QtCore.QRect(10, 90, 430, 31))

        # Main tabs_widget
        self.main_tabs_TabWidget = QtWidgets.QTabWidget(My_Form)
        self.main_tabs_TabWidget.setGeometry(QtCore.QRect(500, 20, 971, 771))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.main_tabs_TabWidget.setFont(font)

        self.tab_current_outputs = QtWidgets.QWidget()
        self.textBrowser_current_outputs = QtWidgets.QTextBrowser(self.tab_current_outputs)
        self.textBrowser_current_outputs.setGeometry(QtCore.QRect(0, 0, 971, 751))
        self.main_tabs_TabWidget.addTab(self.tab_current_outputs, "")

        self.tab_loaded_inventory = QtWidgets.QWidget()
        self.textBrowser_loaded_inventory = QtWidgets.QTextBrowser(self.tab_loaded_inventory)
        self.textBrowser_loaded_inventory.setGeometry(QtCore.QRect(0, 0, 971, 711))
        self.main_tabs_TabWidget.addTab(self.tab_loaded_inventory, "")

        self.tab_configured_hosts = QtWidgets.QWidget()
        self.textBrowser_configured_hosts = QtWidgets.QTextBrowser(self.tab_configured_hosts)
        self.textBrowser_configured_hosts.setGeometry(QtCore.QRect(-5, 1, 971, 711))
        self.main_tabs_TabWidget.addTab(self.tab_configured_hosts, "")

        self.tab_unreachable_hosts = QtWidgets.QWidget()
        self.textBrowser_unreachable_hosts = QtWidgets.QTextBrowser(self.tab_unreachable_hosts)
        self.textBrowser_unreachable_hosts.setGeometry(QtCore.QRect(0, 0, 971, 711))
        self.main_tabs_TabWidget.addTab(self.tab_unreachable_hosts, "")

        self.tab_logs = QtWidgets.QWidget()
        self.textBrowser_logs = QtWidgets.QTextBrowser(self.tab_logs)
        self.textBrowser_logs.setGeometry(QtCore.QRect(0, 0, 971, 711))
        self.main_tabs_TabWidget.addTab(self.tab_logs, "")

        self.tab_final_report = QtWidgets.QWidget()
        self.textBrowser_final_report = QtWidgets.QTextBrowser(self.tab_final_report)
        self.textBrowser_final_report.setGeometry(QtCore.QRect(-10, 0, 981, 711))
        self.main_tabs_TabWidget.addTab(self.tab_final_report, "")

        self.retranslateUi(My_Form)
        self.main_tabs_TabWidget.setCurrentIndex(0)

        self.serial_processing_RadioButton.clicked.connect(self.allowed_cores_Label.hide)
        self.serial_processing_RadioButton.clicked.connect(self.allowed_cores_LineEdit.hide)

        self.parallel_processing_RadioButton.clicked.connect(self.allowed_cores_Label.show)
        self.parallel_processing_RadioButton.clicked.connect(self.allowed_cores_LineEdit.show)

        self.load_inventory_PushButton.clicked.connect(self.load_inventory)  # testing

        QtCore.QMetaObject.connectSlotsByName(My_Form)

    def retranslateUi(self, My_Form):
        """ """
        _translate = QtCore.QCoreApplication.translate
        My_Form.setWindowTitle(_translate("My_Form", "Form"))

        self.allowed_cores_LineEdit.setPlaceholderText(_translate("My_Form", "20"))
        self.connection_timeout_lineEdit.setPlaceholderText(_translate("My_Form", "10"))
        self.command_delay_LineEdit.setPlaceholderText(_translate("My_Form", "4"))

        self.main_tabs_TabWidget.setTabText(self.main_tabs_TabWidget.indexOf(self.tab_current_outputs), _translate("My_Form", "Current Outputs"))
        self.main_tabs_TabWidget.setTabText(self.main_tabs_TabWidget.indexOf(self.tab_loaded_inventory), _translate("My_Form", "Loaded Inventory"))
        self.main_tabs_TabWidget.setTabText(self.main_tabs_TabWidget.indexOf(self.tab_configured_hosts), _translate("My_Form", "Configured Hosts"))
        self.main_tabs_TabWidget.setTabText(self.main_tabs_TabWidget.indexOf(self.tab_unreachable_hosts), _translate("My_Form", "Unreachable Hosts"))
        self.main_tabs_TabWidget.setTabText(self.main_tabs_TabWidget.indexOf(self.tab_logs), _translate("My_Form", "Logs"))
        self.main_tabs_TabWidget.setTabText(self.main_tabs_TabWidget.indexOf(self.tab_final_report), _translate("My_Form", "Final Report"))

    """===================================End of the FrontEnd Setup================================================================================="""

    def scan_credentials(self):
        """ This function will be used to scan the username and password fields and then update their variables """

        if self.username_LineEdit.text():
            self.username = self.username_LineEdit.text()
            self.textBrowser_logs.append(self.username)

        if self.password_LineEdit.text():
            self.password = self.password_LineEdit.text()
            self.textBrowser_logs.append(self.password)
        else:
            self.textBrowser_logs.append("Credentials not valid!\n".upper())

    def control_executions(self):
        """This function will be used to select between Serial and Parallel processing """
        self.scan_credentials()

        if self.serial_processing_RadioButton.isChecked():
            self.new_thread.start()  # start the thread!
        else:
            self.textBrowser_logs.append("Parallel Processing is not yet available\n")
            return

    def load_inventory(self):
        """This function will be used to:
                scan the commands field
                scan the path containing the inventory file
         """
        make_file(self.list_of_commands_TextEdit.toPlainText())
        self.available_commands = read_file()
        [self.textBrowser_logs.append(cmd) for cmd in self.available_commands]

        hosts_file = self.inventory_file_path_LineEdit.text().strip()
        if hosts_file:
            try:
                file = open(hosts_file)
            except:
                self.textBrowser_logs.append("Could not open the >> {0}".format(hosts_file))
            else:
                [self.loaded_inventory_storage.add(host.strip()) for host in file if host]
                [self.textBrowser_loaded_inventory.append(host) for host in self.loaded_inventory_storage if host]
        else:
            self.textBrowser_logs.append("Invalid inventory path provided!\n".upper())

    def start_appication(self):
        """ """
        app = QtWidgets.QApplication(sys.argv)
        My_Form = QtWidgets.QWidget()
        ui = Ui_My_Form()
        ui.setupUi(My_Form)
        My_Form.show()
        app.setStyle("fusion")
        sys.exit(app.exec_())




app = Ui_My_Form()
app.start_appication()





















