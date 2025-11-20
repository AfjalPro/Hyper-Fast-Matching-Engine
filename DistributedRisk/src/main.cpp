#include <iostream>
#include <vector>
#include <cmath>
#include <random>

class GaussianGenerator {

    private:
    std::mt19937 generator;
    std::normal_distribution<double> distribution;

    public:
    //Constructor
    GaussianGenerator(double mean, double std_dev) 
        : distribution(mean, std_dev) {
        
        // Use a hardware "random device" to seed the generator
        std::random_device rd; 
        generator.seed(rd());
    }

    double get_next() {
        return distribution(generator);
    }
    

};
int main() {
    std::cout << "======================================" << std::endl;
    std::cout << "   Day 2: Random Number Generation    " << std::endl;
    std::cout << "======================================" << std::endl;

    // 1. Initialize our Generator (Mean = 0, StdDev = 1.0)
    // This represents standard market noise (Z-score)
    GaussianGenerator rng(0.0, 1.0);

    // 2. Generate 10 random numbers to verify they look "Normal"
    std::cout << "Generating 5 sample market shocks:" << std::endl;
    
    double sum = 0.0;
    for (int i = 0; i < 5; ++i) {
        double noise = rng.get_next();
        std::cout << "Shock " << i+1 << ": " << noise << std::endl;
        sum += noise;
    }

    // 3. Quick logic check
    // Since mean is 0, the sum of many numbers should be close to 0.
    // (Note: with only 5 samples, it won't be exactly 0, but let's just ensure it runs)
    std::cout << "--------------------------------------" << std::endl;
    std::cout << "Generation complete." << std::endl;

    return 0;
}




