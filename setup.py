import setuptools

if __name__ == "__main__":
    setuptools.setup(
        entry_points={'console_scripts': ['phyDataPopulation=physical_data_population.read_CLI_n_run:main_method',
                                          'phyDataPopulation_tmp=physical_data_population.read_CLI_n_run_temp:main_method']},
        install_requires=['pyxlsb', 'xlrd']
    )

