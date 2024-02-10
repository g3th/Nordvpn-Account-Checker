# Nordvpn Account Checker
## Linux Only

### How to Install:

https://github.com/g3th/Nordvpn-Account-Checker/assets/74467654/89d0a0c1-45e2-4d93-82c0-83067321fab2

To remove current google version (and subsequently downgrade as shown above):

```sudo apt remove google-chrome-stable```

Checks a combolist of existing nordvpn accounts, acquired by the usual suspect means, to determine which accounts are valid.

Can be run in Linux distributions. Tested in Kali (Bare-metal), Debian and Ubuntu (Vbox). Make sure to include a "nord.txt" combolist in the program's path.

Install requirements with:

```pip install -r requirements.txt```

Run in terminal:

```python3 nordvpn.py``` (Debian-based distributions, Windows Powershell/cmd line).
