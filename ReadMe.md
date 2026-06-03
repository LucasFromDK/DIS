<h1 align="center">DIS Project</h1>

## Requirements
### Documentation
- Your database model (E/R diagram)
- How to compile your web-app from source (incl. scripts to initialize the database)?
- How to run and interact with your web-app?
- Include an AI declaration (also no usage must be declared)

### Web-App
- Should interact with the database via SQL (at least one INSERT or UPDATE or DELETE or SELECT statement)
- Should perform regular expression matching or context-free grammar parsing
- Bonus points for use of views, triggers, stored procedures, but not required

## How to run
### Requirements
+ `python >= 3.14`
+ `flask >= 3.1.2`
OR
+ `docker`
---
To run the project use:
```bash
flask run
```

To enter debug mode with AutoSignin enabled for test account use:
```bash
flask run --debug
```

To run with docker use
```sh
docker load -i docker-image.tar.gz
docker run --rm \
    -p 5000:5000 \
    -it ku-dis-flask-project \
    dis-flask-project \
    --debug \
    --host 0.0.0.0
```

## Building docker image
### Requirements
+ `nix`
---
run
```bash
nix --extra-experimental-features "flakes nix-command" build .
```

## Notes
The Web-App is NOT optimised in any way, shape or form for mobile devices, it's intended use is PC or Laptop only.

## Provided Test Account(s)
We provide the following test account(s) if unable to create your own login.


|Email|Username|Password|
|-----|--------|--------|
|test@di.ku.dk|test|test1234|


when ran with `--debug` the website will always automatically log you in as this user