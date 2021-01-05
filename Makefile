kafka-up:
	docker-compose -f docker-compose.kafka.yml up
kafka-down:
	docker-compose -f docker-compose.kafka.yml down $(args)
kafka-shell:
	docker-compose -f docker-compose.kafka.yml run --rm zookeeper /bin/bash

trading-up:
	docker-compose -f docker-compose.trading.yml up
trading-down:
	docker-compose -f docker-compose.trading.yml down $(args)
trading-shell:
	docker-compose -f docker-compose.trading.yml run --rm trading /bin/bash

dev-up:
	docker-compose -f docker-compose.kafka.yml -f docker-compose.trading.yml up
dev-down:
	docker-compose -f docker-compose.kafka.yml -f docker-compose.trading.yml down $(args)