from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter

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
w_0 = 1/np.sqrt(L*C)
w02 = (1/(L*C))**2
Cw  = 1/(C*w_0)
Lw  = L*w_0

currType = ["Underdamped", "Critically Damped", "Overdamped"][int(np.sign(tau)+1)]

data = [["Q_0","Charge: ",Q_0,"C"],["C","Capacitance: ",C,"F"],
        ["R","Resistance: ",R,"Ohm"],["L","Inductance: ",L,"H"],
        ["w_0","Resonant Frequency: ",w_0,"rad/s"],
        ["X_C","Capacitive Reactance: ", Cw,"Ohm"],
        ["X_L","Inductive Reactance", Lw,"Ohm"],
        ["Phi","Phase shift",np.arctan((Lw-Cw)/R),"rad"],
        ["Q","Quality Factor",np.sqrt(L/C)/R],
        ["Transient Response: ",currType]]

print(tabulate(data,headers=["","Name","Value","Unit"]))

def RLC_Works(t:float,isCurrent=False) -> float:
    if tau < 0:
        a = -R*w02
        b = (w02)*np.sqrt(-C*tau)
        if isCurrent:
            return -a*Q_0*np.exp(a*t)*np.sin(b*t)*((a/b)+(b/a))
        else:
            return Q_0*np.exp(a*t)*(np.cos(b*t)-(a/b)*np.sin(b*t))
    if tau == 0:
        r_0 = -R*w02
        if isCurrent:
            return -Q_0*r_0*r_0*np.exp(r_0*t)
        else:
            return Q_0*(1-t*r_0)*np.exp(r_0*t)
    if tau > 0:
        r_1 = w02*(-R+np.sqrt(C*tau))
        r_2 = w02*(-R-np.sqrt(C*tau))
        if isCurrent:
            return Q_0*((r_2/(r_2-r_1))*(r_1*np.exp(r_1*t)-r_2*np.exp(r_2*t))+r_2*np.exp(r_2*t))
        else:
            return Q_0*((r_2/(r_2-r_1))*(np.exp(r_1*t)-np.exp(r_2*t))+np.exp(r_2*t))


time = np.linspace(0,40/w_0,1000)

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
