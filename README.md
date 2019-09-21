# garbage_cls
A project to build everything around garbage classification advisor.

---

Updates
- A python eatable catalog for Shanghai garbage classification rules, from guidebook.
- An image scraper to collect training data for ongoing work.
- An EDA and preprocessing images before feeding model.
- First version classifier on [可回收物, 有害垃圾, 湿垃圾, 干垃圾] done.
    - Inception V3 to do the transfer learning.
    - 30 epoches and one average global pooling 2D and without dropout.
    - Now the accuracy is *30%*.

---

Todo
- Scrape more data.
- Build the backend to provide a service.
    - Accept upload image and return class name.
    - Flask.
- Build a transfer learning model on first level.
    - Fine tune the model.
- Build a ransfer learning model on second level.
---

Done
- Completed collecting data from google.
- Done cleansing suffixes of image data files.
- Use "sparse_categorical_crossentropy" instead of "categorical_crossentropy" to fix the loss not change problem. As we are predicting 4 classes of level 0 labels.
- First version classifier on [可回收物, 有害垃圾, 湿垃圾, 干垃圾] has been trained. 
