#coding:utf-8  
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4
import  requests,os
import PyV8
import threading
import sys,re
import wx




reload(sys)
sys.setdefaultencoding('utf-8')


wx_app = wx.App()
frame = wx.Frame(None, -1, 'Google Translate', size = (500, 300),style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)



#wx_app.SetTopWindow( frame )

scroll_text = ''

hbox = ''

panel = ''
100

g_search_count = 0
g_t = 0

g_chang = 500
g_kuan = 300
hanzisize = 12
#print window.geometry(None)



ctxt = PyV8.JSContext()       
ctxt.enter()      
func = ctxt.eval(''' (function(a){ var arr = eval(a); 
    re = ''
    for (i = 0; i < arr[0].length; i++)
    {
        re += arr[0][i][0]

    }
    return re})''')
ctxt2 = PyV8.JSContext() 
func_tk = ctxt2.eval('''
   (function(a, TKK){
    function b(a, b) {
        for (var d = 0; d < b.length - 2; d += 3) {
            var c = b.charAt(d + 2),
                c = "a" <= c ? c.charCodeAt(0) - 87 : Number(c),
                c = "+" == b.charAt(d + 1) ? a >>> c : a << c;
            a = "+" == b.charAt(d) ? a + c & 4294967295 : a ^ c
        }
        return a
    }


    for (var e = TKK.split("."), h = Number(e[0]) || 0, g = [], d = 0, f = 0; f < a.length; f++) {
        var c = a.charCodeAt(f);
        128 > c ? g[d++] = c : (2048 > c ? g[d++] = c >> 6 | 192 : (55296 == (c & 64512) && f + 1 < a.length && 56320 == (a.charCodeAt(f + 1) & 64512) ? (c = 65536 + ((c & 1023) << 10) + (a.charCodeAt(++f) & 1023), g[d++] = c >> 18 | 240, g[d++] = c >> 12 & 63 | 128) : g[d++] = c >> 12 | 224, g[d++] = c >> 6 & 63 | 128), g[d++] = c & 63 | 128)
    }
    a = h;
    for (d = 0; d < g.length; d++) a += g[d], a = b(a, "+-a^+6");
    a = b(a, "+-3^+b+-f");
    a ^= Number(e[1]) || 0;
    0 > a && (a = (a & 2147483647) + 2147483648);
    a %= 1E6;
    return a.toString() + "." + (a ^ h)
    })
    ''')
    
    
app = QApplication([])
clipboard = QApplication.clipboard()

#os.system("chcp 65001")

tk_label = ''


#TKK=eval('((function(){var a\x3d3663761873;var b\x3d-820542038;return 410678+\x27.\x27+(a+b)})())');

def get_tk_fromGoogle():   
    pqyload = {"accept-encoding":"gzip, deflate, sdch",
    "accept-language":"zh-CN,zh;q=0.8,en;q=0.6",
    "host": "translate.google.cn",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2859.0 Safari/537.36",
    "Connection":"keep-alive"}

    pattern = re.compile(r"TKK=eval\('\(\(function\(\)\{var\s+a\\x3d(\d+);var\s+b\\x3d(-?\d+);return\s+(\d+)\+")
     
    r = requests.get("http://translate.google.cn", headers = pqyload)

    match = pattern.findall(r.content)
    ##print r.content
    ##print match
    
    if match:
        return match[0][2] + '.' + str(int(match[0][0]) + int(match[0][1]))


def check_contain_chinese(check_str):

    chinese = 0
    english = 0
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            chinese = chinese + 1
        else:
            english = english + 1

    if chinese > english:
        return 0
    return 1

def on_clipboard_change():
    data1 = clipboard.mimeData()

    print '323'

    try:

        if data1.hasText():    
            global g_search_count
            global g_t

            if g_search_count == 0:
                g_t = get_tk_fromGoogle()


            g_search_count = g_search_count + 1

            if g_search_count > 500 :
                g_t = get_tk_fromGoogle()
                ##print g_t
                g_search_count = 0

            ####print r.content
            ####print data1.text()
            text = str(data1.text())
            text = text.replace("\r\n", " ").replace("\n", " ")


            ###print text
            ###print g_t
            tk = func_tk(text, g_t)
            ###print tk
            ###print type(str(data1.text()))
            
            data = {'q': text}

            if check_contain_chinese(text) == 1:
                url = "http://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&srcrom=1&ssel=0&tsel=0&kc=0&tk=%s" % (tk)
            else:
                url = "http://translate.google.cn/translate_a/single?client=t&sl=zh-CN&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&srcrom=1&ssel=0&tsel=0&kc=0&tk=%s" % (tk)
            
            ####print url
        
            pqyload = {

    "accept-encoding":"gzip, deflate, sdch, br",
    "accept-language":"zh-CN,zh;q=0.8,en;q=0.6",
    "referer":"https://translate.google.com/?hl=zh-CN&tab=wT",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2859.0 Safari/537.36",
    }

            print '11323'
            scroll_text.Clear()
            print 'clear'
            scroll_text.AppendText('...is searching...')
            r = requests.post(url, headers=pqyload, data = data, timeout = 8)
            con = func(r.content)
            global var
            con = con[:-9]


            scroll_text.Clear()
            #print 'clear'
            scroll_text.AppendText(unicode(text + "\r\n" *3  + con, "utf-8"))
    except Exception as e:
        scroll_text.Clear()
        #print 'clear'
        scroll_text.AppendText('failed!!!')

def close_thread(m):
   
    #hbox.Destroy()

    #scroll_text.Destroy()
    panel.Destroy()
    frame.Destroy()
    app.exit()
    
    #sys.exit()


class workthread(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name=threadname)
        self.st = 2 
    def run(self):
        try:
            global scroll_text
            global hbox
            global frame
            global panel
            panel = wx.Panel(frame,style = 0)
            scroll_text = wx.TextCtrl(panel, -1, "" ,size = (500, 300), style=(wx.TE_MULTILINE | wx.BORDER_NONE))

            #scroll_text.SetBackgroundColour(panel.BackgroundColour)


            f=wx.Font(11,wx.SWISS,wx.NORMAL,wx.NORMAL)
            scroll_text.SetFont(f)

            bbox = wx.BoxSizer()
            #bbox.Add(bbox,proportion = 1,flag = wx.ALL,border = 5)

            hbox = wx.BoxSizer(wx.VERTICAL)
            hbox.Add(bbox,proportion = 1,flag = wx.EXPAND | wx.ALL,border = 5)
            hbox.Add(scroll_text,proportion = 1,flag =  wx.EXPAND| wx.LEFT|wx.BOTTOM ,border = 5)
            panel.SetSizer(hbox)

        


            #text.Clear()
            #text.AppendText("rueywriywqedfasdsdsdsdsdsdsdsdsdsdfasddddddddddddddddddddddddddddddsbdddddddddddddddddddddi" )
            frame.Bind(wx.EVT_CLOSE, close_thread)
            frame.Show()
            wx_app.MainLoop()
        except Exception as e:
            print e


#g_t = get_tk_fromGoogle()


##print g_t

clipboard.dataChanged.connect(on_clipboard_change)



work_t = workthread("t1")

work_t.start()
app.exec_()

print 'over'