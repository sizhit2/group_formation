#ifndef STRING_H
#define STRING_H

#include <stdlib.h>
#include <stdio.h>
#include <string>
using std::string;

void trim1(string& str)
{
	string::size_type pos=str.find_last_not_of(' ');
	if (pos != string::npos) {
		str.erase(pos+1);
		pos = str.find_first_not_of(' ');
		if (pos != string::npos) str.erase(0,pos);
	}
	else str.erase(str.begin(),str.end());
}

#endif
