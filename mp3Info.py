# -*- coding: UTF-8 -*-

import sys
import os
import re
import shutil
import time
from os import path
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from pprint import pprint

def setTag(set_data,path):
    audio = MP3(path,ID3=EasyID3)
##    print('Audio---Single---Before:\n'+audio['title'][0]+'---'+
##          audio['artist'][0]+'---'+audio['album'][0]+'---'+audio['genre'][0]+'\n')
    audio['title'] = set_data['title']
    audio['artist'] = set_data['artist']
    audio['genre'] = set_data['genre']
    audio['album'] = set_data['album']
    audio.save()
    print(audio.get('title',['  '])[0]+'---'+audio.get('artist',['  '])[0]+
          '---'+audio.get('album',['  '])[0]+'---'+audio.get('genre',['  '])[0])
    id3 = ID3(path)
    id3.save(v2_version = 3)

def setFile(inpath,outpath):
    audio = EasyID3(inpath)
    artist = audio.get('artist',[''])[0]
    filedir = str(outpath) +'/'+ str(artist)
    if not os.path.isdir(filedir):
        os.makedirs(filedir)
    if re.match(r'.+?\.mp3',inpath):
        shutil.copy(src=inpath,dst=filedir)
        return True
    else:
        return False
    
    
def fullDir(directory):
    _dir = None
    if(directory is None):
        _dir = os.getcwd().replace('\\','/')
    elif(os.path.isdir(directory)):
        _dir = directory
    else:
        raise FileNotFoundError
    fnamelist=os.listdir(path = _dir)
    pathlist = []
    for fname in fnamelist:
        if(os.path.isfile(_dir+'/'+fname)
           and (re.match(r'(.+?)\.mp3',fname))
           ):
            pathlist.append(_dir+'/'+fname)
    print(pathlist)
    return pathlist
    
    


class tagInfo(object):
    def __init__(self,inPath=None,outPath = None,Type = 1,ifLog = False):
        try:
            self.inPath = inPath
            self.transNum = 0
            if(outPath is None):
                self.outPath = inPath
            else:
                self.outPath = outPath
            self.Type = Type
            self.ifLog = ifLog
        except IOError:
            print("input failed")

    @property
    def transNum(self):
        return self._transNum
    @transNum.setter
    def transNum(self,num):
        self._transNum = num
        
    @property
    def inPath(self):
        return self._inPath
    @inPath.setter
    def inPath(self,path):
        self._inPath = path 
        
    @property
    def outPath(self):
        return self._outPath
    @outPath.setter
    def outPath(self,path):
        self._outPath = path

    @property
    def Type(self):
        return self._Type
    @Type.setter
    def Type(self,types):
        self._Type = types

    @property
    def ifLog(self):
        return self._ifLog
    @ifLog.setter
    def ifLog(self,log):
        self._ifLog = log
        

    def setAll(self,set_Dict):
        filelist = fullDir(self.inPath)
        if self.ifLog:
            content=[]
            bjtime = time.strftime("%a, %d %b %Y %H:%M:%S Beijing", time.localtime())
            content.append(
                '{0:^30}{1:^30}{2:^30}{3:^30}{4:^30}\n'.format(
                    'File Name','Title','Artist','Album','Genre'))
        for fpath in filelist:
            basename = os.path.basename(fpath).rstrip('.mp3')
            if basename in set_Dict:
                print('Audio--'+str(self.transNum)+':')
                self.transNum += 1
                setTag(set_data=set_Dict[basename],path=fpath)
            else:
                print(basename+'.mp3 not in dict')
            if self.ifLog:
                    id3 = EasyID3(fpath)
                    content.append(
                    '{0:^30}{1:^30}{2:^30}{3:^30}{4:^30}\n'.format(
                        basename,id3.get('title',[' '])[0],
                        id3.get('artist',[' '])[0],
                        id3.get('album',[' '])[0],id3.get('genre',[' '])[0]))
        if self.ifLog:
            logfile=open(self.inPath+'/Log.txt','w')
            logfile.writelines(['Log Information:\n','Time:'+bjtime+'\n',
                            'Total Numbers:'+str(self.transNum)+'\n']+content)
            logfile.close()
            
    def classiAll(self):
        filelist = fullDir(self.inPath)
        for fpath in filelist:
            if setFile(inpath=fpath,outpath=self.outPath):
                print(fpath+'-----classified successfully')
            else:
                print(fpath+'-----not an available MP3 file!')
            

    
if __name__=='__main__':
    a = tagInfo()
    a.inPath = 'E:/pythonwork/mp3Info'
    a.outPath = 'C:/Users/Administrator/Desktop/tag/obekano'
    a.ifLog = True
    index = {'gray':
             {'title': ['fsdfsd'], 'genre': ['J-Pop'], 'date': ['2014'],
              'tracknumber': ['1'], 'artist': ['fdsfsd'],
              'album': ['jghjg'], 'discnumber': ['1']},
             
             'MYFIRSTSTORY1':{'title': ['dsfsdf'], 'genre': ['J-Pop'],
                     'date': ['2014'], 'tracknumber': ['1'],
                     'artist': ['fdf'], 'album': ['fdsf'],
                     'discnumber': ['1']},
            
            '愛言葉Ⅱ':{'title': ['fdfdf'], 'genre': ['fsdaf'],
                     'date': ['2014'], 'tracknumber': ['1'],
                     'artist': ['1'], 'album': ['fdfd'],
                     'discnumber': ['1']}
             }
##    pprint(index)
##    pprint(a.inPath)
##    pprint(a.outPath)
##    pprint(a.Type)
    a.setAll(index)
    a.classiAll()
