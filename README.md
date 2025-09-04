### 1. Project Introduction
Upload an image and discover celebrities with AI-powered recognition and interactive Q&A.

**Demo:**

![Demo](images/app.gif)

- **Tech stack**

    - Groq --> LLM
    - HuggingFace --> Embedding model
    - Langchain --> AI framework to interact with LLM
    - GCP VM --> Virtual machine on the cloud
    - Minikube --> For making a Kubternetes Cluster where you can deploy your application
    - Flask --> Application backend
    - HTML/CSS --> To make UI or frontend of the app
    - Docker --> For containerization of the app during deployment
    - AstraDB --> Online vector store
    - GitHub --> Work as a Source Code Management (SCM) for your project
    - Prometheus --> Collects and stores real-time metrics (like CPU usage, memory, request rate) from your application running in Kubernetes
    - Grafana Cloud --> Monitoring your Kubernetes Clusters and visualize the metrics in the form of dashboards

- **Workflow**

![alt text](/images/image.png)

### 2. Configure VM Instance

- **Clone your GitHub repo**

  ```bash
  git clone https://github.com/timelesshc/online-product-recommender.git
  ls
  cd online-product-recommender
  ls  # You should see the contents of your project
  ```

- **Install Docker**

  - Search: "Install Docker on Ubuntu"
  - Open the first official Docker website (docs.docker.com)
  - Scroll down and copy the **first big command block** and paste into your VM terminal
  - Then copy and paste the **second command block**
  - Then run the **third command** to test Docker:

    ```bash
    docker run hello-world
    ```

- **Run Docker without sudo**

  - On the same page, scroll to: **"Post-installation steps for Linux"**
  - Paste all 4 commands one by one to allow Docker without `sudo`
  - Last command is for testing

- **Enable Docker to start on boot**

  - On the same page, scroll down to: **"Configure Docker to start on boot"**
  - Copy and paste the command block (2 commands):

    ```bash
    sudo systemctl enable docker.service
    sudo systemctl enable containerd.service
    ```

- **Verify Docker Setup**

  ```bash
  systemctl status docker       # You should see "active (running)"
  docker ps                     # No container should be running
  docker ps -a                 # Should show "hello-world" exited container
  ```


### 3. Configure Minikube inside VM

- **Install Minikube**

  - Open browser and search: `Install Minikube`
  - Open the first official site (minikube.sigs.k8s.io) with `minikube start` on it
  - Choose:
    - **OS:** Linux
    - **Architecture:** *x86*
    - Select **Binary download**
  - Reminder: You have already done this on Windows, so you're familiar with how Minikube works

- **Install Minikube Binary on VM**

  - Copy and paste the installation commands from the website into your VM terminal

- **Start Minikube Cluster**

  ```bash
  minikube start
  ```

  - This uses Docker internally, which is why Docker was installed first

- **Install kubectl**

  - Search: `Install kubectl`
  - Run the first command with `curl` from the official Kubernetes docs
  - Run the second command to validate the download
  - Instead of installing manually, go to the **Snap section** (below on the same page)

  ```bash
  sudo snap install kubectl --classic
  ```

  - Verify installation:

    ```bash
    kubectl version --client
    ```

- **Check Minikube Status**

  ```bash
  minikube status         # Should show all components running
  kubectl get nodes       # Should show minikube node
  kubectl cluster-info    # Cluster info
  docker ps               # Minikube container should be running
  ```

### 4. Interlink your Github on VSCode and on VM

```bash
git config --global user.email "xxx@xxx.com"
git config --global user.name "xxxx"

git add .
git commit -m "commit"
git push origin main
```

- When prompted:
  - **Username**: `xxx`
  - **Password**: GitHub token (paste, it's invisible)

---


### 5. Build and Deploy your APP on VM

```bash
## Point Docker to Minikube
eval $(minikube docker-env)

docker build -t llmops-app:latest .

kubectl create secret generic llmops-secrets \
  --from-literal=GROQ_API_KEY="" \
  --from-literal=HUGGINGFACEHUB_API_TOKEN="" \
  --from-literal=HF_TOKEN="" \
  --from-literal=ASTRA_DB_API_ENDPOINT="" \
  --from-literal=ASTRA_DB_APPLICATION_TOKEN="" \
  --from-literal=ASTRA_DB_KEYSPACE="" 

kubectl apply -f llmops-k8s.yaml


kubectl get pods

### U will see pods runiing


# Do minikube tunnel on one terminal

minikube tunnel


# Open another terminal

kubectl port-forward svc/llmops-service 8501:80 --address 0.0.0.0

## Now copy external ip and :8501 and see ur app there....


```

### 6. PROMETHEUS AND GRAFANA MONITORING OF YOUR APP
```bash
### Open another VM terminal 

kubectl create namespace monitoring

kubectl get ns


kubectl apply -f prometheus/prometheus-configmap.yaml

kubectl apply -f prometheus/prometheus-deployment.yaml

kubectl apply -f grafana/grafana-deployment.yaml

## Check target health also..
## On IP:9090
kubectl port-forward --address 0.0.0.0 svc/prometheus-service -n monitoring 9090:9090

## Username:Pass --> admin:admin
kubectl port-forward --address 0.0.0.0 svc/grafana-service -n monitoring 3000:3000



Configure Grafana
Go to Settings > Data Sources > Add Data Source

Choose Prometheus

URL: http://prometheus-service.monitoring.svc.cluster.local:9090

Click Save & Test

Green success mesaage shown....
```
