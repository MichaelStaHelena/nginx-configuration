import os

# Define the directories for Nginx configurations
AVAILABLE_SITES_DIR = "/etc/nginx/sites-available/"
ENABLED_SITES_DIR = "/etc/nginx/sites-enabled/"

def list_nginx_configurations():
    try:
        # List all available sites
        available_sites = os.listdir(AVAILABLE_SITES_DIR)
        enabled_sites = os.listdir(ENABLED_SITES_DIR)
        
        print("Available Nginx Configurations:")
        for site in available_sites:
            print(f"\n- {site}")
            print_config_content(os.path.join(AVAILABLE_SITES_DIR, site))

        print("\nEnabled Nginx Configurations:")
        for site in enabled_sites:
            print(f"\n- {site}")
            print_config_content(os.path.join(ENABLED_SITES_DIR, site))

    except Exception as e:
        print(f"Error while listing Nginx configurations: {e}")

def print_config_content(config_path):
    try:
        with open(config_path, 'r') as config_file:
            print(config_file.read())
    except Exception as e:
        print(f"Error reading {config_path}: {e}")

if __name__ == "__main__":
    list_nginx_configurations()
