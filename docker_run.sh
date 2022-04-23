docker build -t aws-cdk-python-docker .
# shellcheck disable=SC2086
docker run --rm -itd -v `pwd`:/app -v ${HOME}/.aws/credentials:/root/.aws/credentials:ro aws-cdk-python-docker