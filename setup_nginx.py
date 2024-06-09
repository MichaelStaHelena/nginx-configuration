import os
import json
import subprocess
import logging
from jinja2 import Template

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        logging.info(f"Loaded data from {file_path}.")
        return data
    except Exception as e:
        logging.error(f"Failed to load data from {file_path}: {e}")
        return None

def validate_project(project):
    if not isinstance(project, dict):
        logging.error(f"Invalid project format: {project}. Each project should be a dictionary.")
        return False
    required_keys = ["name", "domain", "port"]
    for key in required_keys:
        if key not in project:
            logging.error(f"Missing required key '{key}' in project: {project}")
            return False
        if key == "port" and (not isinstance(project[key], int) or project[key] <= 0 or project[key] > 65535):
            logging.error(f"Invalid port '{project[key]}' for project: {project}. Port must be an integer between 1 and 65535.")
            return False
    return True

def create_nginx_config(project, templates):
    config_path = f"/etc/nginx/sites-available/{project['name']}"
    symlink_path = f"/etc/nginx/sites-enabled/{project['name']}"
    
    if os.path.exists(config_path) or os.path.exists(symlink_path):
        logging.info(f"Configuration for {project['name']} already exists. Skipping creation.")
        return False
    
    if "subdomain" in project:
        template_content = templates.get("subdomain", {}).get("template")
    else:
        template_content = templates.get("rootdomain", {}).get("template")
    
    if not template_content:
        logging.error(f"Template not found for project: {project}")
        return False
    
    template = Template(template_content)
    config_content = template.render(subdomain=project.get("subdomain", ""), domain=project["domain"], port=project["port"])
    
    try:
        with open(config_path, "w") as config_file:
            config_file.write(config_content)
        
        if not os.path.exists(symlink_path):
            subprocess.run(["ln", "-s", config_path, symlink_path], check=True)
        
        logging.info(f"Configuration for {project['name']} created and enabled.")
        return True
    except Exception as e:
        logging.error(f"Failed to create configuration for {project['name']}: {e}")
        return False

def verify_nginx_configuration():
    try:
        result = subprocess.run(["nginx", "-t"], check=True, capture_output=True, text=True)
        logging.info(f"Nginx configuration test successful:\n{result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Nginx configuration test failed:\n{e.stderr}")
        return False

def restart_nginx():
    try:
        subprocess.run(["systemctl", "restart", "nginx"], check=True)
        logging.info("Nginx restarted successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to restart Nginx: {e}")

def main():
    if os.geteuid() != 0:
        logging.error("This script must be run as root.")
        exit(1)
    
    projects = load_json_file('projects.json')
    if not projects:
        logging.error("Failed to load projects.")
        exit(1)
    
    templates = load_json_file('nginx_templates.json')
    if not templates:
        logging.error("Failed to load Nginx templates.")
        exit(1)
    
    valid_projects = [project for project in projects if validate_project(project)]
    
    if not valid_projects:
        logging.error("No valid projects to configure.")
        exit(1)
    
    changes_made = False
    for project in valid_projects:
        if create_nginx_config(project, templates):
            changes_made = True
    
    if changes_made and verify_nginx_configuration():
        restart_nginx()
    elif not changes_made:
        logging.info("No changes made to Nginx configuration. Skipping restart.")
    else:
        logging.error("Nginx configuration test failed. Not restarting Nginx.")

if __name__ == "__main__":
    main()
