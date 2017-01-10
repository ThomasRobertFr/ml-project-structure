

.env: config.yml config-private.yml
	python src/misc/yaml-to-env.py
