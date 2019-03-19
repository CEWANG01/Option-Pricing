### Least-Square-Monte-Carlo-Option-Pricing

We consider using the Least Square Monte Carlo (LSMC) method to evaluate American-stype exotic options.

The uploaded file lsmc_american.py demostrates the Valuation of American put options with variance reduction.

Valuation of more complexed options, such as Israeli options and so on, are coming up.

### Output

Running lsmc_american.py produces six pairs of numbers:

1. The price estimate and its standard deviation, while the regression model is y~x + x^2

2. The price estimate and its standard deviation, while the regression model is y~first 2 laguerre polynomial

3. The price estimate and its standard deviation, while the regression model is y~first 2 lagendre polynomial

4. The price estimate and its standard deviation, while the regression model is y~first 2 laguerre polynomial, with
   the corresponding call option price as the control variate.
   
5. The price estimate and its standard deviation, while the regression model is y~first 2 laguerre polynomial, with
   the corresponding European put option price as the control variate.
   
6. The price estimate and its standard deviation, while the regression model is y~first 2 laguerre polynomial, with
   an antithetic variate.
   
The regressors in 1 and 3 are wrong choices. 1 and 3 are demonstrations that they are not producing correct estimates.

###Usage

At the beginning of the code, set up option parameters. Input the prices of corresponding call and european put options,

as control variates.

Example:

>>> r=0.03

>>> sigma=0.4

>>> s0=50

>>> k=40

>>> call=13.98

>>> european_put=2.79
   
Do

>>> LSMC(2)

to get an estimate of the price, and its standard deviation.

Don't change the argument to other numbers.

Do

>>> LSMC_CV(2,1,call)

to get an estimate of the price, and its standard deviation, with the corresponding call option price as a control variate

Do

>>> LSMC_CV(2,2,european_put)

to get an estimate of the price, and its standard deviation, with the corresponding european put option price as a control variate

Do

>>> LSMC_antithetic(2)

to get an estimate of the price, and its standard deviation, with an antithetic variate.
