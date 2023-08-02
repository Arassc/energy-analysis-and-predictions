.DEFAULT_GOAL := default

reinstall_package:
	@pip uninstall -y energy-price-production-app || :
	@pip install -e.

run_preprocess_energy_prices:
	python -c 'from energy-price-production-app.preprocess_data.main_energy_prices import preprocess_energy_prices;
	 preprocess_energy_prices()'
