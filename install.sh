cp myapi.service /etc/systemd/system/

mkdir -p /opt/MyAPI/
cp myapi.py /opt/MyAPI

mkdir -p /opt/MyAPI/static
cp static/* /opt/MyAPI/static

mkdir -p /opt/MyAPI/templates
cp templates/* /opt/MyAPI/templates
