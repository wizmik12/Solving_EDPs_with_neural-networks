import autograd.numpy as np
from autograd import grad 
import autograd.numpy.random as npr

from matplotlib import pyplot as plt


#Right hand side of the equation
def f(x, psy, r = 1, P = 10):
    return psy * r * (1 - psy / P)

#Analytic solution
def psy_analytic(x, N0, r = 1, t0 = 0, P = 10):
    return (N0 * P) / (N0 + (P - N0) * np.exp(- r * (x-t0)))


#Parameters
N0 = 3
P = 10
r = 1
t0 = 0
t = 4

#Discretization of the space
nx = 70
dx = t / nx
x_space = np.linspace(t0, t, nx)    
y_space = psy_analytic(x_space, N0, r, t0)

#Analytic solution
plt.figure()
plt.plot(x_space, y_space) 
plt.show()



def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_grad(x):
    return sigmoid(x) * (1 - sigmoid(x))


def neural_network(W, x):
    a1 = sigmoid(np.dot(x, W[0]))
    return np.dot(a1, W[1])


def d_neural_network_dx(W, x, k=1):
    return np.dot(np.multiply(W[1], W[0].T), sigmoid_grad(np.dot(x, W[0])))


#Function to compute de loss (squared error)
def loss_function(W, x, r, P, N0):
    loss_sum = 0.
    for xi in x:
        net_out = neural_network(W, xi)[0][0]
        psy_t = N0 + xi * net_out
        d_net_out = d_neural_network_dx(W, xi)[0][0]
        d_psy_t = net_out + xi * d_net_out
        func = f(xi, psy_t, r, P)       
        err_sqr = (d_psy_t - func)**2

        loss_sum += err_sqr
    return loss_sum

W = [npr.randn(1, nx), npr.randn(nx, 1)] #Random initialization of the weights
lmb = 0.001 #Learning rate


for i in range(1000):
    print(i)
    loss_grad =  grad(loss_function)(W, x_space, r, P, N0)
    
    W[0] = W[0] - lmb * loss_grad[0]
    W[1] = W[1] - lmb * loss_grad[1]

    print (loss_function(W, x_space, r, P, N0))
    res = [N0 + xi * neural_network(W, xi)[0][0] for xi in x_space] 
    plt.figure()
    plt.plot(x_space, y_space) 
    plt.plot(x_space, res)
    plt.show()


#Finite difference solution
psy_fd = np.zeros_like(y_space)
psy_fd[0] = 3. # IC

for i in range(1, len(x_space)):
    psy_fd[i] = psy_fd[i-1] + (psy_fd[i-1] * r * (1 - psy_fd[i-1] / P)) * dx

#Comparison between solutions
plt.figure()
plt.plot(x_space, y_space) 
plt.plot(x_space, res)
plt.plot(x_space, psy_fd)
plt.show()

