/******************************************************************************/
/*            FUNÇÕES PARA GERAR NÚMEROS RANDÔMICOS                           */
/******************************************************************************/

static double oldrand[55];                      /* Array of 55 random numbers */
static int jrand;                                    /* current random number */
static double rndx2;                       /* used with random normal deviate */
static int rndcalcflag;                    /* used with random normal deviate */

void   advance_random(void);
int    flip(float);
void   randomize(float);
float  randomperc(void);
int    rnd(int , int);
float  rndreal(float , float);
void   warmup_random(float);

void advance_random()
/* Create next batch of 55 random numbers */
{
    int j1;
    double new_random;

    for(j1 = 0; j1 < 24; j1++)
    {
        new_random = oldrand[j1] - oldrand[j1+31];
        if(new_random < 0.0) new_random = new_random + 1.0;
        oldrand[j1] = new_random;
    }
    for(j1 = 24; j1 < 55; j1++)
    {
        new_random = oldrand [j1] - oldrand [j1-24];
        if(new_random < 0.0) new_random = new_random + 1.0;
        oldrand[j1] = new_random;
    }
}


int flip(float prob)
/* Flip a biased coin - true if heads */
{
    if(randomperc() <= prob)
        return(1);
    else
        return(0);
}

float randomperc()
/* Fetch a single random number between 0.0 and 1.0 - Subtractive Method */
/* See Knuth, D. (1969), v. 2 for details */
/* name changed from random() to avoid library conflicts on some machines*/
{
    jrand++;
    if(jrand >= 55)
    {
        jrand = 1;
        advance_random();
    }
    return((float) oldrand[jrand]);
}

/* Get seed number for random and start it up */
void randomize(float randomseed)
{
    int j1;

    for(j1=0; j1<=54; j1++)
      oldrand[j1] = 0.0;
    jrand=0;
    warmup_random(randomseed);
}


int rnd(int low, int high)
/* Pick a random integer between low and high */
{
    int i;
    float randomperc();

    if(low >= high)
        i = low;
    else
    {
        i = (int) (randomperc() * (high - low + 1)) + low;
        if(i > high) i = high;
    }
    return(i);
}


float rndreal(float lo ,float hi)
/* real random number between specified limits */
{
    return((randomperc() * (hi - lo)) + lo);
}


void warmup_random(float random_seed)
/* Get random off and running */
{
    int j1, ii;
    double new_random, prev_random;

    oldrand[54] = random_seed;
    new_random = 0.000000001;
    prev_random = random_seed;
    for(j1 = 1 ; j1 <= 54; j1++)
    {
        ii = (21*j1)%54;
        oldrand[ii] = new_random;
        new_random = prev_random-new_random;
        if(new_random<0.0) new_random = new_random + 1.0;
        prev_random = oldrand[ii];
    }

    advance_random();
    advance_random();
    advance_random();

    jrand = 0;
}
