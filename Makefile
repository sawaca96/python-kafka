dev-up:
	docker-compose -f docker-compose.dev.yml up
dev-down:
	docker-compose -f docker-compose.dev.yml down $(args)
dev-shell:
	docker-compose -f docker-compose.dev.yml run --rm zookeeper /bin/bash