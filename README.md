1. Mount your source storage to /mnt/source and destination storage to /mnt/destination in Linux/Ubuntu machine
2. Install rsync eg. for Linux: $ sudo yum install rsync -y
3. run new screen: $ screen -S rsync
4. In the screen run: $ sudo su
5. Launch python script in the screen: $ python3 main.py
6. Observe or detach from screen to let migration finish in the background
