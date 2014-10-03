#***************************************************#
#                                                   #
#      GFI Sandbox -> MAEC XML Converter Script     #
#                                                   #
# Copyright (c) 2014 - The MITRE Corporation        #
#                                                   #
#***************************************************#

#BY USING THE GFI SANDBOX TO MAEC SCRIPT, YOU SIGNIFY YOUR ACCEPTANCE OF THE TERMS AND 
#CONDITIONS OF USE.  IF YOU DO NOT AGREE TO THESE TERMS, DO NOT USE THE GFI TO MAEC SCRIPT.

#For more information, please refer to the LICENSE.txt file.

#GFI Sandbox Converter Script
#Copyright 2014, MITRE Corp
#v0.23 - BETA
#Updated 10/3/2014

__version__ = 0.23

from __init__ import generate_package_from_report_filepath
import sys
import os
import traceback
import argparse

#Create a MAEC output file from a GFI Sandbox input file.
def create_maec(inputfile, outpath, verbose_error_mode):
    """Create the MAEC output from an input GFI Sandbox XML file"""  
    try:
        package = generate_package_from_report_filepath(inputfile)
        #Finally, Export the results
        package.to_xml_file(outpath, {"https://github.com/MAECProject/gfi-sandbox-to-maec":"GFISandboxToMAEC"})

    except Exception, err:
        print('\nError: %s\n' % str(err))
        if verbose_error_mode:
            traceback.print_exc()

#Print the usage text    
def usage():
    print USAGE_TEXT
    sys.exit(1)
    
USAGE_TEXT = """
GFI Sandbox XML Output --> MAEC XML Converter Utility
v0.23 BETA // Supports MAEC v4.1 and CybOX v2.1

Usage: python gfisandbox_to_maec.py <special arguments> -i <input gfi sandbox xml output> -o <output maec xml file>
       OR -d <directory name>

Special arguments are as follows (all are optional):
-v : verbose error mode (prints tracebacks of any errors during execution).

"""    

def main():
    parser = argparse.ArgumentParser(description="GFI Sandbox to MAEC Translator v" + str(__version__))
    parser.add_argument("input", help="the name of the input GFI XML file OR directory of files to translate to MAEC")
    parser.add_argument("output", help="the name of the MAEC XML file OR directory to which the output will be written")
    parser.add_argument("--verbose", "-v", help="enable verbose error output mode", action="store_true", default=False)
    args = parser.parse_args()

    verbose_error_mode = 0

    # Test if the input is a directory or file
    if os.path.isfile(args.input):
        # If we're dealing with a single file, just call create_maec()
        create_maec(args.input, args.output, args.verbose)
    # If a directory was specified, perform the corresponding conversion
    elif os.path.isdir(args.input):
        # Iterate and try to parse/convert each file in the directory
        for filename in os.listdir(args.input):
            # Only handle XML files
            if str(filename)[-3:] != "xml":
                print str("Error: {0} does not appear to be an XML file. Skipping.\n").format(filename)
                continue
            outfilename = str(filename)[:-4] + "_maec.xml"
            create_maec(os.path.join(args.input, filename), os.path.join(args.output, outfilename), args.verbose)

        
if __name__ == "__main__":
    main()
