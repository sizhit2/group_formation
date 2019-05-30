#ifndef INITIALIZE_H

using namespace std;

void InitializePopulation (struct Individual *OldPopulation, int PopulationSize, int NumberOfStudents, int NumberOfProjects, int N_cross)
{   

	arma::vec randnumber(1);
	int value;

	for( int i = 0; i < PopulationSize; i++ ) {
		
		OldPopulation[i].chrom = arma::zeros<arma::ivec>(NumberOfStudents+NumberOfProjects);
		OldPopulation[i].DesignVariableMatrix = arma::zeros<arma::imat>(NumberOfStudents,NumberOfProjects);
		OldPopulation[i].AverageGPAPerProject = arma::zeros<arma::vec>(NumberOfProjects);
		OldPopulation[i].parent = arma::zeros<arma::ivec>(2);
		OldPopulation[i].SelectedProjectToSwap = arma::zeros<arma::ivec>(N_cross);
		OldPopulation[i].NumberOfStudentPerProject = arma::zeros<arma::ivec>(NumberOfProjects);
		for( int j = 0; j < NumberOfStudents; j++ ) {
			randnumber =  arma::randu(1) * NumberOfProjects;
			value = (int) floor(randnumber(0));
			OldPopulation[i].chrom(j) = value;
		}
		int counter = 0;
		for (int j = NumberOfStudents; j<(NumberOfStudents+NumberOfProjects); j++ ) {
			OldPopulation[i].chrom(j) = counter;
			counter ++;
		}
	}
	////---------------------------------------------------
	//std::cout<< "Initial Population of Chromosomes\n";
	//for (int i=0; i<PopulationSize; i++) {
	//	for( int j = 0; j < NumberOfStudents; j++ ) {
	//		std::cout<<OldPopulation[i].chrom(j)<<"\t";
	//	}
	//	std::cout<<"\n";
	//}
	////---------------------------------------------------
}

#endif