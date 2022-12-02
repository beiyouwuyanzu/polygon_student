curl https://req.wangyaqi.site:8080/get_polygon/1234
if [ $? -ne 0 ]; then
    echo "check failed at `date`"
    ps aux | grep server_polygon.py | grep -v grep | awk '{print $2}' | xargs kill -9
    nohup python3 server_polygon.py &
    echo "restart done!"
else
    echo "healthy at `date`"
fi
