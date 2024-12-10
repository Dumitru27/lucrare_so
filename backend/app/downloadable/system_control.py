import os
import platform
import time

def get_system_info():
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }

def restart_computer():
    system = platform.system().lower()
    
    print("System will restart in 5 seconds...")
    time.sleep(5)
    
    if system == 'windows':
        os.system('shutdown /r /t 0')
    elif system in ['darwin', 'linux']:  # darwin is macOS
        os.system('sudo shutdown -r now')

def main():
    while True:
        print("\nSystem Control Menu")
        print("1. Show System Information")
        print("2. Restart Computer")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            info = get_system_info()
            print("\nSystem Information:")
            for key, value in info.items():
                print(f"{key.capitalize()}: {value}")
        
        elif choice == '2':
            confirm = input("Are you sure you want to restart? (yes/no): ")
            if confirm.lower() == 'yes':
                restart_computer()
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
