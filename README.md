# TDA-code
This code is to create a Vietoris-Rips complex to compute persistent homology and use the mapper algorithm.
There are 3 scripts. This is an outline of the structure of how the scripts behave together. Please open them and read the comments for more detail on exactly what they are doing. 

1. main_TDA.py is where the data is imported, checked, and the other scripts are called. You change parameters in this script, for example, max_dimension (for the maximum dimension of a simplex), max_edge_length, and the names of the output files. You will need to adjust the name of the output file every time you run the code, or it will over-write the existing output_file.png. 
2. construct_complex.py should not need any editing, unless you want to change the way the complex is constructed. As of right now, Jan 16, 2025, it is a Vietoris-Rips complex. Seperate functions exist to construct the complex, compute persistence barcodes, and compute the persistence graph.
3. construct_mapper.py you will need to change the output name "output.html" again, if you do not, the existing output.html will get over-written. Other than that, you can tinker with epsilon, number of components, etc all within the mapper script. 
