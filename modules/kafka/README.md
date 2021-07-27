# Deploy Kafka on a Kubernetes cluster

This guide will walk you through deploying Kafka on Kubernetes using Heml.

## Install Helm

To install Helm execute the following commands:

```
$ curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
$ chmod 700 get_helm.sh
$ ./get_helm.sh
```

## Install Kafka

1. Include the bitnami repo:

```
helm repo add bitnami https://charts.bitnami.com/bitnami
```

2. Install Kafka:
```
helm install kafka-release bitnami/kafka
```

The expected output should be similar to this:

```
NAME: kafka-release
LAST DEPLOYED: Mon Jul 26 11:23:49 2021
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
** Please be patient while the chart is being deployed **

Kafka can be accessed by consumers via port 9092 on the following DNS name from within your cluster:

    kafka-release.default.svc.cluster.local

Each Kafka broker can be accessed by producers via port 9092 on the following DNS name(s) from within your cluster:

    kafka-release-0.kafka-release-headless.default.svc.cluster.local:9092

To create a pod that you can use as a Kafka client run the following commands:

    kubectl run kafka-release-client --restart='Never' --image docker.io/bitnami/kafka:2.8.0-debian-10-r55 --namespace default --command -- sleep infinity
    kubectl exec --tty -i kafka-release-client --namespace default -- bash

    PRODUCER:
        kafka-console-producer.sh \
            
            --broker-list kafka-release-0.kafka-release-headless.default.svc.cluster.local:9092 \
            --topic test

    CONSUMER:
        kafka-console-consumer.sh \
            
            --bootstrap-server kafka-release.default.svc.cluster.local:9092 \
            --topic test \
            --from-beginning
```

3. Verify that Kafka is up and running:
```
kubectl get po
```

`kafka-release-zookeeper-0` and `kafka-release-0` should have `STATUS: Running`.