<div align="center">
    <h1>DIS Project</h1>
    <h2>Authors</h2>
    <p>Lucas L (zdw760)</p>
    <p>Magnus E (rqv811)</p>
    <p>Malthe J (xsf318)</p>
    <p>Snorre A (lkx526)</p>
</div>

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
nix --extra-experimental-features "flakes nix-command" run .
```


## Provided Test Info
### User account with sell permission
We provide the following test account(s) if unable to create your own login.


<div>
    <table style="text-align: center;">
        <thead>
            <tr>
                <th style="width: 33%;">Email</th>
                <th style="wdith: 33%;">Username</th>
                <th style="width: 33%;">Password</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>test1@di.ku.dk</td>
                <td>Test1</td>
                <td>test1</td>
            </tr>
            <tr>
                <td>test2@di.ku.dk</td>
                <td>Test2</td>
                <td>test2</td>
            </tr>
        </tbody>
    </table>
</div>

When ran with `--debug` the website will always automatically log you in as this user.
Additionally, all the randomly generated users have the same password of "1234".

### Credit Card
We provide the following debug Credit Cards for checkout.

Source: [Stripe](https://docs.stripe.com/testing)

<div>
    <table style="text-align: center;">
        <thead>
            <tr>
                <th style="width: 25%;">Card Type</th>
                <th style="width: 25%;">Card Number</th>
                <th style="width: 25%;">CVC</th>
                <th style="width: 25%;">Expiration Date</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Visa Credit</td>
                <td>4242 4242 4242 4242</td>
                <td>Any 3 digits</td>
                <td>Any future date</td>
            </tr>
            <tr>
                <td>UnionPay (19 digit)</td>
                <td>6205 5000 0000 0000 004</td>
                <td>Any 3 digits</td>
                <td>Any future date</td>
            </tr>
        </tbody>
    </table>
</div>

## Notes
The Web-App is NOT optimised in any way, shape or form for mobile devices, it's intended use is PC or Laptop only.

## ER Diagram
![ER Diagram](ER%20Diagram.png)

## AI Declaration
<object data="https://github.com/LucasFromDK/DIS/blob/main/AI_Declaration.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="https://github.com/LucasFromDK/DIS/blob/main/AI_Declaration.pdf">
        <p>This browser does not support embedded PDFs. Please open the PDF to view it: <a href="https://github.com/LucasFromDK/DIS/blob/main/AI_Declaration.pdf">Open PDF</a>.</p>
    </embed>
</object>