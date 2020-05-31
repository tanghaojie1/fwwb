
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from timeit import default_timer as timer
import sys
import qtawesome
import win32com.client
import time
import os
import argparse
from yolo import YOLO
from PIL import Image
import cv2
import numpy as np
import pymysql
import xlwt
#import dlib
#import pandas as pd
#import csv
#import datetime
#from skimage import io as iio
#import shutil
connection = pymysql.connect(host='182.92.193.60',
							 port=3306,
							 user='root',
							 password='yyyyyyyyy',
							 db='test',
							 charset='UTF8MB4')
#加载模型并进行初始化
parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
parser.add_argument(
		'--model', type=str,
		help='path to model weight file, default ' + YOLO.get_defaults("model_path")
	)
parser.add_argument(
		'--anchors', type=str,
		help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
	)
parser.add_argument(
		'--classes', type=str,
		help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
	)
parser.add_argument(
		'--gpu_num', type=int,
		help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
	)
parser.add_argument(
		'--image', default=False, action="store_true",
		help='Image detection mode, will ignore all positional arguments'
	)
parser.add_argument(
		"--input", nargs='?', type=str,required=False,default='./path2your_video',
		help = "Video input path"
	)
parser.add_argument(
		"--output", nargs='?', type=str, default="",
		help = "[Optional] Video output path"
	)
FLAGS=parser.parse_args()
yolo=YOLO(**vars(FLAGS))
class Speak:
	def __init__(self):
		self.speak_out=win32com.client.Dispatch('SAPI.SPVOICE')
	def speak(self,data=''):
		self.speak_out.Speak(data)
		time.sleep(1)
class MainUi(QtWidgets.QMainWindow):
	flag=0
	def __init__(self):
		super().__init__()
		self.init_ui() #调用初始化的界面设置，展示界面的功能
	def init_ui(self):
		self.setFixedSize(960, 700)
		self.main_widget = QtWidgets.QWidget()	# 创建窗口主部件
		self.main_layout = QtWidgets.QGridLayout()	# 创建主部件的网格布局
		self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

		self.left_widget = QtWidgets.QWidget()	# 创建左侧部件
		self.left_widget.setObjectName('left_widget')
		self.left_layout = QtWidgets.QGridLayout()	# 创建左侧部件的网格布局层
		self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

		self.right_widget = QtWidgets.QWidget()	 # 创建右侧部件
		self.right_widget.setObjectName('right_widget')
		self.right_layout = QtWidgets.QGridLayout()
		self.right_widget.setLayout(self.right_layout)	# 设置右侧部件布局为网格

		self.right_widget_1 = QtWidgets.QWidget()  # 创建右侧部件
		self.right_widget_1.setObjectName('right_widget_1')
		self.right_layout_1 = QtWidgets.QGridLayout()

		self.right_widget_2 = QtWidgets.QWidget()  # 创建右侧部件
		self.right_widget_2.setObjectName('right_widget_2')
		self.right_layout_2 = QtWidgets.QVBoxLayout()
		self.right_widget_2.setLayout(self.right_layout_2)	# 设置右侧部件布局为网格

		##
		self.right_widget_1.setLayout(self.right_layout_1)	# 设置右侧部件布局为网格
		self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
		self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)	 # 右侧部件在第0行第3列，占8行9列
		self.main_layout.addWidget(self.right_widget_1, 0, 2, 12, 10)  # 右侧部件_1在第0行第3列，占8行9列
		self.main_layout.addWidget(self.right_widget_2, 0, 2, 12, 10)

		self.setCentralWidget(self.main_widget)	 # 设置窗口主部件
		self.left_close = QtWidgets.QPushButton("")	 # 关闭按钮
		self.left_max = QtWidgets.QPushButton("")  # 最大按钮
		self.left_mini = QtWidgets.QPushButton("")	# 最小化按钮

		self.left_label_1 = QtWidgets.QPushButton("基础功能")
		self.left_label_1.setObjectName('left_label')
		self.left_label_2 = QtWidgets.QPushButton("拓展功能")
		self.left_label_2.setObjectName('left_label')
		self.left_label_3 = QtWidgets.QPushButton("联系与帮助")
		self.left_label_3.setObjectName('left_label')

		self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.list-ol', color='white'), "照片识别")
		self.left_button_1.setObjectName('left_button')
		self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.user', color='white'), "本地视频识别")
		self.left_button_2.setObjectName('left_button')
		self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.edit', color='white'), "实时识别")
		self.left_button_3.setObjectName('left_button')
		self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.bar-chart', color='white'), "清除数据库")
		self.left_button_4.setObjectName('left_button')
		self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.envelope', color='white'), "导出excel")
		self.left_button_5.setObjectName('left_button')
		self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.mail-reply', color='white'), "返回主界面")
		self.left_button_6.setObjectName('left_button')
		self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.weibo', color='white'), "建议反馈")
		self.left_button_7.setObjectName('left_button')
		self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "关注我们")
		self.left_button_8.setObjectName('left_button')
		self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.book', color='white'), "使用手册")
		self.left_button_9.setObjectName('left_button')
		self.left_xxx = QtWidgets.QPushButton(" ")
		self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
		self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
		self.left_layout.addWidget(self.left_max, 0, 1, 1, 1)
		self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
		self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 3)
		self.left_layout.addWidget(self.left_button_2, 3, 0, 1, 3)
		self.left_layout.addWidget(self.left_button_3, 4, 0, 1, 3)
		self.left_layout.addWidget(self.left_label_2, 5, 0, 1, 3)
		self.left_layout.addWidget(self.left_button_4, 6, 0, 1, 3)
		self.left_layout.addWidget(self.left_button_5, 7, 0, 1, 3)
		self.left_layout.addWidget(self.left_button_6, 8, 0, 1, 3)
		self.left_layout.addWidget(self.left_label_3, 9, 0, 1, 3)
		self.left_layout.addWidget(self.left_button_7, 10, 0, 1, 3)
		self.left_layout.addWidget(self.left_button_8, 11, 0, 1, 3)
		self.left_layout.addWidget(self.left_button_9, 12, 0, 1, 3)
		self.left_close.setFixedSize(20,20)	 # 设置关闭按钮的大小
		self.left_max.setFixedSize(20,20)  # 设置最大化按钮大小
		self.left_mini.setFixedSize(20,20)	# 设置最小化按钮大小
		self.left_close.setStyleSheet(
			'''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
		self.left_max.setStyleSheet(
			'''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
		self.left_mini.setStyleSheet(
			'''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
		self.left_widget.setStyleSheet('''
			QPushButton{border:none;color:white;}
			QPushButton#left_label{
				border:none;
				border-bottom:1px solid white;
				font-size:20px;
				font-weight:700;
				font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
			}
			QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
			QWidget#left_widget{
	background:gray;
	border-top:0px solid white;
	border-bottom:0px solid white;
	border-left:0px solid white;
	border-top-left-radius:10px;
	border-bottom-left-radius:10px;
}
		''')
		self.right_widget.setStyleSheet('''
			QWidget#right_widget{
				color:#232C51;
				background:white;
				border-top:1px solid darkGray;
				border-bottom:1px solid darkGray;
				border-right:1px solid darkGray;
				border-top-right-radius:10px;
				border-bottom-right-radius:10px;
			}
			QLabel#right_lable{
				border:none;
				font-size:16px;
				font-weight:700;
				font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
			}
		''')
		self.right_widget_1.setStyleSheet('''
						QWidget#right_widget_1{
							color:#232C51;
							background:white;
							border-top:0px solid darkGray;
							border-bottom:0px solid darkGray;
							border-right:0px solid darkGray;
							border-top-right-radius:10px;
							border-bottom-right-radius:10px;
						}
						QLabel#right_lable_1{
							border:none;
							font-size:16px;
							font-weight:700;
							font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
						}
					''')
		self.init_right()
		self.init_right_show()
		self.setWindowOpacity(2)  # 设置窗口透明度
		self.right_widget.setStyleSheet("QWidget#right_widget{border-image:url(./picture/main2.jpg)}")
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
		self.main_layout.setSpacing(0)
		self.left_close.clicked.connect(self.main_close)
		self.left_mini.clicked.connect(self.main_min)
		self.left_max.clicked.connect(self.main_max)
		self.left_button_1.clicked.connect(self.show_photo)
		self.left_button_2.clicked.connect(self.show_video)
		self.left_button_3.clicked.connect(self.show_camera)
		self.left_button_4.clicked.connect(self.clear_databank)
		self.left_button_5.clicked.connect(self.daochu_excel)
		self.left_button_6.clicked.connect(self.init_right)
		self.left_button_6.clicked.connect(self.close_video)
		self.right_widget.hide()
		self.right_widget_2.hide()
		self.register_flag = 0
		self.sc_number=0
# 数据可视化界面初始化界面构造函数
	def init_right_show(self):
		self.listw = QtWidgets.QListWidget()
		self._translate = QtCore.QCoreApplication.translate
		# self.right_combox = QtWidgets.QComboBox(self.right_widget_2)
		# self.right_combox.addItem("")
		# self.right_combox.addItem("")
		# self.right_combox.addItem("")
		# self.right_combox.addItem("")
		# self.right_combox.setMinimumSize(30, 30)
		# self.right_combox.currentIndexChanged.connect(self.right_combox_click)
		self.right_browser = QWebEngineView()
		# self.create_data_image()
		self.right_browser.load(QtCore.QUrl('./render.html'))
		self.right_browser.setMinimumSize(400, 400)
		# self.right_combox.setItemText(0, self._translate("right_widget_2", "lzf"))
		# self.right_combox.setItemText(1, self._translate("right_widget_2", "qz"))
		# self.right_combox.setItemText(2, self._translate("right_widget_2", "hzx"))
		# self.right_combox.setItemText(3, self._translate("right_widget_2", "	"))
		# self.right_layout_2.addWidget(self.right_combox, 0)
		self.right_layout_2.addWidget(self.right_browser, 1)
		self.right_widget_2.setStyleSheet('''
								QWidget#right_widget_2{
									color:#232C51;
									background:white;
									border-top:1px solid darkGray;
									border-bottom:1px solid darkGray;
									border-right:1px solid darkGray;
									border-top-right-radius:10px;
									border-bottom-right-radius:10px;
								}
								QComboBox{
			border:none;
			color:gray;
			font-size:30px;
			height:40px;
			padding-left:5px;
			padding-right:10px;
			text-align:left;
		}
		QComboBox:hover{
			color:black;
			border:1px solid #F3F3F5;
			border-radius:10px;
			background:LightGray;
		}
							''')

	def data_view(self):
		pass
	def main_min(self):
		self.showMinimized()
	def main_max(self):	 # 界面的最大化和正常化的切换
		if self.isMaximized():
			self.showNormal()
		else:
			self.showMaximized()
	def main_close(self):
		exit()
	def recode(self):
		pass
	def Duplicate_checking(self):
		pass
	def Write_info(self):
		pass
	def left_button1(self):
		self.right_label_0 = QtWidgets.QLabel(self)
		self.right_label_0.setObjectName("right_label_0")
		pixmap = QtGui.QPixmap("picture/main.jpg")	# 按指定路径找到图片
		self.right_label_0.setPixmap(pixmap)  # 在label上显示图片
		self.right_label_0.setScaledContents(True)	# 让图片自适应label大小
		self.right_layout_1.addWidget(self.right_label_0, 1, 1, 1, 1)
	def init_right(self):
		self.right_label_0 = QtWidgets.QLabel(self)
		self.right_label_0.setObjectName("right_label_0")
		pixmap = QtGui.QPixmap("picture/main.jpg")	# 按指定路径找到图片
		self.right_label_0.setPixmap(pixmap)  # 在label上显示图片
		self.right_label_0.setScaledContents(True)	# 让图片自适应label大小
		self.right_layout_1.addWidget(self.right_label_0, 1, 1, 1,1)
		movie=QtGui.QMovie('./picture/demo.gif')
		movie.setCacheMode(QtGui.QMovie.CacheAll)
		self.right_label_0.setMovie(movie)
		movie.start()
	def close_video(self):
		#self.show_camera.exit()
		#self.show_camera.quit()
		#self.c = MainUi()
		#self.c.show_camera.vid.release()
		#show_camera.close()
		self.flag=1;
	def show_camera(self):
		video_path=0
		output_path=""
		self.vid1 = cv2.VideoCapture(video_path)
		if not self.vid1.isOpened():
			raise IOError("Couldn't open webcam or video")
		video_FourCC	= int(self.vid1.get(cv2.CAP_PROP_FOURCC))
		video_fps		= self.vid1.get(cv2.CAP_PROP_FPS)
		video_size		= (int(self.vid1.get(cv2.CAP_PROP_FRAME_WIDTH)),
						int(self.vid1.get(cv2.CAP_PROP_FRAME_HEIGHT)))
		isOutput = True if output_path != "" else False
		if isOutput:
			print("!!! TYPE:", type(output_path), type(video_FourCC), type(video_fps), type(video_size))
			out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size)
		accum_time = 0
		curr_fps = 0
		fps = "FPS: ??"
		prev_time = timer()
		while True:
			return_value, frame = self.vid1.read()
			#cv2.imwrite("image.jpg", frame)
			#image.show()
			#------------------
			image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
			image,sum= yolo.detect_image(image)
			#----------------------------------
			result = np.asarray(image)
			#----------------------------------
			#result = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)
			#----------------------------------
			curr_time = timer()
			exec_time = curr_time - prev_time
			prev_time = curr_time
			accum_time = accum_time + exec_time
			curr_fps = curr_fps + 1
			if accum_time > 1:
				accum_time = accum_time - 1
				fps = "FPS: " + str(curr_fps)
				curr_fps = 0
			cv2.putText(result, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
					fontScale=0.50, color=(255, 0, 0), thickness=2)
			if isOutput:
				out.write(result)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			if self.flag==1:
				self.flag=0
				self.vid1.release()
				cv2.destroyAllWindows()
				break
			height, width = frame.shape[:2]
			showImage = QtGui.QImage(result,width,height,QtGui.QImage.Format_RGB888)
			self.right_label_0.setPixmap(QtGui.QPixmap.fromImage(showImage))
	def show_video(self):
		video_info = QFileDialog.getOpenFileName(QtWidgets.QMainWindow(), '选择视频', '',
																		'Video files(*.mp4 , *.avi)')
		video_name = video_info[0]
		if video_name == '':
			return
		video_path=video_name
		output_path=""
		self.vid2= cv2.VideoCapture(video_path)
		if not self.vid2.isOpened():
			raise IOError("Couldn't open webcam or video")
		video_FourCC	= int(self.vid2.get(cv2.CAP_PROP_FOURCC))
		video_fps		= self.vid2.get(cv2.CAP_PROP_FPS)
		video_size		= (int(self.vid2.get(cv2.CAP_PROP_FRAME_WIDTH)),
						int(self.vid2.get(cv2.CAP_PROP_FRAME_HEIGHT)))
		isOutput = True if output_path != "" else False
		if isOutput:
			print("!!! TYPE:", type(output_path), type(video_FourCC), type(video_fps), type(video_size))
			out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size)
		accum_time = 0
		curr_fps = 0
		fps = "FPS: ??"
		prev_time = timer()
		while True:
			return_value, frame = self.vid2.read()
			#cv2.imwrite("image.jpg", frame)
			#image.show()
			#------------------
			image= Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
			image,sum,num= yolo.detect_image(image)
			#----------------------------------
			result = np.asarray(image)
			#----------------------------------
			#result = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
		 #----------------------------------
			curr_time = timer()
			exec_time = curr_time - prev_time
			prev_time = curr_time
			accum_time = accum_time + exec_time
			curr_fps = curr_fps + 1
			if accum_time > 1:
				accum_time = accum_time - 1
				fps = "FPS: " + str(curr_fps)
				curr_fps = 0
			cv2.putText(result, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
					fontScale=0.50, color=(255, 0, 0), thickness=2)
			if isOutput:
				out.write(result)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			if self.flag==1:
				self.flag=0
				self.vid2.release()
				cv2.destroyAllWindows()
				break
			height, width = frame.shape[:2]
			showImage = QtGui.QImage(result,width,height,QtGui.QImage.Format_RGB888)
			self.right_label_0.setPixmap(QtGui.QPixmap.fromImage(showImage))
	def show_photo(self):
		picture_info = QFileDialog.getOpenFileName(QtWidgets.QMainWindow(), '选择图片', '',
																'Picture files(*.jpg)')
		picture_name = picture_info[0]
		if picture_name == '':
			return
		print(picture_name)
		image = Image.open(picture_name)
		print(image.size)
		image,sum,num= yolo.detect_image(image)
		width,height=image.size
		print(image.size)
		img=image.resize((400, 400))
		result = np.asarray(img)
		showImage = QtGui.QImage(result,400,400,QtGui.QImage.Format_RGB888)
		self.right_label_0.setPixmap(QtGui.QPixmap.fromImage(showImage))
		cursor.execute('INSERT INTO `photo` (`name`, `wear_sum`,`no_wear_sum`) VALUES (%s,%s,%s)', (picture_name,num,sum-num))
		connection.commit()
		begin=Speak()
		begin.speak(data="发现"+str(num)+"个头盔")


	def write_databank(self):
		picture_info = QFileDialog.getOpenFileName(QtWidgets.QMainWindow(), '选择图片', '',
																'Picture files(*.jpg)')
		picture_name = picture_info[0]
		if picture_name == '':
			return
		image = Image.open(picture_name)
		self.r_image=yolo.detect_image(image)
		self.r_image.show()
	def clear_databank(self):
		cursor.execute("DROP TABLE IF EXISTS photo")
		cursor.execute("DROP TABLE IF EXISTS video")
		cursor.execute('''
			CREATE TABLE `photo` (
			`id` int(11) NOT NULL AUTO_INCREMENT,
			`name` varchar(255) NOT NULL,
			`wear_sum` INT	NOT NULL DEFAULT '0',
			`no_wear_sum` INT  NOT NULL DEFAULT '0',
			PRIMARY KEY (`id`)
		) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4
		''')
		cursor.execute('''
			CREATE TABLE `video` (
			`id` int(11) NOT NULL AUTO_INCREMENT,
			`name` varchar(255) NOT NULL,
			`wear_sum` INT	NOT NULL DEFAULT '0',
			`no_wear_sum` INT  NOT NULL DEFAULT '0',
			PRIMARY KEY (`id`)
			) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4
		''')
	def daochu_excel(self):
		table_name="photo"
		output_excel="./excel/"
		count = cursor.execute('select * from '+table_name)
		# print(self._cursor.lastrowid)
		print(count)#获取总条数
		# 重置游标的位置
		cursor.scroll(0, mode='absolute')
		# 搜取所有结果
		results = cursor.fetchall()
		print(results)
		# 获取MYSQL里面的数据字段名称
		fields = cursor.description
		workbook = xlwt.Workbook()
		# 注意: 在add_sheet时, 置参数cell_overwrite_ok=True, 可以覆盖原单元格中数据。
		# cell_overwrite_ok默认为False, 覆盖的话, 会抛出异常.
		sheet = workbook.add_sheet('table_'+table_name, cell_overwrite_ok=True)
		# 写上字段信息
		for field in range(0, len(fields)):
			sheet.write(0, field, fields[field][0])
		# 获取并写入数据段信息
		row = 1
		col = 0
		for row in range(1,len(results)+1):
			for col in range(0, len(fields)):
				sheet.write(row, col, u'%s' % results[row-1][col])
		workbook.save(output_excel+'demo'+'.xlsx')
	def mousePressEvent(self, event):
		if event.button()==QtCore.Qt.LeftButton:
			self.m_flag=True
			self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
			event.accept()
			self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))	 #更改鼠标图标

	def mouseMoveEvent(self, QMouseEvent):
		if QtCore.Qt.LeftButton and self.m_flag:
			self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
			QMouseEvent.accept()

	def mouseReleaseEvent(self, QMouseEvent):
		self.m_flag=False
		self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

def main():
	app = QtWidgets.QApplication(sys.argv)
	gui = MainUi()
	gui.show()
	sys.exit(app.exec_())
	yolo.close_session()
	connection.close()
cursor = connection.cursor()
# cursor.execute("DROP TABLE IF EXISTS photo")
# cursor.execute("DROP TABLE IF EXISTS video")
# cursor.execute('''
# CREATE TABLE `photo` (
 # `id` int(11) NOT NULL AUTO_INCREMENT,
# `name` varchar(255) NOT NULL,
 # `wear_sum` INT  NOT NULL DEFAULT '0',
 # `no_wear_sum` INT  NOT NULL DEFAULT '0',
 # PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4
# ''')
# cursor.execute('''
# CREATE TABLE `video` (
 # `id` int(11) NOT NULL AUTO_INCREMENT,
# `name` varchar(255) NOT NULL,
 # `wear_sum` INT  NOT NULL DEFAULT '0',
 # `no_wear_sum` INT  NOT NULL DEFAULT '0',
 # PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4
# ''')
if __name__ == '__main__':
	main()
