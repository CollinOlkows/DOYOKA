# DOYOKA 2

A python based command and control server and agent. Do You Know Amitesh?

NOTE: This was made for educational purposes and for self monitoring machines I own, please only use this on machines you have permission to access

## Installation

Install and run the corresponding files, bot for client, server for server

Note: When setting up the server, ensure you run the add admin python file to create an admin account.
Additionally, change the config "password" to the password for your admin account (Currently it is set to 'password' which is a 
publicly visible in the readme as its meant to be changed)

Additionally, you should be updating the config to reflect the proper ports and IP's for the socket server (You likely will only need to update
the socket server URL to reflect the servers machine IP)

You should be in the repo root folder (same as the config) when running the server and bot, otherwise the config file may be out of scope for the other files and cause issues. An exable of running the file could be "python ./Server/server.py". Future updates will include a simple run script

## Current Features

Ability to remotely monitor a machines screen over screenshare

Access to commands and command output

Support for multiple machines to be connected

Account creation with login support 

## Roadmap

### Server

- [X] Refactoring
    - [X] Config
        - [X] Use for Ports
        - [X] Use for IPs
        - [X] Use for URLS
        - [X] Use for Websocket Domains
    - [ ] UI Overhaul
    - [ ] Javascript seperated into files rather than inline
    - [ ] All inline CSS removed/seperated
- [ ] Callback metrics per ip address/machine

- [x] Homepage
    - [x] Login
    - [x] Redirect
    - [ ] CSRF
    - [x] Cookies
    - [ ] Styling

- [x] Login Restrict Pages

- [ ] Devices Page
    - [x] Screenshare
    - [x] Command Execution
    - [ ] Logs
    - [ ] Processes Running / Monitor
    - [ ] Key logging
    - [ ] Mouse Controlling
    - [ ] Logout
    - [ ] Handle Agent Disconnect
    - [ ] Same command sent to multiple machines in parallel

- [ ] UI Styling Overhaul TBD 

- [ ] Run Script for easy of install and use

### Bot

- [x] ScreenShare
- [x] Command Execution
- [ ] Persistance
- [X] Mouse Visibility
- [ ] Password Monitoring ? 
- [ ] Timeout and Reconnection if server is down or if the bot gets disconnected (polling mode? )
- [ ] Force Kill Agent & a Kill all agents option
- [ ] set to polling mode to minimize detection/add a second agent used to switch modes.
- [ ] Validate Commands Using a set key established on connection.
- [ ] Bulk Command Execution
- [ ] WSS?!?

### Readme

- [ ] Format Readme to have full install examples and walkthrough upon completion

