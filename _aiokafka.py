from aiokafka.cluster import (
    log,
    time,
    Errors,
    collections,
    BrokerMetadata,
    TopicPartition,
    PartitionMetadata,
)

KAFKA_HOST_MAP = {"10.0.2.25": 9091, "10.0.2.26": 9092, "10.0.2.27": 9093}
KAFKA_PORT_MAP = "103.244.108.142"


def _update_metadata(self, metadata):
    """BrokerMetadata 의 host와 port를 수정하기 위해서 cluster의 update_meatadata를 치환 해준다."""
    if not metadata.brokers:
        log.warning("No broker metadata found in MetadataResponse")

    _new_brokers = {}
    for broker in metadata.brokers:
        if metadata.API_VERSION == 0:
            node_id, host, port = broker
            rack = None
        else:
            node_id, host, port, rack = broker

        port = KAFKA_PORT_MAP[host]
        host = KAFKA_HOST_MAP[host]
        _new_brokers.update({node_id: BrokerMetadata(node_id, host, port, rack)})

    if metadata.API_VERSION == 0:
        _new_controller = None
    else:
        _new_controller = _new_brokers.get(metadata.controller_id)

    _new_partitions = {}
    _new_broker_partitions = collections.defaultdict(set)
    _new_unauthorized_topics = set()
    _new_internal_topics = set()

    for topic_data in metadata.topics:
        if metadata.API_VERSION == 0:
            error_code, topic, partitions = topic_data
            is_internal = False
        else:
            error_code, topic, is_internal, partitions = topic_data
        if is_internal:
            _new_internal_topics.add(topic)
        error_type = Errors.for_code(error_code)
        if error_type is Errors.NoError:
            _new_partitions[topic] = {}
            for p_error, partition, leader, replicas, isr in partitions:
                _new_partitions[topic][partition] = PartitionMetadata(
                    topic=topic,
                    partition=partition,
                    leader=leader,
                    replicas=replicas,
                    isr=isr,
                    error=p_error,
                )
                if leader != -1:
                    _new_broker_partitions[leader].add(TopicPartition(topic, partition))

        elif error_type is Errors.LeaderNotAvailableError:
            log.warning(
                "Topic %s is not available during auto-create" " initialization", topic
            )
        elif error_type is Errors.UnknownTopicOrPartitionError:
            log.error("Topic %s not found in cluster metadata", topic)
        elif error_type is Errors.TopicAuthorizationFailedError:
            log.error("Topic %s is not authorized for this client", topic)
            _new_unauthorized_topics.add(topic)
        elif error_type is Errors.InvalidTopicError:
            log.error("'%s' is not a valid topic name", topic)
        else:
            log.error("Error fetching metadata for topic %s: %s", topic, error_type)

    with self._lock:
        self._brokers = _new_brokers
        self.controller = _new_controller
        self._partitions = _new_partitions
        self._broker_partitions = _new_broker_partitions
        self.unauthorized_topics = _new_unauthorized_topics
        self.internal_topics = _new_internal_topics

    now = time.time() * 1000
    self._last_refresh_ms = now
    self._last_successful_refresh_ms = now

    log.debug("Updated cluster metadata to %s", self)

    for listener in self._listeners:
        listener(self)


def _add_coordinator(self, node_id, host, port, rack=None, *, purpose):
    """BrokerMetadata 의 host와 port를 수정하기 위해서 cluster의 add_coordinator를 치환 해준다."""
    port = KAFKA_PORT_MAP[host]
    host = KAFKA_HOST_MAP[host]
    if purpose in self._coordinator_by_key:
        old_id = self._coordinator_by_key.pop(purpose)
        del self._coordinators[old_id]

    self._coordinators[node_id] = BrokerMetadata(node_id, host, port, rack)
    self._coordinator_by_key[purpose] = node_id
