#ifndef OPTIMIZATION_FUNCTIONS_H


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
		std::cout<<"Design Variable Matrix for chromosome: "<<i<<"\n";
		std::cout<<Population[i].DesignVariableMatrix<<std::endl;
	}
}
//***************************************************************************************************************************************//
void RepairDesignVariableForInfeasibility(struct Individual *Population,  int PopulationSize, int NumberOfStudents, int NumberOfProjects,
										   int MaximumNumberStudentsPerProject, const arma::mat &StudentPreferenceMatrix)
{
	std::cout<<"Student Preferences\n";
	std::cout<<StudentPreferenceMatrix<<std::endl;

	int randomstudent;
	int index;
	arma::vec  TempStudPref(NumberOfProjects);
	arma::uvec indices(NumberOfProjects);
	arma::vec  NumberOfStudentPerProject(NumberOfProjects);
	bool       found_another_project;

	for (int i=0; i<PopulationSize; i++) {

		// For each individual, determine the number of students per each project
		std::cout<<"--- Chromosome "<<i<<":\n";
		for (int g = 0; g<NumberOfProjects;g ++) {
			NumberOfStudentPerProject(g) = 0.0;
			for  (int s=0;s<NumberOfStudents;s++) {
				NumberOfStudentPerProject(g)  = NumberOfStudentPerProject(g)  + Population[i].DesignVariableMatrix(s,g);
			}
			std::cout<<"Group "<<g<<" has "<<NumberOfStudentPerProject(g) <<" students"<<std::endl;
		}
		
		for (int g = 0; g<NumberOfProjects;g ++) {
			// Ckeck to see if a project exceeds the maximum number of students
			if ( NumberOfStudentPerProject(g) > MaximumNumberStudentsPerProject) {
				// Selects a student to take out of the project
				for (int j=0; j<NumberOfStudents;j++) {
					if (Population[i].DesignVariableMatrix(j,g) == 1)  {
						randomstudent = j;
						break;
					}
				}
				std::cout<<"Selected student is: "<<randomstudent<<"\n";
				TempStudPref = arma::trans(StudentPreferenceMatrix.row(randomstudent));
				// Rank this student's project preference
				indices = sort_index(TempStudPref,"descend");
				// Try to assign the student in his most preferred group; needs to check for space
				for (int k = 0; k< NumberOfProjects; k++) {
					index = indices(k);  // try to place student in group "index"
					if (NumberOfStudentPerProject(k) < MaximumNumberStudentsPerProject) {
						Population[i].DesignVariableMatrix(randomstudent,g) = 0; //student is no longer placed in that project
						Population[i].DesignVariableMatrix(randomstudent,index) = 0; //student is placed in new project
						Population[i].chrom(randomstudent) = index; //update chromosome
						NumberOfStudentPerProject(g) = NumberOfStudentPerProject(g) - 1;
						NumberOfStudentPerProject(index) = NumberOfStudentPerProject(index) + 1;
					}
				}

			}
		}


	}

}


void CostFunction (const arma::mat& StudentPreferenceMatrix, struct Individual *Population, int PopulationSize, int NumberOfStudents, int NumberOfProjects)
{

	double fval;
	double sumfval = 0.0;

	for (int i=0; i<PopulationSize; i++) {
		fval = 0.0;
		for (int s=0; s<NumberOfStudents; s++) {
			for (int g=0; g<NumberOfProjects;g++) {
				fval = fval + StudentPreferenceMatrix(s,g)*Population[i].DesignVariableMatrix(s,g);
			}
		}
		Population[i].fitness = fval;
		sumfval = sumfval + fval;
	}

	for (int i=0; i<PopulationSize; i++) {
		Population[i].adaptpercent = Population[i].fitness/sumfval;
	}

}
#endif