# DigitalOcean Automation

Create DigitalOcean droplets according to input configuration.
Run particular scripts in particular nodes according to input configuration.


## Installation

Git clone the repository. Python 3.7

```bash
git clone https://github.com/aserhatdemir/digitalocean.git

cd digitalocean
pip install -r requirements.txt
```

## Usage
Save the configuration file as "input.json". [Sample](https://github.com/aserhatdemir/digitalocean/blob/master/input_example.json) input file here. Get Add your own DigitalOcean API token.
```bash
python3 application.controller.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://github.com/aserhatdemir/digitalocean/blob/master/LICENSE)
