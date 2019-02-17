
# munsearch

#### Summary
Directory search tools with simple multi-threading
It was made in `python3`.


#### Introduce
1\. Thread number control method. (File "app.py", line 65 ~ 66)
```python
sem = threading.Semaphore(20) # Threads running concurrently number
thread_num = 100 # Thread number
```

2\. How to use

```shell
$ python app.py [url]
```

##### Example
```shell
$ python app.py http://munsiwoo.kr
$ python app.py http://withphp.com
```

#####  Result example
```shell
$ python app.py http://withphp.com
301 http://withphp.com/static
200 http://withphp.com/robots.txt
403 http://withphp.com/.htaccess
403 http://withphp.com/.htpasswd
403 http://withphp.com/index.phps
End
```