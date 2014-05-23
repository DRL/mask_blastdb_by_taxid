#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File    : mask_blastdb_by_taxid.py
Author  : Dominik R. Laetsch, dominik.laetsch at gmail dot com 
Version : 0.1
"""

import os, argparse
from subprocess import call

class db(object):
	def __init__(self, filename):
		self.filename = filename
		if (self.found):
			call(["module load blast"])
			print call(["blastdbcmd -db" + self.filename + " -info"])
		else:
			print "Database " + self.filename + " can't be found" 

	def found(self):
		return os.path.isfile(self.filename)

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
	parser.add_argument('-db', metavar = 'blastdb_in', help='blastdb input')
	parser.add_argument('-out', metavar = 'blastdb_out', help='blastdb output prefix')
	parser.add_argument('-taxids', metavar = 'taxids' , default=[], type = int, nargs='+', help='TaxIDs for which BLASTdbs should be generated') 
	parser.add_argument('-merge', action='store_true' , help='Set flag for merging ') 

	args = parser.parse_args()

	blastdb_in, taxids, merge_flag, out_prefix = args.db, args.taxids, args.merge, args.out

	gi_taxid_nucl_dmp = db('$BLASTDB/gi_taxid_nucl.dmp', 'n') 
	gi_taxid_prot_dmp = db('$BLASTDB/gi_taxid_prot.dmp', 'p')
	blastdb = db(blastdb_in)
	#nr = db('$BLASTDB/nr', 'p')

	#gi_taxid_dmp = choose_taxid_dmp(blastdb_type) 
	#print gi_taxid_dmp