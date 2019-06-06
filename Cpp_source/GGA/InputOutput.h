#ifndef INPUT_OUTPUT_H

#include "StringFunctions.h"

//void ReadDataFromExcelSpreadsheet (struct MyStudent *Student, arma::mat& StudentPreferenceMatrix);


//===============================================================================================================================//
void ReadDataFromExcelSpreadsheet (int NumberOfProjects, struct MyStudent *Student, arma::mat& StudentPreferenceMatrix, std::string filename)
{

	// File with student information
	std::cout<<"Start reading input file...\n";
	//std::ifstream fileroster("StudentPreference.csv");
	std::ifstream fileroster(filename);
	std::string   stringline;
	std::string   cell;

	if (fileroster.is_open()) {
		std::getline (fileroster, stringline);
		int i = 0;
		while ( std::getline(fileroster,stringline) ) {
			std::stringstream MylineStream(stringline);
			std::getline(MylineStream,cell,','); 				// last name
			//std::cout<<cell.c_str()<<"\n";
			std::strcpy(Student[i].LastName ,cell.c_str());
			std::getline(MylineStream,cell,',');				// first name
			//std::cout<<cell.c_str()<<"\n";
			std::strcpy(Student[i].FirstName ,cell.c_str());
			//std::getline(MylineStream,cell,',');				// uin
			//Student[i].uin = std::stoi(cell);
			//std::getline(MylineStream,cell,',');				// email
			//std::getline(MylineStream,cell,','); 				// major
			std::getline(MylineStream,cell,',');				// gpa
			Student[i].GPA = std::stod(cell);
			std::getline(MylineStream,cell,',');				// SelectedPartner
			Student[i].SelectedPartner = std::stoi(cell);
			//std::getline(MylineStream,cell,','); 				// standing
			for (int j=0;j<NumberOfProjects;j++) {
				std::getline(MylineStream,cell,',');
				//std::cout<<"i = "<<i<<" j = "<<j<<"preference "<<std::stod(cell)<<"\n";
				StudentPreferenceMatrix(i,j) = std::stod(cell);
			}
			if (Student[i].SelectedPartner == 1){
				std::getline(MylineStream,cell,','); 				// last name
				std::strcpy(Student[i].PartnerLastName ,cell.c_str());
				std::getline(MylineStream,cell,',');				// first name
				std::strcpy(Student[i].PartnerFirstName ,cell.c_str());
				std::getline(MylineStream,cell,',');				// gpa
				Student[i].PartnerGPA = std::stod(cell);
			}

		i++;
		}
	}
	std::cout<<"Finished reading input file...\n";

	fileroster.close();

}

//===============================================================================================================================//
void PrintFinalResults(struct MyStudent *Student, int NumberOfStudents, int NumberOfProjects,
						struct Individual BestChromosome, arma::mat StudentPreferenceMatrix, std::ofstream &fileout, std::ofstream &fileout2)
{
	double studenthappiness;


	fileout<<"FirstName,LastName,GPA,SelectedParter?,SelectedProject,Student Satisfaction";
	for (int g=0;g<NumberOfProjects; g++) fileout<<",Project["<<g<<"]";
	fileout<<"\n";
	for (int s=0;s<NumberOfStudents; s++) {
		fileout<<Student[s].FirstName<<","<<Student[s].LastName<<","<<Student[s].GPA<<","<<Student[s].SelectedPartner<<","<<BestChromosome.chrom[s]<<",";
		studenthappiness = 0.0;
		for (int g=0;g<NumberOfProjects; g++) {
			studenthappiness = studenthappiness + StudentPreferenceMatrix(s,g)*BestChromosome.DesignVariableMatrix(s,g);
		}
		fileout<<studenthappiness<<",";
		for (int g=0;g<NumberOfProjects; g++) {
			fileout<<StudentPreferenceMatrix(s,g)<<",";
		}
		fileout<<"\n";
	}


	// Creating table with final groups and their "satisfaction" level
	double groupfitness;

	for (int s=0;s<NumberOfStudents; s++) {
		strcat(Student[s].FirstName, " ");
		strcat(Student[s].FirstName, Student[s].LastName);
		if (Student[s].SelectedPartner == 1){
			strcat(Student[s].PartnerFirstName, " ");
			strcat(Student[s].PartnerFirstName, Student[s].PartnerLastName);
		}
	}

	fileout2<<"Project, GPAaverage, Group Satisfaction, Student names\n";
	for (int g=0;g<NumberOfProjects; g++) {
		fileout2<<g<<","<<BestChromosome.AverageGPAPerProject(g)<<",";
		groupfitness = 0;
		for (int s=0;s<NumberOfStudents; s++) {
			groupfitness = groupfitness + StudentPreferenceMatrix(s,g)*BestChromosome.DesignVariableMatrix(s,g);
		}
		fileout2<<groupfitness<<",";
		for (int s=0;s<NumberOfStudents; s++) {
			if (BestChromosome.DesignVariableMatrix(s,g) == 1) {
				fileout2<<Student[s].FirstName<<",";
				if (Student[s].SelectedPartner == 1) fileout2<<Student[s].PartnerFirstName<<",";
			}
		}
		fileout2<<"\n";
	}



}

//===============================================================================================================================//
void EvaluatePercentStudentAllocatedinPreferredProject(int NumberOfStudents, int NumberOfProjects,
						struct Individual BestChromosome, arma::mat StudentPreferenceMatrix,
						arma::uvec &CountPreference, int MinimumNumberSelectedProjects , std::ofstream &fout2 )
{
	arma::uvec PreferenceOrder = arma::zeros<arma::uvec>(NumberOfProjects);
	arma::uvec Option = arma::zeros<arma::uvec>(MinimumNumberSelectedProjects);
	int temp1, temp2;
	bool found;

	CountPreference = arma::zeros<arma::uvec>(MinimumNumberSelectedProjects+1);

	for (int i=0;i<NumberOfStudents;i++) {

		found =  false;

		PreferenceOrder = stable_sort_index(arma::trans(StudentPreferenceMatrix.row(i)),"descend");

		Option(0) = 0;
		for (int j=1;j<MinimumNumberSelectedProjects;j++) {

			temp1 = PreferenceOrder(j);
			temp2 = PreferenceOrder(j-1);

			if (StudentPreferenceMatrix(i,temp1) == StudentPreferenceMatrix(i,temp2)) {
				Option(j) = Option(j-1);
			}
			else Option(j) = Option(j-1) + 1;
		}

		for (int j=0;j<MinimumNumberSelectedProjects;j++) {

			if (PreferenceOrder(j) == BestChromosome.chrom(i) ) {
				CountPreference(Option(j)) =  CountPreference(Option(j))  + 1;
				found = true;
				break;
			}

		}

		if (found == false) {
			CountPreference(MinimumNumberSelectedProjects) = CountPreference(MinimumNumberSelectedProjects) + 1;
		}

	}
	for (int j=0;j<=MinimumNumberSelectedProjects;j++) fout2<<100*CountPreference(j)/NumberOfStudents<<",";
	fout2<<"\n";

}

//===============================================================================================================================//
void PrintHistoryInfo (int iteration, int PopulationSize, int NumberOfStudents, int N_cross, struct Individual *OldPopulation, std::ofstream &fout)
{
	fout<<" ================================================================================ \n";
	fout<<"Iteration # "<<iteration<<"\n";
	//fout<<"chrom#    chrom representation     fitness "<<"\n";
	fout<<" ================================================================================ \n";
	for (int i=0; i<PopulationSize; i++){
		fout<<i<<"|";
		for (int j=0; j<NumberOfStudents; j++){
			fout<<OldPopulation[i].chrom(j)<<" ";
		}
		fout<<"|"<<OldPopulation[i].costfunctionvalue<<"|"<<OldPopulation[i].fitness<<"|";
		fout<<"("<<OldPopulation[i].parent(0)<<","<<OldPopulation[i].parent(1)<<")|(";
		for (int j=0; j<N_cross; j++){
			fout<<OldPopulation[i].SelectedProjectToSwap(j)<<",";
		}
		fout<<")\n";
	}
	//fout<<"\n";

}
//===============================================================================================================================//
void ReadInputData(std::string & filename, int & NumberOfStudents, int & NumberOfProjects, int & MinimumNumberSelectedProjects,
				   int & MaximumNumberStudentsPerProject, int&  PopulationSize, int & N_Keep, int & N_cross,
				   double & MutationProbability, double & CrossoverProbability, int & Max_Iteration,
				   double & tol, double & gamma, double & gamma_gpa, double& reassign)
{
/*************************************************************************/
/*             Get data info from input file                             */
/*************************************************************************/
	std::ifstream finp("input_Data.txt");
	std::string   keyword;
	size_t   found;
	if (finp.is_open()) {

		while(!finp.eof()) {

			getline(finp, keyword);
			trim1(keyword);

			found=keyword.find("##");
			if (found!=std::string::npos)  continue;

			if (keyword == "#Filename")  {
				finp >> filename;
				continue;
			}
			else if (keyword == "#NumberOfStudents")  {
				finp >> NumberOfStudents;
				continue;
			}
			else if (keyword == "#NumberOfProjects")  {
				finp >> NumberOfProjects;
				continue;
			}
			else if (keyword == "#MinimumNumberSelectedProjects")  {
				finp >> MinimumNumberSelectedProjects;
				continue;
			}
			else if (keyword == "#MaximumNumberStudentsPerProject")  {
				finp >> MaximumNumberStudentsPerProject;
				continue;
			}
			else if (keyword == "#PopulationSize")  {
				finp >> PopulationSize;
				continue;
			}
			else if (keyword == "#CrossoverProbability")  {
				finp >> CrossoverProbability;
				continue;
			}
			else if (keyword == "#MutationProbability")  {
				finp >> MutationProbability;
				continue;
			}
			else if (keyword == "#N_Keep")  {
				finp >> N_Keep;
				continue;
			}
			else if (keyword == "#N_cross")  {
				finp >> N_cross;
				continue;
			}
			else if (keyword == "#reassign")  {
				finp >> reassign;
				continue;
			}
			else if (keyword == "#Max_Iteration")  {
				finp >> Max_Iteration;
				continue;
			}
			else if (keyword == "#costtol")  {
				finp >> tol;
				continue;
			}
			else if (keyword == "#gamma")  {
				finp >> gamma;
				continue;
			}
			else if (keyword == "#gamma_gpa")  {
				finp >> gamma_gpa;
				continue;
			}

		}

	} else {
		std::cout<<"Cannot open Input_Data.txt. Abort"<<std::endl;
		exit(-1);
	}

	finp.close();

}

#endif
