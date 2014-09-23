# snapitforward

Snapchat a pic to @snapitforward and get a pic from the last person who sent one.

## Dependencies

### OSX

```
brew install pip
pip install requests
easy_install pycrypto
```

### Debian

```
sudo apt-get install pip
pip install requests
sudo apt-get install python-crypto
```

## Run

```
git clone https://github.com/kylemcdonald/snapitforward.git
echo '{"username":"username","password":"password"}' > credentials.json
cd snapitforward
python snapitforward.py
```