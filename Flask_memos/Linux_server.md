<h2>Some scribbles about linux server deployment, but it is not full!!!</h2>

At first we'll create linux server from scratch

1) after registering at Linode and setting server there grab 'ssh root'
   and paste it into terminal. Follow the procedures there

2) then enter: hostnamectl set-hostname daniil-server

3) nano /etc/hosts -> below localhost type your IP address and name of the 
hostanme you give above

4) then add limited user: adduser somenameuser; adduser somenameuser sudo
Then log out as root user and login as before created user
-> exit

5)	ssh root@172.104.65.43 here instead of 'root' type that somenameuser

6) mkdir .ssh
then switch to ordinary terminal and type there: ssh-keygen -b 4096 
and skip first prompt

7) then we want to move our 'public key' to server 
[Your public key has been saved in /Users/daniilslobodenuk/.ssh/id_rsa.pub]

(still in new terminal) scp ~/.ssh/id_rsa.pub someusername@ip_address_type_here
+ you can put that key in exact location. To do it you're to pur ':' after
IP address. Example: scp ~/.ssh/id_rsa.pub daniil-server@172.104.65.43:~/.ssh/authorized_keys

8) change some permissions: 'sudo chmod 700 ~/.ssh/'
then 'sudo chmod 600 ~/.ssh/*'

9) sudo nano /etc/ssh/sshd_config

there: PermitRootLogin yes (change to no);
PasswordAuthentication no (uncomment and change to no)

then restart the system: sudo systemctl restart sshd

10) and last set the firewall: sudo apt install ufw;
	sudo ufw default allow outgoing;
	sudo ufw default deny incoming;
	sudo ufw allow ssh;
	sudo ufw allow 5000;
	sudo ufw enable;
	sudo ufw status
