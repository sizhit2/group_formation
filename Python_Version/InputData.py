import json
class InvalidInputException(Exception):
    pass

class InputData(object):
    required_params = ['data_filename', 'num_students', 'num_projects', 'max_students_per_proj']
    def __init__(self, data_dict):
        for p in InputData.required_params:
            if p not in data_dict:
                raise InvalidInputException("Not all relevant parameters provided to algorithm.")
        self.__dict__ = data_dict

    @staticmethod
    def get_data_from_json_string(json_string):
        data_dict = json.loads(json_string)
        in_data = InputData(data_dict)
        return in_data

    @staticmethod
    def get_data_from_json_file(json_filepath):
        f = open(json_filepath, 'r+')
        data_dict = json.load(f)
        in_data = InputData(data_dict)
        return in_data

def main():
    json_string = "{ \"data_filename\":\"../data/StudentPreferenceSpring2019_PredetTeamRemoved.csv\", \"num_students\":100, \"num_projects\":27,\"max_students_per_proj\":5,\"population_size\":500,\"crossover_prob\":0.95,\"mutation_prob\":0.1,\"n_keep\":2,\"n_cross\":2,\"reassign\":1,\"max_iter\":1000,\"cost_tol\":0.000001,\"gamma\":1.0,\"gamma_gpa\":0.125}"
    obj = InputData.get_data_from_json_string(json_string)
    print (obj.__dict__)
    obj = InputData.get_data_from_json_file('inputData.json')
    print (obj.__dict__)


if __name__ == '__main__':
    main()
