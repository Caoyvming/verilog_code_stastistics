#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import prettytable as pt

VLOG_SUFFIX_SET = {'.v', '.vh'}
SVLOG_SUFFIX_SET = {'.sv', '.svh'}

vlogStatistics_dict = {}
svlogStatistics_dict = {}

class code_statistics:
	def __init__(self, fpath):
		self.code_lines = 0
		self.comment_lines = 0
		self.blank_lines = 0
		self.fpath = fpath
	def count_lines(self):
		with open(self.fpath,'r',encoding='utf-8') as f:
			is_comment = False
			start_comment_index = 0 #Record the location of comments starting with /*
			for index,line in enumerate(f,start=1):
				line = line.strip() #Remove whitespace at the beginning and end
				if not is_comment:
					if line.startswith("/*"): #Determine whether the multiline comment has started
						is_comment = True
						start_comment_index = index
					elif line.startswith('//'): #Single line note
						self.comment_lines += 1
					elif line == '': #Blank line
						self.blank_lines += 1
					else: #Code line
						self.code_lines += 1
				else: 
					if line.endswith("*/"): #Multiline comment has ended
						is_comment = False
						self.comment_lines += index - start_comment_index + 1
					else:
						pass

def traverse_path(path):
	'''
	Traverse the project path, count the number of lines if a file is encountered, and recurse if a directory is encountered
	'''
	filenames = os.listdir(path)
	for f in filenames:
		fpath = os.path.join(path, f)
		if (os.path.isfile(fpath)):
			suffix = os.path.splitext(fpath) [-1]
			if suffix in VLOG_SUFFIX_SET:
				vlog_statistics = code_statistics(fpath)
				vlog_statistics.count_lines()
				vlogStatistics_dict.update({fpath:[vlog_statistics.code_lines, vlog_statistics.comment_lines, vlog_statistics.blank_lines]})
			elif suffix in SVLOG_SUFFIX_SET:
				svlog_statistics = code_statistics(fpath)
				svlog_statistics.count_lines()
				svlogStatistics_dict.update({fpath:[svlog_statistics.code_lines, svlog_statistics.comment_lines, svlog_statistics.blank_lines]})
			else:
				pass
		if (os.path.isdir(fpath)):
			traverse_path(fpath)

def print_result():
	'''
	This function depends on the library prettytable. Please use "sudo pip3 install prettytable" for installation
	'''
	total_vlogCodeLines = 0
	total_vlogCommentLines = 0
	total_vlogBlankLines = 0
	vlogtb = pt.PrettyTable()
	vlogtb.field_names = ['VLOG_FILE', 'CODE_LINES', 'COMMENT_LINES', 'BLANK_LINES']
	for k,v in vlogStatistics_dict.items():
		vlogtb.add_row([k, v[0], v[1], v[2]])
		total_vlogCodeLines = total_vlogCodeLines + v[0]
		total_vlogCommentLines = total_vlogCommentLines + v[1]
		total_vlogBlankLines = total_vlogBlankLines + v[2]
	vlogtb.add_row(['TOTAL_VLOG_LINES', total_vlogCodeLines, total_vlogCommentLines, total_vlogBlankLines])
	print(vlogtb)

	print("\n")

	total_svlogCodeLines = 0
	total_svlogCommentLines = 0
	total_svlogBlankLines = 0
	svlogtb = pt.PrettyTable()
	svlogtb.field_names = ['SVLOG_FILE', 'CODE_LINES', 'COMMENT_LINES', 'BLANK_LINES']
	for k,v in svlogStatistics_dict.items():
		svlogtb.add_row([k, v[0], v[1], v[2]])
		total_svlogCodeLines = total_svlogCodeLines + v[0]
		total_svlogCommentLines = total_svlogCommentLines + v[1]
		total_svlogBlankLines = total_svlogBlankLines + v[2]
	svlogtb.add_row(['TOTAL_SVLOG_LINES', total_svlogCodeLines, total_svlogCommentLines, total_svlogBlankLines])
	print(svlogtb)

if __name__ == '__main__':
	if (len(sys.argv) != 2):
		print("Usage : python3 code_statistics.py project_path")
	else:
		project_path = sys.argv[1]
		traverse_path(project_path)
		print_result()


