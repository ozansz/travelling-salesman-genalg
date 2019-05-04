import sys

from algo import gen_trainer, create_sample
from plotter import DynamicPlot

if __name__ == "__main__":
    popsize = 200
    gensize = 500

    if len(sys.argv) > 1:
        popsize = int(sys.argv[1])
    if len(sys.argv) > 2:
        gensize = int(sys.argv[2])

    sample = create_sample(size=popsize)
    plotter = DynamicPlot("Generation", "Fitness", (0, gensize))

    fit_space = gen_trainer(
        genes=sample,
        generation_size=popsize,
        elite_size=20,
        mutation_rate=.01,
        generations=gensize,
        verbose=True,
        verbose_level=1,
        plotter=plotter
    )

    input()