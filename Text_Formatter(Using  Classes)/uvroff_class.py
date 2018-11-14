#!/usr/bin/env python3

import fileinput
import re
import os
import sys

class Invalid_input_exception(Exception):
    def __init__(self, file, none):
        self.file = file
    def __str__(self):
        return repr(self.file)
        
class Invalid_filename_exception(Exception):
    def __init__(self, file, none):
        self.file = file
    def __str__(self):
        return repr(self.file)

class UVroff:
    var = {'.FT': False,'.LW': 0,'.LM': 0,'.LS': 0}
    state = {'line_len':0}
	
    def __init__(self, filename , none):
        self.filename = filename
        self.none = none
        self.out = ""
        self.start()

    def start(self):
        try:
            if self.filename:
                if os.path.isfile(self.filename):
                    txt = open(self.filename, 'r')
                    self.transform(txt)
                elif self.none:
                    self.transform(self.none)
                    
        except IOError:
            print("Can't find file " + self.filename)
        else:
                    name = self.filename.split('.')[0]
                    extension = self.filename.split('.')[1]
                    if not re.findall(r'[^A-Za-z0-9_\-\\]', name):
                        raise Invalid_filename_exception('File name error!!!')
                    if extension != 'txt':
                        raise Invalid_input_exception('Invalid input file!!!')
                    
            

    def extract(self, l):
            strtok = l.split()
            if len(strtok) is not 0:
                if strtok[0] == ".FT":
                    if strtok[1] == "off":
                        UVroff.var['.FT'] = False
                    elif strtok[1] == "on":
                        UVroff.var['.FT'] = True
                    elif strtok != "off" and strtok !="on": 
                        UVroff.var['.FT'] = False
                        raise Invalid_input_exception("Invalid FT state provided" + l)
                elif strtok[0] == ".LW":
                    if isinstance(int(strtok[1]),int):
                        UVroff.var['.LW'] = int(strtok[1])
                        UVroff.var['.FT'] = True
                    elif strtok[1][0] == "-":
                        UVroff.var['.FT'] = True
                        try:
                            UVroff.var['LW'] -= int(strtok[1][1:])
                        except Invalid_input_exception:
                            raise Invalid_input_exception("A number needed")
                    elif strtok[1][0] == "+":
                        UVroff.var['.FT'] = True
                        try:
                            UVroff.var['.LW'] -= int(strtok[1][1:])
                        except Invalid_input_exception:
                            raise Invalid_input_exception("A number needed")
                elif strtok[0] == ".LM":
                    if strtok[1][:1] == "-":
                        try:
                            UVroff.var['.LM'] -= int(strtok[1][1:])
                        except Invalid_input_exception:
                            raise Invalid_input_exception("A number needed")
                            if UVroff.var['.LM'] < 0:
                                UVroff.var['.LM'] = 0
                    elif strtok[1][:1] == "+":
                        try:
                            UVroff.var['.LM'] += int(strtok[1][1:])
                        except Invalid_input_exception:
                            raise Invalid_input_exception("A number needed")
                        else: 
                            UVroff.var['LM'] = int(strtok[1])
                    if UVroff.var['.LM'] > UVroff.var['.LW'] - 20: 
                        UVroff.var['.LM'] = UVroff.var['.LW'] - 20
                    else: 
                        UVroff.var['.LM'] = int(strtok[1])
                elif strtok[0] == ".LS":
                    try:
                        UVroff.var['.LS'] = int(strtok[1])
                    except ValueError:
                        raise ValueError("NUMBER NEEDED!!")
                    except Invalid_input_exception:
                        raise Invalid_input_exception("A number needed")
              
    def transform(self, txt):
        space = "".join(["\n" for i in range(UVroff.var['.LS'])])
        word = ""
        for l in txt:
            strtok = l.split()
            self.extract(l)
            
            if l.startswith(".FT",0) or l.startswith(".LM",0) or l.startswith(".LW",0) or l.startswith(".LS",0):
                continue
            if UVroff.var['.FT'] == False:
                self.out  += l
                continue
            elif l.startswith("\n") and l.endswith("\n"):
                UVroff.state['line_len'] = 0
                if UVroff.var['.LS'] == 0:
                    self.out  = self.out + '\n\n'
                elif UVroff.var['.LS'] == 1:
                    self.out  = self.out + '\n\n\n' + "".join(["\n" for i in range(UVroff.var['.LS'])])
                else:
                    self.out  = self.out + '\n\n\n\n' + "".join(["\n" for i in range(UVroff.var['.LS'])])
                continue
            l.rstrip()
            for word_count, next in enumerate(strtok):
                if word_count != 0:
                    self.add_new_word(word)
                word = next
            self.add_new_word(word)

    def add_new_word(self, word):
        space = "".join(["\n" for i in range(UVroff.var['.LS'])])
        margin = "".join([" " for i in range(UVroff.var['.LM'])])
        if self.state['line_len'] == 0:
            self.out = self.out + margin
            UVroff.state['line_len'] = UVroff.var['.LM']
        
        elif UVroff.state['line_len'] + len(word) >= UVroff.var['.LW']:
            self.out = self.out + '\n' + space + margin
            UVroff.state['line_len'] = UVroff.var['.LM']
        elif UVroff.state['line_len'] != UVroff.var['.LM']:
            UVroff.state['line_len'] += 1
            self.out += " "
        self.out  += word
        UVroff.state['line_len'] += len(word)

            
    def get_lines(self):
        send_lines = iter(self.out.splitlines())
        return send_lines

if __name__ == "__main__":
    uvroff_class = UVroff()
    lines = UVroff.get_lines()
    print(''.join(lines))
    
  