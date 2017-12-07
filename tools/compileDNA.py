#!/usr/bin/env python2
from toontown.dna.ply import lex
from toontown.dna import DNAStorage
from toontown.dna import DNARoot
from toontown.dna.tokens import *

import argparse
import os
import sys
import glob

parser = argparse.ArgumentParser(
    description='This utility can be used to produce compiled DNA files.')
parser.add_argument('--compress', '-c', action='store_true',
                    help='Compress the output file using ZLib.')
parser.add_argument('--verbose', '-v', action='store_true',
                    help='Describe the build process.')
parser.add_argument('--logfile', '-l',
                    help='Optional file to write the console output to.')
parser.add_argument('filenames', nargs='+',
                    help='The raw input file(s). Accepts * and ? as wildcards.')
args = parser.parse_args()

class LogAndOutput:
    def __init__(self, out, filename):
        self.out = out
        self.file = open(filename, 'w')

    def write(self, string):
        self.file.write(string)
        self.out.write(string)
        self.flush()

    def flush(self):
        self.file.flush()
        self.out.flush()


if args.logfile:
    sys.stdout = LogAndOutput(sys.stdout, args.logfile)
    sys.stderr = LogAndOutput(sys.stderr, args.logfile)


lexer = lex.lex(optimize=0)


class DNAError(Exception):
    pass
__builtins__.DNAError = DNAError


def loadDNAFile(dnaStore, filename):
    print 'Reading DNA file...', filename
    root = DNARoot.DNARoot(name='root', dnaStore=dnaStore)
    with open(filename, 'r') as f:
        data = f.read().strip()
        if not data:
            print 'Warning', filename, 'is an empty file.'
            return ''
        f.seek(0)
        root.read(f)
    return str(root.packerTraverse(recursive=True, verbose=args.verbose))


def process_single_file(filename):
    dnaStore = DNAStorage.DNAStorage()
    rootData = loadDNAFile(dnaStore, filename)

    dnaStoreData = dnaStore.dump(verbose=args.verbose)
    output = os.path.splitext(filename)[0] + '.pdna'
    print 'Writing...', output
    data = str(dnaStoreData + rootData)
    if args.compress:
        import zlib
        data = zlib.compress(data)
    header = 'PDNA\n{0}\n'.format(chr(1 if args.compress else 0))
    with open(output, 'wb') as f:
        f.write(header + data)
    if args.verbose:
        catalogCodeCount = 0
        for root, codes in dnaStore.packerCatalogCodes.items():
            catalogCodeCount += len(codes)
        print 'Catalog code count:', catalogCodeCount
        print 'Texture count:', len(dnaStore.textures)
        print 'Font count:', len(dnaStore.fonts)
        print 'Node count:', len(dnaStore.packerNodes)
        print 'Hood node count:', len(dnaStore.packerHoodNodes)
        print 'Place node count:', len(dnaStore.packerPlaceNodes)
        print 'Block number count:', len(dnaStore.packerBlockNumbers)
        print 'Block zone ID count:', len(dnaStore.blockZones)
        print 'Block title count:', len(dnaStore.blockTitles)
        print 'Block article count:', len(dnaStore.blockArticles)
        print 'Block building type count:', len(dnaStore.blockBuildingTypes)
        print 'DNASuitPoint count:', len(dnaStore.suitPoints)
        print 'DNASuitEdge count:', len(dnaStore.suitEdges)
    print 'Done processing %s.' % filename

for filename in args.filenames:
    filelist = []
    if '*' in filename or '?' in filename:
        filelist = glob.glob(filename)
    else:
        filelist.append(filename)

    for file in filelist:
        process_single_file(file)

print 'Done.'