# COMP361-Project

### **📌 Required Dependencies**

| Dependency          | Version | Install Link                                                       | macOS Install Command                    |
| ------------------- | ------- | ------------------------------------------------------------------ | ---------------------------------------- |
| **Docker**          | Latest  | [Download Docker](https://www.docker.com/products/docker-desktop/) | `brew install docker' is current broken! |
| **Docker Compose**  | Latest  | (Included in Docker Desktop)                                       | See above                                |
| **Python**          | 3.8+    | [Download Python](https://www.python.org/downloads/)               | `brew install python`                    |
| **MySQL Connector** | Latest  | `pip install mysql-connector-python`                               | `pip install mysql-connector-python`     |
| **Pygame**          | Latest  | `pip install pygame`                                               | `pip install pygame`                     |

> **⚠ Note:** The Docker Engine **must be running** to compose the container.  
> Open **Docker Desktop** in the background to start.

To start the **MySQL server**, run:

```sh
./setup.sh
```
> **🚀 Future Plan:** As we develop, `setup.sh` will be refactored to `setup.py` to create a `.exe` in the `dist/` folder.
