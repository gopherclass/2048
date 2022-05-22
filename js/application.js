import * as wasm from "internal-wasm";

import Actuator from "./html_actuator.js";
import GameManager from "./game_manager.js"
import HTMLActuator from "./html_actuator.js";
import InputManager from "./keyboard_input_manager.js";
import KeyboardInputManager from "./keyboard_input_manager.js";
import LocalStorageManager from "./local_storage_manager.js";

// Wait till the browser is ready to render the game (avoids glitches)
window.requestAnimationFrame(function () {
  const game = new GameManager(4, KeyboardInputManager, HTMLActuator, LocalStorageManager);
  const source = new wasm.PCGSource(1n, 0n);
  document.getElementById("run").addEventListener("click", (event) => {
    event.preventDefault();
    event.stopPropagation();
    const dir = wasm.walk(game.grid.typedArray(), source);
    game.move(dir);
  });
});

