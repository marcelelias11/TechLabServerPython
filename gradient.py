import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, diff, lambdify

# Gradient Descent Implementation

def gradient_descent(func, params, data, alpha=0.01, epochs=1000):
    """
    Performs gradient descent on a given sympy function.
    
    Parameters:
    - func: The sympy function to minimize.
    - params: A list of sympy symbols representing parameters.
    - data: Tuple of (x, y) numpy arrays representing the dataset.
    - alpha: Learning rate.
    - epochs: Number of iterations.
    
    Returns:
    - updated_params: A list of optimized parameter values.
    """
    x_vals, y_vals = data
    m = len(x_vals)  # Number of data points
    
    # Convert function and gradients to callable functions
    
    gradients = [diff(func, param) for param in params]
    func_lambdified = lambdify(params + [x], func)
    grad_lambdified = [lambdify(params + [x], grad) for grad in gradients]
    
    # Initialize parameters randomly
    param_values = np.random.rand(len(params))
    
    # Gradient descent loop
    for epoch in range(epochs):
        # Accumulate gradients for the entire dataset
        grad_accum = np.zeros(len(params))
        for xi, yi in zip(x_vals, y_vals):
            residual = func_lambdified(*param_values, xi) - yi
            grad_accum += np.array([grad(*param_values, xi) * residual for grad in grad_lambdified])
        
        grad_accum /= m  # Average gradient
        param_values -= alpha * grad_accum  # Update parameters
    
    return param_values

# Example: Fitting a quadratic function
x = symbols('x')
a, b, c = symbols('a b c')  # Parameters
func = a * x**2 + b * x + c  # Quadratic function

# Generate synthetic dataset
np.random.seed(0)
x_data = np.linspace(-10, 10, 100)
y_data = 3 * x_data**2 - 2 * x_data + 5 + np.random.normal(0, 20, size=x_data.shape)

# Perform gradient descent
data = (x_data, y_data)
optimized_params = gradient_descent(func, [a, b, c], data, alpha=0.0001, epochs=1000)

# Regression function with optimized parameters
a_opt, b_opt, c_opt = optimized_params
regression_func = lambdify(x, func.subs({a: a_opt, b: b_opt, c: c_opt}))

# Plot the dataset and the regression curve
plt.scatter(x_data, y_data, label="Data", color="blue", alpha=0.5)
x_fit = np.linspace(min(x_data), max(x_data), 500)
y_fit = regression_func(x_fit)
plt.plot(x_fit, y_fit, label="Fitted Curve", color="red")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Gradient Descent Regression")
plt.legend()
plt.grid(True)
plt.show()
