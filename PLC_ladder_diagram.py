import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtCore import QTimeLine

class LadderDiagram(QWidget):
    def __init__(self):
        super().__init__()
        # Set the name of the window
        self.setWindowTitle("PLC Ladder Diagram")

        connecting_line_position_y = 60
        hot_railposition_x = 50
        self.create_switch(hot_railposition_x, connecting_line_position_y)


        # create coil nr.1 
        self.coil_1 = QGraphicsEllipseItem(250, 50, 20, 20)
        self.coil_1.setPen(QPen(Qt.black, 2))
        self.coil_1.setBrush(QBrush(Qt.green))
        self.coil_1_label = QGraphicsTextItem("LED")
        self.coil_1_label.setPos(255, 35)

        from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

      



        self.line1 = QGraphicsLineItem(70, 60, 249, 60)
        self.line1.setPen(QPen(Qt.black, 2))

        

        self.line3 = QGraphicsLineItem(70, 80, 250, 80)

        self.line4 = QGraphicsLineItem(250, 60, 250, 80)
        self.line4.setPen(QPen(Qt.black, 2))

        self.scene = QGraphicsScene(self)
        self.scene.addItem(self.switch)
        self.scene.addItem(self.switch2)
        self.scene.addItem(self.coil_1)
        self.scene.addItem(self.switch_label)
        self.scene.addItem(self.coil_1_label)
        self.scene.addItem(self.line1)
        self.scene.addItem(self.line2)
        self.scene.addItem(self.line3)
        self.scene.addItem(self.line4)

        self.view = QGraphicsView(self.scene, self)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
        self.setLayout(layout)
    

        # # Create the animation for turning on the LED
        # self.led_on_animation = QGraphicsItemAnimation()
        # self.led_on_animation.setItem(self.coil_1)
        # self.led_on_animation.setTimeLine(QTimeLine(500))
        # self.led_on_animation.setScaleAt(1.0, 1.0, 1.0)
        # self.led_on_animation.setScaleAt(1.0, 1.0, 1.0)
        # self.led_on_animation.setBrush(QBrush(Qt.green))


        # # Create the animation for turning on the LED
        # self.led_off_animation = QGraphicsItemAnimation()
        # self.led_off_animation.setItem(self.coil_1)
        # self.led_off_animation.setTimeLine(QTimeLine(500))
        # self.led_off_animation.setScaleAt(1.0, 1.0, 1.0)
        # self.led_off_animation.setScaleAt(1.0, 1.0, 1.0)
        # self.led_off_animation.setBrush(QBrush(Qt.white))

    def create_switch(self, hot_rail_position_x:float, connecting_line_pos:float):
        # connecting line from the hot rail
        self.line2 = QGraphicsLineItem(hot_rail_position_x, connecting_line_pos, hot_rail_position_x+5, connecting_line_pos)
        self.line2.setPen(QPen(Qt.black, 2))
        # element Switch
        self.switch_label = QGraphicsTextItem("switch")
        self.switch_label.setPos(hot_rail_position_x, connecting_line_pos-30)
        # A contact consists of two vertical lines
        self.switch = QGraphicsLineItem(55, 50, 55, 70)
        self.switch.setPen(QPen(Qt.black, 2))
        # line 2
        self.switch2 = QGraphicsLineItem(69, 50, 69, 70)
        self.switch2.setPen(QPen(Qt.black, 2))
        # Available colors pre_named: Qt.black, Qt.white, Qt.red, Qt.green, Qt.blue, Qt.cyan, Qt.magenta, Qt.yellow, Qt.gray


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ladder_diagram = LadderDiagram()
    # ladder_diagram.start_led()
    ladder_diagram.show()
    sys.exit(app.exec_())

