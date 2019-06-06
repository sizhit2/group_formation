gga : gga.o random_functions.o struct_defs.o input_output.o initialize.o optimization.o ga_functions.o
		clang++ -std=c++11 gga.o random_functions.o struct_defs.o input_output.o initialize.o optimization.o ga_functions.o

gga.o : GGA.cpp
		clang++ -c GGA.cpp

random_functions.o : RandomFunctions.h
		clang++ -c RandomFunctions.h

input_output.o : InputOutput.h
		clang++ -c InputOutput.h

initialize.o : Initialize.h
		clang++ -c Initialize.h

optimization.o : OptimizationFunctions.h
		clang++ -c OptimizationFunctions.h

ga_functions.o : GeneticAlgorithmFunctions.h
		clang++ -c GeneticAlgorithmFunctions.h

struct_defs.o : StructDefs.h
		clang++ -c StructDefs.h
