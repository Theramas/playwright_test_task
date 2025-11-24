# How to start
Install requirements from requirements.txt
```pip install -r requirements.txt```
```playwright install```

Run tests with
```pytest tests```
```pytest tests/test_login.py```

Tests marked with ```pytest.mark.auth``` will ask you to complete manual login on first run, in order to generate state file.
State file will allow to skip re-captcha in consequent runs. State files are browser-specific.
