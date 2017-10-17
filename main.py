#coding=utf-8
#qpy:kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.text import LabelBase
from zt import Zhetian
import json
import os
from contextlib import closing

class MyLayout(BoxLayout):
    searchkey=ObjectProperty()
    sourceweb=ObjectProperty()
    novelname=ObjectProperty()
    shownovellist=ObjectProperty()
    novelid=ObjectProperty()
    showchapterlist=ObjectProperty()
    startreadid=ObjectProperty()
    bodyid=ObjectProperty()
    nextbodyid=ObjectProperty()
    scrollid=ObjectProperty()
    scrollreadid=ObjectProperty()
    newreadid=ObjectProperty()

    def novellist(self):
        #print self.sourceweb.text
        #print self.searchkey.text
        #print self.novelname.text
        if 'Zhetian' in self.sourceweb.text:
            self.z=Zhetian()
        if '作者' in self.searchkey.text:
            nlist=self.z.novellist(author=self.novelname.text)
        else:
            nlist=self.z.novellist(name=self.novelname.text)
        msg=''
        for i in range(len(nlist)):
            nsg='编号: %s\n书名: %s\n作者: %s\n分类: %s\n简介: %s\n最新章节: %s\n最后更新: %s\n\n'%(i,nlist[i][1],nlist[i][2],nlist[i][3],nlist[i][4],nlist[i][5],nlist[i][6])
            msg+=nsg
        if nlist:
            self.shownovellist.text=msg
        else:
            self.shownovellist.text='查询不到'
        self.nlist=nlist
    def readonline(self):
        msg=self.nlist[int(self.novelid.text)]
        chapterlist=self.z.chapterlist(msg[0])
        clist=['%s: %s'%(i,chapterlist[i][1]) for i in range(len(chapterlist))]
        self.num=200
        self.chapterlist=chapterlist
        self.clist=clist
        #print clist[0]
        self.showchapterlist.text=''
        for i in range(len(self.clist)):
            self.showchapterlist.text+=self.clist[i]+'\n'
            if i>0 and i%self.num==0:break
        self.scrollreadid.scroll_y=1-0.00001
    def orderlist(self):
        self.clist.reverse()
        self.num=200
        self.showchapterlist.text=''
        for i in range(len(self.clist)):
            self.showchapterlist.text+=self.clist[i]+'\n'
            if i>0 and i%self.num==0:break
        self.scrollreadid.scroll_y=1-0.00001
    def nextpage(self):
        self.num+=200
        self.showchapterlist.text=''
        for i in range(len(self.clist)):
            if i >= self.num-200:
                self.showchapterlist.text+=self.clist[i]+'\n'
            if i>0 and i%self.num==0:break
        self.scrollreadid.scroll_y=1-0.00001
    def beforepage(self):
        self.num-=200
        self.showchapterlist.text=''
        for i in range(len(self.clist)):
            if i >= self.num-200:
                self.showchapterlist.text+=self.clist[i]+'\n'
            if i>0 and i%self.num==0:break
        self.scrollreadid.scroll_y=1-0.00001
    def startread(self):
        self.readid=int(self.startreadid.text)
        chlist=self.chapterlist[self.readid]
        body=self.z.body(chlist[0])
        body=chlist[1]+'\n\n'+body
        body=body.decode('utf-8')
        if len(body)>2500:
            self.nextbodyid.text='下一页'
            msg=''
            self.body=body
            self.bnum=2500
            for i in range(len(body)):
            	    msg+=body[i]
            	    if i>2500:
            	        break
        else:msg=body
        
        self.bodyid.text=msg
        self.readid+=1
    def nextbody(self):
        try:
            if self.nextbodyid.text=='下一页':
                self.bnum+=2500
                msg=''
                for i in range(len(self.body)):
                    if i >self.bnum-2500+1:
                        msg+=self.body[i]
                    if len(self.body)%self.bnum==0:break
                if self.bnum>=len(self.body):
                    self.nextbodyid.text='下一章'
                    #self.readid+=1
                
                self.bodyid.text=msg
                
            else:
                self.readid=self.readid+1
                chlist=self.chapterlist[self.readid]
                body=self.z.body(chlist[0])
                body=chlist[1]+'\n\n'+body
                self.bodyid.text=''
                body=body.decode('utf-8')
                if len(body)>2500:
                    self.nextbodyid.text='下一页'
                    msg=''
                    self.body=body
                    self.bnum=2500
                    for i in range(len(body)):
            	            msg+=body[i]
            	            if i>2500:
            	                self.readid-=1
            	                break
                else:
                    msg=body
                    #self.readid=self.readid+1
                self.bodyid.text=msg
                #self.readid=self.readid+1
            self.scrollid.scroll_y=1-0.00001
        except:
            self.bodyid.text='已到最后一页'
    def beforebody(self):
        self.readid=self.readid-1
        if self.readid<0:
            self.bodyid.text='已到第一页'
        else:
            chlist=self.chapterlist[self.readid]
            body=self.z.body(chlist[0])
            body=chlist[1]+'\n\n'+body
            self.bodyid.text=''
            body=body.decode('utf-8')
            if len(body)>2500:
                self.nextbodyid.text='下一页'
                msg=''
                self.body=body
                self.bnum=2500
                for i in range(len(body)):
                	    msg+=body[i]
                	    if i>2500:
                	        break
            else:msg=body
            self.bodyid.text=msg
        self.scrollid.scroll_y=1-0.00001
    def writetable(self):
        if os.path.exists('table.json'):
            with closing(open('table.json')) as f:
                j=json.loads(f.read())
            try:del j[self.novelname.text]
            except:pass
            j[self.novelname.text]='%s,%s'%(self.novelid.text,self.readid)
            a=json.dumps(j)
            with closing(open('table.json','w')) as f:
                f.write(a)
            self.showtable()
        else:
            t={}
            t[self.novelname.text]='%s,%s'%(self.novelid.text,self.readid)
            a=json.dumps(t)
            with closing(open('table.json','w')) as f:
                f.write(a)
        self.showtable()
    def showtable(self):
        #self.root.ids.sm.current='screen2'
        if os.path.exists('table.json'):
            #self.root.ids.sm.current='table'
            with closing(open('table.json')) as f:
                j=json.loads(f.read())
            z=Zhetian()
            msg=''
            num=0
            for i in j:
                novel=z.novellist(name=i)
                novelid=int(j[i].split(',')[0])
                readid=int(j[i].split(',')[1])
                nlist=z.chapterlist(novel[novelid][0])
                nread=len(nlist)-readid
                update='%s(%s)'%(novel[novelid][-2],novel[novelid][-1])
                nsg='编号: %s\n%s(%s章未读)\n看到: %s\n最新: %s\n\n'%(num,i.encode('utf-8'),nread-1,nlist[readid][1],nlist[-1][1])
                msg+=nsg
                num+=1
            self.ids.tablelist.text=msg
                
        else:
            self.root.ids.sm.current='index'
    def deletetable(self):
        with closing(open('table.json')) as f:
            j=json.loads(f.read())
        l=[i for i in j]
        novelname=l[int(self.newreadid.text)]
        del j[novelname]
        a=json.dumps(j)
        with closing(open('table.json','w')) as f:
            f.write(a)
        self.showtable()
    def readyread(self):
        self.z=Zhetian()
        with closing(open('table.json')) as f:
            j=json.loads(f.read())
        l=[i for i in j]
        novel=l[int(self.newreadid.text)].encode('utf-8')
        novelid=j[novel.decode('utf-8')].split(',')[0]
        readid=j[novel.decode('utf-8')].split(',')[1]
  
        
        self.novelname.text=novel
        self.novelid.text=novelid
        self.startreadid.text=readid
        self.nlist=self.z.novellist(name=self.novelname.text)
        msg=self.nlist[int(self.novelid.text)]
        self.chapterlist=self.z.chapterlist(msg[0])
        self.clist=['%s: %s'%(i,self.chapterlist[i][1]) for i in range(len(self.chapterlist))]

        self.startread()
        
        
        

class MainApp(App):
    def build(self):
        return MyLayout()
    def on_start(self):
        #self.root.ids.sm.current='screen2'
        if os.path.exists('table.json'):
            self.root.ids.sm.current='table'
            with closing(open('table.json')) as f:
                j=json.loads(f.read())
            z=Zhetian()
            msg=''
            num=0
            for i in j:
                novel=z.novellist(name=i)
                novelid=int(j[i].split(',')[0])
                readid=int(j[i].split(',')[1])
                nlist=z.chapterlist(novel[novelid][0])
                nread=len(nlist)-readid
                update='%s(%s)'%(novel[novelid][-2],novel[novelid][-1])
                nsg='编号: %s\n%s(%s章未读)\n看到: %s\n最新: %s\n\n'%(num,i.encode('utf-8'),nread-1,nlist[readid][1],nlist[-1][1])
                msg+=nsg
                num+=1
            self.root.ids.tablelist.text=msg
                
        else:
            self.root.ids.sm.current='index'
if __name__=='__main__':
    LabelBase.register(name='Roboto',fn_regular='droid.ttf')
    MainApp().run()