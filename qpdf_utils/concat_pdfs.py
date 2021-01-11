import os

PDF_FOLDER_PATH = '/Users/sidhshar/bigdocs/Boson_ExamE'

# qpdf --empty --pages a1.pdf 1-z a2.pdf 1-z -- b.pdf

def run():
	out = []
	l1 = os.listdir(PDF_FOLDER_PATH)
	for i in l1:
		out.append('%s 1-z' % (i,))
	print ' '.join(out)

if __name__ == "__main__":
	run()

