from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

import sys
import random


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle('WH40k Dice Roller')
        self.setGeometry(400, 300, 350, 600)

        font = QFont('Arial', 11)

        # Attacks
        self.lAttacks = QtWidgets.QLabel(self)
        self.lAttacks.setText('Attacks:')
        self.lAttacks.move(50, 50)
        self.lAttacks.setFont(font)

        self.tbAttacks = QtWidgets.QLineEdit(self)
        self.tbAttacks.move(200, 50)
        self.tbAttacks.setFont(font)

        self.lBSWS = QtWidgets.QLabel(self)
        self.lBSWS.setText('BS/WS:')
        self.lBSWS.move(50, 100)
        self.lBSWS.setFont(font)

        self.tbBSWS = QtWidgets.QLineEdit(self)
        self.tbBSWS.move(200, 100)
        self.tbBSWS.setFont(font)

        self.lS = QtWidgets.QLabel(self)
        self.lS.setText('S:')
        self.lS.move(50, 150)
        self.lS.setFont(font)

        self.tbS = QtWidgets.QLineEdit(self)
        self.tbS.move(200, 150)
        self.tbS.setFont(font)

        self.lAP = QtWidgets.QLabel(self)
        self.lAP.setText('AP:')
        self.lAP.move(50, 200)
        self.lAP.setFont(font)

        self.tbAP = QtWidgets.QLineEdit(self)
        self.tbAP.move(200, 200)
        self.tbAP.setFont(font)

        self.lD = QtWidgets.QLabel(self)
        self.lD.setText('D:')
        self.lD.move(50, 250)
        self.lD.setFont(font)

        self.tbD = QtWidgets.QLineEdit(self)
        self.tbD.move(200, 250)
        self.tbD.setFont(font)

        # Defense
        self.lT = QtWidgets.QLabel(self)
        self.lT.setText('T:')
        self.lT.move(50, 300)
        self.lT.setFont(font)

        self.tbT = QtWidgets.QLineEdit(self)
        self.tbT.move(200, 300)
        self.tbT.setFont(font)

        self.lSave = QtWidgets.QLabel(self)
        self.lSave.setText('Save:')
        self.lSave.move(50, 350)
        self.lSave.setFont(font)

        self.tbSave = QtWidgets.QLineEdit(self)
        self.tbSave.move(200, 350)
        self.tbSave.setFont(font)

        self.lInvul = QtWidgets.QLabel(self)
        self.lInvul.setText('Invulnerable save:')
        self.lInvul.move(50, 400)
        self.lInvul.setFont(font)
        self.lInvul.setFixedWidth(100)

        self.tbInvul = QtWidgets.QLineEdit(self)
        self.tbInvul.move(200, 400)
        self.tbInvul.setFont(font)

        # Result
        # self.lResult = QtWidgets.QLabel(self)
        # self.lResult.setText('Result:')
        # self.lResult.move(100, 450)
        # self.lResult.setFont(font)
        # self.lResult.setFixedWidth(200)

        # Button
        self.btn = QtWidgets.QPushButton(self)
        self.btn.move(70, 500)
        self.btn.setText('Roll')
        self.btn.setFixedWidth(200)
        self.btn.clicked.connect(lambda: self.roll_calculate(self.tbAttacks.text(),
                                                             int(self.tbBSWS.text()),
                                                             int(self.tbS.text()),
                                                             int(self.tbAP.text()),
                                                             self.tbD.text(),
                                                             int(self.tbT.text()),
                                                             int(self.tbSave.text()),
                                                             self.tbInvul.text()))

    def roll_calculate(self, attacks, bsws, s, ap, d, t, save, invul):
        # Attacks check
        attacks = string_to_dice(attacks)

        # BS/WS check
        bsws_result = roll_d6(attacks)
        for result in bsws_result:
            if result < bsws:
                attacks -= 1

        if attacks == 0:
            QMessageBox.about(self, "Result", "0 damage")
            return

        # S to T check
        needed_dice = 0
        if s * 2 <= t:
            needed_dice = 6
        elif s < t:
            needed_dice = 5
        elif s == t:
            needed_dice = 4
        elif s >= t * 2:
            needed_dice = 2
        elif s > t:
            needed_dice = 3

        s_t_result = roll_d6(attacks)
        for result in s_t_result:
            if result < needed_dice:
                attacks -= 1

        if attacks == 0:
            QMessageBox.about(self, "Result", "0 damage")
            return

        # Save check
        save_result = roll_d6(attacks)
        for result in save_result:
            if result - ap >= save:
                attacks -= 1

        if attacks == 0:
            QMessageBox.about(self, "Result", "0 damage")
            return

        # Invulnerable save check
        if invul != '':
            invul_result = roll_d6(attacks)
            for result in invul_result:
                if result >= int(invul):
                    attacks -= 1

            if attacks == 0:
                QMessageBox.about(self, "Result", "0 damage")
                return

        # Damage check
        total_damage = 0
        for _ in range(attacks):
            total_damage += string_to_dice(d)

        QMessageBox.about(self, "Result", "Total damage: " + str(total_damage))


def roll_d3(count):
    result = []
    for _ in range(count):
        result.append(random.randint(1, 3))
    return result


def roll_d6(count):
    result = []
    for _ in range(count):
        result.append(random.randint(1, 6))
    return result


def string_to_dice(attacks_str):
    attacks = 0
    count = 1
    dice_type = 0
    try:
        int(attacks_str)
        return int(attacks_str)
    except ValueError:
        if len(attacks_str) == 3:  # ex. 2d6
            count = int(attacks_str[0])
            dice_type = int(attacks_str[2])
        else:  # ex. d6
            dice_type = int(attacks_str[1])

        if dice_type == 3:
            attack_rolls = roll_d3(count)
        else:
            attack_rolls = roll_d6(count)

        for roll in attack_rolls:
            attacks += roll
        return attacks


def application():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    application()
