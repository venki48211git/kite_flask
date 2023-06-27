# marketdepth_flask

This code is to show the market buy order, ltp,O=L,UC for certain stocks in symbol.csv and using the kite ext. 

Now we have added the diffrent page for fno stocks O=L.

![image](https://github.com/suresh-n/marketdepth_flask/assets/17276643/804a04ff-2136-4ae0-bab7-a39b8e8e508c)

![image](https://github.com/suresh-n/marketdepth_flask/assets/17276643/83a4b6c4-c10f-4b4c-80c5-33d72b062719)


### How to make this work in container. 

1. Clone this repo. 
2. Add kite login into config.py
3. Now build the container image using below command , 
>  docker build -t image name .
4. Once the build complete just run the container using the image. 
>  docker run -d -p 5000:5000 imagename
5. Now go to browser and open http://127.0.0.1:5000
