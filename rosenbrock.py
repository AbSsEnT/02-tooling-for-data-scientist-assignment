import numpy as np
import streamlit as st
import plotly.graph_objects as go

# Add widgets to set hyperparameters.
st.title("Rosenbrock function optimization")
st.text("In this demo project we demonstrate the weight trace during Rosenbrock function optimization using the \n"
        "Gradient Descent algorithm. You are free to set the learning rate and the number of optimization steps.")
learning_rate = st.number_input("Learning rate", min_value=1e-4, max_value=1.0, step=1e-4, format="%.4f")
step_size = st.selectbox("Step size", [1, 10, 100, 1000, 10000])
optimization_steps = st.slider("Optimization step", min_value=1, max_value=10000, step=step_size, format="%.0d")

# Define and plot Rosenbrock function contours.
ROSENBROCK_PARAMS = {"a": 1, "b": 100}


@st.cache_data
def rosenbrock_foo(x, y):
    return (x - ROSENBROCK_PARAMS["a"]) ** 2 + ROSENBROCK_PARAMS["b"] * (x ** 2 - y) ** 2


x = np.linspace(-2, 2, 100)
y = np.linspace(-1, 3, 100)
z = rosenbrock_foo(*np.meshgrid(x, y))
fig = go.Figure(data=go.Contour(x=x, y=y, z=z))

global_minima = (ROSENBROCK_PARAMS["a"], ROSENBROCK_PARAMS["a"] ** 2)
fig.add_trace(go.Scatter(x=[global_minima[0]], y=[global_minima[1]],
                         marker=dict(symbol="x", size=12, color='red', line=dict(width=1))))


# Calculate and plot Rosenbrock's function optimization path.
def d_foo_w1(w1, w2): return 2 * w1 - 2 + 400 * w1 * (w1 ** 2 - w2)
def d_foo_w2(w1, w2): return -200 * (w1 ** 2 - w2)


@st.cache_data
def gradient_descent(initial_approx, lr, optim_steps):
    if not isinstance(initial_approx, np.ndarray):
        initial_approx = np.array(initial_approx)

    args = initial_approx
    history = [args]

    for _ in range(optim_steps):
        updates = list()

        for derivative_function in [d_foo_w1, d_foo_w2]:
            updates.append(lr * derivative_function(*args))

        args = args - np.array(updates)
        history.append(args)

    return np.array(history)


start_point = (-1, 1)
optimization_path = gradient_descent(start_point, learning_rate, optimization_steps)
fig.add_trace(go.Scatter(x=optimization_path[:, 0], y=optimization_path[:, 1], mode='lines'))
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)
