import matplotlib.pyplot as plt
import numpy as np
import timeit


MIN_NUMBER_OF_MATRICES = 4
MAX_NUMBER_OF_MATRICES = 240
MIN_DIMENSION = 142
MAX_DIMENSION = 1940
BASE_DIMENSION = 50
MIN_VALUE = 240
MAX_VALUE = 2400
ITER = 70
AVG_OF = 5
PLOT_INPUTS = True


def minmult(nom, m, p):
    for i in range(nom):
        m[i, i] = 0
    for diag in range(1, nom):
        for i in range(nom-diag):
            j = i+diag
            m[i, j] = m[i, i]+m[i+1, j]+d[i]*d[i+1]*d[j+1]
            p[i, j] = i+1
            for k in range(i+1, j):
                if (tmp := m[i, k]+m[k+1, j]+d[i]*d[k+1]*d[j+1]) < m[i, j]:
                    m[i, j] = tmp
                    p[i, j] = k+1

def dp_mul(i, j):
    if i == j:
        return matrices[i]
    if i+1 == j:
        return np.matmul(matrices[i], matrices[j])
    return np.matmul(dp_mul(i, p[i, j]-1), dp_mul(p[i, j], j))

def mul(i, j):
    if i == j:
        return matrices[i]
    if i+1 == j:
        return np.matmul(matrices[i], matrices[j])
    return np.matmul(mul(i, i+1), mul(i+2, j))


MAX_NUMBER_OF_MATRICES += 1
MAX_DIMENSION += 1
MAX_VALUE += 1
MAX_NUMBER_OF_MATRICES -= (MAX_NUMBER_OF_MATRICES -
                           MIN_NUMBER_OF_MATRICES) % ITER
MAX_DIMENSION -= (MAX_DIMENSION-MIN_DIMENSION) % ITER
MAX_VALUE -= (MAX_VALUE-MIN_VALUE) % ITER

if MAX_NUMBER_OF_MATRICES - MIN_NUMBER_OF_MATRICES < ITER:
    NUMBER_OF_MATRICES = [MAX_NUMBER_OF_MATRICES for _ in range(ITER)]
else:
    NUMBER_OF_MATRICES = list(range(MIN_NUMBER_OF_MATRICES, MAX_NUMBER_OF_MATRICES,
                              (MAX_NUMBER_OF_MATRICES-MIN_NUMBER_OF_MATRICES)//ITER))
if MAX_DIMENSION - MIN_DIMENSION < ITER:
    DIMENSIONS = [MAX_DIMENSION for _ in range(ITER)]
else:
    DIMENSIONS = list(range(MIN_DIMENSION, MAX_DIMENSION,
                      (MAX_DIMENSION-MIN_DIMENSION)//ITER))
if MAX_VALUE - MIN_VALUE-1 < ITER:
    VALUES = [MAX_VALUE for _ in range(ITER)]
else:
    VALUES = list(range(MIN_VALUE+1, MAX_VALUE, (MAX_VALUE-MIN_VALUE)//ITER))

if PLOT_INPUTS:
    fig = plt.figure()
    gs = fig.add_gridspec(2, 3)
    ax1 = fig.add_subplot(gs[0, :])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1])
    ax4 = fig.add_subplot(gs[1, 2])
    ax1.set_facecolor('#2b2b2b')
    ax2.set_facecolor('#2b2b2b')
    ax3.set_facecolor('#2b2b2b')
    ax4.set_facecolor('#2b2b2b')
else:
    fig, ax = plt.subplots()
    ax.set_facecolor('#2b2b2b')

fig.tight_layout()
execution_times = []
dp_execution_times = []

for _ in range(ITER):
    total_time = 0
    total_time_dp = 0
    for test in range(AVG_OF):
        d = np.random.randint(
            BASE_DIMENSION, DIMENSIONS[_], NUMBER_OF_MATRICES[_]+1)
        matrices = []
        for i in range(NUMBER_OF_MATRICES[_]):
            matrices.append(np.random.randint(
                0, VALUES[_], [d[i], d[i+1]]).astype(object))

        m = np.empty([NUMBER_OF_MATRICES[_], NUMBER_OF_MATRICES[_]], object)
        p = np.empty([NUMBER_OF_MATRICES[_], NUMBER_OF_MATRICES[_]], np.int64)

        minmult(NUMBER_OF_MATRICES[_], m, p)
        start_time = timeit.default_timer()
        dp_mul(0, NUMBER_OF_MATRICES[_]-1)
        total_time_dp += timeit.default_timer() - start_time

        start_time = timeit.default_timer()
        mul(0, NUMBER_OF_MATRICES[_]-1)
        total_time += timeit.default_timer() - start_time

    dp_execution_times.append(total_time_dp / AVG_OF)
    execution_times.append(total_time / AVG_OF)

    if PLOT_INPUTS:
        ax1.clear()
        ax1.plot([i for i in range(len(dp_execution_times))],
                 dp_execution_times, '-y*', label='dp')
        ax1.plot([i for i in range(len(execution_times))],
                 execution_times, '-co', label='non-dp')
        ax1.set_title('Execution Time vs Input Size')
        ax1.set_xlabel('# Iterations')
        ax1.set_ylabel('Execution Time (seconds)')
        ax1.legend()

        ax2.clear()
        ax2.plot([i for i in range(len(execution_times))],
                 [NUMBER_OF_MATRICES[i] for i in range(len(dp_execution_times))], '-co', label='number of matrices')
        ax2.set_title('Number of Matrices')
        ax2.set_xlabel('# Iterations')
        ax2.set_ylabel('Size')
        ax2.legend()

        ax3.clear()
        ax3.plot([i for i in range(len(dp_execution_times))],
                 [DIMENSIONS[i] for i in range(len(dp_execution_times))], '-y*', label='dimensions')
        ax3.set_title('Dimensions Sizes')
        ax3.set_xlabel('# Iterations')
        ax3.set_ylabel('Size')
        ax3.legend()

        ax4.clear()
        ax4.plot([i for i in range(len(dp_execution_times))],
                 [VALUES[i] for i in range(len(dp_execution_times))], '-co', label='element values')
        ax4.set_title('Element Values')
        ax4.set_xlabel('# Iterations')
        ax4.set_ylabel('Size')
        ax4.legend()
    else:
        ax.clear()
        ax.plot([i for i in range(len(dp_execution_times))],
                dp_execution_times, '-y*', label='dp')
        ax.plot([i for i in range(len(execution_times))],
                execution_times, '-co', label='non-dp')
        ax.set_title('Execution Time vs Input Size')
        ax.set_xlabel('# Iterations')
        ax.set_ylabel('Execution Time (seconds)')
        ax.legend()
    plt.draw()
    plt.pause(0.001)

plt.show()
