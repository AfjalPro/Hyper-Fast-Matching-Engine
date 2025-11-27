import time
import ray
import risk_engine  # Your C++ module

# 1. Initialize Ray (The Distributed OS)
# This will auto-detect how many cores your computer has (e.g., 8, 12, 16)
ray.init()

print("Ray Cluster Started.")
print(f"Resources: {ray.cluster_resources()}")

# 2. Define the "Worker"
# @ray.remote turns a normal Python class into a generic process running on a separate core
@ray.remote
class PricingWorker:
    def __init__(self, simulation_count):
        # Each worker initializes its own C++ Engine
        self.engine = risk_engine.MonteCarloPricer(simulation_count)
    
    def price_option(self, S0, K, r, sigma, T):
        # Call C++ code
        return self.engine.price_call_option(S0, K, r, sigma, T)

# 3. Create a Portfolio of 100 random options
# Let's say we have 100 contracts with slightly different Strike Prices
strikes = [100 + i for i in range(100)]  # 100, 101, 102... 199
N = 1000000  # 1 Million sims PER option

# --- APPROACH A: SEQUENTIAL (The Slow Way) ---
print(f"\n[SEQUENTIAL] Pricing {len(strikes)} options one by one...")
start_seq = time.time()

# We will just do 5 for the demo, otherwise you'll wait 2 minutes
# (A real Sequential run of 100 would take ~14 seconds)
dummy_engine = risk_engine.MonteCarloPricer(N)
for K in strikes[:5]: 
    dummy_engine.price_call_option(100.0, K, 0.05, 0.2, 1.0)

end_seq = time.time()
print(f"Time for 5 options: {end_seq - start_seq:.4f}s")


# --- APPROACH B: DISTRIBUTED (The Fast Way) ---
print(f"\n[DISTRIBUTED] Pricing {len(strikes)} options across all cores...")
start_par = time.time()

# Spin up workers (Actors)
# Ideally, we create one actor per CPU core.
# Let's just create 4 workers for now.
workers = [PricingWorker.remote(N) for _ in range(4)]

# Distribute the work
# We assign options to workers in a round-robin fashion
futures = []
for i, K in enumerate(strikes):
    worker_index = i % 4
    # .remote() sends the task to the background process
    futures.append(workers[worker_index].price_option.remote(100.0, K, 0.05, 0.2, 1.0))

# Wait for all results to come back
results = ray.get(futures)

end_par = time.time()
print(f"Time for 100 options: {end_par - start_par:.4f}s")
print(f"First 5 Prices: {results[:5]}")

# Shutdown Ray
ray.shutdown()