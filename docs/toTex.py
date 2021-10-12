import os
import docutils.core

if not os.path.isdir("tex"):
    os.makedirs("tex/")

for file in os.listdir():
    if file[-4:] == ".rst":
        print(file)
        docutils.core.publish_file(source_path=file,destination_path= "tex/" + file[:-4] + ".tex", writer_name="latex")