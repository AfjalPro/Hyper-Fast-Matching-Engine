#include <pybind11/pybind11.h>
#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <algorithm>

namespace py = pybind11; // Shortcut: type 'py' instead of 'pybind11'

// --- Professional Class from Day 4 (Unchanged Logic) ---
class GaussianGenerator {
private:
    std::mt19937 generator;
    std::normal_distribution<double> distribution;
public:
    GaussianGenerator(double mean = 0.0, double std_dev = 1.0) 
        : distribution(mean, std_dev) {
        std::random_device rd; 
        generator.seed(rd());
    }
    double get_next() { return distribution(generator); }
};

class MonteCarloPricer {
private:
    GaussianGenerator rng;
    int num_sims;

public:
    MonteCarloPricer(int simulations) 
        : num_sims(simulations), rng(0.0, 1.0) {}

    double calculate_price_at_maturity(double S0, double r, double sigma, double T, double Z) const {
        double drift = (r - 0.5 * sigma * sigma) * T;
        double shock = sigma * std::sqrt(T) * Z;
        return S0 * std::exp(drift + shock);
    }

    double price_call_option(double S0, double K, double r, double sigma, double T) {
        double total_payoff = 0.0;
        int pairs = num_sims / 2;

        for (int i = 0; i < pairs; ++i) {
            double Z = rng.get_next();
            // Antithetic Variates (Z and -Z)
            double price_A = calculate_price_at_maturity(S0, r, sigma, T, Z);
            double payoff_A = std::max(price_A - K, 0.0);

            double price_B = calculate_price_at_maturity(S0, r, sigma, T, -Z);
            double payoff_B = std::max(price_B - K, 0.0);

            total_payoff += (payoff_A + payoff_B) / 2.0;
        }

        double average_payoff = total_payoff / pairs;
        return average_payoff * std::exp(-r * T);
    }
};

// --- THE NEW PART: Python Bindings ---
// This tells Python: "Here is a C++ class you can use."
PYBIND11_MODULE(risk_engine, m) {
    m.doc() = "High-Performance Monte Carlo Engine in C++"; 

    // Expose the Class
    py::class_<MonteCarloPricer>(m, "MonteCarloPricer")
        .def(py::init<int>(), "Constructor that takes number of simulations") // __init__
        .def("price_call_option", &MonteCarloPricer::price_call_option, 
             "Calculate the fair price of a European Call Option");
}