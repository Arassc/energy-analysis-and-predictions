.DEFAULT_GOAL := default

reinstall_package:
	@pip uninstall -y energyanalysis|| :
	@pip install -e.

run_preprocess_energy_prices:
	python -c 'from energyanalysis.interface.main_energy_prices import preprocess_energy_prices; preprocess_energy_prices()'

run_train_energy_prices:
	python -c 'from energyanalysis.interface.main_energy_prices import train_energy_prices; train_energy_prices()'

run_plot_test_vs_predict:
	python -c 'from energyanalysis.interface.main_energy_prices import plot_test_vs_predict; plot_test_vs_predict()'
