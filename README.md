# Lucky-Draw-Game
A service which allows users to get Lucky Draw Raffle tickets and use one lucky draw raffle ticket to participate in a lucky draw game.

## Features
* An API for register and login.
* An API which allow users to get the raffle tickets.
* An API which shows the next Lucky Draw Event timing & the corresponding reward.
* An API which allows users to participate in the game.
* An API which lists all the winners of all the events in the last one week.
* An API which computes the winner for the event and announce the winner.

## Setup Guide
1. Python v3.8.7
2. Clone this repository.

    ```
    git clone https://github.com/hkhats95/Lucky-Draw-Game.git
    ```

3. Create a virtural environment and activate it.

    ```
    python -m venv env
    ```

    ```
    env\Scripts\activate.bat
    ```

4. Install the requirements.

    ```
    pip install -r requirements.txt
    ```

5. Thats all Folks.


## How to Run
1. It is recommneded to create super user from command line to access `/admin` portal.

    ```
    python manage.py createsuperuser
    ```

2. Run the server.

    ```
    python manage.py runserver
    ```

## Points to be noted.
* Right now you can create lucky draw events from the admin portal only.
* You must know the id of the lucky draw event you want to end and declare winners.

## To Do
* An API to create new events by admin user.
* An API to show the events that needs to be closed.

## Documentation
Read the [docs].



[docs]: https://documenter.getpostman.com/view/13943044/TzK17amm