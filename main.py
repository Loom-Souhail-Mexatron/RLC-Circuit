import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
import ctypes

# Load the C library
clib = ctypes.windll.msvcrt

#Functions once called from libraries but now aren't
def tabulate(data, headers):
    # Find the maximum length of the headers and data elements
    max_lengths = [len(str(header)) for header in headers]
    for row in data:
        for i, element in enumerate(row):
            max_lengths[i] = max(max_lengths[i], len(str(element)))
    
    # Construct the format string
    format_str = ' | '.join(['{:<' + str(length) + '}' for length in max_lengths])
    
    # Print the headers
    print(format_str.format(*headers))
    print('-' * (sum(max_lengths) + 3 * len(headers) - 1))
    
    # Print the data
    for row in data:
        print(format_str.format(*row))

def sqrt(num) -> float:
    return num**0.5

def linspace(start, stop, num) -> list:
    step = (stop - start) / (num - 1)
    return [start + step * i for i in range(num)]

def sgn(num) -> int:
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0

def set_ctypes_function(func_name):
    func = getattr(clib, func_name)
    func.argtypes = [ctypes.c_double]
    func.restype = ctypes.c_double
    return func

def exp(num):
    return set_ctypes_function("exp")(num)

def sin(num):
    return set_ctypes_function("sin")(num)

def cos(num):
    return set_ctypes_function("cos")(num)

def arctan(num):
    return set_ctypes_function("atan")(num)

    

#Input variables
try:
    V_0 = float(input("Enter voltage at the capacitor (10V): "))
    C   = float(input("Enter capacitance (1F): "))
    Q_0 = V_0 * C
    R   = float(input("Enter resistance (0.1Ohm): "))
    L   = float(input("Enter inductance (1H): "))
except:
    print('Invalid input, assuming the following parameters:')
    C = 1
    Q_0 = 10
    R = 0.1
    L = 1

t_RC = R*C
t_RL = R/L
tau = t_RC*t_RL - 4
w_0 = 1/sqrt(L*C)
w02 = (1/(L*C))**2
Cw  = 1/(C*w_0)
Lw  = L*w_0

currType = ["Underdamped", "Critically Damped", "Overdamped"][int(sgn(tau)+1)]

data = [["Q_0","Charge: ",Q_0,"C"],["C","Capacitance: ",C,"F"],
        ["R","Resistance: ",R,"Ohm"],["L","Inductance: ",L,"H"],
        ["w_0","Resonant Frequency: ",w_0,"rad/s"],
        ["X_C","Capacitive Reactance: ", Cw,"Ohm"],
        ["X_L","Inductive Reactance", Lw,"Ohm"],
        ["Phi","Phase shift",arctan((Lw-Cw)/R),"rad"],
        ["Q","Quality Factor",sqrt(L/C)/R,""],
        ["","Transient Response: ",currType,""]]


print(tabulate(data,headers=["","Name","Value","Unit"]))

def RLC_Works(t:float,isCurrent=False) -> float:
    if tau < 0:
        a = -R*w02
        b = (w02)*sqrt(-C*tau)
        if isCurrent:
            return -a*Q_0*exp(a*t)*sin(b*t)*((a/b)+(b/a))
        else:
            return Q_0*exp(a*t)*(cos(b*t)-(a/b)*sin(b*t))
    if tau == 0:
        r_0 = -R*w02
        if isCurrent:
            return -Q_0*r_0*r_0*exp(r_0*t)
        else:
            return Q_0*(1-t*r_0)*exp(r_0*t)
    if tau > 0:
        r_1 = w02*(-R+sqrt(C*tau))
        r_2 = w02*(-R-sqrt(C*tau))
        if isCurrent:
            return Q_0*((r_2/(r_2-r_1))*(r_1*exp(r_1*t)-r_2*exp(r_2*t))+r_2*exp(r_2*t))
        else:
            return Q_0*((r_2/(r_2-r_1))*(exp(r_1*t)-exp(r_2*t))+exp(r_2*t))


time = linspace(0,40/w_0,1000)

plt.figure()
plt.title("Charge Plot")
plt.plot(time,[RLC_Works(t,False) for t in time])
plt.xlabel('Time [s]')
plt.gca().xaxis.set_major_formatter(EngFormatter(unit='s'))
plt.ylabel("Charge [C]")
plt.gca().yaxis.set_major_formatter(EngFormatter(unit='C'))
plt.grid()
plt.figure()
plt.title("Current Plot")
plt.plot(time,[RLC_Works(t,True) for t in time])
plt.xlabel('Time [s]')
plt.gca().xaxis.set_major_formatter(EngFormatter(unit='s'))
plt.ylabel("Current [A]")
plt.gca().yaxis.set_major_formatter(EngFormatter(unit='A'))
plt.grid()
plt.show()
