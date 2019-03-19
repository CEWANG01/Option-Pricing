import numpy as np
from numpy.linalg import inv
import random
random.seed(9999)
import math
############################
######Stock Parameters######
############################
'''
Change option parameters here. Enter parameters before the program!
'''
r=0.03
sigma=0.4
s0=50
k=40
call=13.98         #The corresponding price of european/american call option
european_put=2.79 #The corresponding price of european put option
##################################
######Stock Price Generation######
##################################
dt=1.0/100.0#Time step
d=math.exp(-r*dt)#The discount factor of one time step
#Don't change dt! The time step is hard coded as 1/100 below.
def a_path():#Generate a stock path and antithetic path
    path=[s0]
    antipath=[s0]
    for i in range(100):
        z=random.normalvariate(0,1)
        new=path[-1]*math.exp((r-0.5*sigma*sigma)*dt+sigma*math.sqrt(dt)*z)
        new2=antipath[-1]*math.exp((r-0.5*sigma*sigma)*dt+sigma*math.sqrt(dt)*(-z))
        path.append(new)
        antipath.append(new2)
    return [path,antipath]
def paths():#Generate a lot of stock paths
    paths=[]
    antipaths=[]
    for i in range(100):
        a_pair=a_path()
        paths.append(a_pair[0])
        antipaths.append(a_pair[1])
    return [paths,antipaths]
both=paths()
path=both[0]#stock paths
antipath=both[1]#antithetic paths
#############################
######Regression Models######
#############################
'''
Different choice of regression models.
Regression 1: y~x+x^2
Regression 2: y~first 2 laguerre polynomial
Regression 3: y~first 2 lagendre polynomial
'''
def regression1(stockprice,stock_vector,future_payoff):
    x=[]#design matrix
    for item in stock_vector:
        x.append([1,item,item*item])
    part1=np.linalg.inv((np.dot(np.transpose(x),x)))
    part2=np.dot(np.transpose(x),future_payoff)
    estimate=np.dot(part1,part2)
    b0=estimate[0]
    b1=estimate[1]
    b2=estimate[2]
    return b0+stockprice*b1+stockprice*b2*b2
def laguerre1(x):
    return -x+1
def laguerre2(x):
    return 0.5*(x*x-4*x+2)
def regression2(stockprice,stock_vector,future_payoff):
    x=[]#design matrix
    for item in stock_vector:
        x.append([1,laguerre1(item),laguerre2(item)])
    part1=np.linalg.inv((np.dot(np.transpose(x),x)))
    part2=np.dot(np.transpose(x),future_payoff)
    estimate=np.dot(part1,part2)
    b0=estimate[0]
    b1=estimate[1]
    b2=estimate[2]
    return b0+b1*laguerre1(stockprice)+b2*laguerre2(stockprice)
def legendre2(x):
    return 0.5*(3*x*x-1)
def legendre3(x):
    return 0.5*(5*x*x*x-3*x)
def regression3(stockprice,stock_vector,future_payoff):
    x=[]#design matrix
    for item in stock_vector:
        x.append([1,item,legendre2(item),legendre3(item)])
    part1=np.linalg.inv((np.dot(np.transpose(x),x)))
    part2=np.dot(np.transpose(x),future_payoff)
    estimate=np.dot(part1,part2)
    b0=estimate[0]
    b1=estimate[1]
    b2=estimate[2]
    b3=estimate[3]
    return b0+b1*stockprice+b2*legendre2(item)+b3*legendre3(item)
#################################
##########The Algorithm##########
#################################
'''
A helper function: discount a cash flow.
A cash flow should have 1 or no non-zero item.
'''
def discount(cf):
    n=len(cf)
    for i in range(len(cf)):
        if cf[i]!=0:
            return cf[i]*math.exp(-r*(i+1)*dt)
    return 0

def LSMC(regression_type):
    cf=[]#cash flow matrix
    for cash_flows in range(100):
        cf.append([])
    for i in range(len(path)):
        if path[i][-1]>=k:
            cf[i].append(0)
        else:
            cf[i].append(k-path[i][-1])
    #up tp now, the cash flow at maturity is obtained.
    for j in range(0,99):#use j to track the index from the back of the cash flow matrix 
        i1=98-j#i1: index in cash flow matrix that we are working on
        i2=100-j#i2: index in path matrix on the next day
        stock_vector=[]
        future_payoff=[]
        index_list=[]#list of index that we are paying attention to
        for i in range(0,100):#over all paths
            if path[i][i2-1]<k:
                stock_vector.append(path[i][i2-1])
                future_payoff.append((path[i][i1+2])*d)
                index_list.append(i)
            else:
                cf[i].insert(0,0)
        for item in index_list:
            stockprice=path[item][i2-1]
            #conduct the regression step, depends on which model was chosen
            if regression_type==1:
                predictpayoff=regression1(stockprice,stock_vector,future_payoff)
            elif regression_type==2:
                predictpayoff=regression2(stockprice,stock_vector,future_payoff)
            else:
                predictpayoff=regression3(stockprice,stock_vector,future_payoff)
            if predictpayoff>=k-stockprice:
                cf[item].insert(0,0)
            else:
                cf[item].insert(0,k-stockprice)
                for m in range(1,len(cf[item])):
                    cf[item][m]=0
    #discount each cash flow and store them in a list
    discounts=[]
    for item in cf:
        discounts.append(discount(item))
    print(np.mean(discounts),np.std(discounts))
'''
Test the three regression models
'''
LSMC(1)
LSMC(2)
LSMC(3)
###################################
##########Control Variate##########
###################################
def LSMC_CV(regression_type,cv_type,bs_price):
#Enter the closed form price of control variate at bs_price
    cf=[]#cash flow matrix
    for cash_flows in range(100):
        cf.append([])
    for i in range(len(path)):
        if path[i][-1]>=k:
            cf[i].append(0)
        else:
            cf[i].append(k-path[i][-1])
    #up tp now, the cash flow at maturity is obtained.
    for j in range(0,99):
        i1=98-j#i1: index in cash flow matrix that we are working on
        i2=100-j#i2: index in path matrix on the next day
        stock_vector=[]
        future_payoff=[]
        index_list=[]#list of index that we are paying attention to
        for i in range(0,100):#over all paths
            if path[i][i2-1]<k:
                stock_vector.append(path[i][i2-1])
                future_payoff.append((path[i][i1+2])*d)
                index_list.append(i)
            else:
                cf[i].insert(0,0)
        for item in index_list:
            stockprice=path[item][i2-1]
            if regression_type==1:
                predictpayoff=regression1(stockprice,stock_vector,future_payoff)
            elif regression_type==2:
                predictpayoff=regression2(stockprice,stock_vector,future_payoff)
            else:
                predictpayoff=regression3(stockprice,stock_vector,future_payoff)
            if predictpayoff>=k-stockprice:
                cf[item].insert(0,0)
            else:
                cf[item].insert(0,k-stockprice)
                for m in range(1,len(cf[item])):
                    cf[item][m]=0
    discounts=[]
    for item in cf:
        discounts.append(discount(item))
    if cv_type==1:#Control is call
        cvs=[]
        for item in path:
            cvs.append(max(((item[-1]-k)*math.exp(-r)),0)-bs_price)
    elif cv_type==2:#Control is european put
        cvs=[]
        for item in path:
            cvs.append(max(((k-item[-1])*math.exp(-r)),0)-bs_price)
    #now we obtain list 'cvs' as control variates
    c=-((np.cov(discounts,cvs))/(np.var(cvs)))
    cv_estimates=[]
    for i in range(len(discounts)):
        cv_estimates.append(discounts[i]+c*cvs[i])
    print(np.mean(cv_estimates),np.std(cv_estimates))
'''
Test the two control variates
'''
LSMC_CV(2,1,call)
LSMC_CV(2,2,european_put)
######################################
##########Antithetic Variate##########
######################################
def LSMC_antithetic(regression_type):
    cf=[]#cash flow matrix
    for cash_flows in range(100):
        cf.append([])
    for i in range(len(antipath)):
        if antipath[i][-1]>=k:
            cf[i].append(0)
        else:
            cf[i].append(k-antipath[i][-1])
    #up tp now, the cash flow at maturity is obtained.
    for j in range(0,99):
        i1=98-j#i1: index in cash flow matrix that we are working on
        i2=100-j#i2: index in path matrix on the next day
        stock_vector=[]
        future_payoff=[]
        index_list=[]#list of index that we are paying attention to
        for i in range(0,100):#over all paths
            if antipath[i][i2-1]<k:
                stock_vector.append(path[i][i2-1])
                future_payoff.append((path[i][i1+2])*d)
                index_list.append(i)
            else:
                cf[i].insert(0,0)
        for item in index_list:
            stockprice=antipath[item][i2-1]
            if regression_type==1:
                predictpayoff=regression1(stockprice,stock_vector,future_payoff)
            elif regression_type==2:
                predictpayoff=regression2(stockprice,stock_vector,future_payoff)
            else:
                predictpayoff=regression3(stockprice,stock_vector,future_payoff)
            if predictpayoff>=k-stockprice:
                cf[item].insert(0,0)
            else:
                cf[item].insert(0,k-stockprice)
                for m in range(1,len(cf[item])):
                    cf[item][m]=0
    discounts2=[]
    for item in cf:
        discounts2.append(discount(item))
    cf=[]#cash flow matrix
    for cash_flows in range(100):
        cf.append([])
    for i in range(len(path)):
        if path[i][-1]>=k:
            cf[i].append(0)
        else:
            cf[i].append(k-path[i][-1])
    #up tp now, the cash flow at maturity is obtained.
    for j in range(0,99):
        i1=98-j#i1: index in cash flow matrix that we are working on
        i2=100-j#i2: index in path matrix on the next day
        stock_vector=[]
        future_payoff=[]
        index_list=[]#list of index that we are paying attention to
        for i in range(0,100):#over all paths
            if path[i][i2-1]<k:
                stock_vector.append(path[i][i2-1])
                future_payoff.append((path[i][i1+2])*d)
                index_list.append(i)
            else:
                cf[i].insert(0,0)
        for item in index_list:
            stockprice=path[item][i2-1]
            if regression_type==1:
                predictpayoff=regression1(stockprice,stock_vector,future_payoff)
            elif regression_type==2:
                predictpayoff=regression2(stockprice,stock_vector,future_payoff)
            else:
                predictpayoff=regression3(stockprice,stock_vector,future_payoff)
            if predictpayoff>=k-stockprice:
                cf[item].insert(0,0)
            else:
                cf[item].insert(0,k-stockprice)
                for m in range(1,len(cf[item])):
                    cf[item][m]=0
    discounts=[]
    for item in cf:
        discounts.append(discount(item))
    antithetic_estimates=[]
    for i in range(len(discounts)):
        antithetic_estimates.append((discounts[i]+discounts2[i])/2)
    print(np.mean(antithetic_estimates),np.std(antithetic_estimates))
LSMC_antithetic(2)


        
