import os
import subprocess

def change_remote_to_ssh(parent_directory):
    for root, dirs, files in os.walk(parent_directory):
        if ".git" in dirs:
            repo_path = root
            print(f"Found Git repository: {repo_path}")
            try:
                # Get the current remote URL
                current_url = subprocess.check_output(
                    ["git", "-C", repo_path, "remote", "get-url", "origin"],
                    text=True
                ).strip()

                # Check if it's already an SSH URL
                if current_url.startswith("git@github.com:"):
                    print(f"Remote for {repo_path} is already using SSH: {current_url}")
                    continue

                # Convert HTTPS URL to SSH
                if current_url.startswith("https://github.com/"):
                    ssh_url = current_url.replace("https://github.com/", "git@github.com:")

                    # Set the new remote URL
                    subprocess.run(
                        ["git", "-C", repo_path, "remote", "set-url", "origin", ssh_url],
                        check=True
                    )
                    print(f"Updated remote URL to SSH: {ssh_url}")
                else:
                    print(f"Skipping non-GitHub URL: {current_url}")

            except subprocess.CalledProcessError as e:
                print(f"Error processing {repo_path}: {e}")

if __name__ == "__main__":
    parent_directory = input("Enter the path to the parent directory: ").strip()
    if os.path.isdir(parent_directory):
        change_remote_to_ssh(parent_directory)
    else:
        print("Invalid directory path.")

