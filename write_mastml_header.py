elements = ["Au","Si","Ge","Ca","Mg","Zn","Fe","B","La","Al","Cu","Ni","Co","Gd","Y","Ag","Nd","Zr","Ti","Sn","Nb","Pd","P","Be"]
header1 = "[[LeaveOneGroupOut_"
header2 = "]]\n    grouping_column = "

for e in elements:
	print(header1 + str(e) + header2 + str(e))