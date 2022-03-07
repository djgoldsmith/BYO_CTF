---
title:  Bring Your Own CTF
---


# Overview

Next few weeks we are going to look at building your own CTF challenge:

Topcis to Cover:

  - Linux Enumeration and Privelege Escelation
  - Linux Configuration
  - Docker

## Task

In Groups you are going to build a Privielge Escelation Challenge.
Next time we will try to complete each others challenges.

  1.  Get yourself onto GTFO Bins and find a relevant Binary
  1.  Work out the method for Privesc
  1.  Build the challenge to demo it.

## Docker

https://docs.docker.com/get-started/overview/



# Setup
## Files

  - **docker-compose.yaml**  A configuration file to get everything up and running
  - **template**  Folder containing template for the privesc challenge
    - **Dockerfile**  Configuration file for Docker
	- **root.txt**  Flag file
	- **sudoers**  Empty Sudoers file if you want to use this
	

## Running the Challenge

In the base folder

```
dang@danglaptop ~/Github/Teaching/BYO_CTF/template$ docker-compose build

----8< Snip -----

dang@danglaptop ~/Github/Teaching/BYO_CTF/template$ docker-compose up
[+] Running 1/0
 ⠿ Container byo_ctf-template-1  Created                                    0.0s
Attaching to byo_ctf-template-1
```


# Process

## Step 1:  Identify the Vulnerability

  - Which Method do you want to use
    - SUID  
	 - (https://www.hackingarticles.in/linux-privilege-escalation-using-suid-binaries/) 
	 - (https://medium.com/go-cyber/linux-privilege-escalation-with-suid-files-6119d73bc620)
	- SUDO 
	  - (https://medium.com/schkn/linux-privilege-escalation-using-text-editors-and-files-part-1-a8373396708d)
	- Capabilities ?
	
  - Pick a relevant Binary using GTFO Bins https://gtfobins.github.io/


## Step 2: Get it to work on your Local Box

  - Read and Test it works locally in Kali
    - What needs to be installed ?
	- What needs to be configured ?

You Will want to keep a note of the commands you are using here...

## Docker File

```
FROM debian:buster

#Install SSH Server
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    openssh-server \
    curl wget sudo less 


#Configure SSH (Cant run as Daemon if this doenst exit)
RUN mkdir /var/run/sshd

RUN cp /sbin/getcap  /usr/bin/getcap

# --- System Configuration --------
#Add a User
RUN useradd -ms /bin/bash cueh && echo cueh:cueh | chpasswd

## -----------------------
## Your Instructions go here.

## -----------------------

# ---- Add the root Flag
COPY root.txt /root/root.txt
RUN chmod 600 /root/root.txt


# PORTS AND BASIC COMMAND
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
```

## Working out the Docker File

I find it easiest to work with a "Live" system.
Can then copy and paste the relevant commands across.
You can use the trick below to get root access in a running container.

1.  Start the Container with ```docker-compose up```

2.  Get the name of the running container, with ```docker ps```

```
$ docker ps                   ✹ ✚ ✭main 
CONTAINER ID   IMAGE                                          COMMAND               CREATED          STATUS          PORTS                                                           NAMES
72ffe464b889   byo_ctf_template                               "/usr/sbin/sshd -D"   17 minutes ago   Up 11 minutes   0.0.0.0:22->22/tcp, :::22->22/tcp                               byo_ctf-template-1
```
  
We can see the container that was created is called **byo_ctf_template**

3. Use docker exec to drop a shell in the docker-constainer

```
$ docker exec -it byo_ctf-template-1 /bin/bash
root@72ffe464b889:/# 
```

NOTE:  You can also change the user using the ```-u <user>``` flag
  

### Example,  Python and Suid

Lets imagine we pick Python for our example.  https://gtfobins.github.io/gtfobins/python/

Our Exploit is going to need several stages.

  1. Check That Pyhon is installed. 
  
     As a stripped back OS,  Python may not be installed on the system.  We can check uing the ```which``` command.
	 
	 ```
	 root@72ffe464b889:/# which python
	 root@72ffe464b889:/# 
	 ```

  2. Install the Application if needed.
  
     As Python is not installed, we need to add it to the docker file. 
	 We can first check the command locally.
	 
	 ```
	 root@72ffe464b889:/# apt search python
	 
	 --- SNIP ----
	 python
	 python-minimal
	 ```

	We can then install python using apt
	
	
	```
	root@72ffe464b889:/# apt install python-minimal
	```
	
	and confirm its there
	
	```
	root@72ffe464b889:/# which python
	/usr/bin/python
    ```
	
  3. Update The Docker file
  
    Finally we can update the docker file to show our changes.
	For this we use the same ```apt install``` command as we did when testing
	
	NOTE:  There is some extra syntax here, to allow docker to auto install
	
	```
	RUN apt-get install --no-install-recommends -y python-minimal
	```


  4. Add the Vulnerablity.
  
     We can also upate he docker file to add the acual vunlerablity.
	 
	 We know if python has SUID rights, then we can exploit it.
	 
	 In the container we would use  ```chmod a+x /usr/bin/python```
	 
	 We add that as a RUN command in the docker file
	 
	 ```
	 RUN chmod a+x /usr/bin/python
	 ```
	 
	 
  5. Shutdown and Rebild the Docker Container,  then Test.
