# RLC Circuit
A Python program that can be used to plot the charge and current plots for a series RLC circuit.

The program only needs 4 values: initial voltage at the capacitor, capacitance, inductance and resistance.

From that, it calculates the charge and current functions depending on the case (underdamped, critically damped, overdamped). The functions don't rely on any ODE solvers, they were solved manually by me, to ensure performance.

Here are the plots by default:

![image](https://user-images.githubusercontent.com/54601024/217243443-2a044337-0917-4bca-8bc4-c17be7a24236.png)
![Figure_1](https://user-images.githubusercontent.com/54601024/217237610-9190ff2a-3d72-4f3f-9604-6a853265b63b.png)
![Figure_2](https://user-images.githubusercontent.com/54601024/217237631-42ff066d-129d-4b4d-8f7b-ae10b7f3d6d8.png)
