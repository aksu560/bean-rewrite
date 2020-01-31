Bean machine's rewrite. Eventual documentation

**Set-up**
- Install pre-requisites. List might come eventually. Vagrant and Virtualbox for now. Python will tell you the rest when you try to run the bot
- Run set-up.sh with your discord bot's key as an argument. So if your key was 1234, `./set-up.sh 1234`
- Run `./bean.sh`. This will boot up the vagrant machine, and run the bot inside it headlessly. If you don't want the bot to run headlessly (maybe you want to see stdout) give the script argument `dev`, like so `./bean.sh dev` If you have no idea what any of this means, just run `./bean.sh` and youll be fine.
