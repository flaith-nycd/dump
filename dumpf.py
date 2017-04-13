# -*- coding: utf-8 -*-
#
#  For sherwood forest protection check: http://www.hackzapple.com/phpBB2/viewtopic.php?t=894
#
"""Usage: python dumpf.py [options] file

Options:
  -h, --help              show this help
  -v, --version           show version

  -d, --dump=             dump file in hexa every 'n' bytes
                          (default value set to 16)
  -o, --org=              set origin address (default: 0)
  -s, --show=             Show all info (0:all, 1:hex, 2:text) - default: 0
  -x, --export=file       Export the result to a file


Examples:
  python dumpf.py <file>
  python dumpf.py -d16 <file>
  python dumpf.py --dump=16 <file>
  python dumpf.py --o8192 <file>
  python dumpf.py --org=8129 <file>

  Special for Sherwood Forest ;)
  python dumpf.py --org=40677 --export=PIC.INDEX#050000.DMP PIC.INDEX#050000
"""
import sys
import os
import getopt

# To convert bin to ascii/hexa
import binascii

__author__ = 'nico_djurovic'

__VERSION = 0.22
__SEP = "  "
__ALL = 1


#############################
# Print usage of the program
def usage():
    # Will print what is written in the beginning of this file between """
    print(__doc__)


#############################
# Return filesize of file
def getfilesize(filename):
    return os.stat(filename).st_size


#############################
# Convert byte to hexadecimal
def byte2hex(data):
    # Given raw bytes, get an ASCII string representing the hex values
    hex_data = binascii.hexlify(data)

    # The resulting value will be an ASCII string but it will be a bytes type
    # It may be necessary to decode it to a regular string
    return hex_data.decode('utf-8')


#############################
# Convert byte to ascii
def byte2ascii(data):
    result = ""
    for x in data:
        if x in range(32, 128):  # Check from ascii code $20 to $7E
            result += chr(x)
        elif x in range(160, 255):  # if between $A0 to $FE
            result += chr(x - 128)  # Substract $80 to go back between $20 to $7E
        else:
            result += '.'

    return result


#############################
# Convert bytes to integer
def byte2int(data):
    return int.from_bytes(data, byteorder='little', signed=False)


#############################
#  Split a line at a fixed size
def linewrap(data, size):
    return [data[index:index + size] for index in range(0, len(data), size)]


#############################
# Insert a separator in the hexa line
# Original is 80AAA28080A0
# returned: 80 AA A2 80 80 A0
def insertseparator(string, sep=" "):
    return sep.join(odd + even for odd, even in zip(string[::2], string[1::2])).rstrip()


#############################
# Dump function
def dump(filename, **kwargs):
    _org = False
    _export = False

    if not filename:
        usage()
        sys.exit()

    if not os.path.exists(filename):
        print('Cannot access \'{}\': No such file or directory !!!'.format(filename))
        sys.exit(3)

    with open(filename, 'rb') as file_to_dump:
        data_read = file_to_dump.read()
        file_to_dump.close()

    for key, value in kwargs.items():
        if key == 'nb_byte':
            if value:
                _bytes = value
        if key == 'org':
            if value:
                _org_address = value
                _org = True
        if key == 'export':
            if value:
                _export_file = value
                _export = True

    # Generate the hexa line
    # and wrap every n bytes
    data_hex = linewrap(
        byte2hex(
            data_read
        ).upper(), int(_bytes) * 2
    )

    # Generate one line of text
    data_txt = linewrap(
        byte2ascii(
            data_read
        ), int(_bytes)
    )

    # Start an index to display the text line
    index = 0

    # To show address of each line
    if _org is True:
        origin = int(_org_address)

    if _export is True:
        print('Saving file "{}"'.format(_export_file))
        f = open(_export_file, 'w')

    # Loop for each line
    for each_line in data_hex:
        chaine = ''

        # If we want to show the address, show it
        if _org is True:
            chaine += '{org:>04X}: '.format(org=origin)
            origin += int(_bytes)
        # Left aligned with a width calculated and multiplied by 3 because of
        # the space between each byte and minus 1 for the last space
        chaine += '{0:<{width}}'.format(insertseparator(each_line), width=(int(_bytes) * 3) - 1)
        # Then add the seperate string and the text
        chaine += '{sep}{data}'.format(data=data_txt[index], sep=__SEP)

        # If we export, wrote inside the file
        if _export is True:
            f.write(chaine + '\n')
        else:
            print(chaine)
        index += 1

    # and close the file
    if _export is True:
        f.close()


#############################
# That's the main program
#############################
def main(argv):
    _org = 0
    # default value of bytes per line
    _bytes = 8 * 2
    # What to show
    _show = __ALL
    # Default filename to export
    _export_file = ''

    # Get arguments
    try:
        opts, args = getopt.getopt(argv, "hd:o:s:vx:", ["help", "dump=", "org=", "show=", "version", "export="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    # Chaeck each argument
    for opt, arg in opts:
        if opt == "-v":
            print("Dumpf version {}".format(__VERSION))
            sys.exit()
        elif opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-o", "--org"):
            _org = arg
        elif opt in ("-s", "--show"):
            _show = arg
        elif opt in ("-x", "--export"):
            _export_file = arg
        elif opt in ("-v", "--version"):
            print("Dumpf version {}".format(__VERSION))
            sys.exit()
        elif opt in ("-d", "--dump"):
            _bytes = arg
        else:
            assert False, "unhandled option"

    # Get real string, not a list (args = filename)
    dump("".join(args), nb_byte=_bytes, org=_org, show=_show, export=_export_file)


# If __name__ = "__main__", the file called is the current executed file
if __name__ == "__main__":
    main(sys.argv[1:])
