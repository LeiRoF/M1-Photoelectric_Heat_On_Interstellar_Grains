To generate a grain:
- open a terminal
- go to the directory that contains GenGrain.py
- type the command: 
   > time python GenGrain.py

Rq: 
- The command "time" measures the execution time of the script
- It is possible to open the file "GenGrain.py" with a text editor and to change the parameters. Do not forget to save the original script!
- The script "GRF_routines.py" must be present in the same directory than "GenGrain.py" because it is called by "GenGrain.py". It is useless (and even discouraged) to open "GRF_routines.py".
- It is possible to choose to visualize or not the grains when they are produced with the variable "doplot" in "GenGrain.py".
- The grain is written in an ASCII file named "Grain_***.txt", where the main parameters are noted.
