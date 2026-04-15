# Bot for [TETR.IO](https://tetr.io/about/desktop/) written in Python and Zig

> [!WARNING]
> 1. Using bots in TETRIO is punishable by a permanent IP ban without the possibility of appeal.
> 2. During execution, this software partially takes control of the user's keyboard.
>    Specifically:
>       * The z, x, c keys
>       * Spacebar
>       * Left and right arrow keys
>       * The activation key chosen at startup
>
>    The author assumes no responsibility for any consequences arising from the use of this software, including but not limited to sanctions from the TETRIO developers, issues with your computer, and corrupted files.
>    This software is provided "as is", without any warranties. Use at your own risk.

## Supported Systems
* Windows x64
* Linux x86_64

## User Instructions

### Windows

Before use, ensure that your system has Python version 3.11 or higher installed.

1. Download the repository and navigate to the folder containing the `start.bat` file
2. Run the `start.bat` file
> [!NOTE]
> The first launch may take several minutes while necessary libraries are being installed.
> Before the first launch, ensure you have an internet connection.
3. In the graphical interface that appears, select the `Windows x64` adapter
4. Configure the bot as desired. For more details on available settings, see [the relevant section](#available-bot-settings).
5. Launch the bot by clicking the `Start` button
6. Switch to the TETRIO fullscreen window
7. In Config, set the following options:
    * Gameplay:
        * Board bounciness - 0%
        * Grey out locked hold piece - off
        * Action text - off
    * Video & Interface:
        * Particle count - few
        * Background visibility - 0%
8. Start a game in Zen or Custom mode
9. To activate/deactivate the bot, press the activation key selected in the graphical interface

### Linux (X11)

Currently, there is no adapter for X11. If you have the desire and ability to write one, see [the relevant instructions](#instructions-for-creating-your-own-adapter).

### Linux (Wayland)

Since Wayland does not support common methods for registering global hotkeys, taking screenshots, and simulating keyboard key presses, adapters must be written specifically for each desktop environment and each window manager.

Currently, there is only an adapter for the Niri window manager.
If you have the desire and ability to write an adapter for your system,
see [the relevant instructions](#instructions-for-creating-your-own-adapter).

### Linux (Niri)

1. Ensure that the following packages or their equivalents for your distribution are installed:
    * `grim`
    * `ydotool`
    * `tk`

2. Create an empty file `~/.config/niri/tetrio-binds.kdl` and import it into your Niri config.

3. Start the `ydotoold` service:
```sh
sudo ydotoold --socket-perm=666 --socket-path=/run/user/1000/.ydotool_socket --mouse-off
```
4. Follow the instructions for Windows with the following modifications:
    * Use `start.sh` instead of `start.bat`
    * Select the `Linux x86_64 (Niri)` adapter

## Available Bot Settings

1. `Activation key` - the key that allows the user to activate/deactivate the bot during gameplay
2. `Delay after move` - the time the bot waits after making a move in milliseconds. If the bot simply drops pieces straight down, try increasing this parameter slightly.
3. `Screenshot attempts` - the number of attempts the bot will make to take a screenshot and parse it before making a forced move (pressing spacebar).
4. `Delay after forced move` - the time the bot waits after making a forced move.
5. `Corners to find` - the number of corners the screenshot parser attempts to locate.
6. `Distance between corners` - the minimum distance between corners found by the parser.

## Instructions for Creating Your Own Adapter

1. Copy `python-src/adapters/adapter-template.py` to a new file
2. Implement all methods in the way that works best for you
3. In the `gui.py` file, add an option to select your adapter
    ```python
    self.adapter_options = ["Windows x64", "Linux x86_64 (Niri)", "My cool adapter"]
    ```
4. In the `bot.py` file, add code to handle your adapter
    ```python
    if conf.adapter == "Windows x64":
        from adapters import windows
        adapter_module = windows
        engine_path = "../engine/engine-windows-x86_64.exe"

    if conf.adapter == "Linux x86_64 (Niri)":
        from adapters import niri
        adapter_module = niri
        engine_path = "../engine/engine-linux-x86-64"

    # Your code
    if conf.adapter == "My cool adapter":
        from adapters import my_adapter
        adapter_module = my_adapter
        engine_path = "../engine/engine-linux-x86-64"
    ```
