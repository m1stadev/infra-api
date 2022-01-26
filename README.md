# Infra-API

[![License](https://img.shields.io/github/license/m1stadev/infra-api)](https://github.com/m1stadev/infra-api/blob/master/LICENSE)
[![Stars](https://img.shields.io/github/stars/m1stadev/infra-api)](https://github.com/m1stadev/infra-api/stargazers)
[![LoC](https://img.shields.io/tokei/lines/github/m1stadev/infra-api)](https://github.com/m1stadev/infra-api)

An API for interacting with infrared devices, utilizing [lirc](https://www.lirc.org). I made this to control a space heater I own, but this can be easily adapted for other IR devices.

## Running
To host, follow these steps:

1. Create a virtual env and install dependencies:

        python3 -m venv --upgrade-deps env && source env/bin/activate
        pip3 install -Ur requirements.txt

2. Start your instance:

        gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80

## API Documentation
API documentation can be found at `http://{IP}:80/docs`, replacing `{IP}` with either `localhost` or the IP address of the device you're hosting Govee API on.

## Support

For any questions/issues you have, join my [Discord](https://m1sta.xyz/discord).
