# Python Assessment

## Installation and Setup
### Prerequisites
* Python 3.x installed on your system
* PostgreSQL installed (if not using a hosted database service)

### 1. Install Python
#### Windows
Download the latest Python installer for Windows from [Here](https://python.org).   
Run the installer and follow the instructions. Make sure to check the option to add Python to your system's PATH.

#### macOS
macOS usually comes with Python pre-installed. You can check the installed version by opening the Terminal and running:

```
python3 --version
```

If Python is not installed, you can install it using Homebrew by running:
```
brew install python
```

#### Linux
Most Linux distributions come with Python pre-installed. You can check the installed version by opening the Terminal and running:
```
python3 --version
```
If Python is not installed, you can install it using your package manager. For example, on Ubuntu, you can run:
```
sudo apt-get update
sudo apt-get install python3
```

### 2. Install PostgreSQL
#### Windows
Download the latest PostgreSQL installer for Windows from [Here](https://postgresql.org).   
Run the installer and follow the instructions.

#### macOS
You can install PostgreSQL on macOS using Homebrew by running:
```
brew install postgresql
```

#### Linux
You can install PostgreSQL on Linux using your package manager. For example, on Ubuntu, you can run:
```
sudo apt-get update
sudo apt-get install postgresql
```

### 3. Clone the Repository
Clone the repository to your local machine:
```
git clone https://github.com/ranjanlamsal/poke_assessment.git
```

### 4. Create and Activate a Virtual Environment
#### Windows
```
cd project-name
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```
cd project-name
python3 -m venv venv
source venv/bin/activate
```

### 5. Install Requirements
Install the required Python packages:
```
pip install -r requirements.txt
```

### 6. Set Environment Variables

Create a .env file in the root directory of the project and add the following variables:
```
DATABASE_HOST=your_database_host
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
```

Replace your_database_host, your_database_name, your_database_user, and your_database_password with your PostgreSQL database details.

### 7. Run the Project
Run the project with uvicorn:

```
uvicorn main:app --reload
```



## File Structure
```
Python Assessment    
│
└───app
│   │ - db.py
│   │ - fetch_insert.py
│   
│   
└───config
|   │ - settings.py
|
|
| - main.py
| - README.md
| - requirements.txt
| - .env
| - .gitignore

```

## API Usage

### Retrieve List of Pokemons
**URL**: /api/v1/pokemons   
**Method**: GET     
**Parameters**:     
name (optional): Filter pokemons by name (case-insensitive).    
pokemon_type (optional): Filter pokemons by type.   
**Response**:   
Status Code: 200 OK    
Content:        
```json
[
    {
        "id": 1,
        "name": "bulbasaur",
        "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
        "type": ["grass", "poison"]
    },
    {
        "id": 2,
        "name": "ivysaur",
        "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png",
        "type": ["grass", "poison"]
    },
    ...
]
```

**Example:**    
Retrieve all pokemons:     
```
GET /api/v1/pokemons
```

Retrieve pokemons with name containing "bul" and type "grass":
```
GET /api/v1/pokemons?name=bul&pokemon_type=grass
```
