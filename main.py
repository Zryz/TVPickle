from engine import TVPickle
from ui import UIEngine, UIElement, Banner, Menu, Title, Page
#import sys

#from PyQt6.QtWidgets import QApplication, QWidget

#app = QApplication(sys.argv)
#window = QWidget()
#app.exec()
#window.show()

#INITALISE THE GUI ELEMENTS
#testTitle = Title("This is A Test", 'header', 'modeSelect')
#testBanner = Banner(testTitle, 'header', 'modeSelect', 2)

#print(testBanner.__dict__)
print(Page.UIElements)

gui = UIEngine()

#api = TVPickle()