# UFG: Modular 2D Fighter Engine
**A robust, Object-Oriented fighting game framework built in Python.**

## 🎮 Overview
**UFG** is a 2D fighting game engine developed as a Computer Science NEA. It is built using **Python** and **Pygame**, focusing on separating game logic from asset rendering.

Unlike simple arcade scripts, this project uses **Object-Oriented Architecture**, allowing for scalable character creation, projectile management, and a distinct "CPU" mode with autonomous decision-making logic.

> **⚠️ Note:** This repository serves as a **logic engine**. To respect copyright and minimize repository size, the original binary assets (sprites and audio) are not included. This engine is designed as a "Bring Your Own Assets" framework. 

## ⚙️ Core Technical Features

### 1. Finite State Machine (FSM)
To manage complex character animations and logic without desynchronization, I implemented a Finite State Machine.
* **States:** The engine tracks specific integer states (0=Idle, 1=Run, 2=Jump, 3=Attack, etc.).
* **Logic:** The `update_action()` method ensures that hitbox logic and sprite rendering are locked to the current state, preventing "floating" or "gliding" bugs during attacks.

### 2. Autonomous AI (CPU)
The project features a CPU opponent that does not rely on random inputs. The AI makes decisions based on real-time spatial data:
* **Distance Vectors:** Calculates `abs(target.x - self.x)` to determine whether to close the gap or initiate an attack.
* **Reaction Logic:** Includes simulated reaction delays and boundary awareness to prevent the AI from getting cornered at the edge of the screen (`screen_width`).

### 3. Object-Oriented Physics & Hitboxes
* **Physics Engine:** Custom implementations of gravity (`vel_y`), acceleration, and friction (`knockFriction`) allow for realistic knockback and weight.
* **Collision Detection:** uses `pygame.Rect.colliderect` for precise combat interactions. Attack hitboxes are generated dynamically based on the direction the character is facing.

### 4. Modular Ability System
Projectiles and special moves are decoupled from the main `Fighter` class into a separate `Ability` class. This allows for:
* Independent cooldown management.
* Separate animation cycles for effects vs. characters.
* Reusability of projectile logic across different character types.

## 🛠️ Code Architecture
The system is built on two primary classes:

```python
class Fighter():
    """ 
    Handles physics, input polling (Human vs CPU), 
    and state transitions (Idle -> Run -> Attack).
    """
    def update(self):
        # Applies gravity, updates animation frames, 
        # and checks for collision events.

class Ability():
    """
    Manages independent entity logic for projectiles,
    including lifecycle management (spawn -> hit -> destroy).
    """
```
## ⚠️ Configuration & Asset Setup

To run this engine locally, you must use your own assets and update the file paths.

### 1. Prerequisites
* Python 3.x
* Pygame (`pip install pygame`)

### 2. Setting up Assets
The engine is designed to load sprites dynamically. You will need to point the script to your local files.

1.  **Download/Create Assets:** You need a standard sprite sheet (rows/columns of animation frames) and audio files for effects.
2.  **Update File Paths:** Open the Python script and locate the **"Load Sprites"** section (approx. line 450).
3.  **Replace Paths:** Change the absolute paths to the relative location of your own files.

**Code Example:**
```python
# ❌ Current Placeholder (Do not use):
shinobi_spritesheet = pygame.image.load("C:\\Users\\...\\Desktop\\spritesheet.png")

# ✅ Update to your local path:
shinobi_spritesheet = pygame.image.load("./assets/my_fighter_sprites.png")
