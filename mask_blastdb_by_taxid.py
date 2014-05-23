#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File    : mask_blastdb_by_taxid.py
Author  : Dominik R. Laetsch, dominik.laetsch at gmail dot com 
Version : 0.1
"""

import os, argparse, subprocess

class db(object):
	def __init__(self, filename):
		self.filename = filename
		self.type =
		if (self.is_blastdb()):
			self.type
			print "Database " + self.filename + " has been found" 
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


#return os.path.isfile(self.filename)

#class blastdb(db):
#	def get_file(self):
#		if self.type = 'n'
#			return 

#def choose_taxid_dmp(blastdb_type):
#	if (blastdb_type == 'p'):
	# 	db
	# 	try:

	# 		gi_taxid_nucl_dmp = '$BLASTDB/gi_taxid_nucl.dmp' 
	# 	except IOError as ex:
	# 		print "File $BLASTDB/gi_taxid_nucl.dmp could not be found" 
	# 	gi_taxid_dmp = gi_taxid_prot_dmp
	# else:
	# 	gi_taxid_dmp = gi_taxid_nucl_dmp
	# return gi_taxid_dmp

if __name__ == "__main__":

	# # # # # # # # # # # # # # # # 
	# COMMAND-LINE ARGUMENT PARSING
	# # # # # # # # # # # # # # # # 

	parser = argparse.ArgumentParser(
		prog='mask_blastdb_by_taxid',
		usage = '%(prog)s -db -type -taxid [-merge] [-h]',
		add_help=True)
	parser.add_argument('-db', metavar = 'db_path', help='blastdb input')
	parser.add_argument('-out', metavar = 'blastdb_out', help='blastdb output prefix')
	parser.add_argument('-taxids', metavar = 'taxids' , default=[], type = int, nargs='+', help='TaxIDs for which BLASTdbs should be generated') 
	parser.add_argument('-merge', action='store_true' , help='Set flag for merging ') 

	args = parser.parse_args()

	db_path, taxids, merge_flag, out_prefix = args.db, args.taxids, args.merge, args.out

	#gi_taxid_nucl_dmp = db('$BLASTDB/gi_taxid_nucl.dmp') 
	#gi_taxid_prot_dmp = db('$BLASTDB/gi_taxid_prot.dmp')
	blastdb = db(db_path)
	#nr = db('$BLASTDB/nr', 'p')

	#gi_taxid_dmp = choose_taxid_dmp(blastdb_type) 
	#print gi_taxid_dmp