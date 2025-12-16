TP 4 les commandes

```
PS C:\Users\ozoux> choco install kubernetes-cli
Chocolatey v2.5.1
3 validations performed. 2 success(es), 1 warning(s), and 0 error(s).

Validation Warnings:
 - A pending system reboot request has been detected, however, this is
   being ignored due to the current Chocolatey configuration.  If you
   want to halt when this occurs, then either set the global feature
   using:
     choco feature enable --name="exitOnRebootDetected"
   or pass the option --exit-when-reboot-detected.

Installing the following packages:
kubernetes-cli
By installing, you accept licenses for the packages.
kubernetes-cli v1.34.2 already installed.
 Use --force to reinstall, specify a version to install, or try upgrade.

Chocolatey installed 0/1 packages.
 See the log for details (C:\ProgramData\chocolatey\logs\chocolatey.log).

Warnings:
 - kubernetes-cli - kubernetes-cli v1.34.2 already installed.
 Use --force to reinstall, specify a version to install, or try upgrade.
PS C:\Users\ozoux> kubectl version --client
Client Version: v1.34.1
Kustomize Version: v5.7.1
PS C:\Users\ozoux> minikube version
minikube version: v1.37.0
commit: 65318f4cfff9c12cc87ec9eb8f4cdd57b25047f3

```
PS C:\Users\ozoux> minikube start --cpus=2 --memory=2048 --driver=docker
😄  minikube v1.37.0 on Microsoft Windows 11 Pro 10.0.26200.6899 Build 26200.6899
✨  Using the docker driver based on user configuration
📌  Using Docker Desktop driver with root privileges
👍  Starting "minikube" primary control-plane node in "minikube" cluster
🚜  Pulling base image v0.0.48 ...
💾  Downloading Kubernetes v1.34.0 preload ...
🔥  Creating docker container (CPUs=2, Memory=2048MB) ...
❗  Failing to connect to https://registry.k8s.io/ from inside the minikube container
💡  To pull new external images, you may need to configure a proxy: https://minikube.sigs.k8s.io/docs/reference/networking/proxy/
🐳  Preparing Kubernetes v1.34.0 on Docker 28.4.0 ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: storage-provisioner, default-storageclass
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default

PS C:\Users\ozoux> minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

```
PS C:\Users\ozoux> kubectl config current-context
minikube
PS C:\Users\ozoux> kubectl get nodes
NAME       STATUS   ROLES           AGE     VERSION
minikube   Ready    control-plane   5m38s   v1.34.0
PS C:\Users\ozoux> kubectl get pods -n kube-system
NAME                               READY   STATUS    RESTARTS        AGE
coredns-66bc5c9577-nj7hb           1/1     Running   0               5m50s
etcd-minikube                      1/1     Running   0               5m55s
kube-apiserver-minikube            1/1     Running   0               5m56s
kube-controller-manager-minikube   1/1     Running   0               5m55s
kube-proxy-hbfxm                   1/1     Running   0               5m50s
kube-scheduler-minikube            1/1     Running   0               5m55s
storage-provisioner                1/1     Running   1 (5m28s ago)   5m53s

```
PS C:\Users\ozoux> kubectl describe node minikube
Name:               minikube
Roles:              control-plane
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=minikube
                    kubernetes.io/os=linux
                    minikube.k8s.io/commit=65318f4cfff9c12cc87ec9eb8f4cdd57b25047f3
                    minikube.k8s.io/name=minikube
                    minikube.k8s.io/primary=true
                    minikube.k8s.io/updated_at=2025_11_24T11_50_16_0700
                    minikube.k8s.io/version=v1.37.0
                    node-role.kubernetes.io/control-plane=
                    node.kubernetes.io/exclude-from-external-load-balancers=
Annotations:        node.alpha.kubernetes.io/ttl: 0
                    volumes.kubernetes.io/controller-managed-attach-detach: true
CreationTimestamp:  Mon, 24 Nov 2025 11:50:12 +0100
Taints:             <none>
Unschedulable:      false
Lease:
  HolderIdentity:  minikube
  AcquireTime:     <unset>
  RenewTime:       Mon, 24 Nov 2025 11:56:43 +0100
Conditions:
  Type             Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
  ----             ------  -----------------                 ------------------                ------                       -------
  MemoryPressure   False   Mon, 24 Nov 2025 11:56:44 +0100   Mon, 24 Nov 2025 11:50:10 +0100   KubeletHasSufficientMemory   kubelet has sufficient memory available
  DiskPressure     False   Mon, 24 Nov 2025 11:56:44 +0100   Mon, 24 Nov 2025 11:50:10 +0100   KubeletHasNoDiskPressure     kubelet has no disk pressure
  PIDPressure      False   Mon, 24 Nov 2025 11:56:44 +0100   Mon, 24 Nov 2025 11:50:10 +0100   KubeletHasSufficientPID      kubelet has sufficient PID available
  Ready            True    Mon, 24 Nov 2025 11:56:44 +0100   Mon, 24 Nov 2025 11:50:13 +0100   KubeletReady                 kubelet is posting ready status
Addresses:
  InternalIP:  192.168.49.2
  Hostname:    minikube
Capacity:
  cpu:                12
  ephemeral-storage:  1055762868Ki
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             7965904Ki
  pods:               110
Allocatable:
  cpu:                12
  ephemeral-storage:  1055762868Ki
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             7965904Ki
  pods:               110
System Info:
  Machine ID:                 92fbbd1313d349149b3cb4c1184f1915
  System UUID:                92fbbd1313d349149b3cb4c1184f1915
  Boot ID:                    18a5ce12-779c-46da-99df-e8f17ecb7fa9
  Kernel Version:             6.6.87.2-microsoft-standard-WSL2
  OS Image:                   Ubuntu 22.04.5 LTS
  Operating System:           linux
  Architecture:               amd64
  Container Runtime Version:  docker://28.4.0
  Kubelet Version:            v1.34.0
  Kube-Proxy Version:
PodCIDR:                      10.244.0.0/24
PodCIDRs:                     10.244.0.0/24
Non-terminated Pods:          (7 in total)
  Namespace                   Name                                CPU Requests  CPU Limits  Memory Requests  Memory Limits  Age
  ---------                   ----                                ------------  ----------  ---------------  -------------  ---
  kube-system                 coredns-66bc5c9577-nj7hb            100m (0%)     0 (0%)      70Mi (0%)        170Mi (2%)     6m31s
  kube-system                 etcd-minikube                       100m (0%)     0 (0%)      100Mi (1%)       0 (0%)         6m36s
  kube-system                 kube-apiserver-minikube             250m (2%)     0 (0%)      0 (0%)           0 (0%)         6m37s
  kube-system                 kube-controller-manager-minikube    200m (1%)     0 (0%)      0 (0%)           0 (0%)         6m36s
  kube-system                 kube-proxy-hbfxm                    0 (0%)        0 (0%)      0 (0%)           0 (0%)         6m31s
  kube-system                 kube-scheduler-minikube             100m (0%)     0 (0%)      0 (0%)           0 (0%)         6m36s
  kube-system                 storage-provisioner                 0 (0%)        0 (0%)      0 (0%)           0 (0%)         6m34s
Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource           Requests    Limits
  --------           --------    ------
  cpu                750m (6%)   0 (0%)
  memory             170Mi (2%)  170Mi (2%)
  ephemeral-storage  0 (0%)      0 (0%)
  hugepages-1Gi      0 (0%)      0 (0%)
  hugepages-2Mi      0 (0%)      0 (0%)
Events:
  Type    Reason                   Age                    From             Message
  ----    ------                   ----                   ----             -------
  Normal  Starting                 6m29s                  kube-proxy
  Normal  NodeHasSufficientMemory  6m44s (x8 over 6m44s)  kubelet          Node minikube status is now: NodeHasSufficientMemory
  Normal  NodeHasNoDiskPressure    6m44s (x8 over 6m44s)  kubelet          Node minikube status is now: NodeHasNoDiskPressure
  Normal  NodeHasSufficientPID     6m44s (x7 over 6m44s)  kubelet          Node minikube status is now: NodeHasSufficientPID
  Normal  NodeAllocatableEnforced  6m44s                  kubelet          Updated Node Allocatable limit across pods
  Normal  Starting                 6m36s                  kubelet          Starting kubelet.
  Normal  NodeAllocatableEnforced  6m36s                  kubelet          Updated Node Allocatable limit across pods
  Normal  NodeHasSufficientMemory  6m36s                  kubelet          Node minikube status is now: NodeHasSufficientMemory
  Normal  NodeHasNoDiskPressure    6m36s                  kubelet          Node minikube status is now: NodeHasNoDiskPressure
  Normal  NodeHasSufficientPID     6m36s                  kubelet          Node minikube status is now: NodeHasSufficientPID
  Normal  RegisteredNode           6m32s                  node-controller  Node minikube event: Registered Node minikube in Controller
PS C:\Users\ozoux>
```

```
PS C:\Users\ozoux> kubectl get pods --all-namespaces
NAMESPACE     NAME                               READY   STATUS    RESTARTS        AGE
kube-system   coredns-66bc5c9577-nj7hb           1/1     Running   0               7m32s
kube-system   etcd-minikube                      1/1     Running   0               7m37s
kube-system   kube-apiserver-minikube            1/1     Running   0               7m38s
kube-system   kube-controller-manager-minikube   1/1     Running   0               7m37s
kube-system   kube-proxy-hbfxm                   1/1     Running   0               7m32s
kube-system   kube-scheduler-minikube            1/1     Running   0               7m37s
kube-system   storage-provisioner                1/1     Running   1 (7m10s ago)   7m35s
```


```
PS C:\Users\ozoux> kubectl describe pod -n kube-system coredns-66bc5c9577-nj7hb
Name:                 coredns-66bc5c9577-nj7hb
Namespace:            kube-system
Priority:             2000000000
Priority Class Name:  system-cluster-critical
Service Account:      coredns
Node:                 minikube/192.168.49.2
Start Time:           Mon, 24 Nov 2025 11:50:20 +0100
Labels:               k8s-app=kube-dns
                      pod-template-hash=66bc5c9577
Annotations:          <none>
Status:               Running
IP:                   10.244.0.2
IPs:
  IP:           10.244.0.2
Controlled By:  ReplicaSet/coredns-66bc5c9577
Containers:
  coredns:
    Container ID:  docker://23599d437c681d2ac5ed77a254fd880d61fac2728c2193667680599e7335ae6a
    Image:         registry.k8s.io/coredns/coredns:v1.12.1
    Image ID:      docker-pullable://registry.k8s.io/coredns/coredns@sha256:e8c262566636e6bc340ece6473b0eed193cad045384401529721ddbe6463d31c
    Ports:         53/UDP (dns), 53/TCP (dns-tcp), 9153/TCP (metrics), 8080/TCP (liveness-probe), 8181/TCP (readiness-probe)
    Host Ports:    0/UDP (dns), 0/TCP (dns-tcp), 0/TCP (metrics), 0/TCP (liveness-probe), 0/TCP (readiness-probe)
    Args:
      -conf
      /etc/coredns/Corefile
    State:          Running
      Started:      Mon, 24 Nov 2025 11:50:22 +0100
    Ready:          True
    Restart Count:  0
    Limits:
      memory:  170Mi
    Requests:
      cpu:        100m
      memory:     70Mi
    Liveness:     http-get http://:liveness-probe/health delay=60s timeout=5s period=10s #success=1 #failure=5
    Readiness:    http-get http://:readiness-probe/ready delay=0s timeout=1s period=10s #success=1 #failure=3
    Environment:  <none>
    Mounts:
      /etc/coredns from config-volume (ro)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-mlglj (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True
  Initialized                 True
  Ready                       True
  ContainersReady             True
  PodScheduled                True
Volumes:
  config-volume:
    Type:      ConfigMap (a volume populated by a ConfigMap)
    Name:      coredns
    Optional:  false
  kube-api-access-mlglj:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    Optional:                false
    DownwardAPI:             true
QoS Class:                   Burstable
Node-Selectors:              kubernetes.io/os=linux
Tolerations:                 CriticalAddonsOnly op=Exists
                             node-role.kubernetes.io/control-plane:NoSchedule
                             node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason     Age                    From               Message
  ----     ------     ----                   ----               -------
  Normal   Scheduled  9m32s                  default-scheduler  Successfully assigned kube-system/coredns-66bc5c9577-nj7hb to minikube
  Normal   Pulled     9m30s                  kubelet            Container image "registry.k8s.io/coredns/coredns:v1.12.1" already present on machine
  Normal   Created    9m30s                  kubelet            Created container: coredns
  Normal   Started    9m30s                  kubelet            Started container coredns
  Warning  Unhealthy  9m16s (x3 over 9m26s)  kubelet            Readiness probe failed: HTTP probe failed with statuscode: 503

  PS C:\Users\ozoux> kubectl logs -n kube-system coredns-66bc5c9577-nj7hb
maxprocs: Leaving GOMAXPROCS=12: CPU quota undefined
[INFO] plugin/kubernetes: waiting for Kubernetes API before starting server
[INFO] plugin/kubernetes: waiting for Kubernetes API before starting server
[INFO] plugin/kubernetes: waiting for Kubernetes API before starting server
[INFO] plugin/kubernetes: waiting for Kubernetes API before starting server
[INFO] plugin/kubernetes: waiting for Kubernetes API before starting server
[INFO] plugin/kubernetes: waiting for Kubernetes API before starting server
[INFO] plugin/kubernetes: waiting for Kubernetes API before starting server
[INFO] plugin/kubernetes: waiting for Kubernetes API before starting server
[INFO] plugin/ready: Still waiting on: "kubernetes"
[INFO] plugin/ready: Still waiting on: "kubernetes"
[INFO] plugin/kubernetes: waiting for Kubernetes API before starting server
[WARNING] plugin/kubernetes: starting server with unsynced Kubernetes API
.:53
[INFO] plugin/reload: Running configuration SHA512 = e7e8a6c4578bf29b9f453cb54ade3fb14671793481527b7435e35119b25e84eb3a79242b1f470199f8605ace441674db8f1b6715b77448c20dde63e2dc5d2169
CoreDNS-1.12.1
linux/amd64, go1.24.1, 707c7c1
[INFO] 127.0.0.1:40946 - 61951 "HINFO IN 2035247207367929305.7215639049679418779. udp 57 false 512" NXDOMAIN qr,rd,ra 57 0.352149239s
[INFO] plugin/ready: Still waiting on: "kubernetes"
[INFO] plugin/kubernetes: pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:251: failed to list *v1.EndpointSlice: Get "https://10.96.0.1:443/apis/discovery.k8s.io/v1/endpointslices?limit=500&resourceVersion=0": dial tcp 10.96.0.1:443: connect: connection refused
[ERROR] plugin/kubernetes: Unhandled Error
[INFO] plugin/kubernetes: pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:251: failed to list *v1.Service: Get "https://10.96.0.1:443/api/v1/services?limit=500&resourceVersion=0": dial tcp 10.96.0.1:443: connect: connection refused
[ERROR] plugin/kubernetes: Unhandled Error
[INFO] plugin/kubernetes: pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:251: failed to list *v1.Namespace: Get "https://10.96.0.1:443/api/v1/namespaces?limit=500&resourceVersion=0": dial tcp 10.96.0.1:443: connect: connection refused
[ERROR] plugin/kubernetes: Unhandled Error
```

```
PS C:\Users\ozoux> kubectl create deployment hello-minikube --image=k8s.gcr.io/echoserver:1.4
deployment.apps/hello-minikube created
PS C:\Users\ozoux> kubectl get deployments
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
hello-minikube   0/1     1            0           34s
PS C:\Users\ozoux> kubectl get pods
NAME                              READY   STATUS             RESTARTS   AGE
hello-minikube-7fd55c845c-2zw76   0/1     ImagePullBackOff   0          45s
PS C:\Users\ozoux> kubectl describe deployment hello-minikube
Name:                   hello-minikube
Namespace:              default
CreationTimestamp:      Mon, 24 Nov 2025 12:05:39 +0100
Labels:                 app=hello-minikube
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=hello-minikube
Replicas:               1 desired | 1 updated | 1 total | 0 available | 1 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=hello-minikube
  Containers:
   echoserver:
    Image:         k8s.gcr.io/echoserver:1.4
    Port:          <none>
    Host Port:     <none>
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      False   MinimumReplicasUnavailable
  Progressing    True    ReplicaSetUpdated
OldReplicaSets:  <none>
NewReplicaSet:   hello-minikube-7fd55c845c (1/1 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  61s   deployment-controller  Scaled up replica set hello-minikube-7fd55c845c from 0 to 1

```

```
PS C:\Users\ozoux> kubectl expose deployment hello-minikube --type=NodePort --port=8080
service/hello-minikube exposed
 
```