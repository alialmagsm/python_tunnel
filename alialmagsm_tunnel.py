#!/usr/bin/env python3
import sys
import os
import subprocess
import time
def check_password(username, password):
    valid_passwords = {
        "admin": "alialmagsm"
    }

    if username in valid_passwords and password == valid_passwords[username]:
        return True
    else:
        return False


# دریافت یوزرنیم و پسورد از کاربر`
username = input("enter username: ")
password = input("enter password alialmagsm: ")

if check_password(username, password):
    print("password currect")
    
    continue_execution = input("get started (yes/no): ")
    if continue_execution.lower() == "yes":
        print("please wait")
        # دانلود فایل bbr.sh
        subprocess.run(["wget", "-N", "--no-check-certificate", "https://github.com/teddysun/across/raw/master/bbr.sh"])
        
        # تغییر سطح دسترسی فایل bbr.sh
        subprocess.run(["chmod", "+x", "bbr.sh"])

        # اجرای فایل bbr.sh
      
        subprocess.run(["bash", "bbr.sh"])
        print("please wait")
    # ادامه فعالیت‌های اسکریپت
    # بررسی وجود دسترسی root
    import os

    if not os.geteuid() == 0:
        print("This script must be run as root.")
        exit(1)

    # آپدیت لیست پکیج‌ها
    update_process = subprocess.run(["apt", "update"], capture_output=True, text=True)
    if update_process.returncode != 0:
        print("An error occurred while updating the package list.")
        print(update_process.stderr)
        exit(1)

    # آپدیت پکیج‌ها
    upgrade_process = subprocess.run(["apt", "upgrade", "-y"], capture_output=True, text=True)
    if upgrade_process.returncode != 0:
        print("An error occurred while upgrading the packages.")
        print(upgrade_process.stderr)
        exit(1)

    # آپگرید سیستم به آخرین نسخه
    dist_upgrade_process = subprocess.run(["apt", "dist-upgrade", "-y"], capture_output=True, text=True)
    if dist_upgrade_process.returncode != 0:
        print("An error occurred while performing system upgrade.")
        print(dist_upgrade_process.stderr)
        exit(1)

    # پاکسازی فایل‌های اضافی
    autoremove_process = subprocess.run(["apt", "autoremove", "-y"], capture_output=True, text=True)
    if autoremove_process.returncode != 0:
        print("An error occurred while removing unused packages.")
        print(autoremove_process.stderr)
        exit(1)

    # پاکسازی فایل‌های کش
    clean_process = subprocess.run(["apt", "clean"], capture_output=True, text=True)
    if clean_process.returncode != 0:
        print("An error occurred while cleaning up the package cache.")
        print(clean_process.stderr)
        exit(1)

    print("server update successfull.")

    # نصب بسته iptables
    install_iptables = subprocess.run(["sudo", "apt-get", "install", "iptables", "-y"], capture_output=True, text=True)
    if install_iptables.returncode != 0:
        print("An error occurred while installing the iptables package.")
        print(install_iptables.stderr)
        exit(1)

    # دریافت مقادیر iranip و kharegip از فرد اجرا کننده
    iranip = input("enter iranIP: ")
    kharegip = input("enter kharejIP: ")

    # تنظیمات iptables
    subprocess.run(["sysctl", "net.ipv4.ip_forward=1"], capture_output=True, text=True)
    subprocess.run(
        ["iptables", "-t", "nat", "-A", "PREROUTING", "-p", "tcp", "--dport", "22", "-j", "DNAT", "--to-destination",
         iranip], capture_output=True, text=True)
    subprocess.run(["iptables", "-t", "nat", "-A", "PREROUTING", "-j", "DNAT", "--to-destination", kharegip],
                   capture_output=True, text=True)
    subprocess.run(["iptables", "-t", "nat", "-A", "POSTROUTING", "-j", "MASQUERADE"], capture_output=True, text=True)

    # اضافه کردن دستورات به فایل rc.local
    rc_local_commands = [
        "#! /bin/bash",
        "sysctl net.ipv4.ip_forward=1",
        f"iptables -t nat -A PREROUTING -p tcp --dport 22 -j DNAT --to-destination {iranip}",
        f"iptables -t nat -A PREROUTING -j DNAT --to-destination {kharegip}",
        "iptables -t nat -A POSTROUTING -j MASQUERADE",
        "exit 0"
    ]

    rc_local_path = "/etc/rc.local"
    with open(rc_local_path, "a") as rc_local_file:
        rc_local_file.write("\n".join(rc_local_commands))

    print(f"added successfull {rc_local_path} ")

    # تغییر سطح دسترسی فایل rc.local
subprocess.run(["sudo", "chmod", "+x", rc_local_path])

print(f"added successfull {rc_local_path}")
print(f"permission changed successfull {rc_local_path}.")

print("enjoy .END")
sys.exit()
