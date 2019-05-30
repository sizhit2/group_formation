#ifndef OPTIMIZATION_FUNCTIONS_H

using namespace std;

void DesignVariableMatrix (struct Individual *Population,  int PopulationSize, int NumberOfStudents, int NumberOfProjects);
void GetNumberOfStudentsPerProject(int chromosome, int NumberOfProjects, int NumberOfStudents, struct MyStudent *Student,
							struct Individual *Population);
void RepairDesignVariableForInfeasibility(struct Individual *Population,  int PopulationSize, int NumberOfStudents, int NumberOfProjects, struct MyStudent *Student,
							int MaximumNumberStudentsPerProject, const arma::mat &StudentPreferenceMatrix);
void EvaluateFitness (int i, const arma::mat& StudentPreferenceMatrix, struct Individual *Population, struct MyStudent *Student, 
					  int PopulationSize, int NumberOfStudents, int NumberOfProjects, double gamma_gpa, double gamma, double tol, 
					  double maxcost , double ClassAverageGPA,  arma::vec& FitnessVector);
double CostFunction (const arma::mat& StudentPreferenceMatrix, struct Individual *Population, struct Individual &BestChromosome, 
					 struct MyStudent *Student, int PopulationSize, int NumberOfStudents, int NumberOfProjects,
				     double gamma_gpa, double gamma, double tol, arma::uvec& RankingPopulation, double maxcost , double& change_costfunction,
					 int MaximumNumberStudentsPerProject, double ClassAverageGPA, double reassign,  int iteration, std::ofstream & foutdebug );
void ReassignStudent (double reassign, int iteration, struct Individual *Population, 
				arma::uvec RankingPopulation, const arma::mat& StudentPreferenceMatrix,
				int PopulationSize, int NumberOfStudents, int NumberOfProjects,  arma::vec& FitnessVector, 
				struct MyStudent *Student, double gamma_gpa, double gamma, double tol, double maxcost , double ClassAverageGPA,
				int MaximumNumberStudentsPerProject, std::ofstream & foutdebug);
double GetClassAverageGPA (int NumberOfStudents, struct MyStudent *Student);
//***************************************************************************************************************************************//
void DesignVariableMatrix (struct Individual *Population,  int PopulationSize, int NumberOfStudents, int NumberOfProjects)
{
	for (int i=0; i<PopulationSize; i++) {
		for (int s=0; s<NumberOfStudents; s++) {
			for (int g=0; g<NumberOfProjects;g++) {
				if (Population[i].chrom(s) == g) {
					Population[i].DesignVariableMatrix(s,g) = 1;
				}
				else {
					Population[i].DesignVariableMatrix(s,g) = 0;
				}
			}
		}
		//std::cout<<"Design Variable Matrix for chromosome: "<<i<<"\n";
		//std::cout<<Population[i].DesignVariableMatrix<<std::endl;
	}
}


//***************************************************************************************************************************************//
void GetNumberOfStudentsPerProject(int chromosome, int NumberOfProjects, int NumberOfStudents, struct MyStudent *Student,
								struct Individual *Population)
{
		// =============================================================================================================
		// For each individual, determine the number of students per each project
		// =============================================================================================================
		for (int g = 0; g<NumberOfProjects;g ++) {
			Population[chromosome].NumberOfStudentPerProject(g) = 0;
			for  (int s=0;s<NumberOfStudents;s++) {
				if (Population[chromosome].DesignVariableMatrix(s,g) != 0) {
					if (Student[s].SelectedPartner == 1) Population[chromosome].NumberOfStudentPerProject(g)  = Population[chromosome].NumberOfStudentPerProject(g)  + 2;
					if (Student[s].SelectedPartner == 0) Population[chromosome].NumberOfStudentPerProject(g)  = Population[chromosome].NumberOfStudentPerProject(g)  + 1;
				}			
			}
		}
		// =============================================================================================================
}

//***************************************************************************************************************************************//
void RepairDesignVariableForInfeasibility(struct Individual *Population,  int PopulationSize, int NumberOfStudents, int NumberOfProjects, struct MyStudent *Student,
										   int MaximumNumberStudentsPerProject, const arma::mat &StudentPreferenceMatrix)
{
	arma::vec  TempStudPref(NumberOfProjects);
	arma::uvec pref_index(NumberOfProjects);
	int assigned_project;
	int tentative_project;
	int crowded_project;
	bool found = false;
	int  i;
	int add;
	
	for (i=0; i<PopulationSize; i++) {

		// Obtain the number of students per each project for chromosome "i"
		GetNumberOfStudentsPerProject(i,NumberOfProjects, NumberOfStudents, Student, Population);	

		// Ckeck to see if a project exceeds the maximum number of students 
		for (int g = 0; g<NumberOfProjects;g ++) {

			if (Population[i].NumberOfStudentPerProject(g) <= MaximumNumberStudentsPerProject) continue; // loop the the next project "g"
	
			crowded_project = g;
			
			// Selects a student to take out of the crowded project
			for (int j=0; j<NumberOfStudents;j++) {		

				assigned_project = Population[i].chrom(j);

				add = 1;
				if (Student[j].SelectedPartner == 1) add = 2;	

				if (assigned_project == crowded_project) { 
				// ======================================================================================================
				// Try to assign the student "j" in his most preferred group; needs to check for space
				// ======================================================================================================				
					pref_index = sort_index(arma::trans(StudentPreferenceMatrix.row(j)),"descend");

					for (int k=0;k<NumberOfProjects;k++){		
						tentative_project = pref_index(k);
						//if (NumberOfStudentPerProject(tentative_project) < MaximumNumberStudentsPerProject && StudentPreferenceMatrix(j,tentative_project) > 0) {
						if (Population[i].NumberOfStudentPerProject(tentative_project) < MaximumNumberStudentsPerProject) {
							Population[i].chrom(j) = tentative_project;
							Population[i].DesignVariableMatrix(j,assigned_project) = 0; //student is no longer placed in that project	
							Population[i].DesignVariableMatrix(j,tentative_project) = 1; //student is placed in new project
							Population[i].NumberOfStudentPerProject(tentative_project) = Population[i].NumberOfStudentPerProject(tentative_project) + add;
							Population[i].NumberOfStudentPerProject(assigned_project) = Population[i].NumberOfStudentPerProject(assigned_project) - add;
							break;
						}
					}
				// ======================================================================================================
				} /* Completed "if" statement */

				if (Population[i].NumberOfStudentPerProject(crowded_project) <= MaximumNumberStudentsPerProject) break; // leave "for" loop

			} /* finish for "j" loop */

			if (Population[i].NumberOfStudentPerProject(crowded_project) > MaximumNumberStudentsPerProject) {
				//std::cout<<"WARNING: Project "<<g<<" is infeasible with "<<Population[i].NumberOfStudentPerProject(g)<<" students\n";
			} 
			
		} /* Finished checking infeseability in all groups for chromosome "i" */

	} 

}

//***************************************************************************************************************************************//
void EvaluateFitness (int i, const arma::mat& StudentPreferenceMatrix, struct Individual *Population, struct MyStudent *Student, 
					  int PopulationSize, int NumberOfStudents, int NumberOfProjects, double gamma_gpa, double gamma, double tol, 
					  double maxcost , double ClassAverageGPA, arma::vec& FitnessVector)
{
	double fval;
	double sigma = 0.0;
	double sigma_gpa = 0.0;
	double AverageSizeGroup;
	double pairGPA;
	arma::ivec FictitiousNumberOfStudentsPerProject;

	FictitiousNumberOfStudentsPerProject = arma::zeros<arma::ivec>(NumberOfProjects);

	AverageSizeGroup = 5.0;// (double) NumberOfStudents/NumberOfProjects;

	//for (int i=0; i<PopulationSize; i++) {

		// Cost function associated with student preference
		fval = 0.0;
		for (int s=0; s<NumberOfStudents; s++) {			
			for (int g=0; g<NumberOfProjects;g++) {
				fval = fval + StudentPreferenceMatrix(s,g)*Population[i].DesignVariableMatrix(s,g);
			}
		}
		fval = fval/maxcost; //Normalizes the cost function 

		//std::cout<<"AverageSizeGroup = "<<AverageSizeGroup<<"\n";

		// Cost function associated with balanced distribution of students per project
		if (gamma != 0) {
			sigma = 0.0;
			for (int g=0; g<NumberOfProjects;g++) {	
				//sigma = sigma + std::pow((Population[i].NumberOfStudentPerProject(g) - AverageSizeGroup), 2.0);
				sigma = sigma + std::pow((Population[i].NumberOfStudentPerProject(g) - AverageSizeGroup)/AverageSizeGroup, 2.0);
				//sigma = sigma + std::pow(((NumberOfStudentPerProject(g)/AverageSizeGroup)-1.0), 2.0)/(NumberOfProjects-1.0); // This is a differentiable function
				//sigma = sigma + fabs(((NumberOfStudentPerProject(g)/AverageSizeGroup)-1.0)/(NumberOfProjects-1.0)); // This is a non-differentiable function
				//sigma = sigma + exp(-pow(NumberOfStudentPerProject(g)-AverageSizeGroup,2.0)/4); // This is a differentiable function

			}
			sigma = sigma / NumberOfProjects;
		}

		// Cost function associated with balanced distribution of average gpa
		Population[i].AverageGPAPerProject = arma::zeros<arma::vec>(NumberOfProjects);
		for (int s=0; s<NumberOfStudents; s++) {
			pairGPA = Student[s].GPA;
			if (Student[s].SelectedPartner == 1) pairGPA = (Student[s].GPA + Student[s].PartnerGPA)/2.0;
			for (int g=0; g<NumberOfProjects;g++) {
				FictitiousNumberOfStudentsPerProject(g) = FictitiousNumberOfStudentsPerProject(g) + Population[i].DesignVariableMatrix(s,g);
				Population[i].AverageGPAPerProject(g) = Population[i].AverageGPAPerProject(g) + pairGPA*Population[i].DesignVariableMatrix(s,g);
			}	
		}
		sigma_gpa = 0.0;	
		for (int g=0; g<NumberOfProjects;g++) {	
			if (FictitiousNumberOfStudentsPerProject(g) != 0) {
				Population[i].AverageGPAPerProject(g) = Population[i].AverageGPAPerProject(g)/FictitiousNumberOfStudentsPerProject(g);
				sigma_gpa = sigma_gpa + std::pow((Population[i].AverageGPAPerProject(g) - ClassAverageGPA), 2.0);
				//sigma_gpa = sigma_gpa + exp(-pow(Population[i].AverageGPAPerProject(g) - ClassAverageGPA,2.0)/4);				
			}
		}
		sigma_gpa = sigma_gpa / NumberOfProjects;

		// Combined cost function
		//FitnessVector(i) = fval + gamma*fabs(1.0 - sigma/tol) + gamma_gpa*fabs(1.0-sigma_gpa/tol);
		//FitnessVector(i) = fval + gamma*(1 - sigma/tol) + gamma_gpa*(1-sigma_gpa/tol);
		//FitnessVector(i) = fval + gamma*(1.0 - sigma) + gamma_gpa*(1.0-sigma_gpa); // To be used with pow function
		//FitnessVector(i) = fval + gamma*(sigma) + gamma_gpa*(sigma_gpa); // To be used with exp function

		FitnessVector(i) = fval;
		if (sigma > 0) FitnessVector(i)  = FitnessVector(i) + gamma*(1.0-sigma);
		//if (sigma > 0) FitnessVector(i)  = FitnessVector(i) + gamma/(sigma);
		//if (sigma_gpa > 0) FitnessVector(i)  = FitnessVector(i) + gamma_gpa/(sigma_gpa);
		if (sigma_gpa > 0) FitnessVector(i)  = FitnessVector(i) + gamma_gpa*(1.0-sigma_gpa);

		// Updating Population record
		Population[i].costfunctionvalue = FitnessVector(i);

	//}
}

//***************************************************************************************************************************************//
double CostFunction (const arma::mat& StudentPreferenceMatrix, struct Individual *Population, struct Individual &BestChromosome, 
					 struct MyStudent *Student, int PopulationSize, int NumberOfStudents, int NumberOfProjects,
				     double gamma_gpa, double gamma, double tol, arma::uvec& RankingPopulation, double maxcost , double& change_costfunction,
					 int MaximumNumberStudentsPerProject, double ClassAverageGPA, double reassign,  int iteration, std::ofstream & foutdebug )
{
	double fitness_sum = 0.0;
	/**********************************************************************************************/
	// Evaluate fitness of each individual of the population
	/**********************************************************************************************/
	arma::vec  FitnessVector(PopulationSize);
	for (int i=0; i<PopulationSize; i++) {
		EvaluateFitness (i,StudentPreferenceMatrix, Population, Student, PopulationSize,NumberOfStudents, NumberOfProjects, gamma_gpa, gamma, tol, maxcost,ClassAverageGPA, FitnessVector);
	}
	/**********************************************************************************************/
	// Finding the ranking of each individual
	/**********************************************************************************************/
	RankingPopulation = stable_sort_index(FitnessVector,"descend");
	fitness_sum = arma::sum(FitnessVector);
	for (int i=0; i<PopulationSize; i++) {
		Population[i].fitness =  FitnessVector(i)/fitness_sum;
	}
	//std::cout<<arma::trans(FitnessVector)<<"\n";
	//std::cout<<arma::trans(RankingPopulation)<<"\n";	
	//**********************************************************************************************/
	// Reassign students that were place in undesired options and recalculate their ranking
	//**********************************************************************************************/
	if (reassign > 0) {
		ReassignStudent (reassign, iteration, Population, RankingPopulation, StudentPreferenceMatrix, PopulationSize, NumberOfStudents, NumberOfProjects, 
					FitnessVector, Student, gamma_gpa, gamma, tol, maxcost , ClassAverageGPA, MaximumNumberStudentsPerProject, foutdebug);
		RankingPopulation = stable_sort_index(FitnessVector,"descend");
		fitness_sum = arma::sum(FitnessVector);
		for (int i=0; i<PopulationSize; i++) {
			Population[i].fitness =  FitnessVector(i)/fitness_sum;
		}
	}
	/**********************************************************************************************/
	//Saving the best chromosome
	/**********************************************************************************************/	
	int best = RankingPopulation(0);
	// Evaluating the relative change of the cost function for convergence check
	change_costfunction = std::abs((BestChromosome.costfunctionvalue - FitnessVector(best))/FitnessVector(best));
	// Updating Best Chromosome record
	BestChromosome.costfunctionvalue = FitnessVector(best);
	BestChromosome.fitness = Population[best].fitness;
	BestChromosome.AverageGPAPerProject = Population[best].AverageGPAPerProject;
	BestChromosome.DesignVariableMatrix = Population[best].DesignVariableMatrix;
	BestChromosome.chrom = Population[best].chrom;
	/**********************************************************************************************/

	return (FitnessVector(best));
}

//===============================================================================================================================//
void ReassignStudent (double reassign, int iteration, struct Individual *Population, 
				arma::uvec RankingPopulation, const arma::mat& StudentPreferenceMatrix,
				int PopulationSize, int NumberOfStudents, int NumberOfProjects,  arma::vec& FitnessVector, 
				struct MyStudent *Student, double gamma_gpa, double gamma, double tol, double maxcost , double ClassAverageGPA,
				int MaximumNumberStudentsPerProject, std::ofstream & foutdebug)

{
	int chromosome;
	int assigned_project, tentative_project;
	bool found;
	arma::uvec pref_index(NumberOfProjects); 
	double oldfitness;
	double flip;
	bool   ReassignThisStudent;
	int add;


	foutdebug<<"===========================================================\n";
	foutdebug<<"Iteration "<<iteration<<"\n";
	foutdebug<<"===========================================================\n";

	//For the top 5% chromosomes, reassign  students that were place in undesired options and recalculate their fitness

	for (int k=0; k<0.05*PopulationSize; k++) {

		chromosome = RankingPopulation(k); // Get one individual of the population in decreasing order of fitness - highest adapted to least adapted

		for (int j=0;j<NumberOfStudents;j++) {

			assigned_project = Population[chromosome].chrom(j); // For each student, check the assigned project		
			
			found = false;

			ReassignThisStudent = true;

			add = 1;
			if (Student[j].SelectedPartner == 1) add = 2;	

			if (reassign < 1) { // reassign is done depending on probability
				flip = arma::randu(1).at(0,0);
				if (flip > reassign)  ReassignThisStudent = false;
			}

			// If assigned project was not selected by the student, try to place student in one of the selected projects in order of preference
			//==================================================================================================================================
			if (StudentPreferenceMatrix(j,assigned_project) == 0 && ReassignThisStudent == true) {  // assigned project was not selected by the student

				pref_index = sort_index(arma::trans(StudentPreferenceMatrix.row(j)),"descend");
				for (int i=0;i<NumberOfProjects;i++){		
					tentative_project = pref_index(i);
					if (Population[chromosome].NumberOfStudentPerProject(tentative_project) < MaximumNumberStudentsPerProject && StudentPreferenceMatrix(j,tentative_project) > 0) {
						Population[chromosome].chrom(j) = tentative_project;
						Population[chromosome].DesignVariableMatrix(j,assigned_project) = 0; //student is no longer placed in that project
						Population[chromosome].DesignVariableMatrix(j,tentative_project) = 1; //student is placed in new project
						Population[chromosome].NumberOfStudentPerProject(tentative_project) = Population[chromosome].NumberOfStudentPerProject(tentative_project) + add;
						Population[chromosome].NumberOfStudentPerProject(assigned_project) = Population[chromosome].NumberOfStudentPerProject(assigned_project) - add;
						found = true;
						break;
					}					
				}

				if (found) { 
					if (reassign == 2) { // Check if fitness increased when moving student "j" out of undesirable group "assigned_project"
						oldfitness = FitnessVector(chromosome);
						EvaluateFitness (chromosome,StudentPreferenceMatrix, Population, Student, PopulationSize,NumberOfStudents, NumberOfProjects, gamma_gpa, gamma, tol, maxcost, ClassAverageGPA, FitnessVector);
						if (FitnessVector(chromosome) < oldfitness) { // revert project allocation
							Population[chromosome].chrom(j) = assigned_project;
							Population[chromosome].DesignVariableMatrix(j,assigned_project) = 1; 
							Population[chromosome].DesignVariableMatrix(j,tentative_project) = 0;	
							Population[chromosome].NumberOfStudentPerProject(tentative_project) = Population[chromosome].NumberOfStudentPerProject(tentative_project) - 1;
							Population[chromosome].NumberOfStudentPerProject(assigned_project) = Population[chromosome].NumberOfStudentPerProject(assigned_project) + 1;
							foutdebug<<"DISCARDED: In chromosome "<<chromosome<<", student "<<j<<" was assigned to undesired project "<<assigned_project<<" and attempted to be reassigned to project "<<tentative_project<<" but had decrease in fitness"<<std::endl;
						}
						else {
							foutdebug<<"ACCEPTED: In chromosome "<<chromosome<<", student "<<j<<" was assigned to undesired project "<<assigned_project<<" and is now reassigned to project "<<tentative_project<<" with new fitness = "<<FitnessVector(chromosome)<<std::endl;
						}
					}
				}
				else foutdebug<<"NOT FOUND: In chromosome "<<chromosome<<", student "<<j<<" was assigned to undesired project "<<assigned_project<<" and was not able to be reassigned to any other desirable project" <<std::endl;
			}
			//==================================================================================================================================
		}

		if (found && reassign != 2) { // reassign students regardeless of the cost function
			EvaluateFitness (chromosome,StudentPreferenceMatrix, Population, Student, PopulationSize,NumberOfStudents, NumberOfProjects, gamma_gpa, gamma, tol, maxcost, ClassAverageGPA, FitnessVector);
			foutdebug<<"Some students were moved in chromosomo "<<chromosome<<" and the new fitness is "<<FitnessVector(chromosome)<<"\n";
		}


	}
}
				
//===============================================================================================================================//
double GetClassAverageGPA (int NumberOfStudents, struct MyStudent *Student)
{
	
	double meanGPA = 0.0;
	int Nstudent = 0;

	for (int s=0; s<NumberOfStudents; s++) {		
		meanGPA = meanGPA + Student[s].GPA;
		Nstudent++;
		if (Student[s].SelectedPartner == 1) {
			meanGPA = meanGPA + Student[s].PartnerGPA;
			Nstudent++;
		}
	}
	meanGPA = meanGPA/Nstudent;	

	return (meanGPA);
}

#endif

