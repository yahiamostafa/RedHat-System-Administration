# RedHat-System-Administration

## Edit the /etc/skel Configuration 

First We have to edit some configuraion in the `/etc/skel` directory, **the directory used by useradd to create the default settings in a new user's home directory.**
```
yahia@yahia:~$ ll -a /etc/skel/
total 32
drwxr-xr-x   3 root root  4096 نوف 29 16:43 ./
drwxr-xr-x 148 root root 12288 ديس  9 13:15 ../
-rw-r--r--   1 root root   220 ينا  6  2022 .bash_logout
-rw-r--r--   1 root root  3771 ينا  6  2022 .bashrc
-rw-r--r--   1 root root   807 ينا  6  2022 .profile
```
Those three files by default will exist in each new user home directory, so I'm going to add some files to be displayed to all new users.
I'm going to edit the `.bashrc` ,so when a new user is added two files will be created **welcome file** which display some information about the Agency, **user_info** which will contain some info about the user such as username , email , Age and mobile number.
- Open the `.bashrc` using any text editor.
	```Yahia@localhost skel]$ sudo vim .bashrc ```
- add those lines at the end of the file
```
echo "Username : ${USER}" > user-info.txt
echo "Email : ${USER}@guc.com" >> user-info.txt
echo "Mobile Number : +20$(shuf -i 1000000000-1999999999 -n 1)" >> user-info.txt
echo "Country : Egypt" >> user-info.txt
echo "Age is $(shuf -i 20-70 -n 1)" >>  user-info.txt
```
- We can add a welcome text to every user to intoduce our agency to them.
- ```Yahia@localhost skel]$ sudo vim .bashrc ```
- Open the previous file and append Your welcome text
```
echo "Hi $USER  We are very excited to introduce GUC Travel Agency as the one stop provider for all your travel needs and requirements. We label ourselves as leading, innovative, and highly efficient and look forward to demonstrate these qualities at the earliest possible chance.

Since established in 2022, the primary aim was to provide quality travel services to business and leisure travellers. The agency continued to grow and branch out its interests to rise as one of the exponents in the travel industry.

Supported by strong financial management, impressive customer satisfaction and constant improvement, GUC has expanded to cover various facets of the industry. Our experience led to perfection in both our outbound and inbound units.

Our academy offers IATA accredited Travel and Tourism training programs, bringing comprehensive industry specific courses that cover all aspects of the aviation and travel business.

In 2022, we initiated a seven month process to complete a three-tier ISO certification and secure recognition in Quality Management and Safety.

Our Profile:
- Established Year: 2022
- Head Quarters: Cairo
- Other Locations: Alexandria
Activities:
- Airlines and Leisure Representation
- Inbound Travel
- Corporate Travel
- Leisure Travel (Outbound)
- Travel and Aviation Training

Affiliations: IATA
Certifications: ISO 9001-2008

Our Advantage
- Experienced management team.
- In-depth knowledge of region's travel needs.
- Widely and closely networked with trade, corporate and diplomatic community.
- One Stop Shop to provide all services to customers and travel community.
- Excellent relations with the Government, national airlines, civil aviation and airport authorities.
" > welcome.txt
```
- If You add a new user to the system his home dir should contain two extra files **user-info and welcome** .

### PoC
- Add a new User
	`[Yahia@localhost ~]$ sudo useradd newU`
- switch to the home dir of the new user.
	`[Yahia@localhost ~]$ su - newU `
- List all files in his home dir
```
[newU@localhost ~]$ ll -a
total 20
drwx------.  3 newU newU  118 Dec 10 03:18 .
drwxr-xr-x. 10 root root  119 Dec 10 03:18 ..
-rw-r--r--.  1 newU newU   18 Aug 29  2019 .bash_logout
-rw-r--r--.  1 newU newU  141 Aug 29  2019 .bash_profile
-rw-r--r--.  1 newU newU 2387 Dec 10 03:17 .bashrc
drwxr-xr-x.  4 newU newU   39 Sep 25 09:57 .mozilla
-rw-rw-r--.  1 newU newU   93 Dec 10 03:18 user-info.txt
-rw-rw-r--.  1 newU newU 1705 Dec 10 03:18 welcome.txt
```
- Cat the body of user-info file
```
[newU@localhost ~]$ cat user-info.txt 
Username : newU
Email : newU@guc.com
Mobile Number : +201259172948
Country : Egypt
Age is 50
```

### Conclusion 
- If any new user has been added to the system it will have two files by default.
---


## Design the System
- We have Six groups and each group contains three directories:
	- **IT**.
		1) Logs ==> In this folder the it would be able to track the logs and usres' activities.
		2) Infrastructue ==> other equipment necessary to make an IT system function according to the established needs and system "size" of the company.
		3) Functionality ==> refers to creating and maintaining operational applications; developing, securing, and storing electronic data that belongs to the organization.
	- **HR**.
		1) Screening ==> Applications.
		2) Recruting.
		3) Training.
	- **Clients**.
		1) Flights ==> book flights.
		2) Accomodation ==> Hotels
		3) Car Rentals
	- **Employees**.
		1) Flights ==> book flights.
		2) Accomodation ==> Hotels
		3) Car Rentals
	- **Egypt Air**.
		1) Flights ==> book flights.
		2) Accomodation ==> Hotels
		3) Car Rentals
	- **Qatar Air Ways**.
		1) Flights ==> book flights.
		2) Accomodation ==> Hotels
		3) Car Rentals

	![image](https://user-images.githubusercontent.com/61708947/209587680-2b532540-cc3f-4c77-b440-b28b6818919a.png)

- Each group contains at least 6 users.
- Each user contain at least two files user_info and welcome.
--- 
## Create Groups
- Instead of creating each group, create dirs and assign users manaully, I've create a bash script (**create_group.sh**) to automate this process.
```
#!/bin/bash

# Take the group_name is an input
read -p "Enter Group name " group_name

# create the group
sudo groupadd $group_name

# Take the directoreis from the user as an array
read -p "Enter the directories you want to create seperate by space" -a dirs

# loop over each Dir
for dir in ${dirs[@]}
do
        # make a dir
        mkdir $dir

        # change the group owner to this Group
        sudo chgrp -R $group_name $dir

done


# Take the users is an input list
read -p "Enter users that would be assigned for this Group seperated by a space " -a users

# loop over each user
for user in ${users[@]}

do
        # add users to the group
        sudo useradd -m  $user -g $group_name

        # add password to the current user
        sudo echo -en "${user}password\n${user}password\n" | sudo  passwd $user >> /dev/null
done
```
- We need to change  the permission for this file
```[Yahia@localhost Desktop]$ sudo chmod +x create_group.sh```

### PoC
- Create The groups , assign users, set passwords and make dirs.
- Create the IT Group
```
[Yahia@localhost Desktop]$ sudo ./create_group.sh 
Enter Group name IT
Enter the directories you want to create seperate by space Infrastructure Functionality Logs
Enter users that would be assigned for this Group seperated by a space Ya7ia Ali Yasser Badr Ahmed
```
- Check if the users has been added to the system.
```
[Yasser@localhost ~]$ tail -5 /etc/passwd
Ya7ia:x:1002:1004::/home/Ya7ia:/bin/bash
Ali:x:1003:1004::/home/Ali:/bin/bash
Yasser:x:1004:1004::/home/Yasser:/bin/bash
Badr:x:1005:1004::/home/Badr:/bin/bash
Ahmed:x:1006:1004::/home/Ahmed:/bin/bash
```
- Check if the users are assigned to the correct group.
```
[Yasser@localhost ~]$ id Ya7ia & id Ali & id Yasser & id Badr && id Ahmed 
uid=1005(Badr) gid=1004(IT) groups=1004(IT)
uid=1002(Ya7ia) gid=1004(IT) groups=1004(IT)
uid=1003(Ali) gid=1004(IT) groups=1004(IT)
uid=1004(Yasser) gid=1004(IT) groups=1004(IT)
uid=1006(Ahmed) gid=1004(IT) groups=1004(IT)
```
- Check if the dirs have been created with the correct owner.
```
[Yahia@localhost Desktop]$ ll -a
total 8
drwxr-xr-x.  6 Yahia Yahia   114 Dec 10 12:51 .
drwx------. 15 Yahia Yahia  4096 Dec 10 12:52 ..
-rwxrwxr-x.  1 Yahia Yahia   787 Dec 10 12:50 create_group.sh
drwxr-xr-x.  2 root  IT        6 Dec 10 12:51 Functionality
drwxr-xr-x.  2 root  IT        6 Dec 10 12:51 Infrastructure
drwxr-xr-x.  2 root  IT        6 Dec 10 12:51 Logs
[Yahia@localhost Desktop]$ 
```
As show above the owner group is **IT**.
- **Employees**

```
[Yahia@localhost Desktop]$ sudo ./create_group.sh 
Enter Group name Employees
Enter the directories you want to create seperate by space Flights Accomodation Cars
Enter users that would be assigned for this Group seperated by a space YahiaE AliE YasserE BadrE AhmedE
```
- Check if the users have been added to the system.
```
[Yahia@localhost Desktop]$ tail -5 /etc/passwd
YahiaE:x:1007:1005::/home/YahiaE:/bin/bash
AliE:x:1008:1005::/home/AliE:/bin/bash
YasserE:x:1009:1005::/home/YasserE:/bin/bash
BadrE:x:1010:1005::/home/BadrE:/bin/bash
AhmedE:x:1011:1005::/home/AhmedE:/bin/bash
```
- Check if the users are assigned to **Employee**

```
[Yahia@localhost Desktop]$ id YahiaE & id AliE & id YasserE & id BadrE && id AhmedE
uid=1009(YasserE) gid=1005(Employees) groups=1005(Employees)
uid=1007(YahiaE) gid=1005(Employees) groups=1005(Employees)
uid=1010(BadrE) gid=1005(Employees) groups=1005(Employees)
uid=1008(AliE) gid=1005(Employees) groups=1005(Employees)
uid=1011(AhmedE) gid=1005(Employees) groups=1005(Employees)
```
-  Check if the dirs have been created with the correct owner.
```
[Yahia@localhost Desktop]$ ll -a
total 8
drwxr-xr-x.  9 Yahia Yahia      161 Dec 11 11:39 .
drwx------. 15 Yahia Yahia     4096 Dec 10 12:52 ..
drwxr-xr-x.  2 root  Employees    6 Dec 11 11:39 Accomodation
drwxr-xr-x.  2 root  Employees    6 Dec 11 11:39 Cars
-rwxrwxr-x.  1 Yahia Yahia      787 Dec 10 12:50 create_group.sh
drwxr-xr-x.  2 root  Employees    6 Dec 11 11:39 Flights
drwxr-xr-x.  2 root  IT           6 Dec 10 12:51 Functionality
drwxr-xr-x.  2 root  IT           6 Dec 10 12:51 Infrastructure
drwxr-xr-x.  2 root  IT           6 Dec 10 12:51 Logs
```
- **HR**
```
[Yahia@localhost Desktop]$ sudo ./create_group.sh 
Enter Group name HR
Enter the directories you want to create seperate by space Screening Recruting Training
Enter users that would be assigned for this Group seperated by a space YahiaHR AliHR YasserHR BadrHR AhmedHR

```
-  Check if the users have been added to the system.
```
[Yahia@localhost Desktop]$ tail -5 /etc/passwd
YahiaHR:x:1012:1006::/home/YahiaHR:/bin/bash
AliHR:x:1013:1006::/home/AliHR:/bin/bash
YasserHR:x:1014:1006::/home/YasserHR:/bin/bash
BadrHR:x:1015:1006::/home/BadrHR:/bin/bash
AhmedHR:x:1016:1006::/home/AhmedHR:/bin/bash
```
- Check if the users have been added to **HR**.
```
[Yahia@localhost Desktop]$ id YahiaHR & id AliHR & id YasserHR & id BadrHR && id AhmedHR
uid=1015(BadrHR) gid=1006(HR) groups=1006(HR)
uid=1013(AliHR) gid=1006(HR) groups=1006(HR)
uid=1012(YahiaHR) gid=1006(HR) groups=1006(HR)
uid=1014(YasserHR) gid=1006(HR) groups=1006(HR)
uid=1016(AhmedHR) gid=1006(HR) groups=1006(HR)
```
- Check if the dirs have been created with the correct owner.
```
[Yahia@localhost Desktop]$ ll -a
total 8
drwxr-xr-x. 12 Yahia Yahia      196 Dec 11 11:47 .
drwx------. 15 Yahia Yahia     4096 Dec 10 12:52 ..
drwxr-xr-x.  2 root  Employees    6 Dec 11 11:39 Accomodation
drwxr-xr-x.  2 root  Employees    6 Dec 11 11:39 Cars
-rwxrwxr-x.  1 Yahia Yahia      787 Dec 10 12:50 create_group.sh
drwxr-xr-x.  2 root  Employees    6 Dec 11 11:39 Flights
drwxr-xr-x.  2 root  IT           6 Dec 10 12:51 Functionality
drwxr-xr-x.  2 root  IT           6 Dec 10 12:51 Infrastructure
drwxr-xr-x.  2 root  IT           6 Dec 10 12:51 Logs
drwxrwxr-x.  2 Yahia Yahia        6 Dec  9 05:19 Project
drwxr-xr-x.  2 root  HR           6 Dec 11 11:44 Recruting
drwxr-xr-x.  2 root  HR           6 Dec 11 11:44 Screening
drwxr-xr-x.  2 root  HR           6 Dec 11 11:44 Training
```
- **Clients**
```
[Yahia@localhost Desktop]$ sudo ./create_group.sh 
Enter Group name Clients
Enter the directories you want to create seperate by space FlightsC AccomodationC CarsC
Enter users that would be assigned for this Group seperated by a space YahiaC AliC YasserC BadrC AhmedC
```
- Check if the user are added to the system
```
[Yahia@localhost Desktop]$ tail -5 /etc/passwd
YahiaC:x:1017:1007::/home/YahiaC:/bin/bash
AliC:x:1018:1007::/home/AliC:/bin/bash
YasserC:x:1019:1007::/home/YasserC:/bin/bash
BadrC:x:1020:1007::/home/BadrC:/bin/bash
AhmedC:x:1021:1007::/home/AhmedC:/bin/bash
[Yahia@localhost Desktop]$ 
```
- Check if the user have been assigned to **Clients**
```
[Yahia@localhost Desktop]$ id YahiaC & id AliC & id YasserC & id BadrC && id AhmedC
uid=1020(BadrC) gid=1007(Clients) groups=1007(Clients)
uid=1017(YahiaC) gid=1007(Clients) groups=1007(Clients)
uid=1019(YasserC) gid=1007(Clients) groups=1007(Clients)
uid=1018(AliC) gid=1007(Clients) groups=1007(Clients)
uid=1021(AhmedC) gid=1007(Clients) groups=1007(Clients)
```
- Check if the dirs have been created with the correct owner.
```
[Yahia@localhost Desktop]$ ll -a
total 8
drwxr-xr-x. 15 Yahia Yahia      246 Dec 11 11:48 .
drwx------. 15 Yahia Yahia     4096 Dec 10 12:52 ..
drwxr-xr-x.  2 root  Employees    6 Dec 11 11:39 Accomodation
drwxr-xr-x.  2 root  Clients      6 Dec 11 11:48 AccomodationC
drwxr-xr-x.  2 root  Employees    6 Dec 11 11:39 Cars
drwxr-xr-x.  2 root  Clients      6 Dec 11 11:48 CarsC
-rwxrwxr-x.  1 Yahia Yahia      787 Dec 10 12:50 create_group.sh
drwxr-xr-x.  2 root  Employees    6 Dec 11 11:39 Flights
drwxr-xr-x.  2 root  Clients      6 Dec 11 11:48 FlightsC
drwxr-xr-x.  2 root  IT           6 Dec 10 12:51 Functionality
drwxr-xr-x.  2 root  IT           6 Dec 10 12:51 Infrastructure
drwxr-xr-x.  2 root  IT           6 Dec 10 12:51 Logs
drwxrwxr-x.  2 Yahia Yahia        6 Dec  9 05:19 Project
drwxr-xr-x.  2 root  HR           6 Dec 11 11:44 Recruting
drwxr-xr-x.  2 root  HR           6 Dec 11 11:44 Screening
drwxr-xr-x.  2 root  HR           6 Dec 11 11:44 Training

```
- **Qatar Air**
```
Yahia@localhost Desktop]$ sudo ./create_group.sh 
Enter Group name Qatar
Enter the directories you want to create seperate by space FlightQ AccomodationQ CarsQ
Enter users that would be assigned for this Group seperated by a space YahiaQ AliQ YasserQ AhmedQ BadrQ
```
- Check if the user are added to the system
```
[Yahia@localhost Desktop]$ tail -5 /etc/passwd
YahiaQ:x:1022:1008::/home/YahiaQ:/bin/bash
AliQ:x:1023:1008::/home/AliQ:/bin/bash
YasserQ:x:1024:1008::/home/YasserQ:/bin/bash
AhmedQ:x:1025:1008::/home/AhmedQ:/bin/bash
BadrQ:x:1026:1008::/home/BadrQ:/bin/bash
```
- Check if the user have been assigned to **Qatar**
```
[Yahia@localhost Desktop]$ id YahiaQ & id AliQ & id YasserQ & id BadrQ && id AhmedQ
uid=1024(YasserQ) gid=1008(Qatar) groups=1008(Qatar)
uid=1022(YahiaQ) gid=1008(Qatar) groups=1008(Qatar)
uid=1026(BadrQ) gid=1008(Qatar) groups=1008(Qatar)
uid=1023(AliQ) gid=1008(Qatar) groups=1008(Qatar)
uid=1025(AhmedQ) gid=1008(Qatar) groups=1008(Qatar)
```
- Check if the dirs have been created with the correct owner.
```
[Yahia@localhost Desktop]$ ll -a
total 12
drwxr-xr-x. 18 Yahia Yahia     4096 Dec 11 11:52 .
drwx------. 15 Yahia Yahia     4096 Dec 10 12:52 ..
drwxr-xr-x.  2 root  Employees    6 Dec 11 11:39 Accomodation
drwxr-xr-x.  2 root  Clients      6 Dec 11 11:48 AccomodationC
drwxr-xr-x.  2 root  Qatar        6 Dec 11 11:52 AccomodationQ
drwxr-xr-x.  2 root  Employees    6 Dec 11 11:39 Cars
drwxr-xr-x.  2 root  Clients      6 Dec 11 11:48 CarsC
drwxr-xr-x.  2 root  Qatar        6 Dec 11 11:52 CarsQ
-rwxrwxr-x.  1 Yahia Yahia      787 Dec 10 12:50 create_group.sh
drwxr-xr-x.  2 root  Qatar        6 Dec 11 11:52 FlightQ
drwxr-xr-x.  2 root  Employees    6 Dec 11 11:39 Flights
drwxr-xr-x.  2 root  Clients      6 Dec 11 11:48 FlightsC
drwxr-xr-x.  2 root  IT           6 Dec 10 12:51 Functionality
drwxr-xr-x.  2 root  IT           6 Dec 10 12:51 Infrastructure
drwxr-xr-x.  2 root  IT           6 Dec 10 12:51 Logs
drwxrwxr-x.  2 Yahia Yahia        6 Dec  9 05:19 Project
drwxr-xr-x.  2 root  HR           6 Dec 11 11:44 Recruting
drwxr-xr-x.  2 root  HR           6 Dec 11 11:44 Screening
drwxr-xr-x.  2 root  HR           6 Dec 11 11:44 Training
```
- **Egypt**
```
[Yahia@localhost Desktop]$ sudo ./create_group.sh 
Enter Group name Egypt
Enter the directories you want to create seperate by space FlightsEG AccomodationEG CarsEG
Enter users that would be assigned for this Group seperated by a space YahiaEG YasserEG AliEG BadrEG AhmedEG
```
- Check if the user are added to the system
```
[Yahia@localhost Desktop]$ tail -5 /etc/passwd
YahiaEG:x:1027:1009::/home/YahiaEG:/bin/bash
YasserEG:x:1028:1009::/home/YasserEG:/bin/bash
AliEG:x:1029:1009::/home/AliEG:/bin/bash
BadrEG:x:1030:1009::/home/BadrEG:/bin/bash
AhmedEG:x:1031:1009::/home/AhmedEG:/bin/bash
```
- Check if the user have been assigned to **Egypt**
```
[Yahia@localhost Desktop]$ id YahiaEG & id AliEG & id YasserEG & id BadrEG && id AhmedEG
uid=1030(BadrEG) gid=1009(Egypt) groups=1009(Egypt)
uid=1028(YasserEG) gid=1009(Egypt) groups=1009(Egypt)
uid=1029(AliEG) gid=1009(Egypt) groups=1009(Egypt)
uid=1027(YahiaEG) gid=1009(Egypt) groups=1009(Egypt)
uid=1031(AhmedEG) gid=1009(Egypt) groups=1009(Egypt)
```
- Check if the dirs have been created with the correct owner.
```
[Yahia@localhost Desktop]$ ll -a
total 12
drwxr-xr-x. 21 Yahia Yahia     4096 Dec 11 11:57 .
drwx------. 15 Yahia Yahia     4096 Dec 10 12:52 ..
drwxr-xr-x.  2 root  Employees    6 Dec 11 11:39 Accomodation
drwxr-xr-x.  2 root  Clients      6 Dec 11 11:48 AccomodationC
drwxr-xr-x.  2 root  Egypt        6 Dec 11 11:57 AccomodationEG
drwxr-xr-x.  2 root  Qatar        6 Dec 11 11:52 AccomodationQ
drwxr-xr-x.  2 root  Employees    6 Dec 11 11:39 Cars
drwxr-xr-x.  2 root  Clients      6 Dec 11 11:48 CarsC
drwxr-xr-x.  2 root  Egypt        6 Dec 11 11:57 CarsEG
drwxr-xr-x.  2 root  Qatar        6 Dec 11 11:52 CarsQ
-rwxrwxr-x.  1 Yahia Yahia      787 Dec 10 12:50 create_group.sh
drwxr-xr-x.  2 root  Qatar        6 Dec 11 11:52 FlightQ
drwxr-xr-x.  2 root  Employees    6 Dec 11 11:39 Flights
drwxr-xr-x.  2 root  Clients      6 Dec 11 11:48 FlightsC
drwxr-xr-x.  2 root  Egypt        6 Dec 11 11:57 FlightsEG
drwxr-xr-x.  2 root  IT           6 Dec 10 12:51 Functionality
drwxr-xr-x.  2 root  IT           6 Dec 10 12:51 Infrastructure
drwxr-xr-x.  2 root  IT           6 Dec 10 12:51 Logs
drwxrwxr-x.  2 Yahia Yahia        6 Dec  9 05:19 Project
drwxr-xr-x.  2 root  HR           6 Dec 11 11:44 Recruting
drwxr-xr-x.  2 root  HR           6 Dec 11 11:44 Screening
drwxr-xr-x.  2 root  HR           6 Dec 11 11:44 Training
```

---
## Handling Permissions
- Give all users access to read and execute **/home/Yahia** (The main user) to be able to list and cd into this Dir.
```
[Yahia@localhost home]$ chmod 705 Yahia
```
- List to verify the new permissions
```
[Yahia@localhost home]$ ll -a | grep Yahia 
drwx---r-x. 15 Yahia    Yahia     4096 Dec 12 12:39 Yahia
```
- No one outside the **IT** group can see the content if their dirs.
```
[Yahia@localhost Desktop]$ sudo chmod o= -R Logs/ ; sudo chmod o= -R Infrastructure/ ; sudo chmod o= -R Functionality/
[Yahia@localhost Desktop]$ ll -a | grep IT
drwxr-x---.  2 root  IT           6 Dec 10 12:51 Functionality
drwxr-x---.  2 root  IT           6 Dec 10 12:51 Infrastructure
drwxr-x---.  2 root  IT           6 Dec 10 12:51 Logs
```
- Let **Ya7ia** be the IT head, so I'll change dirs owner from root --> Ya7ia, Now Ya7ia is the only user that can add or delete files. 
```
[Yahia@localhost Desktop]$ sudo chown Ya7ia -R Logs/; sudo chown Ya7ia -R Infrastructure/; sudo chown Ya7ia -R Functionality/
[Yahia@localhost Desktop]$ ll -a | grep IT
drwxr-x---.  2 Ya7ia IT           6 Dec 10 12:51 Functionality
drwxr-x---.  2 Ya7ia IT           6 Dec 10 12:51 Infrastructure
drwxr-x---.  2 Ya7ia IT           6 Dec 10 12:51 Logs
```
- Give **Ya7ia** the root's permission so, he can give other IT members the requiered permission, Accorfding to their rules.
- edit the **/etc/sudoes** file 
```[Yahia@localhost Desktop]$ sudo vim /etc/sudoers```
- Add Ya7ia and give him all permissions.
```
root    ALL=(ALL)       ALL
Yahia  ALL=(ALL)     ALL
Ya7ia All=(ALL)    ALL
```

- For **Egypt** & **Qatar**
- Make **YahiaQ** and **YahiaEG** the owner of the dirs
```
[Yahia@localhost Desktop]$ sudo chown YahiaQ *Q
[Yahia@localhost Desktop]$ ll -a | grep Q
drwxr-x---+  2 YahiaQ  Qatar         6 Dec 11 21:52 AccomodationQ
drwxr-x---+  2 YahiaQ  Qatar         6 Dec 11 21:52 CarsQ
drwxr-x---+  2 YahiaQ  Qatar         6 Dec 11 21:52 FlightQ
[Yahia@localhost Desktop]$ sudo chown YahiaEG *EG
[Yahia@localhost Desktop]$ ll -a | grep Egypt
drwxr-x---+  2 YahiaEG Egypt         6 Dec 11 21:57 AccomodationEG
drwxr-x---+  2 YahiaEG Egypt         6 Dec 11 21:57 CarsEG
drwxr-x---+  2 YahiaEG Egypt         6 Dec 11 21:57 FlightsEG

```
- We will allow **Employees** to be able to read and execute the files and dirs from **Egypt** and **Qatar** by setting an **ACL** because we don't want to change the group owner (Assuming The Employees will take data uploaded by the **Egypt** and **Qatar** and add it to the database).
```
[Yahia@localhost Desktop]$ sudo setfacl -m g:Employees:r-x AccomodationEG/ AccomodationQ/ CarsEG/ CarsQ/ FlightsEG/ FlightQ/
[Yahia@localhost Desktop]$ sudo chmod o= -R AccomodationEG/ CarsEG/ FlightsEG/ AccomodationQ/ FlightQ/ CarsQ/
```
- Check if the **ACL** is applied using **getfacl**
```
[Yahia@localhost Desktop]$ getfacl CarsQ/
# file: CarsQ/
# owner: root
# group: Qatar
user::rwx
group::r-x
group:Employees:r-x
mask::r-x
other::---
```
- **HR**
- No one outside the **HR** group can see the content if their dirs.
```
[Yahia@localhost Desktop]$ sudo chmod o= -R Recruting/ Screening/ Training/
[Yahia@localhost Desktop]$ ll -a | grep HR
drwxr-x---.  2 root  HR           6 Dec 11 21:44 Recruting
drwxr-x---.  2 root  HR           6 Dec 11 21:44 Screening
drwxr-x---.  2 root  HR           6 Dec 11 21:44 Training
```
- I will make **YahiaHR** the dirs' owner
```
[Yahia@localhost Desktop]$ sudo chown YahiaHR Recruting/ Screening/ Training/
[Yahia@localhost Desktop]$ ll -a | grep HR
drwxr-x---.  2 YahiaHR HR           6 Dec 11 21:44 Recruting
drwxr-x---.  2 YahiaHR HR           6 Dec 11 21:44 Screening
drwxr-x---.  2 YahiaHR HR           6 Dec 11 21:44 Training

```
- **YahiaHR** can create new files in the system.
- **Employees**
- I will prevent **clients , Egypt and Qatar**  from accesing the directories.
```
[Yahia@localhost Desktop]$ sudo setfacl -m g:Egypt:--- Accomodation/ Cars/ Flights/
[Yahia@localhost Desktop]$ sudo setfacl -m g:Qatar:--- Accomodation/ Cars/ Flights/
[Yahia@localhost Desktop]$ sudo setfacl -m g:Clients:--- Accomodation/ Cars/ Flights/

```
- Check the ACL
```
[Yahia@localhost Desktop]$ getfacl Accomodation/
# file: Accomodation/
# owner: root
# group: Employees
user::rwx
group::r-x
group:Clients:---
group:Qatar:---
group:Egypt:---
mask::r-x
other::r-x
```
- **Clients**
- Add a sticky bit, so no clinet can delete or rename files of other clintes.
```
[Yahia@localhost Desktop]$ sudo chmod 2775 *C
[Yahia@localhost Desktop]$ ll -a | grep Cl
drwxrwsr-x+  2 root    Clients       6 Dec 11 21:48 AccomodationC
drwxrwsr-x+  2 root    Clients       6 Dec 11 21:48 CarsC
drwxrwsr-x+  2 root    Clients       6 Dec 11 21:48 FlightsC
```
- Prevent **Egypr and Qatar** from accessing any information related to our clients.
```
[Yahia@localhost Desktop]$ sudo setfacl -m g:Egypt:--- AccomodationC/ CarsC/ FlightsC/
[Yahia@localhost Desktop]$ sudo setfacl -m g:Qatar:--- AccomodationC/ CarsC/ FlightsC/
```
- Check The ACL
```
[Yahia@localhost Desktop]$ getfacl CarsC/
# file: CarsC/
# owner: root
# group: Clients
user::rwx
group::r-x
group:Qatar:---
group:Egypt:---
mask::r-x
other::r-x
```
 - To sum up the permissions
Group Dirs | Allow | Deny 
-- | -- |--
IT| None|All
Qatar | Employees | All
Egypt | Employees | All
HR | None | All
Employees | All | Clinets , Egypt & Qatar
Clinets | All | Egypt & Qatar


 --- 
## Fetch online Data
- I'm Going to use python to retrive some online data.
- First I'm going to fetch the airlines that had a contract with the Agency using **RapidApi**.
- `[Yahia@localhost Desktop]$ vim get_AirLines.py`
```
# import the requierd libraries
import json
import pandas as pd

# URL To get the airlines list
url = "https://flight-radar1.p.rapidapi.com/airlines/list"

# Headers which contain the API Key
headers = {
"X-RapidAPI-Key": "e8ceadd810msh0048b96168083d5p170c78jsnd21f2b796cf9",
"X-RapidAPI-Host": "flight-radar1.p.rapidapi.com"
}

# request the url and get the response
response = requests.request("GET", url, headers=headers)

# format the response from text to json
json_response = json.loads(response.text)['rows']

# create a dataframe
df = pd.DataFrame.from_records(json_response , index = ['Name' , 'Code' , 'ICAO'])

# save the dataframe as a csv File
df.to_csv('Flights/AirLines.csv')
```
- Fetch the Airports in the world 
```
# import the requierd libraries

import json
import pandas as pd
import requests

# URL To get the airlines list
url = "https://flight-radar1.p.rapidapi.com/airports/list"

# Headers which contain the API Key
headers = {
"X-RapidAPI-Key": "e8ceadd810msh0048b96168083d5p170c78jsnd21f2b796cf9",
"X-RapidAPI-Host": "flight-radar1.p.rapidapi.com"
}

# request the url and get the response
response = requests.request("GET", url, headers=headers)

# format the response from text to json
json_response = json.loads(response.text)['rows']

# create a dataframe
df = pd.DataFrame.from_records(json_response)

# save the dataframe as a csv File
df.to_csv('Flights/AirPorts.csv')
```

---
## User interface
- using python and XML.
![image](https://user-images.githubusercontent.com/61708947/209587694-fd7d9f43-5ead-415a-9ad7-58b8be912242.png)

![image](https://user-images.githubusercontent.com/61708947/209587699-d66353f2-2a95-4520-95c3-ef0ee7a93f70.png)

![image](https://user-images.githubusercontent.com/61708947/209587706-f5713b3b-b36e-4aea-9cc5-925f581d28b6.png)

![image](https://user-images.githubusercontent.com/61708947/209587701-bd14b0c4-601c-4c6a-82c5-77cc98d004f4.png)

![image](https://user-images.githubusercontent.com/61708947/209587730-d4a1c765-1142-4afa-ad8a-7923ae51e353.png)

--- 
## Bonus
- Run a script periodically to get new data from the internet.
- I'm going to use **Cron** service.
```
[Yahia@localhost ~]$ systemctl status crond.service 
● crond.service - Command Scheduler
   Loaded: loaded (/usr/lib/systemd/system/crond.service; enabled; vendor preset: enabled)
   Active: active (running) since Tue 2022-12-13 13:36:16 EET; 4 days ago
 Main PID: 1251 (crond)
    Tasks: 1 (limit: 11355)
   Memory: 14.4M
   CGroup: /system.slice/crond.service
           └─1251 /usr/sbin/crond -n

Warning: Journal has been rotated since unit was started. Log output is incomplete or unavailable.
[Yahia@localhost ~]$ 
```
- The service is installed, by default enabled and active.
- Say I need to check if the airlines or airports have changes so i'm going to run the two scripts that will fetch the requierd information.
```
[Yahia@localhost ~]$ crontab -e
```
- inside the vim editor add the following two lines
```
0 0 * * * python3 /home/yahia/Desktop/get_AirPorts.py

0 0 * * * python3 /home/yahia/Desktop/get_AirLines.py
```
- The two scripts will be run everyday at **00:00**.

---
## Summary


![image](https://user-images.githubusercontent.com/61708947/209587740-db9bb5d4-dd5d-4754-90d1-688d80fb8fd8.png)

![image](https://user-images.githubusercontent.com/61708947/209587855-9388050d-d611-481b-a11c-0aa0d4a671f2.png)
