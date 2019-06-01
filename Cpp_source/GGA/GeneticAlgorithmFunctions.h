#ifndef GENETIC_ALGORITHM_FUNCTIONS_H

using namespace std;


int RouletteWheel (struct Individual *Population,  int PopulationSize);

//===============================================================================================================================//
void CrossoverWithRandomOffspringGeneration (struct Individual *NewPopulation, struct Individual *Population, const arma::uvec& RankingPopulation,
				int PopulationSize, int NumberOfStudents, int NumberOfProjects, int N_Keep, int N_cross, double CrossoverProbability)
{
	int father_index;
	int mother_index;
	int select_project;
	double flip;

	int i;


	for (i=0; i<N_Keep; i++) {
		NewPopulation[i].chrom = Population[RankingPopulation(0+i)].chrom;
	}
	
	do {			
		flip = arma::randu(1).at(0,0);
		if (flip < CrossoverProbability ) {
			// Two individual are selected to be the parents
			father_index = RouletteWheel (Population, PopulationSize);
			do {mother_index = RouletteWheel (Population, PopulationSize);} while (mother_index == father_index);
			NewPopulation[i].parent(0) = mother_index;
			NewPopulation[i].parent(1) = father_index;
			// Equalize the offspring to the mother
			//std::cout<<"Chromosome["<<i<<"] is equalized to mother ["<<mother_index<<"] and has father ["<<father_index<<"]\n";		
			NewPopulation[i].chrom = arma::trans(Population[mother_index].chrom);
			// Select "N_cross" projects randomly; Insert the elements of the father belonging to the two selected groups into the offspring
			for (int k=0;k<N_cross;k++){
				select_project = (int) floor(arma::randu(1).at(0,0)*NumberOfProjects);
				if (k>0 && select_project == NewPopulation[i].SelectedProjectToSwap(k-1)) continue;
				//select_project = rand() % NumberOfProjects;
				//std::cout<<"Selected project ["<<k<<"] is "<<select_project<<"\n";
				for (int s=0;s<NumberOfStudents;s++){
					if (Population[father_index].chrom(s) == select_project) {
						NewPopulation[i].chrom(s) = select_project;
					}
				}
				NewPopulation[i].SelectedProjectToSwap(k) = select_project;
			}
		}
		else { 
			//NewPopulation[i].chrom = Population[i].chrom; // if crossover does not happen, the chromosome at position "i" is transferred to next generation
			for (int s=0;s<NumberOfStudents;s++) NewPopulation[i].chrom(s) = (int) floor(arma::randu(1).at(0,0) * NumberOfProjects);
			NewPopulation[i].parent(0) = i;
			NewPopulation[i].parent(1) = i;
			NewPopulation[i].SelectedProjectToSwap = arma::zeros<arma::ivec>(N_cross);
		}
		i++;
	} while (i < PopulationSize);

}

//===============================================================================================================================//
int RouletteWheel (struct Individual *Population,  int PopulationSize)
{
	int i; 

	arma::vec randnumber(1);
	randnumber =  arma::randu(1);
	double pick = randnumber(0);

	double sum = 0.0;
    for(i = 0; (sum < pick) && (i < PopulationSize); i++) {
            sum += Population[i].fitness;
    }

	int parent = 0;
	if (i>0) parent = i-1;

	//std::cout<<"Parent = "<<parent<<"\n";

	return(parent);


}
//===============================================================================================================================//

void Mutation (struct Individual *Population, int PopulationSize, int NumberOfStudents, double MutationProbability, int N_keep)

{
	double flip;
	int student1, student2;
	int temp;

	for (int k=N_keep; k<PopulationSize; k++) {
		//flip = (double) rand()/RAND_MAX;
		flip = arma::randu(1).at(0,0);
		if (flip < MutationProbability) {
			//student1 = rand() % NumberOfStudents;
			//student2 = rand() % NumberOfStudents;
			student1 = (int) floor(arma::randu(1).at(0,0)*NumberOfStudents);
			student2 = (int) floor(arma::randu(1).at(0,0)*NumberOfStudents);
			//std::cout<<"Flip = ["<<flip<<"] - Mutation in chromosome ["<<k<<"] - exchange students "<<student1<<" and "<<student2<<"\n";
			temp = Population[k].chrom(student1);
			Population[k].chrom(student1) = Population[k].chrom(student2);
			Population[k].chrom(student2) = temp;
		}
	}
}

//===============================================================================================================================//
void UpdatePopulation (struct Individual *NewPopulation,  struct Individual *OldPopulation, int PopulationSize, int NumberOfStudents)
{
	for (int k=0; k<PopulationSize; k++) {
		for (int j=0; j<NumberOfStudents; j++) {
			OldPopulation[k].chrom(j) = NewPopulation[k].chrom(j);
		}
		OldPopulation[k].parent = NewPopulation[k].parent;
		OldPopulation[k].SelectedProjectToSwap = NewPopulation[k].SelectedProjectToSwap;
	}
}
#endif
