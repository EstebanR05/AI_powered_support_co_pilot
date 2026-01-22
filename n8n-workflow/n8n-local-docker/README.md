(# n8n - Local Docker Compose

This project provides a tiny Docker Compose setup to run n8n with a Postgres database so you don't have to install and run every dependency locally.

## Why this project

Running n8n via Docker Compose keeps your system clean and makes it easy to start/stop the full stack (n8n + Postgres) with a single command.

## Where to access n8n

Once the containers are running, open your browser at:

http://localhost:5678

**Credentials:**
- Username: admin
- Password: admin123

## How to run

Prerequisite: Install Docker and Docker Compose.

- On Linux:

	Install Docker (your distribution package manager or Docker documentation). Then run:

	```bash
	sudo docker compose up -d
	```

	Note: `sudo` is required unless your user is in the `docker` group. To avoid using `sudo` every time, add your user to the `docker` group and re-login:

	```bash
	sudo usermod -aG docker $USER
	newgrp docker
	```

- On Windows (Docker Desktop):

	Install Docker Desktop for Windows and enable WSL2 integration if prompted. Then open a PowerShell or CMD and run:

	```powershell
	docker compose up -d
	```

	On Windows you normally don't need `sudo`.

## Troubleshooting

- If you get a permission error connecting to the Docker socket on Linux, it's usually because your user is not a member of the `docker` group. See the `usermod` command above.
- If the browser can't reach n8n, verify the containers are running:

	```bash
	docker compose ps
	docker compose logs -f n8n
	```

## Notes

- Default Compose maps container port 5678 to host port 5678. The UI is available at `http://localhost:5678`.
- The compose file uses basic auth (configured in the compose environment). Adjust credentials in `docker-compose.yml` if you want different values.

Enjoy running n8n with Docker Compose — it's a simple way to try and develop with n8n without installing everything locally.
)
