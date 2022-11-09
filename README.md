# MS2

For EC2 dockers:

```
sudo yum update
sudo yum install git
```

Add requirements.txt and Dockerfile

Install docker

```
sudo yum install docker
sudo service docker start
```

```
sudo docker image build -t ms2 .
sudo docker run -p 5011:5011 -d ms2
```

Remember to add port 5011 to the securtiy group.

Show all docker
```
sudo docker ps
```

Stop a docker
```
sudo docker stop container_id
```

Show all container
```
sudo docker ps -a
```

Delete conatiner
```
sudo docker rm container_id
```
