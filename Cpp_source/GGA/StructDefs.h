using namespace std;


struct MyStudent *CreateVectorStudentInfo(int li, int lf);
struct Individual *CreateVectorChromosomeInfo(int li, int lf);

//===================================================================================//
// Defining structure to store student information
//===================================================================================//
struct MyStudent {
	int uin;		
	double GPA;
	int SelectedPartner;
	char LastName[40]; 
	char FirstName[40];
	char PartnerLastName[40]; 
	char PartnerFirstName[40];
	double PartnerGPA;
	//std::string LastName; 
	//std::string FirstName;
};
//===================================================================================//
struct MyStudent *CreateVectorStudentInfo(int li, int lf)
{
	struct MyStudent *v;
    v=(struct MyStudent *) malloc((unsigned)(lf-li+2)*sizeof(struct MyStudent));
    if(!v) printf("allocation failure 1 in svector()\n");
	return v;
}
//===================================================================================//
struct Individual
{
    arma::ivec chrom;                   /* chromosome string for the individual */
    double     fitness;                 /* fitness of the individual  - associatated to cost function */
	double     costfunctionvalue;       /* cost function to be maximized */
	//double     adaptpercent;          /* how adapt the individual is comparing to the rest of the population - ranking */
    arma::ivec SelectedProjectToSwap;   /* projects transferred from father to offspring */
    arma::ivec parent;                  /* parents of the offspring */
	arma::imat DesignVariableMatrix;    // associated with the StudentPreference matrix 
	arma::vec  AverageGPAPerProject;    
	arma::ivec NumberOfStudentPerProject;
};
//===================================================================================//
struct Individual *CreateVectorChromosomeInfo(int li, int lf)
{
	struct Individual *v;
    v=(struct Individual *) malloc((unsigned)(lf-li+2)*sizeof(struct Individual));
    if(!v) printf("allocation failure 1 in svector()\n");
	return v;
}