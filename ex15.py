# imports argv from sys module
from sys import argv

# unpacks it into script and filename
script, filename = argv

# open a file and assign it to txt
txt = open(filename)

# prints the name of the file (filename)
print "Here's your file %r:" % filename
# prints the stuff in the filename
print txt.read()

txt.close()

# asks for the filename again
print "Type the filename again:"
file_again = raw_input("> ")

# opens that file
txt_again = open(file_again)

# spits out what's inside the file
print txt_again.read()

txt_again.close()
