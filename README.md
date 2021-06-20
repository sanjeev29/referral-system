# Referral System

This repository contains code for Referral System.

## Usage

Clone repository and switch to `develop` branch. Follow the steps show below:

1. Copy and rename .env.template file to .env with appropriate environment values.

2. Make sure docker and docker-compose are installed on your system.

3. Build docker image with the following command:
    ```
   docker-compose build
   ```

4. Run docker containers in background using:
    ```
   docker-compose up -d
   ```

5. Apply model migrations and create django superuser with below commands inside
   `referral-system_web_1` container
    ```
   a. docker exec -it referral-system_web_1 bash
   b. python manage.py migrate
   c. python manage.py createsuperuser
   ```

6. Access the django admin at `http://localhost:8000/admin` with the superuser credentials created in step 5.

7. Click on add next to the Profiles section, set the `user` field to admin and save it.


## API Usage

1. `api/v1/invitations/` (POST) - This API is used to send invite link to a user's email.

2. `api/v1/invitations/` (GET) - This API returns all the invitations sent out by the current user logged in.

3. `api/v1/signup/?code=<string>` (POST) - The invite link sent to the mail can be used to signup.

4. `api/v1/referred_users/` (GET) - This API returns all the users who have signed in using the referral link sent by 
   the current user logged in.
   
### Note 

The `invitations/` and `referred_users/` APIs use Basic Authentication i.e., pass the username and password
of the user in the header as a key-value pair.

## Reference

Postman collection - https://documenter.getpostman.com/view/13024503/TzeZE6mZ
