clear
sudo systemctl stop myapi
sudo ./install.sh
sudo systemctl daemon-reload
sudo systemctl start myapi
systemctl status myapi
