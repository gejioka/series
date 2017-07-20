# Open file with series info for reading.
target = open ( 'kala', 'r' )
# Read all file.
data = [x.strip('\n') for x in target.readlines ( )]
# Close file.
target.close ( )
# Try to find serie with same id and update it.
count=0
replace_string='ska'
print data
for serie in data:
	if serie == replace_string:
		print 'im hereeeeee'
		data[count] = 'kala'
	count += 1
data_str = "\n".join(data)
# Check if serie is the first serie.
if len ( data ) == 0:
	data.append ( 'first' )

# Open a file for writing.
with  open ( 'kala', 'w' ) as target:
	# Write updated serie to file.
	target.write(data_str)
