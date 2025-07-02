# DOYOKA 2

A python based command and control server and agent. Do You Know Amitesh?

NOTE: This was made for educational purposes and for self monitoring machines I own, please only use this on machines you have permission to access

## Installation

Install and run the corresponding files, bot for client, server for server

Note: When setting up the server, ensure you run the add admin python file to create an admin account.
Additionally, change the config "password" to the password for your admin account (Currently it is set to 'password' which is a 
publicly visible in the readme as its meant to be changed)

The server and bot "IP" are set to localhost (127.0.0.1) and should be updated to reflect the proper address of the machine you will be hosting
the server files on. A planned feature update will be to have all IP's be updated based on the config file

## Current Features

Ability to remotely monitor a machines screen over screenshare

Access to commands and command output

Support for multiple machines to be connected

Account creation with login support 

## Roadmap

### Server

- [ ] Refactoring
    - [ ] Config
        - [ ] Use for Ports
        - [ ] Use for IPs
        - [ ] Use for URLS
        - [ ] Use for Websocket Domains
    - [ ] UI Overhaul
    - [ ] Javascript seperated into files rather than inline
    - [ ] All inline CSS removed/seperated 

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

### Bot

- [x] ScreenShare
- [x] Command Execution
- [ ] Persistance
- [X] Mouse Visibility
- [ ] Password Monitoring ? 

### Readme

- [ ] Format Readme to have full install examples and walkthrough upon completion

