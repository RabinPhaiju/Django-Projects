# tempates/registration - 

- Built-in URLs: Fastest setup and automatically configured URLs for authentication (like login, logout, and password management). 
- These views use default templates unless you override them.
- This will automatically give you the following paths without any extra configuration:

    /accounts/login/
    /accounts/logout/
    /accounts/password_change/
    /accounts/password_change/done/
    /accounts/password_reset/
    /accounts/password_reset/done/
    /accounts/reset/<uidb64>/<token>/
    /accounts/reset/done/

- if there url html are not provided. Django will try to use default forms.(If it have.)