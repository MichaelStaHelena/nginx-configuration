import os
import subprocess


def delete_domain(domain_name):
    available_path = f"/etc/nginx/sites-available/{domain_name}"
    enabled_path = f"/etc/nginx/sites-enabled/{domain_name}"

    if os.path.islink(enabled_path):
        os.remove(enabled_path)
        print(f"Removed symlink: {enabled_path}")
    else:
        print(f"No symlink found for: {enabled_path}")

    if os.path.exists(available_path):
        os.remove(available_path)
        print(f"Removed config file: {available_path}")
    else:
        print(f"No config file found for: {available_path}")

    result = subprocess.run(["sudo", "nginx", "-t"], capture_output=True, text=True)
    if result.returncode == 0:
        subprocess.run(["sudo", "systemctl", "reload", "nginx"])
        print("Nginx configuration is valid. Reloaded nginx.")
    else:
        print("Nginx configuration test failed:")
        print(result.stdout)
        print(result.stderr)


if __name__ == "__main__":
    domain_to_delete = ""
    delete_domain(domain_to_delete)
