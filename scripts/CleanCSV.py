#!/usr/bin/env python
# encoding: utf-8
'''
CleanCSV -- Clean up the CSV provided by the yumellow spider

CleanCSV is a CSV clean up script

It defines TBD

@author:     Solvire
            
@copyright:  2013 SJS. All rights reserved.
            
@license:    private

@contact:    steve@openfoc.us
@deffield    updated: Updated
'''
import sys
import os
import csv

from optparse import OptionParser

__all__ = []
__version__ = 0.1
__date__ = '2013-09-21'
__updated__ = '2013-09-21'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

def main(argv=None):
    '''Command line options.'''    
    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"
    program_build_date = "%s" % __updated__
 
    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    #program_usage = '''usage: spam two eggs''' # optional - will be autogenerated by optparse
    program_longdesc = '''''' # optional - give further explanation about what the program does
    program_license = "Copyright 2013 Solvire (SJS)                                            \
                Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0"

    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
        parser.add_option("-i", "--in", dest="infile", help="set input path [default: %default]", metavar="FILE")
        parser.add_option("-o", "--out", dest="outfile", help="set output path [default: %default]", metavar="FILE")
        parser.add_option("-x", "--exclusion_file", dest="exclusion_file", help="set path of the exclusion file [default: %default]", metavar="FILE")
        parser.add_option("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %default]")
        
        # set defaults
        ## probably should not be used to store data inside the working machine... use your local directory
        parser.set_defaults(outfile="~/data/output.csv", infile="~/data/items.csv", exclusion_file="./data/exclusion.txt")

        # process options
        (opts, args) = parser.parse_args(argv)
        
        if opts.verbose > 0:
            print("verbosity level = %d" % opts.verbose)
        if opts.infile:
            print("infile = %s" % opts.infile)
        if opts.outfile:
            print("outfile = %s" % opts.outfile)
        if opts.exclusion_file:
            print("exclusion_file = %s" % opts.exclusion_file)
            
        # MAIN BODY #
        if DEBUG:
            print "Starting to run CSV parsing "
    
        excluded_words = [line.strip().lower() for line in open(opts.exclusion_file)]
        
        if DEBUG:
            print "Using excluded words as: " 
            print excluded_words
        
        # clean up the output files 
        f_out = open(opts.outfile,'w')
        f_out.close()
        f_outx = open(opts.outfile.replace('.csv', '.ex.csv'),'w')
        f_outx.close()        
        
        
        with open(opts.infile) as csvfile:
            crawl_list = csv.reader(csvfile)
            if DEBUG: print "starting csv read " + opts.infile
            for row in crawl_list:
                write_csv(row,opts.outfile,excluded_words)
                
        
    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


def write_csv(row,outfile,excluded_words):
#     if DEBUG:
#         print "Writing row: " + outfile
#         print row
    if(is_excluded(row,excluded_words)):
        write_file(row,outfile.replace('.csv', '.ex.csv') )
    else:
        write_file(row,outfile)
        # and do it again for the individual city
#         print "Writing new file name " + outfile + " to new " + outfile.replace('.csv','.city.' + row[2] + '.csv') 
#         write_file(row,outfile.replace('.','.city.' + row[2] + '.csv'))
        
        
def write_file(row,file_name):
#     if DEBUG: print "Writing to file: " + file_name
    with open(file_name,'a') as csvfile:
        row = map(lambda s: s.strip(), row)
        writer = csv.writer(csvfile)
        writer.writerow(row)
    return

# loop through the excluded words
# if there are any matches to the restaurant name then skip it
def is_excluded(row,excluded_words):
    valstring = ' ' . join(row)
    for word in excluded_words:
#         print "ITEM: " + valstring.lower() + " WORD: " + word.lower() + "\n"
        if(valstring.lower().find(word.lower()) > 0):
            if DEBUG: print "Found word match for exclusion with word " + word
            return True
    return False

if __name__ == "__main__":
    if DEBUG:
#         sys.argv.append("-h")
        print "DEBUGGING ON"
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'CleanCSV_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())