# Linux

- Fedora linux disable suspend
  - `sudo vim /etc/systemd/logind.conf`
  - Do the following change in the file
    ```
    HandleSuspendKey=ignore`
    HandleLidSwitch=ignore
    HandleLidSwitchExternalPower=ignore
    HandleLidSwitchDocked=ignore
    ```
  - Restart the logind with `sudo systemctl restart systemd-logind`
  - Now the laptop will not suspend when the lid is closed
