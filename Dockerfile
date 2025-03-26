
FROM ubuntu:22.04

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y apache2 git docker.io python3-pip unzip && \
    pip3 install gdown

WORKDIR /home/user/
RUN git clone https://github.com/FranGoncal/ProjetoLEI/ ProjetoLEI

WORKDIR /home/user/ProjetoLEI/Website
RUN gdown "https://drive.google.com/uc?export=download&id=1Fx2nGbXlamnzuwETZfkyHSpuU3tNfzpX" -O models.zip && \
    unzip models.zip -d models && \
    rm models.zip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]