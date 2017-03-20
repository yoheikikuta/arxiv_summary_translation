# arxiv summary translation
Chekc the arxiv summaries in your favorite language on jupyter notebook.<br>
Translations will be executed using Google Cloud Translation API (You can select Neural Machine Translation or old version).

## Prerequisites
- Google Cloud Translate API premium edition
  - Sigh up for premium edition on https://services.google.com/fb/forms/translationapi-beta/
  - Get your own credentials json file and put it in the root directory of this repository
- Docker environment

## Set up
Clone the repository and set your own credentials file.
```
$ git clone https://github.com/yoheikikuta/arxiv_summary_translation.git
$ cd arxiv_summary_translation
$ mv /PATH/TO/YOUR/OWN/credentials.json .
```
Build the docker image (change the tag as you like).
```
$ docker build -t arxiv_translate .
```
Create the container (change the host port or name as you like).
```
$ docker run -it -p 8888:8888 -v $PWD:/root/work --name arxiv_translate arxiv_translate /bin/bash
```

## Run the translation script
Launch the jupyter notebook.
```
(in the container) $ cd /root/work
(in the container) $ jupyter notebook --ip="*"
```
Then access `localhost:8888` or `<host ip of your docker machine>:8888` on your browser.
Run the cells in `arxiv_translator.ipynb` from top.
