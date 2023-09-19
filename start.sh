if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/TeamKazukai/wedtesting.git /
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /wedtesting
fi
cd /wedtesting
pip3 install -U -r requirements.txt
echo "Starting wednesday...."
python3 bot.py
