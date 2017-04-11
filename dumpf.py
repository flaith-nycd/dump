"""Usage: python dumpf.py [options] file

Options:
  -h, --help              show this help
  -d n, --dump=n          dump file in hexa every 'n' bytes
                          (default value set to 16)
  -v, --version.          show version

Examples:
  python dumpf.py exe_file.exe
  python dumpf.py -d16 exe_file.exe
  python dumpf.py --dump=16 exe_file.exe
"""
import sys
import os
import getopt  # https://docs.python.org/3.6/library/getopt.html

# To convert bin to ascii/hexa
import binascii

_version = 0.17


def usage():
    # Will print what is written in the beginning of this file between """
    print(__doc__)


def getfilesize(filename):
    return os.stat(filename).st_size


def byte2hex(data):
    # Given raw bytes, get an ASCII string representing the hex values
    hex_data = binascii.hexlify(data)

    # The resulting value will be an ASCII string but it will be a bytes type
    # It may be necessary to decode it to a regular string
    return hex_data.decode('utf-8')


def byte2ascii(data):
    result = ""
    for x in data:
        if x < 32:  # or x > 127:
            result += '.'
        else:
            result += chr(x)
    return result


def byte2int(data):
    return int.from_bytes(data, byteorder='little', signed=False)


# Split a line at a fixed size
def linewrap(data, size):
    return [data[index:index + size] for index in range(0, len(data), size)]


# Insert a separator in the hexa line
# Original is 80AAA28080A0
# returned: 80 AA A2 80 80 A0
def insertseparator(string, sep=" "):
    return sep.join(odd + even for odd, even in zip(string[::2], string[1::2])).rstrip()


def dump(filename, option):
    if not filename:
        usage()
        sys.exit()

    if not os.path.exists(filename):
        print('Cannot access \'{}\': No such file or directory !!!'.format(filename))
        sys.exit(3)

    with open(filename, 'rb') as file_to_dump:
        data_read = file_to_dump.read()
        file_to_dump.close()

    # Generate the hexa line
    # and wrap every n bytes
    data_hex = linewrap(
        byte2hex(
            data_read
        ).upper(), int(option) * 2
    )

    # Generate one line of text
    data_txt = linewrap(
        byte2ascii(
            data_read
        ), int(option)
    )

    # Start an index to display the text line
    index = 0

    # Print our result
    for each_line in data_hex:
        # left aligned with a width calculated (option is the number of bytes)
        # and multiply by 3 because of the space between each byte and minus 1 for the last space
        print("{:<{width}}|{}".format(insertseparator(each_line), data_txt[index], width=(int(option) * 3) - 1))
        index += 1


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hd:v", ["help", "dump=", "version"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    dump_option = 16  # default value of bytes per line

    for opt, arg in opts:
        if opt == "-v":
            print("Dumpf version {}".format(_version))
            sys.exit()
        elif opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-v", "--version"):
            print("Dumpf version {}".format(_version))
            sys.exit()
        elif opt in ("-d", "--dump"):
            dump_option = arg
        else:
            assert False, "unhandled option"

    # Get real string, not a list (args = filename)
    dump("".join(args), dump_option)


if __name__ == "__main__":
    main(sys.argv[1:])
