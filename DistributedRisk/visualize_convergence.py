import risk_engine
import matplotlib.pyplot as plt
import time

# 1. Setup Parameters
S0 = 100.0
K = 100.0
r = 0.05
sigma = 0.2
T = 1.0

# Black-Scholes Theoretical Price (The "Truth")
actual_price = 10.45058

# 2. Run Experiments with increasing N
simulation_counts = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]
prices = []
times = []

print(f"{'Simulations':<15} {'Price':<10} {'Error':<10} {'Time (s)':<10}")
print("-" * 50)

for N in simulation_counts:
    start_time = time.time()
    
    # --- CALLING C++ ENGINE ---
    pricer = risk_engine.MonteCarloPricer(N)
    price = pricer.price_call_option(S0, K, r, sigma, T)
    # --------------------------
    
    end_time = time.time()
    
    prices.append(price)
    times.append(end_time - start_time)
    
    error = abs(price - actual_price)
    print(f"{N:<15} {price:<10.4f} {error:<10.4f} {times[-1]:<10.4f}")

# 3. Plotting the Convergence
plt.figure(figsize=(10, 6))

# Draw the "Truth" line
plt.axhline(y=actual_price, color='r', linestyle='--', label='Black-Scholes Truth ($10.45)')

# Draw our C++ estimates
plt.plot(simulation_counts, prices, marker='o', label='Monte Carlo Estimate')

plt.xscale('log') # Log scale because we jump from 1k to 1M
plt.xlabel('Number of Simulations (Log Scale)')
plt.ylabel('Option Price')
plt.title('Monte Carlo Convergence: Accuracy vs Scale')
plt.legend()
plt.grid(True)

# Save the plot
plt.savefig("convergence_plot.png")
print("\nPlot saved as 'convergence_plot.png'. Open it to see your results!")