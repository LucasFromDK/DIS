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
To run the project use:
```bash
flask run
```

To enter debug mode with AutoSignin enabled for test account use:
```bash
flask run --debug
```

## Notes
The Web-App is NOT optimised in any way, shape or form for mobile devices, it's intended use is PC or Laptop only.

## Provided Test Account(s)
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
            <td>test@di.ku.dk</td>
            <td>test</td>
            <td>test1234</td>
            </tr>
        </tbody>
    </table>
</div>