FROM python:3.7-alpine
ENV PYTHONDONTWRITEBYTECODE 1
RUN apk add --no-cache --update build-base ca-certificates make
RUN apk --no-cache add \
    libjpeg \
    zlib \
    zlib-dev \
    libwebp \
    openjpeg \
    jpeg-dev \
    postgresql-libs \
    postgresql-dev \
    ncurses-dev \
    readline-dev \
    gettext \
    bash \
    gcc \
    musl-dev \
    libffi-dev \
    cairo-dev \
    pango-dev \
    gdk-pixbuf \
    ttf-freefont

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

EXPOSE 8000