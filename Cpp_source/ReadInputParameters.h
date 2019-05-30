  void Read_Input_Parameters(ifstream& finp, int& finitedifference, int& Optimization, int& OptAlgorithm, 
					int& OptProblemFlag, double& ObjectivePenaltyWeight, double& p, double& q, 
					int& costfunctiontype, double& InitialGuess, 
					double& vf_min, double& SpaceNorm, double& TimeNorm, int& NumberOfIntruders, 
					double& kkttol, int& maxoutit, double& costtol, double& designtol)
{
	string keyword;
		
    try {  
		finp >> keyword >> finitedifference;  
		if (keyword.find("finitedifference") == string::npos)	{ throw "finitedifference"; }
		finp >> keyword >> Optimization;  
		if (keyword.find("Optimization") == string::npos)	{ throw "Optimization"; }
		finp >> keyword >> OptAlgorithm;  
		if (keyword.find("OptAlgorithm") == string::npos)	{ throw "OptAlgorithm"; }
		finp >> keyword >> OptProblemFlag;  
		if (keyword.find("OptProblemFlag") == string::npos)	{ throw "OptProblemFlag"; }
		finp >> keyword >> ObjectivePenaltyWeight;  
		if (keyword.find("ObjectivePenaltyWeight") == string::npos)	{ throw "ObjectivePenaltyWeight"; }		
		finp >> keyword >> p;  
		if (keyword.find("simp_p") == string::npos) 	{ throw "simp_p"; }
		finp >> keyword >> q;  
		if (keyword.find("simp_q") == string::npos) 	{ throw "simp_q"; }
		finp >> keyword >> costfunctiontype;  
		if (keyword.find("costfunctiontype") == string::npos)	{ throw "costfunctiontype"; }
		finp >> keyword >> InitialGuess;  
		if (keyword.find("InitialGuess") == string::npos) 	{ throw "InitialGuess"; }
		finp >> keyword >> vf_min; 
		if (keyword.find("Min_Volu_fraction") == string::npos) 	{ throw "Min_Volu_fraction"; }
		finp >> keyword >> SpaceNorm; 
		if (keyword.find("SpaceNorm") == string::npos) 	{ throw "SpaceNorm"; }
		finp >> keyword >> TimeNorm;  
		if (keyword.find("TimeNorm") == string::npos) 	{ throw "TimeNorm"; }
		finp >> keyword >> NumberOfIntruders;  
		if (keyword.find("NumberOfIntruders") == string::npos) 	{ throw "NumberOfIntruders"; }		
		finp >> keyword >> kkttol;  
		if (keyword.find("kkttol") == string::npos) 	{ throw "kkttol"; }	
		finp >> keyword >> maxoutit;  
		if (keyword.find("maxoutit") == string::npos) 	{ throw "maxoutit"; }	
		finp >> keyword >> costtol;  
		if (keyword.find("costtol") == string::npos) 	{ throw "costtol"; }
		finp >> keyword >> designtol;  
		if (keyword.find("designtol") == string::npos) 	{ throw "designtol"; }		
	}
	catch (char* str) {
		cout << "Error in input_Optimization.txt: keyword " << str << " is not found or is in a wrong place." << endl;
		exit(-1);
	}

}
