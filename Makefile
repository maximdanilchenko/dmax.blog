format:
	black builder.py

deploy:
	firebase deploy

builder:
	python builder.py
