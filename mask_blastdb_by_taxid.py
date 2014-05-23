#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File    : mask_blastdb_by_taxid.py
Author  : Dominik R. Laetsch, dominik.laetsch at gmail dot com 
Version : 0.1
"""

import os, argparse, subprocess

class blastdb(object):
	def __init__(self, filename):
		self.filename = filename
		if (self.is_blastdb()):
			if self.get_dbtype():
				print "Database " + self.filename + " is of type " + self.get_dbtype() 
		else:
			print "Database " + self.filename + " can't be found" 

	def is_blastdb(self):
		try:
			'''Runs a system call of blastdbcmd -info on the database to see whether db_path points to a blast_db''' 
			#call(["module load blast"]) # for bigfoot
			out = subprocess.check_output("blastdbcmd -db " + self.filename + " -info", stderr=subprocess.STDOUT, shell=True)
			#call(["module unload blast"]) # for bigfoot
			if out.startswith('Database:'):
				return True
			else:
				return False
		except:
			pass

	def get_dbtype(self):
		try:
			'''Return type based on file extension... could probably be improved'''
			if os.path.isfile(self.filename + '.psq'):
				return 'prot'
			elif os.path.isfile(self.filename + '.nin'):
				return 'nucl'
		except:
			return False

	def get_gi_taxid_dmp_path(self):
		gi_taxid_dmp_paths={'nucl' : os.path.abspath(os.path.dirname(self.filename)) + '/gi_taxid_nucl.dmp', 'prot' : os.path.abspath(os.path.dirname(self.filename)) + '/gi_taxid_prot.dmp'}
		try:
			if os.path.isfile(gi_taxid_dmp_paths[self.type]):
				return gi_taxid_dmp_paths[self.type]
			else:
				print gi_taxid_dmp_paths[self.type] + " was not found" 
		except:
			return False


if __name__ == "__main__":

	# # # # # # # # # # # # # # # # 
	# COMMAND-LINE ARGUMENT PARSING
	# # # # # # # # # # # # # # # # 

	parser = argparse.ArgumentParser(
		prog='mask_blastdb_by_taxid',
		usage = '%(prog)s -db -type -taxid [-merge] [-h]',
		add_help=True)
	parser.add_argument('-db', metavar = 'db_path', help='path of blastdb input')
	parser.add_argument('-out', metavar = 'blastdb_out', help='blastdb output prefix')
	parser.add_argument('-taxids', metavar = 'taxids' , default=[], type = int, nargs='+', help='TaxIDs for which BLASTdbs should be generated') 
	parser.add_argument('-merge', action='store_true' , help='Set flag for merging ') 

	args = parser.parse_args()

	blastdb_path, taxids, merge_flag, out_prefix = args.db, args.taxids, args.merge, args.out

	db = blastdb(blastdb_path)
	db.get_gi_taxid_dmp_path()