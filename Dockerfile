FROM nikolaik/python-nodejs:python3.10-nodejs14

COPY requirements.txt ./

RUN apt-get update && apt-get install -y curl unzip

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip && ./aws/install

RUN npm install -g aws-cdk@latest
RUN pip3 install -r requirements.txt