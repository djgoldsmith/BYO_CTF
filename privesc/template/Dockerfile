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

# For Installing use
# apt-get install --no-install-recommends -y <packages> 

## -----------------------

# ---- Add the root Flag
COPY root.txt /root/root.txt
RUN chmod 600 /root/root.txt


# PORTS AND BASIC COMMAND
EXPOSE 22  
CMD ["/usr/sbin/sshd", "-D"]
