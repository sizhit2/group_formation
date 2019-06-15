from GGA import *

def get_best_runs(num_iter=5, dir='../data/Run10_noGPAweight/'):
    ga_results = []
    best_fitness = 0
    fit_index = 0
    most_satisfied = 0
    msat_index = 0
    best_satisfaction = 0
    bsat_index = 0
    for i in range(num_iter):
        print ("\nrun #%d" % (i+1))
        result = run_ga(dir=dir)
        if len(ga_results) == 0:
            best_fitness = result[2]
            best_satisfaction = result[0]
            most_satisfied = result[1]
        else:
            if result[2] > best_fitness:
                fit_index = i
                best_fitness = result[2]
            if result[0] > best_satisfaction:
                bsat_index = i
                best_satisfaction = result[0]
            if result[1] == most_satisfied:
                if result[0] == best_satisfaction:
                    msat_index = i
                    most_satisfied = result[1]
            if result[1] > most_satisfied:
                msat_index = i
                most_satisfied = result[1]
        ga_results.append(result)

    return (ga_results[fit_index], ga_results[bsat_index], ga_results[msat_index])

def main():
    best_fit, best_sat, most_sat = get_best_runs(dir='../data/Run10_noGPAweight/')

if __name__ == '__main__':
    main()
