#!/usr/bin/python
#
# The MIT License (MIT)
# 
# Copyright (c) 2015 Johan Kanflo
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 

import sys, array

# Convert a hex file to binary
def hex2bin(in_file, out_file):
  done = 0
  cur = 0
  have_token = 0
  while not done:
    a = in_file.read(1)
    if a == '':
      done = 1 # EOF
    else:
      if a == '\r' or a == '\n' or a == ' ':
        if have_token:
            have_token = 0
            out_file.write(chr(cur))
            cur = 0
      else:
        have_token = 1
        cur = cur * 16 + int(a, 16)
  
  if have_token:
    out_file.write(chr(cur))

# Convert a binary file to a hex file
def bin2hex(in_file, out_file):
  done = 0
  cur = 0
  line_len = 0
  max_line_len = 16
  while not done:
    a = in_file.read(1)
    if a == '':
      done = 1 # EOF
    else:
      out_file.write("%02x " % ord(a))
      line_len = line_len + 1
      if line_len == max_line_len:
        out_file.write("\n")
        line_len = 0

# Convert a binary file to a C file
def bin2c(in_file, out_file):
  done = 0
  cur = 0
  line_len = 0
  cur_line = array.array('c')
  num_bytes = 0
  max_line_len = 10
  
  if len(sys.argv) == 5:
    var_name = sys.argv[4]
  else:
    var_name = "BIN_DATA"

  out_file.write("uint8_t %s[] = {\n  " % var_name)
  b = in_file.read(1)
  while not done:
    # We need a 1 byte look ahead to ne able to determine if
    # the current byte should be followed by a comma sign.
    a = b
    if a == '':
      done = 1 # EOF
    else:
      if ord(a) > 31 and ord(a) < 127:
        cur_line.append(a)
      else:
        cur_line.append(".")
      out_file.write("0x%02x" % ord(a))
      line_len = line_len + 1
      num_bytes = num_bytes + 1
    b = in_file.read(1)
    if b == '':
      done = 1 # EOF
    else:
      out_file.write(", ")
      if line_len == max_line_len:
        out_file.write(" // \"" + cur_line.tostring() + "\"")
        out_file.write("\n  ")
        line_len = 0
        cur_line = array.array('c')
  
  for i in range(line_len, max_line_len):
    out_file.write("      ")
    
  if len(cur_line) > 0:
    out_file.write("   // \"" + cur_line.tostring() + "\"\n")
  out_file.write("};\n")
  out_file.write("\n")
  out_file.write("#define %s_LENGTH" % var_name.upper())
  out_file.write(" (%d)\n" % num_bytes )


# Main
def usage():
  print "Usage: hexbin.py INFILE OUTFILE MODE"
  print " hexbin.py converts data from INFILE and writes to OUTFILE."
  print " Data can be converted between binary and hex."
  print ""
  print " If you replace INFILE or OUTFILE with - (a dash), stdin/stdout will be used."
  print " Note that you cannot pipe binary data through stdin."
  print ""
  print " MODE can be one of the following:"
  print "  hex2bin    Read a hex file and print the binary representations of each byte."
  print "  bin2hex    Read a binary file and print the hex representing each byte."
  print "  bin2c      Read a binary file convert it to a C uint8_t array."
  print ""
  print " A binary file is a file consisting of binary data. The ascii character # would be."
  print " represented as one byte 35 (0x23) in the file."
  print ""
  print " A hex file is a file consisting of the hex representation of binary data. The"
  print " character # would be representated as the ascii characters '2' and '3' followed"
  print " by a space."
  print ""
  print " Examples:"
  print ""
  print "   % echo Hello | hexbin.py - - bin2hex"
  print "   48 65 6c 6c 6f 0a"
  print ""
  print "   % echo 48 65 6c 6c 6f 0a | hexbin.py - - hex2bin"
  print "   Hello"
  print ""
  print "   % echo Hello | hexbin.py - - bin2c test_string"
  print "   uint8_t test_string[] = {"
  print "     0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x0a                                   // \"Hello.\""
  print "   };"
  print "   #define TEST_STRING_LENGTH (14)"
  print ""

# Main
def main():
  if len(sys.argv) < 2:
    usage()
  else:
    if sys.argv[1] == "-":
      in_file = sys.stdin
    else:
      try:
        in_file  = open(sys.argv[1], "rb")
      except:
        sys.stdout.write("Could not open %s.\n" % sys.argv[1])
        sys.exit(0)

    if sys.argv[2] == "-":
      out_file = sys.stdout
    else:
      try:
        out_file = open(sys.argv[2], "wb")
      except:
        sys.stdout.write("Could not open %s for writing.\n" % sys.argv[2])
        sys.exit(0)

    if sys.argv[3] == "hex2bin":
      hex2bin(in_file, out_file)
    elif sys.argv[3] == "bin2hex":
      bin2hex(in_file, out_file)
    elif sys.argv[3] == "bin2c":
      bin2c(in_file, out_file)
    else:
      usage()

    if in_file and in_file != sys.stdin:
      in_file.close()
    if out_file and out_file != sys.stdout:
      out_file.close()
    sys.exit(1)


if __name__ == "__main__":
  main()
