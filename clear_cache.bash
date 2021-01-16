sudo /etc/init.d/mysql stop
sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
sudo /etc/init.d/mysql start
