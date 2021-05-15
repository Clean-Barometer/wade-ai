FROM python:3.6

ENV FLASK_APP=app
ENV FLASK_DEBUG=1

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt
RUN mkdir weights
RUN wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1QdJhisbSDRTHgxASgJzgo3P1m1xC4qzz' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1QdJhisbSDRTHgxASgJzgo3P1m1xC4qzz" -O weights/mask_rcnn_trash_0200_030519_large.h5 && rm -rf /tmp/cookies.txt
RUN wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=17wp_QODQNeEnRCKyqjTl8kfISzASbVbD' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=17wp_QODQNeEnRCKyqjTl8kfISzASbVbD" -O weights/mask_rcnn_coco.h5 && rm -rf /tmp/cookies.txt
CMD ["gunicorn","wsgi:app"]