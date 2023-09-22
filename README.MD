# Nordvpn Account Checker
## Includes Windows executable

22/09/23 - Currently not working on Windows due to undetected_chromedriver problems with latest Chrome update (117).

Checks a combolist of existing nordvpn accounts, acquired by the usual suspect means, to determine which accounts are valid.

Can be run in Linux distributions (tested in Kali/Debian only), or by downloading the mega-bloated Windows executable. Make sure to include a "nord.txt" combolist in the program's path.

Install requirements with:

```pip install -r requirements.txt```

Run in terminal:

```python3 nordvpn.py``` (Debian-based distributions)

or download and run the executable for windows.
