#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File    : mask_blastdb_by_taxid.py
Author  : Dominik R. Laetsch, dominik.laetsch at gmail dot com 
Version : 0.1
"""

import os, argparse, subprocess, re

class blastdb(object):
	def __init__(self, filename):
		self.filename = filename
		self.type = ''
		if (self.is_blastdb()):
			if (self.get_dbtype()):
				self.type = self.get_dbtype() 
				print "Database " + self.filename + " is of type " + self.get_dbtype() 
			else:
				print "Database " + self.filename + " is not a BLAST db"

	def is_blastdb(self):
		'''Returns true if system call blastdbcmd -info returns a meaningful result''' 
		try:
			#call(["module load blast"]) # for bigfoot
			blastdbcmd_output = subprocess.check_output("blastdbcmd -db " + self.filename + " -info", stderr=subprocess.STDOUT, shell=True)
			#call(["module unload blast"]) # for bigfoot
			if blastdbcmd_output.startswith('Database:'):
				return True
			else:
				return False
		except:
			print "Blast db " + self.filename + " can't be found"

	def get_dbtype(self):
		'''Returns type based on file extension... could probably be improved'''
		if os.path.isfile(self.filename + '.pal'):
			return 'prot'
		elif os.path.isfile(self.filename + '.nal'):
			return 'nucl'
		else: 
			return False

	def get_gi_taxid_dmp_path(self):
		'''Returns path of gi_taxid_dmp file of the same type as blastdb ('nucl' or 'prot')'''
		gi_taxid_dmp_paths={'nucl' : os.path.dirname(self.filename) + '/gi_taxid_nucl.dmp', 'prot' : os.path.dirname(self.filename) + '/gi_taxid_prot.dmp'}
		if os.path.isfile(gi_taxid_dmp_paths[self.type]):
			return gi_taxid_dmp_paths[self.type]
		else:
			print gi_taxid_dmp_paths[self.type] + " was not found" 

def parse_gi_taxid_dmp_for_taxids(gi_taxid_dmp):
	gi_taxid_dmp_format = r'^\d+\t\d+\n$'
	line_number = 0
	current_gi, current_taxid = 0, 0
	gis_of_taxid = {}

	print "Parsing " + gi_taxid_dmp + " for " + str(taxid_dict.keys()) + " ..."
	with open(gi_taxid_dmp) as fh:
		for line in fh:
			line_number += 1
			if re.search(gi_taxid_dmp_format, line):
				current_gi, current_taxid = line.rstrip("\n").split("\t")
				current_gi, current_taxid = int(current_gi), int(current_taxid)
				if current_taxid in taxid_dict:
					taxid_dict[current_taxid] += 1
					if current_taxid in gis_of_taxid:
						gis_of_taxid[current_taxid].append(current_gi)
					else:
						gis_of_taxid[current_taxid] = [current_gi]
			else:
				print "line "+ str(line_number) + " : [\"" + line.rstrip("\n") + "\"] looks bad"
				break
	fh.close()
	for taxid in sorted(taxid_dict):
		print str(taxid) + "\t: " + str(taxid_dict[taxid])
	return gis_of_taxid

def output_gis(db, gis_of_taxid, out_suffix, merge_flag):
	taxid_string = ''
	gi_string = ''
	gi_filenames = []
	if (merge_flag):
		for taxid in sorted(gis_of_taxid):
			taxid_string += str(taxid) + "."
		output_filename = db.filename + "." + db.type + ".filtered." + taxid_string + "txt"
		gi_filenames.append(output_filename)
		output_file = open(output_filename + "txt" , "w")
		for taxid in sorted(gis_of_taxid):
			for gi in gis_of_taxid[taxid]:
				output_file.write(str(gi)+"\n")
		output_file.close()
	else:
		for taxid in gis_of_taxid:
			taxid_string = str(taxid)
			output_filename = db.filename + "." + db.type + ".filtered." + taxid_string
			gi_filenames.append(output_filename)
			output_file = open(output_filename + ".txt", "w")
			for gi in gis_of_taxid[taxid]:
				output_file.write(str(gi)+"\n")	 
		output_file.close()
	return gi_filenames
	
def make_alias_blastdbs(db, gi_filenames):
	'''Makes alias blastdbs of db based on gi lists in output_filenames and returns the paths for the alias blastdbs''' 
	for gi_filename in gi_filenames:
		subprocess.call("blastdb_aliastool -gilist " + gi_filename + " -db " + db.filename + " -out " + gi_filename + "db", shell=True)
		#try:
			#call(["module load blast"]) # for bigfoot
			
			#call(["module unload blast"]) # for bigfoot
		#except:
		#	pass

if __name__ == "__main__":

	# # # # # # # # # # # # # # # # 
	# COMMAND-LINE ARGUMENT PARSING
	# # # # # # # # # # # # # # # # 

	parser = argparse.ArgumentParser(
		prog='mask_blastdb_by_taxid',
		usage = '%(prog)s -db -type -taxid [-merge] [-h]',
		add_help=True)
	parser.add_argument('-db', metavar = 'db_path', help='path of blastdb input')
	parser.add_argument('-out', metavar = 'blastdb_out', default='', type = str,  help='blastdb output suffix')
	parser.add_argument('-taxids', metavar = 'taxids' , default=[], type = int, nargs='+', help='TaxIDs for which BLASTdbs should be generated') 
	parser.add_argument('-merge', action='store_true' , help='Set flag for merging ') 

	args = parser.parse_args()



	blastdb_path, taxids, merge_flag, out_suffix = os.path.abspath(args.db), args.taxids, args.merge, args.out

	taxid_dict = {}
	
	for taxid in taxids:
		taxid_dict[taxid] = 0

	db = blastdb(blastdb_path)
	
	gi_taxid_dmp = db.get_gi_taxid_dmp_path()

	#gis_of_taxid = parse_gi_taxid_dmp_for_taxids(gi_taxid_dmp)  
	
	#gi_filenames = output_gis(db, gis_of_taxid, out_suffix, merge_flag)
	gi_filenames = ['/exports/blast_db/nt.nucl.filtered.36090txt']
	alias_blastdbs = make_alias_blastdbs(db, gi_filenames)   

