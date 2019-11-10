# garbage_cls
A project to build everything around garbage classification advisor.  
构建一个生活垃圾分类助手。

---
## Project Structure -- 项目结构 
    .
    ├── gc_api                  # Backend RESTful APIs, based on Flask.
    ├── simple-citizen          # Frontend interface, based on React.
    ├── models                  # Models and models configuration file folder.
    ├── notebooks               # Jupyter notebooks for oneoff actions (images pre-processing, model training, etc).
    └── spiders                 # Data collector for collecting images of garbages.

---
## Demo
Browser may prompt warning saying this site is not secure, you can click "Advanced" and proceed to visit the site.    
https://122.51.49.45
---
## What is it?
- Currently, the taxonomy is base on Shanghai guideline. 4 kinds of domestic rubbish, which are [可回收物, 有害垃圾, 湿垃圾, 干垃圾]. 
    - A taxonomy on Guangzhou guideline is coming.
- Model is building on transfer learning based on Inception V3 and MobileNet V2.
    - Current Accuracy is around 80%. 
    - Currently it's using top layers as classifier labels. Next is to train a model on recognize the object itself, such as wasted paper, wasted can, food waste, etc.
- A Flask based RESTful backend, accepting image and return a classification result.
- A React based frontend, serving the API as a Web application. Allowing user to take a photo and upload and display the result.
