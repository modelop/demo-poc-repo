PUBLIC_HOSTNAME=`curl http://169.254.169.254/latest/meta-data/public-hostname`

echo $PUBLIC_HOSTNAME

sed "s/localhost/$PUBLIC_HOSTNAME/g" index.html.template > index.html

nohup sudo python -m SimpleHTTPServer 80 &
