# Introduction

Let’s Encrypt is a free, automated, and open certificate authority (CA), run for the public’s benefit. Let’s Encrypt is a service provided by the Internet Security Research Group (ISRG). This guide shows you how you can obtain a free SSL certificate.
<!--more-->
# Requirements
* [Ubuntu server](https://janikvonrotz.ch/2014/03/13/deploy-ubuntu-server/)
* [Python](https://janikvonrotz.ch/2015/10/22/install-python/)
* [Apache2](https://httpd.apache.org/)

# Installation
Install Apache2 web server
```bash
sudo apt install apache2
```
To check status of apache2 web server
```bash
sudo systemctl status apache2
```
Output: 
    Active: inactive (dead)
To start apache2 web server
```bash
sudo systemctl start apache2
```
Output: 
     Active: active (running)

To update the package lists for available software packages
```bash
sudo apt-get update
```
To install snapd
```bash
sudo apt install snapd
```
Remove certbot-auto and any Certbot OS packages
```bash
sudo apt-get remove certbot
```
Install Certbot
```bash
sudo snap install --classic certbot
```
Prepare the Certbot command
```bash
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```
Get a certificate and have Certbot edit your apache configuration automatically to serve it, turning on HTTPS access in a single step.
```bash
sudo certbot certonly --cert-name certificate_name -d domain_name
```
Run bash file to copy certificates generated to certs folder
```bash
sudo ./get_cert.sh
```
Stop apache2 web server services
```bash
sudo systemctl stop apache2

```
