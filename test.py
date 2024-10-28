import os
import sys
import logging
import psutil
import smtplib
from email.mime.text import MIMEText

# Configure logging
logging.basicConfig(filename='stress_test.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def send_email(subject, message):
    sender = 'prachibballa@gmail.com'
    receiver = 'pbb8112002@gmail.com'
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, 'ndekflmigmerqupz')
            server.sendmail(sender, [receiver], msg.as_string())
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")

def check_memory_usage(threshold=80):
    memory = psutil.virtual_memory()
    usage_percentage = memory.percent
    if usage_percentage > threshold:
        send_email("Memory Usage Alert", f"Memory usage has exceeded {threshold}%. Current usage: {usage_percentage}%")
        logging.warning(f"Memory usage exceeded threshold: {usage_percentage}%")
    return usage_percentage

def memory_stress_test():
    print("Starting Memory Stress Test...")
    os.system("stress --vm 1 --vm-bytes 1G --timeout 10s")
    usage = check_memory_usage()
    print(f"Memory Stress Test Complete. Current Memory Usage: {usage}%\n")

def disk_stress_test():
    print("Starting Disk Stress Test...")
    os.system("sysbench fileio --file-total-size=1G --file-test-mode=rndrw prepare")
    os.system("sysbench fileio --file-total-size=1G --file-test-mode=rndrw run")
    os.system("sysbench fileio --file-total-size=1G --file-test-mode=rndrw cleanup")
    print("Disk Stress Test Complete.\n")

def network_stress_test():
    print("Starting Network Stress Test...")
    os.system("iperf3 -c 192.168.0.111 -t 10") 
    print("Network Stress Test Complete.\n")

def cpu_stress_test():
    print("Starting CPU Stress Test...")
    os.system("stress --cpu 4 --timeout 10s")
    usage = check_cpu_usage()
    print(f"CPU Stress Test Complete. Current CPU Usage: {usage}%\n")

def check_cpu_usage(threshold=80):
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > threshold:
        send_email("CPU Usage Alert", f"CPU usage has exceeded {threshold}%. Current usage: {cpu_usage}%")
        logging.warning(f"CPU usage exceeded threshold: {cpu_usage}%")
    return cpu_usage

def mysql_stress_test():
    print("Starting MySQL Stress Test...")

    # Prepare the database before running the stress test
    prepare_command = "sysbench /usr/share/sysbench/oltp_read_write.lua --db-driver=mysql --mysql-host=192.168.0.111 --mysql-port=3306 --mysql-user=exporter --mysql-password=password --mysql-db=newdb prepare"
    os.system(prepare_command)

    # Run the stress test
    run_command = "sysbench /usr/share/sysbench/oltp_read_write.lua --db-driver=mysql --mysql-host=192.168.0.111 --mysql-port=3306 --mysql-user=exporter --mysql-password=password --mysql-db=newdb run"
    os.system(run_command)

    # Cleanup after the test
    cleanup_command = "sysbench /usr/share/sysbench/oltp_read_write.lua --db-driver=mysql --mysql-host=192.168.0.111 --mysql-port=3306 --mysql-user=exporter --mysql-password=password --mysql-db=newdb cleanup"
    os.system(cleanup_command)

    print("MySQL Stress Test Complete.\n")

def menu():
    while True:
        print("Select a Stress Test to Run:")
        print("1. Memory Stress Testing")
        print("2. Disk Stress Testing")
        print("3. Network Stress Testing")
        print("4. CPU Stress Testing")
        print("5. MySQL Stress Testing")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            memory_stress_test()
        elif choice == '2':
            disk_stress_test()
        elif choice == '3':
            network_stress_test()
        elif choice == '4':
            cpu_stress_test()
        elif choice == '5':
            mysql_stress_test()
        elif choice == '6':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    menu()
