#_*_coding:utf-8_*_

#数据库操作
HOSTNAME = "222.186.190.213"
PORT = 3306
USER = "root"
PASSWD = "lyb1092"
DATABASE = "config"
TABLE = "stock_datas_sectordaysdata_2018"
INSERTTIME = 4

#速度设置
SPEED = 5 #一个时间点停留时间（单位s)
UPDATESPEED = 1.8 #时间更新速度
FLOATSPEED = 0.015 #上下浮动速度
SCORESPEED = 3.5 #长短变化速度

#颜色设置
SHADOWCOLOR = (105,105,105)

#屏幕大小
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

#显示边界值
CENTER_X = SCREEN_WIDTH / 2
BORDER_X = 150 #数值条左边界值
BORDER_Y = 40 #数值条上边界值 

TITLE = "Histogram"
BGCOLOR = (0, 0, 0)

FONTSIZE = 13 #字体大小
BOXHEIGHT = 13 #数值条高度
RANKHEIGHT = 16 #相邻数值条距离
MAXLEN = SCREEN_WIDTH * 0.4 #最大长度
BOXLEN = 1 #单位长度
MAXNLENGTH = 1 #所选时间里最长长度

#按钮
BUTTONWIDTH = 28 #按钮长度
BUTTONHEIGHT = 15 #按钮高度
BUTTONDIS = 5 #间距

#输入框
BORDERX_INPUTBOX = 230 
BORDERY_INPUTBOX = SCREEN_HEIGHT - 100
INPUTBOXWIDTH = 70 #文本框长度
INPUTBOXHEIGHT= 15 #文本框宽度
