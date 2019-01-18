t-SNE for FaceNet

link to FaceNet repo: https://github.com/davidsandberg/facenet
link to lapjv repo: https://github.com/src-d/lapjv
Installation Python Libraries:

tensorflow (1.4.0) scipy (0.17.0) scikit-learn (0.19.1) Opencv (2.4.9.1) lapjv (link ^)

Usage:

To model folder add
https://drive.google.com/file/d/1R77HmFADxe87GmoLwzfgMu_HY0IhcyBz/view

Add photos to folder train_img

Run scrypt Go.py - that will get faces from images and export them to aling_img directory
Now you can run scrypt t-SNE.py 

If you want you can add to folder align_img other photos, but remember they have to have size 160x160

IMPORTANT: Number of photos in align_img dir must be square of some natural number.

Good luck! :)