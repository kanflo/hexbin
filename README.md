# hexbin
Convert files, stdin from hex to binary and back.

Usage: `hexbin.py INFILE OUTFILE MODE`

hexbin.py converts data from `INFILE` and writes to `OUTFILE`.
Data can be converted between binary and hex and C character arrays can be generated.

 If you replace `INFILE` or `OUTFILE` with - (a dash), stdin/stdout will be used.

 `MODE` can be one of the following:
 
  `hex2bin`    Read a hex file and print the binary representations of each byte.
  
  `bin2hex`    Read a binary file and print the hex representing each byte.
  
  `bin2c`      Read a binary file convert it to a C uint8_t array.

A binary file is a file consisting of binary data. The ascii character # would be.
represented as one byte 35 (0x23) in the file.

A hex file is a file consisting of the hex representation of binary data. The
character # would be representated as the ascii characters '2' and '3' followed
by a space.

**Examples:**

View ascii character representation of the string "Hello":

```
% echo Hello | hexbin.py - - bin2hex
48 65 6c 6c 6f 0a
```

Convert back:

```
% echo 48 65 6c 6c 6f 0a | hexbin.py - - hex2bin
Hello
```

Convert a JPEG for inclusion in a C program:

```
% hexbin.py image.jpg - bin2c img_data
uint8_t img_data[] = {
  0xff, 0xd8, 0xff, 0xe0, 0x00, 0x10, 0x4a, 0x46, 0x49, 0x46,  // "......JFIF"
  0x00, 0x01, 0x01, 0x01, 0x00, 0x48, 0x00, 0x48, 0x00, 0x00,  // ".....H.H.."
  0xff, 0xdb, 0x00, 0x43, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01,  // "...C......"
  0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,  // ".........."
 .
 .
 .
};

#define IMG_DATA_LENGTH (12386)

```
