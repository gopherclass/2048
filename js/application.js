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
    const r = wasm.walk(game.grid.typedArray(), source);
    if (r == 0) {
      game.move(3);
    } else if (r == 1) {
      game.move(1);
    } else if (r == 2) {
      game.move(2);
    } else if (r == 3) {
      game.move(0);
    }
  });
});

