/******************************************************************************/
/*                    GENETIC ALGORITH PROGRAM FOR GROUP MATCHING             */
/*                          MARIANA SILVA SOHN - SUMMER 2014                  */
/******************************************************************************/
/* This version has the feature that one student can represent another one
/* so that it is guaranteed they stay in the same group
/* Input file of version 8 is different than version 7
/******************************************************************************/
#include "stdafx.h"
#include <stdlib.h>
#include <string.h>
#include <cmath>
#include <time.h>
#include <iomanip>
#include <iostream>
#include <windows.h>

//=========================================//
// INCLUDE ARMADILLO LIBRARY DEFINITIONS
// add armadillo library in system path
// include folder "armadillo/include" in properties-C++-general
#include "armadillo"
//=========================================//
// INCLUDE MY FUNCTIONS
#include "RandomFunctions.h"
#include "StructDefs.h"
#include "InputOutput.h"
#include "Initialize.h"
#include "OptimizationFunctions.h"
#include "GeneticAlgorithmFunctions.h"
//=========================================//

using namespace std;


#define BUFFER_SIZE 300

static char help[] = "This program create Senior Design Team based on Student's Preference";

int _tmain(int argc, _TCHAR* argv[])
{
	std::string filename;						//Input file name
	int NumberOfStudents;						//Number of students taking the course
	int NumberOfProjects;						//Number of available projects
	int MaximumNumberStudentsPerProject;		//Maximum number of students per project
	int MinimumNumberSelectedProjects;			//Minimum number of projects that students should rank
	int PopulationSize;							//Number of chromosomes in the population
	int N_Keep;									//Number of chromosomes to keep in the next generation	
	int N_cross;								//Number of groups that will be swapped during crossover operation
	double MutationProbability;					//Probability of mutation 
	double CrossoverProbability;				//Probability of crossover
	int iteration;								//iteration number (generation)
	int Max_Iteration;							//maximum number of iterations
	double tol;									//Tolerance term in the cost function
	double gamma;								//Weight factor for the balanced groups term in the cost function
	double gamma_gpa;							//Weight factor for the gpa term in the cost function
	double costval;								//Cost function value for the "best" chromosome
	double maxcost;								//Maximum value for the first term of the cost function based on student's preference
	double change_costfunction;					//Relative change in the cost function for convergence check
	int    iter_check;							//Number of iterations for convergence check
	bool   converged;							//true if change_costfunction < 1e-6
	double reassign;							//0: does not reassign; 1: reassign all students; 2: reassign only when fitness improves
	double ClassAverageGPA;						//Average GPA of the entire ME 470 class
	struct MyStudent *Student;
	struct Individual *OldPopulation;
	struct Individual *NewPopulation;
	struct Individual BestChromosome;			//This is the most adapted chromosome with the optimized solution
	arma::imat AuxPopulation;
	arma::mat  StudentPreferenceMatrix;
	arma::uvec RankingPopulation; 	
	//RankingPopulation(0) = chromossome index with highest fitness value
	//RankingPopulation(1) = chromossome index with second highest fitness value ...
	arma::uvec CountPreference;

	//*************************************************************************************/  
	// For debugging purposes, the seeding is fixed
	//arma::arma_rng::set_seed(4);
	// Randomize the seeding 
	arma::arma_rng::set_seed_random() ;
	//*************************************************************************************/  

	//*************************************************************************************/  
	// Open file for output optimization results
	std::ofstream fout("optimization_history.txt");
	std::ofstream fileout("Results.csv");
	std::ofstream fileout2("FinalTeams.csv");
	std::ofstream fout2("percentual_history.csv");
	std::ofstream foutdebug("Debugging.txt");
	/*************************************************************************************/
	


	/************************************************************************************/
	/***************** Input data - read from "input_Data.txt" **************************/
	//************************************************************************************/
	 ReadInputData(filename, NumberOfStudents, NumberOfProjects, MinimumNumberSelectedProjects,
		MaximumNumberStudentsPerProject , PopulationSize, N_Keep, N_cross, MutationProbability, 
		CrossoverProbability, Max_Iteration, tol, gamma, gamma_gpa, reassign);
	//************************************************************************************/
	 
	//************************************************************************************/
	// Initializing vector and matrices sizes
	Student = CreateVectorStudentInfo(0,NumberOfStudents);
	for (int i=0; i<NumberOfStudents; i++) {
		Student[i].GPA = 0;
		Student[i].uin = 0;
		Student[i].SelectedPartner = 0;
	}
	StudentPreferenceMatrix = arma::zeros<arma::mat>(NumberOfStudents,NumberOfProjects);

	RankingPopulation = arma::zeros<arma::uvec>(PopulationSize);
	CountPreference = arma::zeros<arma::uvec>(MinimumNumberSelectedProjects);
	AuxPopulation = arma::zeros<arma::imat>(PopulationSize,NumberOfStudents+NumberOfProjects);


	OldPopulation = CreateVectorChromosomeInfo(0,PopulationSize);

	InitializePopulation (OldPopulation,PopulationSize,NumberOfStudents,NumberOfProjects,N_cross);
	NewPopulation = CreateVectorChromosomeInfo(0,PopulationSize);
	InitializePopulation (NewPopulation,PopulationSize,NumberOfStudents,NumberOfProjects,N_cross);
	//*************************************************************************************/



	std::cout<<"Before reading Excel Input Data\n";
	//*************************************************************************************/  
	// Read data from excel file (ugradrecs)
	ReadDataFromExcelSpreadsheet (NumberOfProjects, Student, StudentPreferenceMatrix, filename);
	// Get the maximum value of the cost function - evaluated when students get their first preference
	arma::colvec temp = arma::max(StudentPreferenceMatrix,1);
	maxcost = arma::sum(temp);
	std::cout<<"Maximum Cost Function = "<<maxcost<<"\n";
	// Get average GPA for the class
	ClassAverageGPA = GetClassAverageGPA (NumberOfStudents, Student);
	std::cout<<"Class GPA Average = "<<ClassAverageGPA<<"\n";
	//std::cout<<StudentPreferenceMatrix<<"\n";
	////*************************************************************************************/

	//*************************************************************************************/
	///***************************** Optimization loop ************************************/
	//*************************************************************************************/
	iteration = 0;
	iter_check = 0;
	change_costfunction = 10;
	converged = false;
	 do {

	//	//-----------------------------
	//	// Build design variable matrix
	//	//-----------------------------	
		DesignVariableMatrix (OldPopulation,PopulationSize,NumberOfStudents,NumberOfProjects);
	
		//-----------------------------------------------------------------------------------------------------------
		// Move students from overly crowded projects to other less populated projects based on student's preferences
		//-----------------------------------------------------------------------------------------------------------
		RepairDesignVariableForInfeasibility(OldPopulation, PopulationSize, NumberOfStudents, NumberOfProjects, Student, MaximumNumberStudentsPerProject,StudentPreferenceMatrix);

		//---------------------
		// Evaluate function 
		//---------------------
		costval = CostFunction (StudentPreferenceMatrix, OldPopulation, BestChromosome, Student, PopulationSize, NumberOfStudents, NumberOfProjects, gamma_gpa, gamma, tol,
								RankingPopulation, maxcost, change_costfunction, MaximumNumberStudentsPerProject, ClassAverageGPA, reassign, iteration, foutdebug);
		//--------------------
		// Print output files
		//--------------------
		PrintHistoryInfo (iteration, PopulationSize, NumberOfStudents, N_cross, OldPopulation,fout);
		EvaluatePercentStudentAllocatedinPreferredProject(NumberOfStudents, NumberOfProjects, BestChromosome, StudentPreferenceMatrix, CountPreference, MinimumNumberSelectedProjects, fout2);
		std::cout<<"Iteration = "<<iteration<<" - Cost function = "<<costval<<" - Change = "<<change_costfunction<<std::endl;
		//--------------------
		// Check convergence
		//--------------------
		if (change_costfunction < 1e-6) {
			if (converged == false) {
				iter_check = 0;
				converged = true;}
			else iter_check ++;
		}
		else converged = false;
		if (iter_check > 10 && converged == true && reassign == -1) reassign = 1;
		if (iter_check > 30 && converged == true) break;
		//--------------------
		// ga operations
		//--------------------		
		CrossoverWithRandomOffspringGeneration (NewPopulation, OldPopulation, RankingPopulation, PopulationSize, NumberOfStudents, NumberOfProjects, N_Keep, N_cross, CrossoverProbability);
		
		Mutation (NewPopulation,PopulationSize, NumberOfStudents, MutationProbability, N_Keep);
		
		UpdatePopulation (NewPopulation, OldPopulation, PopulationSize, NumberOfStudents);
		
		iteration ++;

	} while (iteration < Max_Iteration);
	//*************************************************************************************/

	
	PrintFinalResults( Student, NumberOfStudents, NumberOfProjects, BestChromosome, StudentPreferenceMatrix, fileout, fileout2);

	std::cout<<BestChromosome.AverageGPAPerProject<<std::endl;
	
	system("pause");

	fout.close();
	fout2.close();
	fileout.close();
	fileout2.close();
	
	return 0;

}
