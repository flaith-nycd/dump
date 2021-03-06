# Dump a file in Python3

## Version 0.22

```
Usage: python dumpf.py [options] file

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

  --Special for Sherwood Forest ;)
  python dumpf.py --org=40677 --export=PIC.INDEX#059EE5.DMP PIC.INDEX#050000
```

![Screenshot](https://github.com/flaith-nycd/dump/blob/master/screen_shot.png)

## TODO

- [x] use the org option
- [ ] use the show option
- [x] export (save) file
- [ ] save it as a binary, or special text files for other languages (ex: .h)
- [x] dump with choice of total of bytes
- [ ] extract part of a file, from address to address (using [from:to] ?)
