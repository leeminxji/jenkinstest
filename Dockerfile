FROM nvidia/cuda:10.2-cudnn7-runtime-ubuntu18.04

RUN apt-get update \
    && apt-get remove --purge -y python3.7

# Install Python
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3.8 python3-pip python3.8-dev python3.8-venv

# RUN : \
#     && apt-get update \
#     && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
#         software-properties-common \
#     && add-apt-repository -y ppa:deadsnakes \
#     && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
#         python3.8-venv \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/* \
#     && :

RUN python3.8 -m venv /venv
ENV PATH=/venv/bin:$PATH
# RUN apt-get install -y python3.8 \
#     && ln -s /usr/bin/python3.8 /usr/bin/python3 \
#     && apt-get install python3-pip -y
RUN python -V
RUN pip -V

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt




