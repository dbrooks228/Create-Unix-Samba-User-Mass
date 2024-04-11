import sys
import argparse
import paramiko

def create_user_on_server(hostname, username, password, script_args):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(f"sudo create_user.sh {script_args}")
        print(f"Output from {hostname}:")
        print(stdout.read().decode())
        print(stderr.read().decode())
    except Exception as e:
        print(f"Failed to execute script on {hostname}: {str(e)}")
    finally:
        client.close()

def main():
    parser = argparse.ArgumentParser(description="Create a user on multiple servers using SSH.")
    parser.add_argument("new_user_id", help="ID of the new user to create.")
    parser.add_argument("similar_user_id", help="ID of a similar user to base the new user configuration on.")
    parser.add_argument("password", help="Password for the new user.")
    parser.add_argument("--admin_username", required=True, help="Admin username for SSH login.")
    parser.add_argument("--admin_password", required=True, help="Admin password for SSH login.")
    args = parser.parse_args()

    servers = [
        {"hostname": "server-a", "username": args.admin_username, "password": args.admin_password, "script_args": f"{args.new_user_id} {args.similar_user_id} {args.password}"},
        {"hostname": "server-b", "username": args.admin_username, "password": args.admin_password, "script_args": f"{args.new_user_id} {args.similar_user_id} {args.password}"},
        {"hostname": "server-c", "username": args.admin_username, "password": args.admin_password, "script_args": f"{args.new_user_id} {args.password}"}  # Adjusted for hydronas2
    ]

    for server in servers:
        create_user_on_server(server["hostname"], server["username"], server["password"], server["script_args"])

if __name__ == "__main__":
    main()